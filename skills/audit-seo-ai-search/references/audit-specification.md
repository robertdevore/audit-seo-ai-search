# Audit specification

## Contents

1. Evidence model
2. Baseline inventory
3. Search and AI visibility
4. Crawlability and indexability
5. Metadata and content
6. Linking and architecture
7. Schema and semantics
8. Media and performance
9. Authority, competition, and AI readiness
10. Implementation and verification

## 1. Evidence model

Classify every material claim as one of:

- official requirement;
- official recommendation;
- broadly supported best practice;
- site-specific hypothesis;
- experimental/emerging practice.

Store the source, date, scope, and uncertainty. Prefer current first-party documentation. Never promote a validator warning or SEO-tool heuristic into a ranking claim.

Preserve these evidence layers separately:

1. repository source;
2. untouched generated artifact;
3. live origin/CDN response;
4. search/analytics/log platform data;
5. dated manual or API observations;
6. post-change artifact and production verification.

## 2. Baseline inventory

For every discovered page capture, where applicable:

- URL, source file, page type, local/live HTTP status;
- indexability, robots directives, canonical and target status;
- sitemap inclusion/lastmod, redirect chain, canonical host/protocol;
- title/description and duplicate indicators;
- H1, H2/H3 structure, visible word count, language;
- author, published/modified dates, breadcrumb presence;
- JSON-LD blocks/types/parse state;
- internal inbound/outbound and external outbound links;
- depth, orphan state, broken destinations;
- images, alt attributes, dimensions, loading, format, bytes;
- HTML/CSS/JS/image/font weights and request estimates;
- content hash or near-duplicate signal.

Discover from sitemap plus crawlable HTML. Compare sitemap routes, generated HTML files, navigation, feeds, and known route generators so one source cannot hide omissions.

## 3. Search and AI visibility

Use real sources when available:

- Google Search Console and Bing Webmaster Tools;
- privacy-appropriate analytics;
- CDN/server logs;
- CrUX/RUM and PageSpeed data;
- authorized rank/search APIs;
- controlled AI-answer platforms.

Record query/page impressions, clicks, CTR, average position, country, device, search appearance, index coverage, sitemap state, crawl problems, field CWV, and provider-specific AI reporting where exposed.

Create a representative query set from observed queries, page topics, branded/non-branded intents, problems, comparisons, and high-intent searches. A dated observation is not a universal rank. Preserve provider, date, locale, device, observed page/range, competing results, rich features, and AI-result presence.

Create a separate AI benchmark using natural questions: definitions, how-to, recommendations, comparisons, alternatives, troubleshooting, technical adoption, branded, and category questions. Record platform/date, mention, citation, cited URL, context/order, competing domains, factual accuracy, and gaps. Do not fabricate inaccessible sessions.

## 4. Crawlability and indexability

Audit:

- `robots.txt`, meta robots, X-Robots-Tag, blocked assets;
- sitemap/index files, lastmod accuracy, redirects/404/noindex exclusions;
- canonical consistency across markup, internal links, sitemap, JSON-LD, and Open Graph;
- HTTPS and host variants, trailing slash, parameters, duplicates, pagination, soft 404s, alternate languages, and hreflang where relevant;
- important pages reachable through crawlable HTML;
- AI search/indexing crawlers, user-triggered fetchers, and training crawlers as distinct policy decisions;
- CDN/WAF behavior for legitimate crawlers.

Do not change training-crawler policy merely to improve search discovery.

## 5. Metadata and content

Review titles, descriptions, canonical, robots, language, Open Graph/social cards, media metadata, author, dates, and page type. Character counts are review signals, not rigid targets.

Inspect actual front-matter support before adding fields. Keep source metadata and rendered HTML synchronized.

For every substantive page determine:

