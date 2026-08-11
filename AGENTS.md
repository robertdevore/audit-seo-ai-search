# Repository instructions

- Keep `skills/audit-seo-ai-search/` as the canonical distributable skill.
- Keep `package.json` and `.codex-plugin/plugin.json` versions synchronized.
- Preserve the installer's refusal to overwrite existing skills unless `--force` is explicit; forced replacement must retain a recoverable backup.
- Run `npm test`, `npm run pack:check`, the plugin validator, and the skill validator before release.
- Do not commit npm tarballs, temporary audit output, credentials, or machine-specific paths.
