#!/usr/bin/env python3
"""Valida PDFs recuperados sem contornar controles de acesso."""
import argparse,csv,hashlib
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument("directory",type=Path); p.add_argument("--output",type=Path,required=True); a=p.parse_args(); rows=[]
 for path in sorted(a.directory.rglob("*.pdf")):
  data=path.read_bytes(); rows.append({"path":str(path),"bytes":len(data),"pdf_signature":data.startswith(b"%PDF-"),"sha256":hashlib.sha256(data).hexdigest()})
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=["path","bytes","pdf_signature","sha256"]); w.writeheader(); w.writerows(rows)
 print(f"{len(rows)} arquivos avaliados")
if __name__=="__main__": main()
