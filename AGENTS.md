# Repository instructions

- Keep `skills/audit-seo-ai-search/` as the canonical distributable skill.
- Preserve the installer's refusal to overwrite existing skills unless `--force` is explicit; forced replacement must retain a recoverable backup.
- Keep the package vendor-neutral and compatible with the Agent Skills specification; do not add product-specific packaging to the core distribution.
- Run `npm test`, `npm run pack:check`, and the skill validator before release.
- Do not commit npm tarballs, temporary audit output, credentials, or machine-specific paths.
