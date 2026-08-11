#!/usr/bin/env node

import { cp, mkdir, readFile, rename, stat } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const skillName = "audit-seo-ai-search";
const packageRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const source = join(packageRoot, "skills", skillName);
const packageJson = JSON.parse(await readFile(join(packageRoot, "package.json"), "utf8"));

function usage() {
  return `audit-seo-ai-search ${packageJson.version}

Install the portable SEO + AI Search Audit Agent Skill.

Usage:
  audit-seo-ai-search [install] [--target <skills-directory>] [--force] [--dry-run]
  audit-seo-ai-search doctor [--target <skills-directory>]
  audit-seo-ai-search path [--target <skills-directory>]
  audit-seo-ai-search --help
  audit-seo-ai-search --version

Options:
  --target <dir>  Skills directory used by your agent (default: ~/.agents/skills)
  --force         Back up an existing installation before replacing it
  --dry-run       Show the destination without writing files
`;
}

function parseArgs(argv) {
  const parsed = { command: "install", force: false, dryRun: false, target: undefined };
  let commandSeen = false;

  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--help" || value === "-h") parsed.command = "help";
    else if (value === "--version" || value === "-v") parsed.command = "version";
    else if (value === "--force") parsed.force = true;
    else if (value === "--dry-run") parsed.dryRun = true;
    else if (value === "--target") {
      const target = argv[index + 1];
      if (!target || target.startsWith("-")) throw new Error("--target requires a directory");
      parsed.target = target;
      index += 1;
    } else if (!value.startsWith("-") && !commandSeen && ["install", "doctor", "path"].includes(value)) {
      parsed.command = value;
      commandSeen = true;
    } else {
      throw new Error(`Unknown argument: ${value}`);
    }
  }

  return parsed;
}

function skillRoot(target) {
  if (target) return resolve(target);
  if (process.env.AGENT_SKILLS_HOME) return resolve(process.env.AGENT_SKILLS_HOME);
  return join(homedir(), ".agents", "skills");
}

async function exists(path) {
  try {
    await stat(path);
    return true;
  } catch (error) {
    if (error.code === "ENOENT") return false;
    throw error;
  }
}

async function validateSkill(path) {
  const required = [
    "SKILL.md",
    "references/artifact-schemas.md",
    "references/audit-specification.md",
    "references/evidence-and-measurement.md",
    "references/production-diagnostics.md",
    "scripts/scaffold_audit.py",
    "scripts/seal_baseline.py",
    "scripts/validate_audit.py"
  ];

  for (const relativePath of required) {
    if (!(await exists(join(path, relativePath)))) {
      throw new Error(`Missing required skill file: ${relativePath}`);
    }
  }

  const instructions = await readFile(join(path, "SKILL.md"), "utf8");
  if (!instructions.startsWith("---\nname: audit-seo-ai-search\n")) {
    throw new Error("SKILL.md has invalid front matter");
  }
}

async function install(options) {
  const root = skillRoot(options.target);
  const destination = join(root, skillName);
  if (resolve(destination) === resolve(source)) {
    throw new Error("Refusing to install over the package's bundled source skill");
  }

  await validateSkill(source);
  if (options.dryRun) {
    process.stdout.write(`Would install ${skillName} to ${destination}\n`);
    return;
  }

  await mkdir(root, { recursive: true });
  const present = await exists(destination);
  if (present && !options.force) {
    throw new Error(`Skill already exists at ${destination}; rerun with --force to replace it safely`);
  }

  const stamp = new Date().toISOString().replaceAll(":", "-");
  const staging = join(root, `.${skillName}.installing-${process.pid}-${stamp}`);
  const backup = join(root, `${skillName}.backup-${stamp}`);
  await cp(source, staging, { recursive: true, errorOnExist: true });
  await validateSkill(staging);

  let backedUp = false;
  try {
    if (present) {
      await rename(destination, backup);
      backedUp = true;
    }
    await rename(staging, destination);
  } catch (error) {
    if (backedUp && !(await exists(destination))) await rename(backup, destination);
    throw error;
  }

  process.stdout.write(`Installed ${skillName} to ${destination}\n`);
  if (backedUp) process.stdout.write(`Previous installation backed up at ${backup}\n`);
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const root = skillRoot(options.target);
  const destination = join(root, skillName);

  if (options.command === "help") process.stdout.write(usage());
  else if (options.command === "version") process.stdout.write(`${packageJson.version}\n`);
  else if (options.command === "path") process.stdout.write(`${destination}\n`);
  else if (options.command === "doctor") {
    await validateSkill(destination);
    process.stdout.write(`Valid installation: ${destination}\n`);
  } else await install(options);
}

main().catch((error) => {
  process.stderr.write(`Error: ${error.message}\n`);
  process.exitCode = 1;
});
