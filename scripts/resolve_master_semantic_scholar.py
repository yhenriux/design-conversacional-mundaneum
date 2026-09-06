#!/usr/bin/env python3
"""Resolve DOI pendentes pelo endpoint em lote do Semantic Scholar."""
import argparse,csv,json,re,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution"/"master";SOURCE=ROOT/"data"/"corpus"/"master-corpus.csv";ATTEMPTS=BASE/"semantic-scholar-resolution.csv";UA="DesignConversacionalMundaneum/1.1"
def rows(path):
 if not path.exists():return []
 with path.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def doi(v):return re.sub(r"^https?://(dx\.)?doi\.org/","",v or "",flags=re.I)
def main():
 p=argparse.ArgumentParser();p.add_argument("--batch-size",type=int,default=500);p.add_argument("--retries",type=int,default=3);a=p.parse_args()
 corpus=rows(SOURCE);old=rows(ATTEMPTS);done={x["corpus_id"] for x in old};eligible=[x for x in corpus if x["document_status"]=="sem-url-pdf-resolucao-pendente" and x["doi"] and x["corpus_id"] not in done];selected=eligible[:a.batch_size]
 payload=json.dumps({"ids":["DOI:"+doi(x["doi"]) for x in selected]}).encode();url="https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,externalIds,url,openAccessPdf"
 data=None;error=""
 for attempt in range(a.retries):
  try:
   req=urllib.request.Request(url,data=payload,method="POST",headers={"User-Agent":UA,"Accept":"application/json","Content-Type":"application/json"})
   with urllib.request.urlopen(req,timeout=120) as response:data=json.loads(response.read());break
  except Exception as exc:error=repr(exc);time.sleep(5*(attempt+1))
 now=datetime.now(timezone.utc).isoformat();new=[]
 if data is not None:
  for source,item in zip(selected,data):
   item=item or {};oa=item.get("openAccessPdf") or {}
   new.append({"corpus_id":source["corpus_id"],"title":source["title"],"doi":source["doi"],"semantic_scholar_id":item.get("paperId") or "","resolved":str(bool(item)).lower(),"open_access_pdf_url":oa.get("url") or "","open_access_status":oa.get("status") or "","landing_url":item.get("url") or "","retrieved_at":now,"error":""})
 else:
  for source in selected:new.append({"corpus_id":source["corpus_id"],"title":source["title"],"doi":source["doi"],"semantic_scholar_id":"","resolved":"false","open_access_pdf_url":"","open_access_status":"","landing_url":"","retrieved_at":now,"error":error})
 combined=old+new;fields=list(combined[0]) if combined else []
 with ATTEMPTS.open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(combined)
 summary={"eligible_at_start":len(eligible)+len(old),"attempted_total":len(combined),"attempted_this_run":len(new),"resolved_total":sum(x["resolved"]=="true" for x in combined),"with_open_pdf":sum(bool(x["open_access_pdf_url"]) for x in combined),"studies_with_open_pdf":len({x["corpus_id"] for x in combined if x["open_access_pdf_url"]}),"errors_total":sum(bool(x["error"]) for x in combined),"remaining":max(0,len(eligible)-len(selected))}
 (BASE/"semantic-scholar-resolution-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
