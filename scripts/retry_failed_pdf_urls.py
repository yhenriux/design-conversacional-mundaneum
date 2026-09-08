#!/usr/bin/env python3
"""Repete tentativas de URLs que falharam, preservando o manifesto original."""
import argparse,csv,hashlib,json,re,urllib.error,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fetch(row, dest, timeout):
 out=dict(row); out["retry_at"]=datetime.now(timezone.utc).isoformat(); out["retry_error"]=""; out["retry_pdf_signature"]="false"
 url=row.get("url") or row.get("pdf_url") or row.get("source_pdf_url") or ""
 if not url:return out
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"DesignConversacionalMundaneum/1.3 (open research collection)","Accept":"application/pdf"})
  with urllib.request.urlopen(req,timeout=timeout) as response:data=response.read();out["retry_content_type"]=response.headers.get("Content-Type","")
  valid=data.startswith(b"%PDF-");out["retry_pdf_signature"]=str(valid).lower();out["retry_bytes"]=str(len(data));out["retry_sha256"]=hashlib.sha256(data).hexdigest()
  if valid:
   target=dest/(row.get("candidate_id","retry")+"-retry.pdf");target.write_bytes(data);out["retry_path"]=target.relative_to(ROOT).as_posix()
  elif not out.get("retry_error"):out["retry_error"]="response-is-not-pdf"
 except Exception as exc:out["retry_error"]=repr(exc)
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("--output",type=Path,required=True);p.add_argument("--destination",type=Path,required=True);p.add_argument("--limit",type=int,default=200);p.add_argument("--timeout",type=int,default=15);a=p.parse_args()
 with a.source.open(encoding="utf-8-sig",newline="") as h:allrows=list(csv.DictReader(h))
 rows=[r for r in allrows if r.get("error") and len([r for r in allrows if r.get("error")])>=0][:a.limit]
 dest=a.destination if a.destination.is_absolute() else ROOT/a.destination;dest.mkdir(parents=True,exist_ok=True);out=[]
 with ThreadPoolExecutor(max_workers=8) as pool:
  for f in as_completed([pool.submit(fetch,r,dest,a.timeout) for r in rows]):out.append(f.result())
 fields=sorted({k for r in out for k in r})
 output=a.output if a.output.is_absolute() else ROOT/a.output;output.parent.mkdir(parents=True,exist_ok=True)
 with output.open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(out)
 print(json.dumps({"eligible_failures":len(rows),"retry_pdf_signatures":sum(r.get("retry_pdf_signature")=="true" for r in out),"output":output.as_posix()},ensure_ascii=False))
if __name__=="__main__":main()
