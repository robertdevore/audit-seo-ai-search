---
name: audit-seo-ai-search
description: Perform comprehensive, evidence-based traditional SEO and AI-search/GEO/AEO audits for one site, multiple origins, repositories, and live delivery chains. Preserve and seal an immutable before baseline; research current first-party guidance; inventory source, generated, rendered, and production states; audit crawling, indexing, metadata, content, links, schema, media, performance, authority, crawler policy, search visibility, and AI citations; implement authorized fixes; validate artifact schemas; deploy only when authorized; and verify comparable before/after evidence without fabricating outcomes. Use for full-site or multi-subdomain SEO audits, technical remediation, AI-search readiness reviews, migrations, post-launch audits, ranking/citation baselines, or discoverability improvements.
---

# SEO + AI Search Audit

## Objective

Own the engagement from baseline through verified remediation. Optimize for discovery, crawling, indexing, interpretation, usefulness, authority, and citation-worthiness—not vanity scores.

## Load the right references

- Read [references/audit-specification.md](references/audit-specification.md) completely for every full audit.
- Read [references/artifact-schemas.md](references/artifact-schemas.md) completely before creating the audit workspace, datasets, scores, or final report.
- Read [references/evidence-and-measurement.md](references/evidence-and-measurement.md) completely before testing crawler access, rankings, AI answers, performance, or multiple origins.
- Read [references/production-diagnostics.md](references/production-diagnostics.md) completely when production, DNS, CDN/WAF, redirects, HTTP status, crawlers, or request logs are in scope.

## Non-negotiable rules

1. Record the baseline before editing anything.
2. Research current guidance at audit time. Browse primary sources because search, crawler, schema, and AI-search behavior changes.
3. Separate documented requirements, documented recommendations, supported best practices, hypotheses, and experiments.
4. Never invent rankings, traffic, index coverage, Core Web Vitals, citations, referrals, backlinks, dates, authorship, expertise, reviews, or product claims.
5. Mark unavailable measurements exactly as `NOT AVAILABLE — DATA ACCESS REQUIRED`.
6. Preserve author voice and factual meaning. Do not bulk-rewrite pages for keywords or word count.
7. Prefer systemic template/generator fixes when one correct change repairs many pages; keep page-specific facts page-specific.
8. Verify rendered output and production behavior. Source code that looks correct is not evidence that the live site works.
9. Preserve dated, structured artifacts so a later audit can compare the same fields and benchmark questions.
10. Treat internal health/readiness scores only as transparent trend heuristics, never platform scores.
11. Keep SEO findings separate from accessibility, security, deployment, or general maintenance findings unless they directly change discovery, crawling, indexing, rendering, or search presentation.
12. Use the same URL set, normalization rules, tool versions, environment, and measurement protocol before and after. Explain every exception.

## Workflow

### 1. Establish scope, authority, and safety

- Read repository instructions and inspect worktree state.
- Identify which changes are authorized: repository, deployment, DNS/CDN, analytics, search consoles, or read-only audit only.
- Record the production origin, canonical host, locale, audience, business goals, important conversions, and critical page groups.
- For multiple hosts or subdomains, define each origin as a separate audit unit and create a portfolio map for ownership, cross-origin links, canonicals, search properties, and shared infrastructure.
- Preserve unrelated user changes. Do not alter external systems merely because access exists.

### 2. Research current primary guidance

Consult the current official documentation relevant to the site, including Google Search Central/Search Console, Bing Webmaster Tools/IndexNow, Schema.org, and relevant AI search/crawler providers. Record URLs, retrieval date, and the conclusion supported by each source.

Use primary sources for technical claims. Record provider guidance separately because crawler names, purposes, IP ranges, and reporting surfaces change. Treat `llms.txt`, content chunking for AI, and other AI-only files or protocols as experiments unless a target provider documents a concrete use. Do not present them as Google requirements.

### 3. Understand the site and delivery chain

Map:

- content, front matter, templates, components, navigation, routes, archives, pagination, feeds, sitemaps, robots, canonicals, metadata, JSON-LD, images, and JavaScript-rendered content;
- build commands, pinned dependencies, generated-output validation, deployment, hosting, custom domains, redirects, CDN/WAF, and error handling;
- the relationship `source → generated artifact → origin host → CDN/edge → browser/crawler`.

Do not assume framework fields or hosting features. Verify what the repository and provider actually support.

### 4. Create a dated audit workspace

Run:

```bash
python3 <skill-dir>/scripts/scaffold_audit.py --root . --date YYYY-MM-DD
```

Use `--label NAME` when the same origin needs more than one immutable workspace on the same date. Pass `--origin` when known. Use the repository's existing convention when present. Never overwrite an earlier audit. Extend the scaffold when the site needs additional datasets.

### 5. Capture the immutable baseline

- Build the untouched site using the documented pinned toolchain.
- Preserve the generated baseline outside any directory the next build deletes.
- Seal the preserved baseline and provenance before editing:

```bash
python3 <skill-dir>/scripts/seal_baseline.py --audit seo-audit/YYYY-MM-DD --source PATH_TO_UNTOUCHED_OUTPUT --repo-root .
```

