# Production and edge diagnostics

## Contents

1. Delivery-chain model
2. Redirect verification
3. Status-code diagnosis
4. Error-URL observability
5. Crawler access
6. Operational lessons

## 1. Delivery-chain model

Diagnose the whole path:

`request → DNS → CDN/WAF/edge rule → origin host → generated route/asset`

A correct source file does not prove a correct generated artifact. A correct artifact does not prove the host supports its redirect/config format. A healthy origin does not prove DNS/CDN routing is healthy.

Record host, DNS record/proxy state, certificate/protocol, edge rule, origin target, response headers/status, redirect location, and final response.

## 2. Redirect verification

Resolve the exact source variants before writing rules:

- apex and `www`;
- HTTP and HTTPS;
- trailing and non-trailing slash;
- nested paths;
- representative query strings.

Prefer an exact host/path expression for a single retired route. For many routes, use a provider-supported bulk redirect map when available. Avoid sending unrelated retired pages to the homepage merely to remove 404s; select the closest relevant live canonical URL, or consider a truthful 410 when content is intentionally gone and no substitute exists.

After deployment, verify each response without following, then follow the complete chain. Confirm permanent status, exact Location, intentional query behavior, one-hop routing where practical, and final 200.

## 3. Status-code diagnosis

- `404`: route/file absent at the effective origin or redirect rule did not match/run.
- soft 404: HTTP 200 but page communicates missing/empty content.
- `521` at Cloudflare: Cloudflare could not connect to the configured origin; inspect proxied DNS target, origin availability, firewall, and whether a redirect should run at the edge before origin access.
- `5xx`: preserve provider/origin evidence and request ID; do not infer a single cause from status alone.
- third-party `401/403/405/429`: access blocked or indeterminate, not automatically broken.

Do not assume files such as `_redirects`, `vercel.json`, `_headers`, or framework routing configs work on a different host. Confirm provider support. GitHub Pages, for example, does not execute Netlify-style `_redirects` files.

## 4. Error-URL observability

For a complete list of requested 404/5xx URLs, use edge/origin request logs containing path, timestamp, method, status, host, user agent, referrer, and request ID. Configure retention and privacy appropriately.

Client-side web analytics is incomplete for this purpose:

- bots may not execute the beacon;
- redirects may happen before page JavaScript;
- error pages may omit or block analytics;
- page views do not provide authoritative response-status counts;
- a view cannot be assumed human.

Search Console can reveal crawl/indexing problems but is not a complete access log. When logs are unavailable, say so and use client analytics only as partial evidence.

## 5. Crawler access

Test robots policy and live CDN/WAF response separately for relevant search discovery crawlers. Distinguish indexing/search bots, user-triggered fetchers, and training bots. Preserve the current owner policy unless explicitly authorized to change it.

Verify representative user agents against robots, sitemap, homepage, and key pages. A permissive robots file is ineffective if the CDN blocks the crawler.

## 6. Operational lessons

- Preserve pre-fix evidence before changing DNS or edge rules.
- Make one narrow rule, verify it, then expand.
- Keep query handling explicit.
- Test propagation repeatedly when an edge rule has just been deployed; transient mixed results may occur.
- Do not commit generated output when repository policy excludes it.
- Keep provider configuration documented in the audit even when it is not stored in Git.
- Add production monitors for canonical host, `www`, robots, sitemap, and critical routes when the site matters operationally.
- Keep repository/build dependency pins portable. Use documented environment overrides or temporary pinned worktrees instead of absolute machine paths.
