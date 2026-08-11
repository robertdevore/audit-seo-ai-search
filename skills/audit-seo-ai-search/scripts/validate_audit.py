#!/usr/bin/env python3
"""Validate SEO audit structure, stable schemas, baseline integrity, and final readiness."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

from scaffold_audit import CSV_HEADERS, MARKDOWN, SCHEMA_VERSION


FINAL_JSON = ("baseline-summary.json", "after-summary.json")
PLACEHOLDERS = (
    "BLOCKED — audit not yet completed.",
    "NOT YET COMPLETED",
)


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path.name}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"JSON root must be an object: {path.name}")
        return {}
    return value


def validate_csv(path: Path, expected: list[str], final: bool, errors: list[str]) -> list[dict]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            header = reader.fieldnames or []
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        errors.append(f"invalid CSV {path.name}: {exc}")
        return []
    if header != expected:
        errors.append(f"schema drift in {path.name}: expected {expected}, found {header}")
    if final and path.name in {"baseline.csv", "after.csv"} and not rows:
        errors.append(f"final audit requires data rows in {path.name}")
    return rows


def verify_seal(audit: Path, manifest: dict, errors: list[str]) -> None:
    baseline = manifest.get("baseline", {})
    if not baseline.get("sealed"):
        errors.append("baseline is not sealed")
        return
    seal_path = audit / baseline.get("manifest", "raw/baseline-manifest.json")
    seal = load_json(seal_path, errors)
    if not seal:
        return
    root_value = seal.get("verification_root", "raw/baseline-output")
    root = Path(root_value)
    if not root.is_absolute():
        root = audit / root
    if not root.is_dir():
        errors.append(f"sealed baseline root missing: {root_value}")
        return

    expected: dict[str, dict] = {}
    for row in seal.get("files", []):
        relative = str(row.get("path", ""))
        if not relative or relative in expected or Path(relative).is_absolute() or ".." in Path(relative).parts:
            errors.append(f"invalid or duplicate sealed baseline path: {relative!r}")
            continue
        expected[relative] = row

    actual = {
        path.relative_to(root).as_posix(): {
            "bytes": path.stat().st_size,
            "sha256": hash_file(path),
        }
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }
    for relative in sorted(expected.keys() - actual.keys()):
        errors.append(f"sealed baseline file missing: {relative}")
    for relative in sorted(actual.keys() - expected.keys()):
        errors.append(f"unsealed file added to baseline: {relative}")
    for relative in sorted(expected.keys() & actual.keys()):
        row = expected[relative]
        if actual[relative]["bytes"] != row.get("bytes") or actual[relative]["sha256"] != row.get("sha256"):
            errors.append(f"sealed baseline file changed: {relative}")
    if seal.get("file_count") != len(expected):
        errors.append("baseline seal file_count does not match its file inventory")
    if seal.get("total_bytes") != sum(int(row.get("bytes", 0)) for row in expected.values()):
        errors.append("baseline seal total_bytes does not match its file inventory")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", type=Path)
    parser.add_argument("--final", action="store_true", help="enforce completion gates")
    args = parser.parse_args()
    audit = args.audit.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not audit.is_dir():
        raise SystemExit(f"Audit workspace is not a directory: {audit}")
    manifest_path = audit / "audit-manifest.json"
    manifest = load_json(manifest_path, errors)
    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"audit-manifest schema_version must be {SCHEMA_VERSION}, "
            f"found {manifest.get('schema_version')!r}"
        )
    audit_date = str(manifest.get("audit_date", ""))
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", audit_date):
        errors.append("audit-manifest audit_date must be YYYY-MM-DD")

    for name in MARKDOWN:
        path = audit / name
        if not path.is_file():
            errors.append(f"missing required artifact: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if audit_date and f"Audit date: {audit_date}" not in text:
            warnings.append(f"audit date not found in {name}")
        if args.final:
            for placeholder in PLACEHOLDERS:
                if placeholder in text:
                    errors.append(f"completion placeholder {placeholder!r} remains in {name}")

    csv_rows: dict[str, list[dict]] = {}
    for name, header in CSV_HEADERS.items():
        path = audit / name
        if not path.is_file():
            errors.append(f"missing required artifact: {name}")
            continue
        csv_rows[name] = validate_csv(path, header.split(","), args.final, errors)

    if manifest.get("baseline", {}).get("sealed"):
        verify_seal(audit, manifest, errors)

    if args.final:
        if manifest.get("status") != "complete":
            errors.append("final audit-manifest status must be 'complete'")
        if manifest.get("outcome") not in {"PASS", "PASS WITH RECOMMENDATIONS", "BLOCKED"}:
            errors.append("final audit-manifest outcome must be PASS, PASS WITH RECOMMENDATIONS, or BLOCKED")
        if not manifest.get("baseline", {}).get("sealed"):
            errors.append("baseline is not sealed")
        for name in FINAL_JSON:
            path = audit / name
            if not path.is_file():
                errors.append(f"missing required final artifact: {name}")
            else:
                load_json(path, errors)
        issues = csv_rows.get("issues.csv", [])
        ids = [row.get("id", "") for row in issues]
        if any(not value for value in ids):
            errors.append("every issues.csv row requires an id")
        if len(ids) != len(set(ids)):
            errors.append("issues.csv ids must be unique")
        allowed_severity = {"P0", "P1", "P2", "P3"}
        invalid = sorted({row.get("severity", "") for row in issues} - allowed_severity)
        if invalid:
            errors.append(f"issues.csv contains invalid severity values: {invalid}")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "mode": "final" if args.final else "structure",
        "errors": errors,
        "warnings": warnings,
    }
    report_path = audit / "validation-report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
