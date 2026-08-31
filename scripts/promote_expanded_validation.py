#!/usr/bin/env python3
"""Promove somente PDFs com correspondência bibliográfica validada."""
import argparse,csv,json
from pathlib import Path

def main():
 p=argparse.ArgumentParser(); p.add_argument("--downloads",type=Path,required=True); p.add_argument("--inspection",type=Path,required=True); p.add_argument("--output-dir",type=Path,required=True); a=p.parse_args()
 with a.downloads.open(encoding="utf-8-sig",newline="") as h: downloads={r["expanded_id"]:r for r in csv.DictReader(h)}
 with a.inspection.open(encoding="utf-8-sig",newline="") as h: inspected=list(csv.DictReader(h))
 rows=[]
 for item in inspected:
  if item["correspondence"]!="true" or item["error"]: continue
  source=downloads[item["expanded_id"]]
  rows.append({"expanded_id":item["expanded_id"],"title":item["title"],"doi":item["doi"],"local_path":item["path"],"pages":item["pages"],"sha256":source["sha256"],"source_url":source["url"],"license":source["license"],"validation":"pdf-integral-validado-local"})
 a.output_dir.mkdir(parents=True,exist_ok=True); output=a.output_dir/"validated-documents.csv"
 fields=list(rows[0]) if rows else []
 with output.open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows(rows)
 summary={"inspected":len(inspected),"validated":len(rows),"rejected_mismatch":sum(r["correspondence"]!="true" for r in inspected),"validation_rule":"Assinatura PDF, leitura estrutural e cobertura mínima de 60% dos tokens do título nas três primeiras páginas."}
 (a.output_dir/"validation-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__": main()
