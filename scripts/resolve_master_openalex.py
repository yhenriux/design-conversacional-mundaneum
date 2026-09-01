#!/usr/bin/env python3
"""Resolve, de forma retomável, todas as localizações OpenAlex dos DOI pendentes."""

from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "corpus" / "master-corpus.csv"
OUTPUT_DIR = ROOT / "data" / "document-resolution" / "master"
ATTEMPTS = OUTPUT_DIR / "openalex-resolution-attempts.csv"
LOCATIONS = OUTPUT_DIR / "openalex-locations.csv"
RAW = OUTPUT_DIR / "raw" / "openalex"
UA = "DesignConversacionalMundaneum/1.1 (systematic evidence mapping)"


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists(): return []
    with path.open(encoding="utf-8-sig", newline="") as handle: return list(csv.DictReader(handle))


def doi_value(value: str) -> str:
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", (value or "").strip(), flags=re.I)


def resolve(row: dict[str, str], timeout: int) -> tuple[dict[str, str], list[dict[str, str]], dict]:
    doi = doi_value(row["doi"])
    url = "https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi, safe="")
    attempt = {"corpus_id":row["corpus_id"],"title":row["title"],"doi":doi,"resolved":"false","locations":"0","resolved_at":datetime.now(timezone.utc).isoformat(),"error":""}
    locations=[]; raw={}
    try:
        request=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
        with urllib.request.urlopen(request,timeout=timeout) as response: raw=json.loads(response.read())
        for number,item in enumerate(raw.get("locations") or [],1):
            source=item.get("source") or {}
            locations.append({"corpus_id":row["corpus_id"],"title":row["title"],"doi":doi,"openalex_id":raw.get("id") or "","location_number":str(number),"is_oa":str(bool(item.get("is_oa"))).lower(),"landing_url":item.get("landing_page_url") or "","pdf_url":item.get("pdf_url") or "","license":item.get("license") or "","version":item.get("version") or "","source_name":source.get("display_name") or "","source_type":source.get("type") or ""})
        attempt.update({"resolved":"true","locations":str(len(locations))})
    except Exception as exc: attempt["error"]=repr(exc)
    return attempt,locations,raw


def write_csv(path: Path, rows: list[dict[str,str]], fallback: list[str]) -> None:
    fields=list(rows[0]) if rows else fallback
    with path.open("w",encoding="utf-8-sig",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=fields); writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--limit",type=int,default=200); parser.add_argument("--workers",type=int,default=8); parser.add_argument("--timeout",type=int,default=45); args=parser.parse_args()
    corpus=read_rows(SOURCE); existing_attempts=read_rows(ATTEMPTS); existing_locations=read_rows(LOCATIONS)
    attempted={row["corpus_id"] for row in existing_attempts}
    pending=[row for row in corpus if row["document_status"]=="sem-url-pdf-resolucao-pendente" and row["doi"] and row["corpus_id"] not in attempted][:args.limit]
    OUTPUT_DIR.mkdir(parents=True,exist_ok=True); RAW.mkdir(parents=True,exist_ok=True)
    new_attempts=[]; new_locations=[]
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures={executor.submit(resolve,row,args.timeout):row["corpus_id"] for row in pending}
        for future in as_completed(futures):
            attempt,locations,raw=future.result(); new_attempts.append(attempt); new_locations.extend(locations)
            if raw: (RAW/f"{attempt['corpus_id']}.json").write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding="utf-8")
    combined_attempts=existing_attempts+sorted(new_attempts,key=lambda row:row["corpus_id"]); combined_locations=existing_locations+sorted(new_locations,key=lambda row:(row["corpus_id"],int(row["location_number"])))
    write_csv(ATTEMPTS,combined_attempts,["corpus_id","title","doi","resolved","locations","resolved_at","error"])
    write_csv(LOCATIONS,combined_locations,["corpus_id","title","doi","openalex_id","location_number","is_oa","landing_url","pdf_url","license","version","source_name","source_type"])
    all_pending={row["corpus_id"] for row in corpus if row["document_status"]=="sem-url-pdf-resolucao-pendente" and row["doi"]}
    summary={"eligible_doi":len(all_pending),"attempted_total":len(combined_attempts),"attempted_this_run":len(new_attempts),"resolved_total":sum(row["resolved"]=="true" for row in combined_attempts),"locations_total":len(combined_locations),"pdf_urls_total":sum(bool(row["pdf_url"]) for row in combined_locations),"studies_with_pdf_url":len({row["corpus_id"] for row in combined_locations if row["pdf_url"]}),"remaining":len(all_pending-{row["corpus_id"] for row in combined_attempts})}
    (OUTPUT_DIR/"openalex-resolution-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
