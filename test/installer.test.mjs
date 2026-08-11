import assert from "node:assert/strict";
import { readdir, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { mkdtemp } from "node:fs/promises";
import test from "node:test";
import { fileURLToPath } from "node:url";

const repositoryRoot = resolve(fileURLToPath(new URL("..", import.meta.url)));
const cli = join(repositoryRoot, "bin", "audit-seo-ai-search.mjs");

function run(...args) {
  return spawnSync(process.execPath, [cli, ...args], { encoding: "utf8" });
}

test("reports help and package version", async () => {
  const packageJson = JSON.parse(await readFile(join(repositoryRoot, "package.json"), "utf8"));
  const help = run("--help");
  const version = run("--version");
  assert.equal(help.status, 0);
  assert.match(help.stdout, /Install the SEO \+ AI Search Audit skill/);
  assert.equal(version.stdout.trim(), packageJson.version);
});

test("installs, diagnoses, refuses overwrite, and safely backs up on force", async (context) => {
  const target = await mkdtemp(join(tmpdir(), "audit-seo-ai-search-test-"));
  context.after(() => rm(target, { recursive: true, force: true }));

  const dryRun = run("--target", target, "--dry-run");
  assert.equal(dryRun.status, 0);
  assert.match(dryRun.stdout, /Would install/);

  const first = run("--target", target);
  assert.equal(first.status, 0, first.stderr);
  assert.match(first.stdout, /Installed audit-seo-ai-search/);

  const doctor = run("doctor", "--target", target);
  assert.equal(doctor.status, 0, doctor.stderr);
  assert.match(doctor.stdout, /Valid installation/);

  const second = run("install", "--target", target);
  assert.equal(second.status, 1);
  assert.match(second.stderr, /already exists/);

  const forced = run("install", "--target", target, "--force");
  assert.equal(forced.status, 0, forced.stderr);
  assert.match(forced.stdout, /Previous installation backed up/);

  const entries = await readdir(target);
  assert.ok(entries.includes("audit-seo-ai-search"));
  assert.ok(entries.some((entry) => entry.startsWith("audit-seo-ai-search.backup-")));
});
