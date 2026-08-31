#!/usr/bin/env python3
"""Reúne documentos validados por diferentes resolvedores em um manifesto canônico."""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/"data"/"document-resolution"
def read(name):
 with (BASE/name).open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def main():
 downloads={r["doi"]:r for r in read("download-manifest.csv")};rows=[]
 for inspection in read("pdf-inspection.csv"):
  if inspection["correspondence"]!="true":continue
  d=downloads[inspection["doi"]];rows.append({"title":inspection["title"],"doi":inspection["doi"],"local_path":d["path"],"pages":inspection["pages"],"sha256":d["sha256"],"resolver":"OpenAlex","license":d["license"],"version":d["version"]})
 for item in read("openaire-download-manifest.csv"):
  if item["correspondence"]!="true" or any(r["doi"]==item["doi"] for r in rows):continue
  rows.append({"title":item["title"],"doi":item["doi"],"local_path":item["local_path"],"pages":item["pages"],"sha256":item["sha256"],"resolver":"OpenAIRE","license":item["license"],"version":""})
 if (BASE/"europe-pmc-download-manifest.csv").exists():
  for item in read("europe-pmc-download-manifest.csv"):
   if item["correspondence"]!="true" or any(r["doi"]==item["doi"] for r in rows):continue
   rows.append({"title":item["title"],"doi":item["doi"],"local_path":item["local_path"],"pages":item["pages"],"sha256":item["sha256"],"resolver":"Europe PMC","license":item["license"],"version":"publishedVersion"})
 fields=list(rows[0]);
 with (BASE/"validated-documents.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
 print(f"validated={len(rows)}")
if __name__=="__main__":main()
