#!/usr/bin/env python3
"""Consolida o estado documental depois de resolução, download e inspeção."""
import csv,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/"data"/"document-resolution"
def read(name):
 with (BASE/name).open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def main():
 resolution=read("document-resolution.csv"); downloads={r["doi"]:r for r in read("download-manifest.csv")}; validated={r["doi"]:r for r in read("validated-documents.csv")}
 rows=[]
 for r in resolution:
  d=downloads.get(r["doi"],{}); v=validated.get(r["doi"],{})
  if v: status="pdf-integral-validado-local"
  elif d and d.get("valid_pdf")!="true": status="falha-recuperacao-pdf"
  elif r["is_oa"]=="true" and not r["pdf_url"]: status="acesso-aberto-sem-url-pdf"
  elif r["is_oa"]=="true": status="pdf-localizacao-a-validar"
  elif r["resolved"]=="true": status="sem-versao-aberta-localizada"
  else: status="lacuna-documental"
  rows.append({"title":r["title"],"doi":r["doi"],"screening_decision":r["screening_decision"],"document_status":status,"is_oa":r["is_oa"],
   "pdf_url":r["pdf_url"],"license":v.get("license") or r["license"],"local_path":v.get("local_path","") ,"pages":v.get("pages",""),
   "sha256":v.get("sha256","") ,"retrieval_error":d.get("error","")})
 fields=list(rows[0]);
 with (BASE/"document-status.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
 summary={"records":len(rows),"status":dict(Counter(r["document_status"] for r in rows)),"validated_documents":sum(r["document_status"]=="pdf-integral-validado-local" for r in rows)}
 (BASE/"document-status-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
