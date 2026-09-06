#!/usr/bin/env python3
"""Recupera PDFs abertos indicados pelo Semantic Scholar."""
import csv,hashlib,json,re,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution"/"master";SOURCE=BASE/"semantic-scholar-resolution.csv";MANIFEST=BASE/"semantic-scholar-download-manifest.csv";DEST=ROOT/"library"/"staging"/"master-semantic-scholar";UA="DesignConversacionalMundaneum/1.1"
def rows():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def fetch(x):
 target=DEST/f"{x['candidate_id']}-{re.sub(r'[^a-zA-Z0-9]+','-',x['title']).strip('-')[:65]}.pdf";out={"candidate_id":x["candidate_id"],"corpus_id":x["corpus_id"],"title":x["title"],"doi":x["doi"],"url":x["open_access_pdf_url"],"license":"","version":x["open_access_status"],"source_name":"Semantic Scholar","path":target.relative_to(ROOT).as_posix(),"downloaded":"false","pdf_signature":"false","bytes":"0","sha256":"","content_type":"","retrieved_at":datetime.now(timezone.utc).isoformat(),"error":""}
 try:
  req=urllib.request.Request(x["open_access_pdf_url"],headers={"User-Agent":UA,"Accept":"application/pdf,*/*;q=0.5"})
  with urllib.request.urlopen(req,timeout=60) as response:data=response.read();out["content_type"]=response.headers.get("Content-Type","")
  valid=data.startswith(b"%PDF-")
  if valid:target.write_bytes(data)
  out.update({"downloaded":"true","pdf_signature":str(valid).lower(),"bytes":str(len(data)),"sha256":hashlib.sha256(data).hexdigest(),"error":"" if valid else "response-is-not-pdf"})
 except Exception as exc:out["error"]=repr(exc)
 return out
def main():
 selected=[{**x,"candidate_id":f"{x['corpus_id']}-SS"} for x in rows() if x["open_access_pdf_url"]];DEST.mkdir(parents=True,exist_ok=True);result=[]
 with ThreadPoolExecutor(max_workers=8) as pool:
  for future in as_completed([pool.submit(fetch,x) for x in selected]):result.append(future.result())
 result.sort(key=lambda x:x["candidate_id"]);fields=list(result[0]) if result else []
 with MANIFEST.open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(result)
 summary={"urls":len(result),"pdf_signatures":sum(x["pdf_signature"]=="true" for x in result),"failures":sum(bool(x["error"]) for x in result)};(BASE/"semantic-scholar-download-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
