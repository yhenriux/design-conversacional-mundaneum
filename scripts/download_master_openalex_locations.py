#!/usr/bin/env python3
"""Recupera todas as URLs de PDF localizadas pelo OpenAlex no corpus mestre."""
import csv,hashlib,json,re,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/"data"/"document-resolution"/"master"
SOURCE=BASE/"openalex-locations.csv"; MANIFEST=BASE/"openalex-download-manifest.csv"; DEST=ROOT/"library"/"staging"/"master-openalex"
UA="DesignConversacionalMundaneum/1.1 (systematic evidence mapping)"
def rows(path):
 if not path.exists(): return []
 with path.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def name(item):
 slug=re.sub(r"[^a-zA-Z0-9]+","-",item["title"]).strip("-")[:65]; return f"{item['candidate_id']}-{slug}.pdf"
def get(item):
 target=DEST/name(item); out={"candidate_id":item["candidate_id"],"corpus_id":item["corpus_id"],"title":item["title"],"doi":item["doi"],"url":item["pdf_url"],"license":item["license"],"version":item["version"],"source_name":item["source_name"],"path":target.relative_to(ROOT).as_posix(),"downloaded":"false","pdf_signature":"false","bytes":"0","sha256":"","content_type":"","retrieved_at":datetime.now(timezone.utc).isoformat(),"error":""}
 try:
  request=urllib.request.Request(item["pdf_url"],headers={"User-Agent":UA,"Accept":"application/pdf,*/*;q=0.5"})
  with urllib.request.urlopen(request,timeout=60) as response:data=response.read(); out["content_type"]=response.headers.get("Content-Type","")
  valid=data.startswith(b"%PDF-");
  if valid:target.write_bytes(data)
  out.update({"downloaded":"true","pdf_signature":str(valid).lower(),"bytes":str(len(data)),"sha256":hashlib.sha256(data).hexdigest(),"error":"" if valid else "response-is-not-pdf"})
 except Exception as exc:out["error"]=repr(exc)
 return out
def main():
 locations=[]; seen=set()
 for item in rows(SOURCE):
  url=item["pdf_url"].strip()
  if not url or url in seen:continue
  seen.add(url); item={**item,"candidate_id":f"{item['corpus_id']}-OA{int(item['location_number']):03d}"}; locations.append(item)
 DEST.mkdir(parents=True,exist_ok=True); BASE.mkdir(parents=True,exist_ok=True)
 result=[]
 with ThreadPoolExecutor(max_workers=8) as pool:
  futures=[pool.submit(get,item) for item in locations]
  for future in as_completed(futures):result.append(future.result())
 result.sort(key=lambda x:x["candidate_id"]); fields=list(result[0]) if result else []
 with MANIFEST.open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(result)
 summary={"unique_urls":len(result),"pdf_signatures":sum(x["pdf_signature"]=="true" for x in result),"failures":sum(bool(x["error"]) for x in result),"studies_with_pdf":len({x["corpus_id"] for x in result if x["pdf_signature"]=="true"})}
 (BASE/"openalex-download-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
