#!/usr/bin/env python3
"""Testa as localizações abertas encontradas no OpenAIRE."""
import csv,hashlib,json,re,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution"/"master";SOURCE=BASE/"openaire-locations.csv";MANIFEST=BASE/"openaire-download-manifest.csv";DEST=ROOT/"library"/"staging"/"master-openaire";UA="DesignConversacionalMundaneum/1.1"
def rows(path):
 with path.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def fetch(item):
 target=DEST/f"{item['candidate_id']}-{re.sub(r'[^a-zA-Z0-9]+','-',item['title']).strip('-')[:65]}.pdf";out={"candidate_id":item["candidate_id"],"corpus_id":item["corpus_id"],"title":item["title"],"doi":item["doi"],"url":item["candidate_url"],"license":item["license"],"version":item["version"],"source_name":item["hosted_by"],"path":target.relative_to(ROOT).as_posix(),"downloaded":"false","pdf_signature":"false","bytes":"0","sha256":"","content_type":"","retrieved_at":datetime.now(timezone.utc).isoformat(),"error":""}
 try:
  req=urllib.request.Request(item["candidate_url"],headers={"User-Agent":UA,"Accept":"application/pdf,*/*;q=0.5"})
  with urllib.request.urlopen(req,timeout=60) as response:data=response.read();out["content_type"]=response.headers.get("Content-Type","")
  valid=data.startswith(b"%PDF-")
  if valid:target.write_bytes(data)
  out.update({"downloaded":"true","pdf_signature":str(valid).lower(),"bytes":str(len(data)),"sha256":hashlib.sha256(data).hexdigest(),"error":"" if valid else "response-is-not-pdf"})
 except Exception as exc:out["error"]=repr(exc)
 return out
def main():
 selected=[];seen=set()
 for number,item in enumerate(rows(SOURCE),1):
  url=item["candidate_url"].strip()
  if item["is_open"]!="true" or not url or url in seen:continue
  seen.add(url);selected.append({**item,"candidate_id":f"{item['corpus_id']}-OP{number:04d}"})
 DEST.mkdir(parents=True,exist_ok=True);result=[]
 with ThreadPoolExecutor(max_workers=8) as pool:
  for future in as_completed([pool.submit(fetch,x) for x in selected]):result.append(future.result())
 result.sort(key=lambda x:x["candidate_id"]);fields=list(result[0]) if result else []
 with MANIFEST.open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(result)
 summary={"unique_open_urls":len(result),"pdf_signatures":sum(x["pdf_signature"]=="true" for x in result),"failures":sum(bool(x["error"]) for x in result),"studies_with_pdf":len({x["corpus_id"] for x in result if x["pdf_signature"]=="true"})}
 (BASE/"openaire-download-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
