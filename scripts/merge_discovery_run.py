#!/usr/bin/env python3
"""Deduplica um novo ciclo de descoberta contra o corpus já registrado."""
from __future__ import annotations
import argparse,csv,json,re
from collections import Counter
from pathlib import Path
from build_master_corpus import identity

ROOT=Path(__file__).resolve().parents[1]
def norm_doi(value:str)->str:return re.sub(r"^https?://(dx\.)?doi\.org/","",value or "",flags=re.I).strip().lower()
def norm_title(value:str)->str:return re.sub(r"[^a-z0-9]+"," ",(value or "").lower()).strip()
def key(row):return identity(row)
def read(path):
 with path.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def main():
 p=argparse.ArgumentParser();p.add_argument("run_id");p.add_argument("--minimum-ontology",type=int,default=3);a=p.parse_args();source=ROOT/"data"/"search-runs"/a.run_id/"candidates.csv";existing=read(ROOT/"data"/"corpus"/"master-corpus.csv");existing_keys={key(x) for x in existing};candidates=read(source);seen=set();out=[]
 prior_path=ROOT/'data'/'discovery'/f'supplemental-{a.run_id}.csv'
 prior=read(prior_path) if prior_path.exists() else []
 out=list(prior);seen={key(row) for row in prior}
 for row in candidates:
  if int(row.get("ontology_score") or 0)<a.minimum_ontology:continue
  item_key=key(row)
  if item_key in existing_keys or item_key in seen:continue
  seen.add(item_key);out.append(row)
 output=ROOT/"data"/"discovery"/f"supplemental-{a.run_id}.csv";output.parent.mkdir(parents=True,exist_ok=True);fields=list(candidates[0]) if candidates else list(prior[0]) if prior else ['source_id','doi','title','ontology_score']
 with output.open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(out)
 summary={"run_id":a.run_id,"raw_occurrences":len(candidates),"centrality_minimum":a.minimum_ontology,"eligible_raw":sum(int(x.get('ontology_score') or 0)>=a.minimum_ontology for x in candidates),"new_unique":len(out),"excluded_as_existing_or_intra_run_duplicate":sum(int(x.get('ontology_score') or 0)>=a.minimum_ontology for x in candidates)-len(out),"by_api":dict(Counter(x['source_api'] for x in out)),"with_pdf_url":sum(bool(x['pdf_url']) for x in out),"output":output.relative_to(ROOT).as_posix()}
 (output.with_suffix('.summary.json')).write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
