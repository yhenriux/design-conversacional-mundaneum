#!/usr/bin/env python3
"""Extrai textos paginados de PDFs cuja correspondência foi validada."""
import csv,hashlib
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
INSPECTION=ROOT/"data"/"document-resolution"/"pdf-inspection.csv"
DOWNLOADS=ROOT/"data"/"document-resolution"/"download-manifest.csv"
DEST=ROOT/"extracted-text"/"local-only"
MANIFEST=ROOT/"data"/"document-resolution"/"extraction-manifest.csv"
def main():
 with INSPECTION.open(encoding="utf-8-sig",newline="") as h: valid={r["doi"]:r for r in csv.DictReader(h) if r["correspondence"]=="true"}
 with DOWNLOADS.open(encoding="utf-8-sig",newline="") as h: downloads={r["doi"]:r for r in csv.DictReader(h)}
 DEST.mkdir(parents=True,exist_ok=True); results=[]
 for doi,inspection in valid.items():
  source=ROOT/downloads[doi]["path"]; reader=PdfReader(source); parts=[]; extracted_pages=0
  for number,page in enumerate(reader.pages,1):
   text=(page.extract_text() or "").strip()
   if text: extracted_pages+=1
   parts.append(f"\n\n===== PAGE {number} =====\n\n{text}")
  content="".join(parts).lstrip(); target=DEST/(source.stem+".txt"); target.write_text(content,encoding="utf-8")
  results.append({"title":inspection["title"],"doi":doi,"pdf_path":str(source.relative_to(ROOT)),"text_path":str(target.relative_to(ROOT)),
   "pages":len(reader.pages),"pages_with_text":extracted_pages,"characters":len(content),"text_sha256":hashlib.sha256(content.encode()).hexdigest(),
   "extraction_status":"complete" if extracted_pages==len(reader.pages) else "partial-page-coverage"})
 fields=list(results[0]) if results else ["title","doi","pdf_path","text_path","pages","pages_with_text","characters","text_sha256","extraction_status"]
 with MANIFEST.open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 print(f"documents={len(results)} complete={sum(r['extraction_status']=='complete' for r in results)}")
if __name__=="__main__":main()
