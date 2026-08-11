---
name: audit-seo-ai-search
description: Perform comprehensive, evidence-based traditional SEO and AI-search/GEO/AEO audits for website repositories and live sites. Preserve an immutable before baseline; research current first-party search and crawler guidance; crawl local and production URLs; audit crawlability, indexability, metadata, content, internal/external links, schema, media, performance, authority, AI crawler access, rankings, and AI citations; implement justified fixes; rebuild and verify generated output and edge routing; create before/after evidence and future measurement plans. Use for full-site SEO audits, technical SEO remediation, AI-search readiness reviews, migrations, post-launch audits, ranking/citation baselines, or requests to improve organic and generative-search discoverability without fabricating outcomes.
---

# SEO + AI Search Audit

## Objective

Own the engagement from baseline through verified remediation. Optimize for discovery, crawling, indexing, interpretation, usefulness, authority, and citation-worthiness—not vanity scores.

## Load the right references

- Read [references/audit-specification.md](references/audit-specification.md) completely for every full audit.
- Read [references/artifact-schemas.md](references/artifact-schemas.md) completely before creating the audit workspace, datasets, scores, or final report.
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

## Workflow

### 1. Establish scope, authority, and safety

- Read repository instructions and inspect worktree state.
- Identify which changes are authorized: repository, deployment, DNS/CDN, analytics, search consoles, or read-only audit only.
- Record the production origin, canonical host, locale, audience, business goals, important conversions, and critical page groups.
- Preserve unrelated user changes. Do not alter external systems merely because access exists.

### 2. Research current primary guidance

Consult the current official documentation relevant to the site, including Google Search Central/Search Console, Bing Webmaster Tools/IndexNow, Schema.org, and relevant AI search/crawler providers. Record URLs, retrieval date, and the conclusion supported by each source.

Use primary sources for technical claims. Label emerging practices such as `llms.txt` or new AI protocols as experimental unless official documentation establishes a concrete use.

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

Use the repository's existing convention when present. Never overwrite an earlier audit. Extend the scaffold when the site needs additional datasets.

### 5. Capture the immutable baseline

- Build the untouched site using the documented pinned toolchain.
- Preserve the generated baseline outside any directory the next build deletes.
- Crawl every canonical/indexable page discoverable through sitemap and HTML links.
- Probe the live production equivalent separately.
- Save raw receipts and normalized CSV/JSON summaries before editing.
- Record unavailable platform data without inference.

Do not proceed to implementation until the baseline artifacts exist and can be reopened.

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
- every reported result points to evidence;
- repository changes are verified and handed off according to repository policy.

Return `PASS`, `PASS WITH RECOMMENDATIONS`, or `BLOCKED` based on those gates—not on whether a tool produced a green score.
