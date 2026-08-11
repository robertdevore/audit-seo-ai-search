# Audit artifacts and reporting

## Contents

1. Workspace
2. Required CSV fields
3. Before/after metrics
4. Internal scores
5. Final report

## 1. Workspace

Use `seo-audit/YYYY-MM-DD/` or the repository convention. Keep prior audits immutable.

Core artifacts:

- `executive-summary.md`
- `methodology.md`
- `research-sources.md`
- `data-availability.md`
- `site-inventory.csv`
- `baseline.csv` and `baseline-summary.json`
- `after.csv` and `after-summary.json`
- `metadata-audit.csv`
- `content-audit.csv`
- `keyword-map.csv`
- `search-rankings.csv`
- `ai-search-benchmark.csv`
- `internal-links.csv`
- `external-links.csv`
- `broken-links.csv`
- `schema-audit.csv`
- `indexability.csv`
- `crawlability.csv`
- `crawler-access.csv`
- `performance.csv`
- `image-audit.csv`
- `redirects.csv`
- `issues.csv`
- `changes.md`
- `before-after.md`
- `unresolved.md`
- `recommendations.md`

Add raw JSON receipts for Lighthouse, search/API observations, headers, or richer crawl data when useful.

## 2. Required CSV fields

At minimum use these stable fields; extend rather than rename between comparison audits.

### Inventory/baseline/after

`phase,url,source_file,page_type,local_status,production_status,indexable,robots_directives,canonical,canonical_target_status,title,title_length,meta_description,description_length,h1,heading_structure,word_count,lang,published_date,modified_date,author,breadcrumbs,schema_types,internal_inbound_links,internal_outbound_links,external_outbound_links,broken_internal_links,broken_external_links,image_count,missing_alt,missing_dimensions,page_depth,orphan,sitemap_included,duplicate_title,duplicate_description,content_hash,issues`

### Issues

`id,phase,category,severity,affected_urls,affected_count,evidence,expected_benefit,confidence,difficulty,recommended_action,owner,status`

### Redirects

`phase,source_url,source_variant,http_status,target_url,chain_length,final_status,canonical_target,query_preserved,verification,issues`

### Search rankings

`query,search_engine,date,country,device,page_found,observed_position_or_range,competing_results,rich_features,ai_result_presence,evidence,limitations`

### AI benchmark

`question,platform,date,domain_appeared,domain_cited,cited_url,citation_context,citation_order,competing_domains,accurate_representation,content_gap,evidence,limitations`

### Links

`phase,source_url,destination_url,anchor_text,link_context,http_status,final_url,chain_length,verification,rel,recommended_action`

### Performance

`phase,url,template,run_date,environment,lighthouse_version,html_bytes,css_bytes,js_bytes,image_bytes,font_bytes,requests,lcp_ms,inp_ms,cls,ttfb_ms,source,notes`

## 3. Before/after metrics

Report at least:

- canonical and indexable pages;
- missing/duplicate titles and descriptions;
- missing canonicals and H1 problems;
- broken internal/external links and unique destinations;
- orphans and pages deeper than three clicks;
- missing alt/dimensions and broken media;
- JSON-LD parse/type errors and valid-schema coverage;
- sitemap/noindex/duplicate-route problems;
- redirect chains and production host failures;
- AI/search crawler access issues;
- P0/P1 counts;
- representative lab/field performance;
- internal SEO and AI-readiness scores.

Explain intentional page-count reductions and distinguish affected-page counts from root causes.

## 4. Internal scores

Scores are optional but useful for repeat audits when weights and evidence remain stable.

Suggested SEO health weights:

- crawlability/indexability 20;
- metadata/SERP presentation 15;
- architecture/internal linking 15;
- content quality/currentness 15;
- structured data 10;
- performance/CWV evidence 10;
- media 5;
- authority/trust 5;
- AI-search readiness 5.

Suggested AI Search Readiness weights:

- search crawler access 15;
- indexability 10;
- information/entity clarity 10;
- source attribution/authorship 10;
- original/citable information 15;
- semantic/structured data 10;
- internal topic relationships 10;
- freshness 5;
- technical/media readiness 5;
- measured AI visibility 10.

Award points only for evidence. Missing measured AI visibility earns zero, not an inferred score. Label both as internal heuristics.

## 5. Final report

Report:

- overall status: `PASS`, `PASS WITH RECOMMENDATIONS`, or `BLOCKED`;
- exact audit date;
- pages audited/changed and files changed;
- baseline/final internal scores;
- P0 and P1 before/after;
- technical, content, linking, schema, performance, and production changes;
- real search visibility baseline;
- real AI visibility baseline;
- unavailable data and outstanding access/editorial/infrastructure work;
- exact future measurements and comparison windows.

The executive summary must answer: where was the site, what was wrong, what changed, where is it now technically, what was measured, what could not be measured, and what should happen next.
