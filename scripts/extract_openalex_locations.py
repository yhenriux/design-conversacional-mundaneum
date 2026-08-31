#!/usr/bin/env python3
"""Extrai todas as localizações OpenAlex das respostas já preservadas localmente."""
import csv,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution";RAW=BASE/"raw"
def doi(v):return re.sub(r"^https?://(dx\.)?doi\.org/","",v or "",flags=re.I).lower()
def main():
 with (BASE/"document-status.csv").open(encoding="utf-8-sig",newline="") as h:pending={r["doi"].lower():r for r in csv.DictReader(h) if r["document_status"]!="pdf-integral-validado-local"}
 results=[];seen=set()
 for path in RAW.glob("*.json"):
  data=json.loads(path.read_text(encoding="utf-8"));key=doi(data.get("doi") or "")
  if key not in pending:continue
  for location in data.get("locations") or []:
   pdf=location.get("pdf_url") or "";landing=location.get("landing_page_url") or "";signature=(key,pdf,landing)
   if not pdf or signature in seen:continue
   seen.add(signature);source=location.get("source") or {}
   results.append({"title":pending[key]["title"],"doi":key,"pdf_url":pdf,"landing_url":landing,"is_oa":str(bool(location.get("is_oa"))).lower(),"license":location.get("license") or "","version":location.get("version") or "","source":source.get("display_name") or "","source_type":source.get("type") or ""})
 fields=["title","doi","pdf_url","landing_url","is_oa","license","version","source","source_type"]
 with (BASE/"openalex-all-locations.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 print(f"pending={len(pending)} alternate_pdf_locations={len(results)}")
if __name__=="__main__":main()
