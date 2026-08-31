#!/usr/bin/env python3
"""Deduplica uma execução e publica métricas sem aprovar fontes automaticamente."""
import argparse,csv,json,re,unicodedata
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def norm(s):
 s=unicodedata.normalize("NFKD",s or "").encode("ascii","ignore").decode().lower()
 return re.sub(r"[^a-z0-9]+"," ",s).strip()
def key(row):
 doi=(row.get("doi") or "").lower().replace("https://doi.org/","").strip()
 return "doi:"+doi if doi else "title:"+norm(row.get("title"))+":"+(row.get("year") or "")
def main():
 p=argparse.ArgumentParser(); p.add_argument("run_id"); a=p.parse_args(); folder=ROOT/"data"/"search-runs"/a.run_id
 with (folder/"candidates.csv").open(encoding="utf-8-sig",newline="") as h: rows=list(csv.DictReader(h))
 unique={}
 for row in rows:
  k=key(row)
  if k not in unique or int(row["provisional_score"] or 0)>int(unique[k]["provisional_score"] or 0): unique[k]=row
 values=list(unique.values()); eligible=[r for r in values if int(r["ontology_score"] or 0)>=3 and int(r["provisional_score"] or 0)>=7]
 fields=list(rows[0]) if rows else []
 with (folder/"candidates-deduplicated.csv").open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows(values)
 with (folder/"screening-queue.csv").open("w",encoding="utf-8-sig",newline="") as h:
  queue_fields=fields+["manual_centrality","manual_field_relevance","manual_documentary_evidence","manual_actionable_contribution","reviewer","review_date"]
  w=csv.DictWriter(h,fieldnames=queue_fields,extrasaction="ignore"); w.writeheader(); w.writerows(eligible)
 report={"run_id":a.run_id,"raw_candidates":len(rows),"unique_candidates":len(values),"duplicates":len(rows)-len(values),
   "automatic_high_priority_for_screening":len(eligible),"not_included_automatically":True,
   "by_api":dict(Counter(r["source_api"] for r in rows)),"with_pdf_url":sum(bool(r.get("pdf_url")) for r in values),
   "with_doi":sum(bool(r.get("doi")) for r in values)}
 (folder/"coverage.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__": main()
