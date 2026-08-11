# SEO + AI Search Audit

An evidence-based, portable [Agent Skill](https://agentskills.io/specification) for comprehensive traditional SEO and AI-search/GEO/AEO audits. It preserves an immutable baseline, audits source and production behavior, implements justified fixes, and produces reproducible before-and-after evidence without inventing rankings, traffic, or citation outcomes.

The skill uses the open `SKILL.md` format and is not tied to a specific AI agent or coding assistant.

## One-line install

Install the published npm package with:

```bash
npx @robertdevore/audit-seo-ai-search
```

`npx` downloads the current package from npm, runs the installer, and does not require a permanent global installation.

By default, the installer copies the skill to `~/.agents/skills/audit-seo-ai-search`. To install for a product that uses a different skills directory, pass its directory explicitly:

```bash
npx @robertdevore/audit-seo-ai-search --target /path/to/your/agent/skills
```

You can also set `AGENT_SKILLS_HOME` to change the default skills directory. Restart or reload your agent after installation so it discovers the skill.

Then ask your agent to use the skill, using whatever invocation syntax that client supports. For example:

```text
Use $audit-seo-ai-search to audit this site, implement safe fixes, and verify the result.
```

## Installer options

```text
audit-seo-ai-search [install] [--target <skills-directory>] [--force] [--dry-run]
audit-seo-ai-search doctor [--target <skills-directory>]
audit-seo-ai-search path [--target <skills-directory>]
```

An existing installation is never overwritten implicitly. `--force` first renames it to a timestamped backup.

## What the skill covers

- Immutable local and production baselines
- Cryptographically sealed baseline copies and final artifact validation
- Crawlability, indexability, canonicals, redirects, sitemaps, and robots
- Metadata, content quality, entity clarity, internal links, and schema
- Media, accessibility, performance, authority, and historical URL handling
- AI crawler access, AI citation benchmarks, GEO/AEO readiness, and current primary-source research
- Separate evidence states for verified results, observations, inferences, hypotheses, and unavailable data
- Multi-origin and subdomain portfolio controls with per-origin denominators
- Reproducible crawler-policy checks that distinguish robots rules, spoofable User-Agent probes, WAF/IP policy, and verified logs
- Controlled search, AI-answer, and multi-sample performance measurement protocols
- Safe remediation, rebuilds, production checks, and before/after artifacts
- CDN, DNS, WAF, 4xx/5xx, and redirect diagnostics when infrastructure is in scope

## Development and release

Requirements: Node.js 18+ and Python 3 for the skill's audit scaffold.

```bash
npm test
npm run pack:check
python3 /path/to/skill-creator/scripts/quick_validate.py skills/audit-seo-ai-search
python3 skills/audit-seo-ai-search/scripts/scaffold_audit.py --root /tmp/example --date 2026-01-01 --origin https://example.com
```

To publish a new npm release, update the package version first, then run:

```bash
npm login
npm whoami
npm publish --access public
```

## License

MIT
