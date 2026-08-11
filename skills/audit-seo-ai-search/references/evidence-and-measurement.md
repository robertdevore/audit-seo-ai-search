# Evidence and measurement protocol

## Contents

1. Evidence states
2. URL and origin controls
3. Crawler-policy verification
4. Search and AI observations
5. Performance measurements
6. Structured data and content evidence
7. Scope boundaries

## 1. Evidence states

Give each material result an evidence state:

- `verified`: directly reproduced from an authoritative interface, preserved response, log, or deterministic artifact;
- `observed`: measured once or in a limited sample with the stated conditions;
- `inferred`: reasoned from evidence but not directly measured;
- `hypothesis`: plausible and testable but not established;
- `not available`: requires missing access or data.

Never collapse these states. A successful build is verified source/artifact evidence, not verified production behavior. A live `200` is access at that moment, not proof of indexing or citation. A validator pass establishes syntax or eligibility checks, not ranking benefit.

For every metric record the numerator, denominator, population, exclusions, collection time, tool/version, and raw evidence location. Count unique root causes separately from affected URLs and occurrences.

## 2. URL and origin controls

Define URL normalization before crawling: scheme, host, case policy, default ports, fragments, query handling, percent encoding, trailing slash, `/index.html`, and redirect aliases. Preserve the raw URL and normalized URL when normalization affects a result.

Create the inventory from at least sitemap, crawlable HTML links, generated files/routes, feeds, navigation, and known route generators. Reconcile the sets explicitly. A page missing from one source is not automatically an orphan or error.

Treat every origin as a separate audit unit. For multi-origin portfolios record:

- canonical owner and purpose of each host;
- its own robots, sitemap, Search Console/Bing property, redirect policy, and production chain;
- cross-origin links and whether they are intentional;
- cross-origin canonicals or hreflang and their reciprocal/target state;
- shared templates or infrastructure that can create systemic defects.

Do not aggregate host-level availability or scores until each origin has its own denominator. A healthy apex does not prove a healthy subdomain.

## 3. Crawler-policy verification

Keep four layers separate:

1. **Declared policy:** parse the effective live `robots.txt` for the exact crawler token and URL. Preserve the body and response headers.
2. **Generic probe:** request representative URLs with a crawler-like User-Agent. Label this `spoofable UA probe`; it tests only how the delivery chain handled that request.
3. **Network policy:** compare WAF/CDN allowlists and blocks with the provider's current published IP ranges where available.
4. **Verified traffic:** use request logs and provider-supported IP verification. This is the strongest evidence that the actual crawler reached the site.

Never call a UA-string request a verified Googlebot, OAI-SearchBot, Claude-SearchBot, or PerplexityBot request. User agents are spoofable. Preserve source IP and request ID only in private raw evidence when privacy policy permits.

Separate search/index crawlers, user-triggered fetchers, training crawlers, ad/safety bots, and agentic/browser fetchers. Their robots behavior and owner policy may differ. Do not change training permission as an SEO fix.

Remember that robots controls crawling, not guaranteed index exclusion. A crawler must access a page to see `noindex`; do not simultaneously block the URL in robots and rely on page-level `noindex` without documenting the conflict.

## 4. Search and AI observations

Record numeric search position only when the exact engine/product, locale, device, account/personalization state, timestamp, query, result depth, and result URL are known. Otherwise set position to blank and classify the evidence as a dated sampled observation.

For AI answers preserve:

- exact platform, product/mode, model when exposed, account state, locale, timestamp, and full question;
- whether the domain was mentioned, linked, or cited—these are different outcomes;
- exact cited URL, citation order/context, answer accuracy, competing sources, and raw receipt;
- repeated-run count and variability when the platform is nondeterministic.

Do not use one answer session to claim platform-wide visibility. Do not infer citations from referral traffic, crawler access, schema, or conventional search results.

For Google generative features, treat foundational SEO and Search Console's available generative-AI reporting as first-party evidence. Do not require special AI files, artificial content chunking, or inauthentic mentions.

## 5. Performance measurements

Prefer field data for outcome claims and lab data for diagnosis. Keep them separate.

For Lighthouse or equivalent lab comparisons:

- use the same URL/template, tool and browser version, device profile, throttling, server type, cache state, geography, and network conditions;
- run at least three comparable samples when a timing or score influences prioritization, and report the median plus range;
- preserve every raw result, not only the best run;
- compare deterministic payload, request, image-dimension, and render-path changes alongside variable scores;
- never report a single lab run as field Core Web Vitals.

Record field LCP, INP, and CLS at the 75th percentile with the source, window, device segment, and URL group when available. Do not average lab and field values.

## 6. Structured data and content evidence

Validate structured data at three independent levels:

1. valid serialization and Schema.org vocabulary;
2. factual alignment with visible page content and the page's primary purpose;
3. target search-engine feature eligibility and required properties.

Do not equate Schema.org validity with rich-result eligibility, or eligibility with appearance. Preserve Rich Results Test or Search Console receipts when available.

Evaluate content with page-specific evidence: intended audience and task, first-hand experience, source artifacts, methods, examples, limitations, currentness, author/responsibility, and unique information. Word count, heading count, title length, and keyword frequency are triage signals only.

## 7. Scope boundaries

Track non-SEO findings in a separate appendix or issue category when useful. Security headers, CI runtime warnings, accessibility defects, privacy, and general maintenance matter, but do not award or deduct SEO score unless a documented discovery, crawling, indexing, rendering, usability, or presentation consequence exists.

Require explicit authorization before deployments, DNS/CDN/WAF changes, Search Console submissions, IndexNow notifications, analytics changes, or crawler-policy changes. An IndexNow success response proves receipt, not crawling or indexing.