- purpose, audience, search intent, central topic/entity;
- primary and supporting query themes;
- whether the page fulfills its promise;
- competing internal pages/cannibalization;
- missing context and currentness;
- first-hand experience, examples, source code, measurements, cases, or primary evidence;
- unique information that makes the page worth ranking or citing.

Do not add filler, mass FAQs, doorway pages, keyword variants, fake expertise, or generic AI prose. Preserve factual voice.

Assess information hierarchy: one clear primary heading, meaningful sections, definitions, examples, tables/lists/code only when useful, conclusions/next actions, and related resources.

Create a topic/query map with URL, topic/entity, intent, primary/secondary themes, related entities/questions, competing URL, gap, and action.

## 6. Linking and architecture

Build the internal graph with source, destination, anchor, context, status, and depths. Identify orphans, weakly linked key pages, excessive depth, broken links, outdated paths, redirect hops, vague/misleading anchors, repetitive exact matches, and missed contextual links.

Inspect navigation, breadcrumbs, contextual links, related-content components, taxonomy/archive pages, and footer links. Add links only when they help readers.

For external links record status, final URL, verification result, context, and rel attributes. Prioritize primary sources. Treat access-blocked statuses as indeterminate. Do not mass-replace historical citations without editorial judgment.

## 7. Schema and semantics

Inventory JSON-LD and validate parsing, factual visibility alignment, and page-purpose type. Consider only appropriate types such as Person, Organization, WebSite, WebPage, CollectionPage, AboutPage, ContactPage, Article/BlogPosting/TechArticle, BreadcrumbList, SoftwareApplication/SoftwareSourceCode, Product/Offer, Event, VideoObject, ImageObject, or Dataset.

Never fabricate visible facts, authors, dates, organizations, reviews, ratings, products, offers, or FAQs. Separate Schema.org validity from search-engine rich-result eligibility.

Inspect semantic HTML: main/article/nav/header/footer, headings, lists, tables, figures/captions, links/buttons, code/pre. Fix structural issues that improve accessibility, comprehension, or crawling; avoid meaningless rewrites.

## 8. Media and performance

Audit filenames where practical, accurate alt text, dimensions, responsive sources, compression, formats, lazy loading, above-fold priority, captions/context, image/video sitemap need, and truthful structured data.

Measure representative templates with Lighthouse plus field data when available. Preserve raw receipts. Record LCP, INP, CLS, TTFB, transfer sizes, requests, render-blocking assets, JavaScript/CSS weight, fonts, media, and third parties.

Static sites should preserve server-rendered/static HTML advantages. Watch for full-stylesheet swaps, hidden or animated primary headings, missing intrinsic dimensions, client-rendered core content, and cache invalidation failures.

## 9. Authority, competition, and AI readiness

Verify truthful responsibility and provenance: About, author identity, contact, project/source links, dates, update history, corrections, privacy/legal pages where relevant, primary evidence, real expertise, and maintainership.

Compare representative competing results on intent satisfaction, originality, technical depth, evidence, examples, media, structure, usability, freshness, source quality, and observed citation visibility. Do not compare word counts alone.

Ask for each important page: what reliable, unique information would justify an AI system citing this page over ten alternatives? Record the content opportunity when the answer is unclear.

Treat `llms.txt`, IndexNow, and future discovery protocols according to current documented adoption. Keep experiments separate from ranking requirements.

## 10. Implementation and verification

Implement only justified, in-scope fixes after baseline preservation. Prefer global fixes for global defects and page-level edits for page-level facts.

After changes:

1. rebuild with the pinned/documented toolchain;
2. run repository validators;
3. crawl the same route set and regenerate datasets;
4. validate links, metadata, canonicals, robots, sitemap, schema, HTML, content preservation, routes, and assets;
5. repeat representative performance tests;
6. deploy only when authorized;
7. verify live responses and infrastructure independently;
8. quantify before/after technical changes;
9. preserve unresolved access/editorial/external items;
10. define 7/28/60/90-day outcome measurements.
