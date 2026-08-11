# SEO + AI Search Audit

An evidence-based Codex skill for comprehensive traditional SEO and AI-search/GEO/AEO audits. It preserves an immutable baseline, audits source and production behavior, implements justified fixes, and produces reproducible before-and-after evidence without inventing rankings, traffic, or citation outcomes.

The repository is packaged both as a [Codex plugin](https://developers.openai.com/plugins/build/plugins) and as an npm command-line installer.

## One-line install

After the package is published to npm:

```bash
npx audit-seo-ai-search
```

Until then, after this repository is pushed to GitHub:

```bash
npx github:robertdevore/audit-seo-ai-search
```

The installer copies the skill to `$CODEX_HOME/skills/audit-seo-ai-search` when `CODEX_HOME` is set, otherwise to `~/.codex/skills/audit-seo-ai-search`. Restart Codex after installation so the new skill is discovered.

Then invoke it explicitly:

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
- Crawlability, indexability, canonicals, redirects, sitemaps, and robots
- Metadata, content quality, entity clarity, internal links, and schema
- Media, accessibility, performance, authority, and historical URL handling
- AI crawler access, AI citation benchmarks, GEO/AEO readiness, and current primary-source research
- Safe remediation, rebuilds, production checks, and before/after artifacts
- CDN, DNS, WAF, 4xx/5xx, and redirect diagnostics when infrastructure is in scope

## Development and release

Requirements: Node.js 18+ and Python 3 for the skill's audit scaffold.

```bash
npm test
npm run pack:check
python3 /path/to/plugin-creator/scripts/validate_plugin.py .
python3 /path/to/skill-creator/scripts/quick_validate.py skills/audit-seo-ai-search
```

Keep the versions in `package.json` and `.codex-plugin/plugin.json` synchronized. To release after creating the GitHub repository:

```bash
git remote add origin git@github.com:robertdevore/audit-seo-ai-search.git
git push -u origin main
npm login
npm publish --access public
```

The package name `audit-seo-ai-search` was unclaimed when this repository was created, but registry availability can change before publication.

## License

MIT