- Crawl every canonical/indexable page discoverable through sitemap and HTML links.
- Probe the live production equivalent separately.
- Save raw receipts and normalized CSV/JSON summaries before editing.
- Record unavailable platform data without inference.

Do not proceed to implementation until the baseline artifacts exist, the seal verifies, and the baseline can be reopened. If preserving the full output is impractical, stop and document a safe project-specific immutable storage approach before editing.

### 6. Audit the whole system

Cover every category in `references/audit-specification.md`. At minimum inspect:

- canonical host/protocol, status codes, redirects, robots, sitemaps, noindex, duplicates, parameters, pagination, and orphans;
- titles, descriptions, H1/heading structure, language, social metadata, authorship, dates, and front matter;
- purpose, intent, audience, entity/topic clarity, originality, evidence, staleness, cannibalization, and citation-worthiness;
- internal/external link graphs, anchor context, depth, broken destinations, redirect chains, and historical-link uncertainty;
- visible-content-aligned JSON-LD and rich-result eligibility as separate questions;
- image accessibility/dimensions/weight/loading, semantic HTML, asset weight, lab performance, and field data when available;
- search-console/analytics/log data, representative query observations, controlled AI-answer benchmarks, competitor evidence, and AI crawler access.

Do not call 401/403/405/429 external destinations broken without corroboration. Record them as blocked or indeterminate.

Do not infer real crawler access from a spoofed User-Agent request. Report robots policy, generic UA probe, published-IP/WAF policy, and verified log evidence as separate layers.

### 7. Prioritize evidence

Create an issue register with category, affected URLs, evidence, severity, expected benefit, confidence, difficulty, action, owner, and status.

- `P0`: blocks or seriously damages crawling, indexing, canonicalization, access, or safe operation.
- `P1`: material discovery, architecture, content, or production problem affecting important pages.
- `P2`: meaningful quality, trust, performance, or maintainability improvement.
- `P3`: polish or explicitly labeled experiment.

Keep affected-page counts separate from unique root causes. Prevent low-value warnings from obscuring P0/P1 work.

### 8. Implement justified fixes

Fix repository-safe issues only after the baseline is sealed. Prefer the narrowest factual change that removes the verified cause. Suitable work may include templates, metadata, canonicals, internal links, schema, media attributes, broken references, sitemap/robots logic, semantic HTML, performance, and redirects.

Require editorial approval for new claims, positioning, commercial intent, or substantial rewrites. Require owner approval for crawler training policy, DNS changes, destructive migrations, and ambiguous redirect destinations.

### 9. Rebuild and re-audit

- Run the repository's required validation chain.
- Rebuild the full generated site.
- Crawl the same inventory and regenerate the same fields.
- Validate internal routes, assets, canonicals, sitemap, robots, JSON-LD parsing/types, metadata uniqueness, image integrity, and accidental content removal.
- Repeat representative performance measurements under comparable conditions.
- Run the final artifact validator and resolve every error:

```bash
python3 <skill-dir>/scripts/validate_audit.py seo-audit/YYYY-MM-DD --final
```

Set `audit-manifest.json` status to `complete` and outcome to `PASS`, `PASS WITH RECOMMENDATIONS`, or `BLOCKED` before the final validation.

- Diff baseline and after datasets; explain intentional URL-count changes.

If the pinned build cannot run, stop claiming repository validation, preserve the exact blocker, and continue only with independent checks that remain valid.

### 10. Verify production and infrastructure

After deployment, test production independently of local output. Verify canonical host/protocol, apex and `www`, HTTP and HTTPS, nested paths, query preservation, robots, sitemap, feeds, key page groups, crawlers, redirects, 404s, and 5xx behavior.

For every redirect, verify:

- source variants actually match;
- status is 301/308 when permanent;
- destination is the intended live canonical URL;
- the chain is one hop when practical;
- query handling is intentional;
- the final destination returns 200;
- the host really supports the configured redirect mechanism.

Use CDN/request logs for complete error-URL enumeration. Client-side analytics cannot prove full request counts or status distributions.

### 11. Report without overclaiming

Produce the artifact set and final report defined in `references/artifact-schemas.md`. Distinguish:

- immediate technical validation;
- existing search/AI visibility baseline;
- outcomes that require elapsed time and platform data.

Recommend comparable 7-, 28-, 60-, and 90-day measurements. Never say rankings, traffic, or citations improved unless post-change evidence proves it.

For rank or AI-answer observations, preserve the exact provider/product, account state, locale, device, prompt/query, timestamp, result depth, cited URL, and raw receipt. When those controls are unknown, call the result a sampled observation and leave numeric position blank.

## Definition of done

Complete only when:

- current primary guidance and interpretation limits are recorded;
- the site/build/deployment chain is understood;
- the untouched baseline is preserved;
- every meaningful page and audit category is covered;
- safe P0/P1/P2 fixes in scope are implemented or explicitly blocked;
- generated output is rebuilt and re-audited;
- production infrastructure is verified where access permits;
- before/after datasets, scores, unresolved items, and future benchmarks are reproducible;
- the baseline seal and final artifact validation pass;
- every reported result points to evidence;
- repository changes are verified and handed off according to repository policy.

Return `PASS`, `PASS WITH RECOMMENDATIONS`, or `BLOCKED` based on those gates—not on whether a tool produced a green score.
