#!/usr/bin/env python3
"""Resolve versões abertas no Unpaywall e preserva proveniência documental."""
import argparse,csv,json,re,time,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"screening"/"screening-decisions.csv"
OUT=ROOT/"data"/"document-resolution"
UA="DesignConversacionalMundaneum/1.0 (systematic evidence mapping)"

def doi_value(value): return re.sub(r"^https?://(dx\.)?doi\.org/","",(value or "").strip(),flags=re.I)
def get_json(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
 with urllib.request.urlopen(req,timeout=45) as response: return json.loads(response.read())

def main():
 p=argparse.ArgumentParser(); p.add_argument("--provider",choices=["openalex","unpaywall"],default="openalex"); p.add_argument("--email",default=""); p.add_argument("--delay",type=float,default=.12); a=p.parse_args()
 if a.provider=="unpaywall" and not a.email: raise SystemExit("Unpaywall exige --email e autorização explícita para transmiti-lo ao serviço.")
 with SOURCE.open(encoding="utf-8-sig",newline="") as h: rows=list(csv.DictReader(h))
 selected=[r for r in rows if r["screening_decision"] in {"provisional-include","full-text-review"}]
 OUT.mkdir(parents=True,exist_ok=True); raw_dir=OUT/"raw"; raw_dir.mkdir(exist_ok=True)
 fields=["title","doi","screening_decision","resolver","resolved","is_oa","oa_status","pdf_url","landing_url","license","version","host_type","repository","source_pdf_url","resolved_at","error"]
 results=[]
 for number,row in enumerate(selected,1):
  doi=doi_value(row.get("doi")); existing=(row.get("pdf_url") or "").strip()
  result={"title":row.get("title",""),"doi":doi,"screening_decision":row["screening_decision"],"resolver":a.provider,
   "resolved":"false","is_oa":"","oa_status":"","pdf_url":existing,"landing_url":row.get("landing_url",""),"license":row.get("license",""),
   "version":"","host_type":"","repository":"","source_pdf_url":existing,"resolved_at":datetime.now(timezone.utc).isoformat(),"error":""}
  if not doi:
   result["resolver"]="source-metadata"; result["resolved"]="true" if existing else "false"; results.append(result); continue
  try:
   if a.provider=="unpaywall":
    url="https://api.unpaywall.org/v2/"+urllib.parse.quote(doi,safe="")+"?email="+urllib.parse.quote(a.email)
    data=get_json(url); best=data.get("best_oa_location") or {}; pdf=best.get("url_for_pdf") or existing
    update={"resolved":"true","is_oa":str(bool(data.get("is_oa"))).lower(),"oa_status":data.get("oa_status") or "","pdf_url":pdf or "",
     "landing_url":best.get("url_for_landing_page") or result["landing_url"],"license":best.get("license") or result["license"],
     "version":best.get("version") or "","host_type":best.get("host_type") or "","repository":best.get("repository_institution") or ""}
   else:
    url="https://api.openalex.org/works/https://doi.org/"+urllib.parse.quote(doi,safe="")
    data=get_json(url); best=data.get("best_oa_location") or {}; oa=data.get("open_access") or {}; pdf=best.get("pdf_url") or existing
    source=best.get("source") or {}
    update={"resolved":"true","is_oa":str(bool(oa.get("is_oa"))).lower(),"oa_status":oa.get("oa_status") or "","pdf_url":pdf or "",
     "landing_url":best.get("landing_page_url") or result["landing_url"],"license":best.get("license") or result["license"],
     "version":best.get("version") or "","host_type":source.get("type") or "","repository":source.get("display_name") or ""}
   (raw_dir/f"{number:03d}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8"); result.update(update)
  except Exception as exc: result["error"]=repr(exc)
  results.append(result); time.sleep(a.delay)
 with (OUT/"document-resolution.csv").open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows(results)
 summary={"records":len(results),"resolved":sum(r["resolved"]=="true" for r in results),"open_access":sum(r["is_oa"]=="true" for r in results),
  "with_pdf_url":sum(bool(r["pdf_url"]) for r in results),"errors":sum(bool(r["error"]) for r in results),
  "generated_at":datetime.now(timezone.utc).isoformat(),"redistribution_not_inferred":True}
 (OUT/"resolution-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__": main()
