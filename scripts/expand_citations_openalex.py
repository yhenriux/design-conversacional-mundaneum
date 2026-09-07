#!/usr/bin/env python3
"""Expansão por citações a partir de estudos centrais já incluídos.

Preserva candidatos separados do corpus mestre: toda referência citada ou citante
precisa novamente passar por deduplicação e pelo portão ontológico.
"""
from __future__ import annotations
import argparse,csv,json,re,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
UA="DesignConversacionalMundaneum/1.2 (systematic evidence mapping)"
def doi(value): return re.sub(r"^https?://(dx\.)?doi\.org/","",value or "",flags=re.I)
def rows(path):
 with path.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
 with urllib.request.urlopen(req,timeout=60) as r:return json.loads(r.read())
def record(work,relation,seed):
 return {"seed_corpus_id":seed["corpus_id"],"seed_title":seed["title"],"relation":relation,"openalex_id":work.get("id","") ,"doi":work.get("doi","") or "","title":work.get("title","") or "","year":work.get("publication_year","") or "","type":work.get("type","") or "","cited_by_count":work.get("cited_by_count",0),"landing_url":((work.get("primary_location") or {}).get("landing_page_url") or ""),"pdf_url":((work.get("best_oa_location") or {}).get("pdf_url") or ""),"discovery_status":"pendente-de-deduplicacao-e-portao-ontologico"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--limit-seeds",type=int,default=50);p.add_argument("--seed-offset",type=int,default=0);p.add_argument("--citing-per-seed",type=int,default=50);p.add_argument("--references-per-seed",type=int,default=25,help="Limite explícito por ciclo; ciclos posteriores percorrem sementes adicionais.");a=p.parse_args()
 corpus=rows(ROOT/"data/corpus/master-corpus.csv")
 seeds=[r for r in corpus if r.get('ontology_score')=='4' and r['doi']][a.seed_offset:a.seed_offset+a.limit_seeds]
 out=[];seen=set();run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
 rawdir=ROOT/"data/citation-runs"/run_id/"raw";rawdir.mkdir(parents=True,exist_ok=True)
 for seed in seeds:
  try:
   work=fetch("https://api.openalex.org/works/https://doi.org/"+urllib.parse.quote(doi(seed["doi"]),safe=""))
   (rawdir/f"{seed['corpus_id']}-seed.json").write_text(json.dumps(work,ensure_ascii=False,indent=2),encoding="utf-8")
   for ref in (work.get("referenced_works") or [])[:a.references_per_seed]:
    try:
     item=fetch('https://api.openalex.org/works/'+ref.rsplit('/',1)[-1]); key=(seed['corpus_id'],'referenciado',item.get('id'))
     if key not in seen:seen.add(key);out.append(record(item,"referenciado",seed))
    except Exception as exc:
     (rawdir/'errors.jsonl').open('a',encoding='utf-8').write(json.dumps({'seed':seed['corpus_id'],'reference':ref,'error':repr(exc)})+'\n')
   url="https://api.openalex.org/works?filter=cites:"+urllib.parse.quote(work.get("id","").rsplit('/',1)[-1],safe="")+"&per-page="+str(a.citing_per_seed)
   citing=fetch(url)
   (rawdir/f"{seed['corpus_id']}-citantes.json").write_text(json.dumps(citing,ensure_ascii=False,indent=2),encoding="utf-8")
   for item in citing.get("results") or []:
    key=(seed['corpus_id'],'citante',item.get('id'))
    if key not in seen:seen.add(key);out.append(record(item,"citante",seed))
  except Exception as exc:
   print(f"erro {seed['corpus_id']}: {exc}")
 target=ROOT/"data/citation-runs"/run_id;fields=list(out[0]) if out else ["seed_corpus_id","seed_title","relation","openalex_id","doi","title","year","type","cited_by_count","landing_url","pdf_url","discovery_status"]
 with (target/"candidates.csv").open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(out)
 (target/"run.json").write_text(json.dumps({"run_id":run_id,"seed_count":len(seeds),"candidates":len(out),"rule":"Candidatos exigem deduplicação e novo portão ontológico antes do corpus mestre."},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"run_id":run_id,"seeds":len(seeds),"candidates":len(out)},ensure_ascii=False))
if __name__=="__main__":main()
