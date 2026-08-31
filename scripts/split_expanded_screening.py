#!/usr/bin/env python3
"""Divide a triagem expandida em lotes estáveis e identificáveis."""
import csv,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/"data"/"screening"/"expanded-screening-queue.csv";DEST=ROOT/"data"/"screening"/"batches"
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h:rows=list(csv.DictReader(h))
 for index,row in enumerate(rows,1):row["expanded_id"]=f"X{index:03d}";row["batch_id"]=f"B{math.ceil(index/50):02d}"
 DEST.mkdir(parents=True,exist_ok=True);fields=["expanded_id","batch_id"]+[x for x in rows[0] if x not in {"expanded_id","batch_id"}]
 for batch in sorted({r["batch_id"] for r in rows}):
  with (DEST/f"{batch}.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows([r for r in rows if r["batch_id"]==batch])
 manifest={"records":len(rows),"batch_size":50,"batches":{b:sum(r["batch_id"]==b for r in rows) for b in sorted({r["batch_id"] for r in rows})}}
 (DEST/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(manifest,ensure_ascii=False))
if __name__=="__main__":main()
