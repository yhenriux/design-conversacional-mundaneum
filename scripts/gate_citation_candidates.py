#!/usr/bin/env python3
"""Aplica o portão ontológico preliminar aos candidatos descobertos por citações."""
import argparse,csv,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def norm(s): return re.sub(r"\s+"," ",(s or "").casefold()).strip()
def main():
 p=argparse.ArgumentParser();p.add_argument("input");p.add_argument("--output",required=True);a=p.parse_args()
 gate=json.loads((ROOT/"config"/"ontology-gate.json").read_text(encoding="utf-8"));terms=[norm(x) for x in gate["title_anchors"]+gate["system_terms"]+gate["field_relevance_terms"]]
 with Path(a.input).open(encoding="utf-8-sig",newline="") as h: rows=list(csv.DictReader(h))
 out=[]
 for r in rows:
  text=norm(" ".join([r.get("title",""),r.get("seed_title","")]))
  hits=sum(1 for t in terms if t and t in text)
  if hits<2: continue
  out.append({"run_id":"citation-20260907T231123Z","query":r.get("relation","citacao"),"source_api":"OpenAlex-citation","source_id":r.get("openalex_id",""),"doi":r.get("doi",""),"title":r.get("title",""),"year":r.get("year",""),"authors":"","type":r.get("type",""),"abstract":"","landing_url":r.get("landing_url",""),"pdf_url":r.get("pdf_url",""),"license":"","oa_status":"","ontology_score":"2","provisional_score":str(min(5,2+hits)),"automatic_signal":f"termos={hits}; relação={r.get('relation','')}","decision":"candidato-por-citacao","decision_reason":"Aderência preliminar por título; requer confirmação posterior.","citation_relation":r.get("relation","")})
 fields=list(out[0]) if out else ["run_id","query","source_api","source_id","doi","title","year","authors","type","abstract","landing_url","pdf_url","license","oa_status","ontology_score","provisional_score","automatic_signal","decision","decision_reason","citation_relation"]
 with Path(a.output).open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(out)
 print(json.dumps({"input":len(rows),"eligible":len(out),"output":a.output},ensure_ascii=False))
if __name__=="__main__": main()
