#!/usr/bin/env python3
"""Create a dated, non-destructive SEO + AI-search audit workspace."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from pathlib import Path


MARKDOWN = {
    "executive-summary.md": "# Executive summary\n\nAudit date: {date}\n\n## Overall status\n\nBLOCKED — audit not yet completed.\n\n## Where the site was\n\n## What was wrong\n\n## What changed\n\n## Where the site is now\n\n## Available measurements\n\n## Unavailable measurements\n\n## Next actions\n",
    "methodology.md": "# Methodology\n\nAudit date: {date}\n\n## Scope\n\n## Evidence sequence\n\n## Current primary guidance consulted\n\n## Build and crawl commands\n\n## Interpretation limits\n",
    "research-sources.md": "# Research sources\n\nAudit date: {date}\n\n| Source | Retrieved | Supported conclusion | Classification |\n| --- | --- | --- | --- |\n",
    "data-availability.md": "# Data availability\n\nAudit date: {date}\n\n| Source | Available | Scope / limitation |\n| --- | --- | --- |\n",
    "changes.md": "# Implemented changes\n\nAudit date: {date}\n\n",
    "before-after.md": "# Before and after\n\nAudit date: {date}\n\nImmediate technical evidence only; search outcomes require post-deployment data and elapsed time.\n",
    "unresolved.md": "# Unresolved items\n\nAudit date: {date}\n\n",
    "recommendations.md": "# Recommendations and measurement plan\n\nAudit date: {date}\n\n## Immediate after deployment\n\n## 7-day checks\n\n## 28-, 60-, and 90-day comparisons\n\n## Editorial decisions\n",
}


INVENTORY_HEADER = "phase,url,source_file,page_type,local_status,production_status,indexable,robots_directives,canonical,canonical_target_status,title,title_length,meta_description,description_length,h1,heading_structure,word_count,lang,published_date,modified_date,author,breadcrumbs,schema_types,internal_inbound_links,internal_outbound_links,external_outbound_links,broken_internal_links,broken_external_links,image_count,missing_alt,missing_dimensions,page_depth,orphan,sitemap_included,duplicate_title,duplicate_description,content_hash,issues"


CSV_HEADERS = {
    "site-inventory.csv": INVENTORY_HEADER,
    "baseline.csv": INVENTORY_HEADER,
    "after.csv": INVENTORY_HEADER,
    "metadata-audit.csv": "phase,url,source_file,page_type,title,title_length,meta_description,description_length,canonical,robots_directives,lang,author,og_title,og_description,og_url,og_type,og_image,twitter_card,duplicate_title,duplicate_description,issues",
    "content-audit.csv": "phase,url,source_file,page_type,primary_purpose,search_intent,target_audience,central_entity,primary_query_theme,supporting_topics,h1,heading_structure,word_count,published_date,modified_date,first_hand_signals,content_gap,competing_internal_url,recommended_action",
    "keyword-map.csv": "phase,url,primary_topic,primary_entity,search_intent,primary_query_theme,secondary_queries,related_entities,relevant_questions,competing_internal_url,content_gap,recommended_action",
    "search-rankings.csv": "query,search_engine,date,country,device,page_found,observed_position_or_range,competing_results,rich_features,ai_result_presence,evidence,limitations",
    "ai-search-benchmark.csv": "question,platform,date,domain_appeared,domain_cited,cited_url,citation_context,citation_order,competing_domains,accurate_representation,content_gap,evidence,limitations",
    "internal-links.csv": "phase,source_url,destination_url,anchor_text,link_context,http_status,final_url,chain_length,verification,rel,recommended_action",
    "external-links.csv": "phase,source_url,destination_url,anchor_text,link_context,http_status,final_url,chain_length,verification,rel,recommended_action",
    "broken-links.csv": "phase,source_url,destination_url,link_type,anchor_text,http_status,evidence,recommended_action",
    "schema-audit.csv": "phase,url,schema_types,json_ld_blocks,valid_json,visible_match,rich_result_eligible,issues,recommended_action",
    "indexability.csv": "phase,url,local_status,production_status,indexable,robots_directives,canonical,canonical_target_status,sitemap_included,sitemap_lastmod,reason",
    "crawlability.csv": "phase,url,page_depth,internal_inbound_links,internal_outbound_links,external_outbound_links,orphan,pages_over_three_clicks,broken_internal_links,redirect_chain,crawlable_html_links,issues",
    "crawler-access.csv": "crawler,purpose,robots_access,live_status,waf_or_cdn_result,recommended_action,action_taken,evidence",
    "performance.csv": "phase,url,template,run_date,environment,lighthouse_version,html_bytes,css_bytes,js_bytes,image_bytes,font_bytes,requests,lcp_ms,inp_ms,cls,ttfb_ms,source,notes",
    "image-audit.csv": "phase,page_url,image_url,alt_text,alt_present,decorative,width,height,loading,format,local_exists,file_bytes,issues",
    "redirects.csv": "phase,source_url,source_variant,http_status,target_url,chain_length,final_status,canonical_target,query_preserved,verification,issues",
    "issues.csv": "id,phase,category,severity,affected_urls,affected_count,evidence,expected_benefit,confidence,difficulty,recommended_action,owner,status",
}


def parse_date(value: str) -> str:
    try:
        return dt.date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must be YYYY-MM-DD") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--date", type=parse_date, default=dt.date.today().isoformat())
    parser.add_argument("--directory", default="seo-audit", help="audit directory relative to root")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    directory = Path(args.directory)
    if directory.is_absolute():
        raise SystemExit("Refusing absolute --directory; provide a path relative to --root")
    audit_base = (root / directory).resolve()
    try:
        audit_base.relative_to(root)
    except ValueError as exc:
        raise SystemExit("Refusing --directory outside --root") from exc
    audit = audit_base / args.date
    if audit.exists():
        raise SystemExit(f"Refusing to overwrite existing audit workspace: {audit}")

    audit.mkdir(parents=True)
    for name, template in MARKDOWN.items():
        (audit / name).write_text(template.format(date=args.date), encoding="utf-8")
    for name, header in CSV_HEADERS.items():
        with (audit / name).open("w", newline="", encoding="utf-8") as handle:
            csv.writer(handle).writerow(header.split(","))

    print(f"Created {audit} with {len(MARKDOWN)} Markdown and {len(CSV_HEADERS)} CSV artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
