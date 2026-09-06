#!/usr/bin/env python3
"""Resolve de forma retomável instâncias documentais no OpenAIRE."""
import argparse,csv,json,urllib.parse,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/"data"/"document-resolution"/"master"; SOURCE=ROOT/"data"/"corpus"/"master-corpus.csv"
ATTEMPTS=BASE/"openaire-resolution-attempts.csv"; LOCATIONS=BASE/"openaire-locations.csv"; RAW=BASE/"raw"/"openaire"; UA="DesignConversacionalMundaneum/1.1"
def rows(path):
 if not path.exists():return []
 with path.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def resolve(row,timeout):
 url="https://api.openaire.eu/graph/v3/research-products?"+urllib.parse.urlencode({"pid":row["doi"],"pageSize":10})
 attempt={"corpus_id":row["corpus_id"],"title":row["title"],"doi":row["doi"],"resolved":"false","instances":"0","resolved_at":datetime.now(timezone.utc).isoformat(),"error":""}; found=[]; raw={}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
  with urllib.request.urlopen(req,timeout=timeout) as response:raw=json.loads(response.read())
  products=raw.get("results") or []
  for product in products:
   for instance in product.get("instances") or []:
    access=instance.get("accessRight") or {}; hosted=instance.get("hostedBy") or {}; collected=instance.get("collectedFrom") or {}
    for candidate in instance.get("urls") or []:
     found.append({"corpus_id":row["corpus_id"],"title":row["title"],"doi":row["doi"],"openaire_id":product.get("id") or "","candidate_url":candidate,"is_open":str(access.get("label") in {"OPEN","Open Access"}).lower(),"access_label":access.get("label") or "","oa_route":access.get("openAccessRoute") or "","license":instance.get("license") or "","version":instance.get("type") or "","hosted_by":hosted.get("value") or "","collected_from":collected.get("value") or ""})
  attempt.update({"resolved":str(bool(products)).lower(),"instances":str(len(found))})
 except Exception as exc:attempt["error"]=repr(exc)
 return attempt,found,raw
def write(path,data,fallback):
 fields=list(data[0]) if data else fallback
 with path.open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(data)
def main():
 p=argparse.ArgumentParser();p.add_argument("--limit",type=int,default=100);p.add_argument("--workers",type=int,default=6);p.add_argument("--timeout",type=int,default=60);a=p.parse_args()
 corpus=rows(SOURCE); old=rows(ATTEMPTS); loc=rows(LOCATIONS); done={x["corpus_id"] for x in old}; eligible=[x for x in corpus if x["document_status"]=="sem-url-pdf-resolucao-pendente" and x["doi"]]; pending=[x for x in eligible if x["corpus_id"] not in done][:a.limit]
 BASE.mkdir(parents=True,exist_ok=True);RAW.mkdir(parents=True,exist_ok=True);new=[];newloc=[]
 with ThreadPoolExecutor(max_workers=a.workers) as pool:
  futures={pool.submit(resolve,x,a.timeout):x for x in pending}
  for future in as_completed(futures):
   attempt,found,raw=future.result();new.append(attempt);newloc.extend(found)
   if raw:(RAW/f"{attempt['corpus_id']}.json").write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding="utf-8")
 allattempts=old+sorted(new,key=lambda x:x["corpus_id"]);allloc=loc+sorted(newloc,key=lambda x:(x["corpus_id"],x["candidate_url"]))
 write(ATTEMPTS,allattempts,["corpus_id","title","doi","resolved","instances","resolved_at","error"]);write(LOCATIONS,allloc,["corpus_id","title","doi","openaire_id","candidate_url","is_open","access_label","oa_route","license","version","hosted_by","collected_from"])
 summary={"eligible_doi":len(eligible),"attempted_total":len(allattempts),"attempted_this_run":len(new),"resolved_total":sum(x["resolved"]=="true" for x in allattempts),"locations_total":len(allloc),"open_urls_total":sum(x["is_open"]=="true" and bool(x["candidate_url"]) for x in allloc),"studies_with_open_url":len({x["corpus_id"] for x in allloc if x["is_open"]=="true" and x["candidate_url"]}),"errors_total":sum(bool(x["error"]) for x in allattempts),"remaining":len(eligible)-len(allattempts)}
 (BASE/"openaire-resolution-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
