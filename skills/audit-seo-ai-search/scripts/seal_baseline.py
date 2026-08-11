#!/usr/bin/env python3
"""Preserve and cryptographically seal an untouched generated-site baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root: Path) -> list[dict[str, object]]:
    rows = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        rows.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": hash_file(path),
            }
        )
    return rows


def git_value(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", required=True, type=Path, help="existing audit workspace")
    parser.add_argument("--source", required=True, type=Path, help="untouched generated output")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    audit = args.audit.expanduser().resolve()
    source = args.source.expanduser().resolve()
    repo = args.repo_root.expanduser().resolve()
    audit_manifest_path = audit / "audit-manifest.json"
    seal_path = audit / "raw" / "baseline-manifest.json"
    preserved = audit / "raw" / "baseline-output"

    if not audit_manifest_path.is_file():
        raise SystemExit(f"Missing audit manifest: {audit_manifest_path}")
    if not source.is_dir():
        raise SystemExit(f"Baseline source is not a directory: {source}")
    try:
        audit.relative_to(source)
    except ValueError:
        pass
    else:
        raise SystemExit("Refusing a baseline source that contains the audit workspace")
    if seal_path.exists() or preserved.exists():
        raise SystemExit("Refusing to overwrite an existing baseline seal or preserved output")

    audit_manifest = json.loads(audit_manifest_path.read_text(encoding="utf-8"))
    if audit_manifest.get("baseline", {}).get("sealed"):
        raise SystemExit("Audit manifest already marks the baseline as sealed")

    seal_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, preserved, copy_function=shutil.copy2)
    target = preserved

    files = inventory(target)
    if not files:
        raise SystemExit(f"Refusing to seal an empty baseline: {target}")

    seal = {
        "schema_version": "1.0",
        "sealed_at": datetime.now(timezone.utc).isoformat(),
        "mode": "preserved-copy",
        "verification_root": "raw/baseline-output",
        "git_commit": git_value(repo, "rev-parse", "HEAD"),
        "git_status_porcelain": git_value(repo, "status", "--short"),
        "file_count": len(files),
        "total_bytes": sum(int(row["bytes"]) for row in files),
        "files": files,
    }
    seal_path.write_text(json.dumps(seal, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit_manifest["baseline"]["sealed"] = True
    audit_manifest["baseline"]["file_count"] = seal["file_count"]
    audit_manifest["baseline"]["total_bytes"] = seal["total_bytes"]
    audit_manifest["baseline"]["git_commit"] = seal["git_commit"]
    audit_manifest_path.write_text(
        json.dumps(audit_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"Sealed {seal['file_count']} files ({seal['total_bytes']} bytes) at {seal_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
