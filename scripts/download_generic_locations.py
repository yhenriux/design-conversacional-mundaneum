#!/usr/bin/env python3
"""Baixa URLs de um CSV de localizações usando campos configuráveis."""
import argparse,csv,hashlib,json,re,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];UA="DesignConversacionalMundaneum/1.1"
def fetch(x,url_field,dest,label,index):
 corpus_id=x.get('corpus_id') or x.get('seed_corpus_id') or f'candidate-{index:05d}';candidate=f"{corpus_id}-{label}{index:04d}";target=dest/f"{candidate}-{re.sub(r'[^a-zA-Z0-9]+','-',x['title']).strip('-')[:65]}.pdf";url=x[url_field]
 out={"candidate_id":candidate,"corpus_id":corpus_id,"title":x["title"],"doi":x.get("doi",""),"url":url,"license":x.get("license",""),"version":x.get("version",x.get("link_type","")),"source_name":x.get("repository",x.get("resolver",label)),"path":target.relative_to(ROOT).as_posix(),"downloaded":"false","pdf_signature":"false","bytes":"0","sha256":"","content_type":"","retrieved_at":datetime.now(timezone.utc).isoformat(),"error":""}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/pdf,*/*;q=0.5"})
  with urllib.request.urlopen(req,timeout=60) as response:data=response.read();out["content_type"]=response.headers.get("Content-Type","")
  valid=data.startswith(b"%PDF-")
  if valid:target.write_bytes(data)
  out.update({"downloaded":"true","pdf_signature":str(valid).lower(),"bytes":str(len(data)),"sha256":hashlib.sha256(data).hexdigest(),"error":"" if valid else "response-is-not-pdf"})
 except Exception as exc:out["error"]=repr(exc)
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument("--source",type=Path,required=True);p.add_argument("--url-field",required=True);p.add_argument("--label",required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--destination",type=Path,required=True);a=p.parse_args()
 with a.source.open(encoding="utf-8-sig",newline="") as h:source=[x for x in csv.DictReader(h) if x.get(a.url_field)]
 dest=a.destination if a.destination.is_absolute() else ROOT/a.destination;output=a.output if a.output.is_absolute() else ROOT/a.output;dest.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True);result=[]
 with ThreadPoolExecutor(max_workers=8) as pool:
  for future in as_completed([pool.submit(fetch,x,a.url_field,dest,a.label,i) for i,x in enumerate(source,1)]):result.append(future.result())
 result.sort(key=lambda x:x["candidate_id"]);fields=list(result[0]) if result else []
 with output.open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(result)
 summary={"urls":len(result),"pdf_signatures":sum(x["pdf_signature"]=="true" for x in result),"failures":sum(bool(x["error"]) for x in result)};output.with_suffix(".summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
