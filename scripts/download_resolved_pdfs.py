#!/usr/bin/env python3
"""Baixa apenas localizações marcadas como OA para a biblioteca local de estágio."""
import argparse,csv,hashlib,json,re,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"document-resolution"/"document-resolution.csv"
DEST=ROOT/"library"/"staging"
MANIFEST=ROOT/"data"/"document-resolution"/"download-manifest.csv"
UA="DesignConversacionalMundaneum/1.0 (systematic evidence mapping)"

def slug(doi,title):
 base=doi or title; clean=re.sub(r"[^a-zA-Z0-9._-]+","-",base).strip("-")[:100]
 return clean or hashlib.sha256(title.encode()).hexdigest()[:16]
def main():
 parser=argparse.ArgumentParser(); parser.add_argument("--doi",default=""); parser.add_argument("--summarize-only",action="store_true"); args=parser.parse_args()
 if args.summarize_only:
  with MANIFEST.open(encoding="utf-8-sig",newline="") as h: combined=list(csv.DictReader(h))
  summary={"records_in_manifest":len(combined),"attempted_this_run":0,"valid_pdfs":sum(r["valid_pdf"]=="true" for r in combined),"invalid_responses":sum(r["downloaded"]=="true" and r["valid_pdf"]!="true" for r in combined),"errors":sum(bool(r["error"]) for r in combined)}
  (MANIFEST.parent/"download-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8"); print(json.dumps(summary,ensure_ascii=False)); return
 with SOURCE.open(encoding="utf-8-sig",newline="") as h: rows=list(csv.DictReader(h))
 selected=[r for r in rows if r["is_oa"]=="true" and r["pdf_url"]]
 if args.doi: selected=[r for r in selected if r["doi"].lower()==args.doi.lower()]
 overrides=json.loads((ROOT/"config"/"document-url-overrides.json").read_text(encoding="utf-8"))["overrides"]
 DEST.mkdir(parents=True,exist_ok=True); results=[]
 for row in selected:
  override=overrides.get(row["doi"],{}); url=override.get("pdf_url") or row["pdf_url"]; license_value=override.get("license") or row["license"]
  target=DEST/(slug(row["doi"],row["title"])+".pdf"); result={"title":row["title"],"doi":row["doi"],"url":url,"path":str(target.relative_to(ROOT)),
   "downloaded":"false","valid_pdf":"false","bytes":"0","sha256":"","content_type":"","license":license_value,"version":row["version"],"retrieved_at":"","error":""}
  try:
   req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/pdf,*/*;q=0.5"})
   with urllib.request.urlopen(req,timeout=90) as response:
    data=response.read(); ctype=response.headers.get("Content-Type","")
   valid=data.startswith(b"%PDF-")
   if valid: target.write_bytes(data)
   result.update({"downloaded":"true","valid_pdf":str(valid).lower(),"bytes":str(len(data)),"sha256":hashlib.sha256(data).hexdigest(),
    "content_type":ctype,"retrieved_at":datetime.now(timezone.utc).isoformat(),"error":"" if valid else "response-is-not-pdf"})
  except Exception as exc: result["error"]=repr(exc)
  results.append(result); time.sleep(.2)
 fields=list(results[0]) if results else ["title","doi","url","path","downloaded","valid_pdf","bytes","sha256","content_type","license","version","retrieved_at","error"]
 existing=[]
 if args.doi and MANIFEST.exists():
  with MANIFEST.open(encoding="utf-8-sig",newline="") as h: existing=[r for r in csv.DictReader(h) if r["doi"].lower()!=args.doi.lower()]
 combined=existing+results
 with MANIFEST.open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows(combined)
 summary={"records_in_manifest":len(combined),"attempted_this_run":len(results),"valid_pdfs":sum(r["valid_pdf"]=="true" for r in combined),"invalid_responses":sum(r["downloaded"]=="true" and r["valid_pdf"]!="true" for r in combined),"errors":sum(bool(r["error"]) for r in combined)}
 (MANIFEST.parent/"download-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__": main()
