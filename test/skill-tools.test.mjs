import assert from "node:assert/strict";
import { appendFile, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const repositoryRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const scripts = join(repositoryRoot, "skills", "audit-seo-ai-search", "scripts");

function python(script, ...args) {
  return spawnSync("python3", ["-B", join(scripts, script), ...args], { encoding: "utf8" });
}

test("scaffolds, seals, and validates a complete audit workspace", async (context) => {
  const root = await mkdtemp(join(tmpdir(), "seo-audit-tools-test-"));
  context.after(() => rm(root, { recursive: true, force: true }));

  const scaffold = python(
    "scaffold_audit.py",
    "--root", root,
    "--date", "2026-01-02",
    "--label", "example",
    "--origin", "https://example.com"
  );
  assert.equal(scaffold.status, 0, scaffold.stderr);

  const audit = join(root, "seo-audit", "2026-01-02-example");
  const generated = join(root, "output");
  await mkdir(generated);
  await writeFile(join(generated, "index.html"), "<!doctype html><title>Example</title>\n", "utf8");

  const seal = python(
    "seal_baseline.py",
    "--audit", audit,
    "--source", generated,
    "--repo-root", root
  );
  assert.equal(seal.status, 0, seal.stderr);

  for (const name of ["baseline.csv", "after.csv"]) {
    const header = (await readFile(join(audit, name), "utf8")).trim().split(",");
    const values = header.map((field) => field === "phase" ? name.replace(".csv", "") : field === "url" ? "https://example.com/" : "");
    await appendFile(join(audit, name), `${values.join(",")}\n`, "utf8");
  }
  const issueHeader = (await readFile(join(audit, "issues.csv"), "utf8")).trim().split(",");
  const issue = issueHeader.map((field) => field === "id" ? "SEO-001" : field === "severity" ? "P2" : "");
  await appendFile(join(audit, "issues.csv"), `${issue.join(",")}\n`, "utf8");
  await writeFile(join(audit, "baseline-summary.json"), "{}\n", "utf8");
  await writeFile(join(audit, "after-summary.json"), "{}\n", "utf8");

  const executivePath = join(audit, "executive-summary.md");
  const executive = (await readFile(executivePath, "utf8"))
    .replace("BLOCKED — audit not yet completed.", "PASS WITH RECOMMENDATIONS");
  await writeFile(executivePath, executive, "utf8");

  const manifestPath = join(audit, "audit-manifest.json");
  const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  manifest.status = "complete";
  manifest.outcome = "PASS WITH RECOMMENDATIONS";
  await writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");

  const validate = python("validate_audit.py", audit, "--final");
  assert.equal(validate.status, 0, validate.stdout + validate.stderr);
  assert.match(validate.stdout, /"status": "PASS"/);
});

test("refuses to overwrite workspaces and detects baseline mutation", async (context) => {
  const root = await mkdtemp(join(tmpdir(), "seo-audit-integrity-test-"));
  context.after(() => rm(root, { recursive: true, force: true }));
  assert.equal(python("scaffold_audit.py", "--root", root, "--date", "2026-01-03").status, 0);
  assert.notEqual(python("scaffold_audit.py", "--root", root, "--date", "2026-01-03").status, 0);

  const audit = join(root, "seo-audit", "2026-01-03");
  const generated = join(root, "output");
  await mkdir(generated);
  await writeFile(join(generated, "index.html"), "before\n", "utf8");
  assert.equal(python("seal_baseline.py", "--audit", audit, "--source", generated, "--repo-root", root).status, 0);
  await writeFile(join(audit, "raw", "baseline-output", "index.html"), "changed\n", "utf8");

  const validate = python("validate_audit.py", audit);
  assert.notEqual(validate.status, 0);
  assert.match(validate.stdout, /sealed baseline file changed/);
});
