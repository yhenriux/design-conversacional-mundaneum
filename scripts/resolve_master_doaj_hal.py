#!/usr/bin/env python3
"""Consulta DOAJ e HAL para todos os DOI ainda sem documento validado."""
import argparse,csv,json,urllib.parse,urllib.request
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution"/"master";SOURCE=ROOT/"data"/"corpus"/"master-corpus.csv";ATTEMPTS=BASE/"doaj-hal-attempts.csv";LOCATIONS=BASE/"doaj-hal-locations.csv";UA="DesignConversacionalMundaneum/1.1"
def rows(path):
 if not path.exists():return []
 with path.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
 with urllib.request.urlopen(req,timeout=60) as response:return json.loads(response.read())
def resolve(row):
 found=[];errors=[]
 try:
  url="https://doaj.org/api/search/articles/"+urllib.parse.quote("doi:"+row["doi"],safe=":/")+"?pageSize=5";data=get(url)
  for item in data.get("results") or []:
   bib=item.get("bibjson") or {};journal=bib.get("journal") or {}
   for link in bib.get("link") or []:
    found.append({"corpus_id":row["corpus_id"],"title":row["title"],"doi":row["doi"],"resolver":"DOAJ","candidate_url":link.get("url") or "","link_type":link.get("type") or "","content_type":link.get("content_type") or "","license":"","repository":journal.get("title") or ""})
 except Exception as exc:errors.append("DOAJ="+repr(exc))
 try:
  params={"q":'doiId_s:"'+row["doi"]+'"',"fl":"title_s,doiId_s,fileMain_s,uri_s,license_s","wt":"json","rows":5};data=get("https://api.archives-ouvertes.fr/search/?"+urllib.parse.urlencode(params))
  for item in (data.get("response") or {}).get("docs") or []:
   if item.get("fileMain_s"):found.append({"corpus_id":row["corpus_id"],"title":row["title"],"doi":row["doi"],"resolver":"HAL","candidate_url":item.get("fileMain_s") or "","link_type":"fulltext","content_type":"application/pdf","license":item.get("license_s") or "","repository":"HAL"})
 except Exception as exc:errors.append("HAL="+repr(exc))
 attempt={"corpus_id":row["corpus_id"],"title":row["title"],"doi":row["doi"],"locations":str(len(found)),"queried_at":datetime.now(timezone.utc).isoformat(),"error":" | ".join(errors)};return attempt,found
def write(path,data,fallback):
 fields=list(data[0]) if data else fallback
 with path.open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(data)
def main():
 p=argparse.ArgumentParser();p.add_argument("--limit",type=int,default=150);p.add_argument("--workers",type=int,default=8);a=p.parse_args();corpus=rows(SOURCE);old=rows(ATTEMPTS);loc=rows(LOCATIONS);done={x["corpus_id"] for x in old};eligible=[x for x in corpus if x["document_status"]=="sem-url-pdf-resolucao-pendente" and x["doi"]];pending=[x for x in eligible if x["corpus_id"] not in done][:a.limit];new=[];newloc=[]
 with ThreadPoolExecutor(max_workers=a.workers) as pool:
  for future in as_completed([pool.submit(resolve,x) for x in pending]):attempt,found=future.result();new.append(attempt);newloc.extend(found)
 attempts=old+sorted(new,key=lambda x:x["corpus_id"]);locations=loc+sorted(newloc,key=lambda x:(x["corpus_id"],x["resolver"],x["candidate_url"]));write(ATTEMPTS,attempts,["corpus_id","title","doi","locations","queried_at","error"]);write(LOCATIONS,locations,["corpus_id","title","doi","resolver","candidate_url","link_type","content_type","license","repository"])
 summary={"eligible_doi":len(eligible),"attempted_total":len(attempts),"attempted_this_run":len(new),"locations_total":len(locations),"studies_with_location":len({x["corpus_id"] for x in locations if x["candidate_url"]}),"doaj_locations":sum(x["resolver"]=="DOAJ" for x in locations),"hal_locations":sum(x["resolver"]=="HAL" for x in locations),"errors_total":sum(bool(x["error"]) for x in attempts),"remaining":len(eligible)-len(attempts)};(BASE/"doaj-hal-resolution-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
