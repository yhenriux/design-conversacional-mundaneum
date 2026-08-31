#!/usr/bin/env python3
"""Corrige o funil inicial e inclui candidatos que podem alcançar 7/10."""
import csv,json,re,unicodedata
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];RUN=ROOT/"data"/"search-runs"/"20260831T003810Z";OUT=ROOT/"data"/"screening"
ACTION_TERMS=["guideline","framework","design implication","implications for design","design principle","pattern","method","evaluation","we propose","we identify","findings","recommendation","heuristic","model"]
def norm(v):return re.sub(r"[^a-z0-9]+"," ",unicodedata.normalize("NFKD",v or "").encode("ascii","ignore").decode().lower()).strip()
def key(row):
 doi=(row.get("doi") or "").lower().replace("https://doi.org/","").strip();return "doi:"+doi if doi else "title:"+norm(row.get("title"))+":"+(row.get("year") or "")
def read(path):
 with path.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def main():
 candidates=read(RUN/"candidates-deduplicated.csv");reviewed={key(r) for r in read(OUT/"screening-decisions.csv")};rows=[]
 for row in candidates:
  if key(row) in reviewed or int(row["ontology_score"] or 0)<3:continue
  document=2 if row.get("pdf_url") else (1 if row.get("doi") else 0);abstract=(row.get("abstract") or "").lower();action=1 if any(term in abstract for term in ACTION_TERMS) else 0
  expanded=int(row["provisional_score"] or 0)+document+action
  if expanded<7:continue
  row.update({"documentary_signal":document,"actionable_signal":action,"expanded_possible_score":expanded,"queue_reason":"Pode alcançar o limiar 7/10 após evidência documental e contribuição aplicável.","screening_decision":"screening-required"});rows.append(row)
 fields=list(rows[0]) if rows else []
 with (OUT/"expanded-screening-queue.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
 summary={"deduplicated_candidates":len(candidates),"already_screened":len(reviewed),"ontology_at_least_3":sum(int(r["ontology_score"] or 0)>=3 for r in candidates),"new_queue":len(rows),"by_possible_score":dict(Counter(r["expanded_possible_score"] for r in rows)),"decision_required":True}
 (OUT/"expanded-screening-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
