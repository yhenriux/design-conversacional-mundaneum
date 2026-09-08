#!/usr/bin/env python3
"""Extrai textos paginados de PDFs cuja correspondência foi validada."""
import argparse,csv,hashlib
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
VALIDATED=ROOT/"data"/"document-resolution"/"validated-documents.csv"
DEST=ROOT/"extracted-text"/"local-only"
MANIFEST=ROOT/"data"/"document-resolution"/"extraction-manifest.csv"
def main():
 p=argparse.ArgumentParser(); p.add_argument("--validated",type=Path,default=VALIDATED); p.add_argument("--destination",type=Path,default=DEST); p.add_argument("--manifest",type=Path,default=MANIFEST); p.add_argument("--resume",action="store_true",help="Reaproveita registros já extraídos e grava o manifesto após cada documento."); a=p.parse_args()
 with a.validated.open(encoding="utf-8-sig",newline="") as h: valid={r.get("corpus_id") or r.get("expanded_id") or r["doi"]:r for r in csv.DictReader(h)}
 destination=a.destination if a.destination.is_absolute() else ROOT/a.destination
 manifest=a.manifest if a.manifest.is_absolute() else ROOT/a.manifest
 destination.mkdir(parents=True,exist_ok=True); results=[]
 previous={}
 if a.resume and manifest.exists():
  with manifest.open(encoding="utf-8-sig",newline="") as h:
   previous={r["record_id"]:r for r in csv.DictReader(h)}
 fields=["record_id","title","doi","pdf_path","text_path","pages","pages_with_text","page_errors","characters","text_sha256","extraction_status"]
 def write_manifest():
  manifest.parent.mkdir(parents=True,exist_ok=True)
  with manifest.open("w",encoding="utf-8-sig",newline="") as h:
   w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 for record_id,inspection in valid.items():
  if record_id in previous and (ROOT/previous[record_id]["text_path"]).exists():
   results.append(previous[record_id]); continue
  doi=inspection["doi"]
  source=ROOT/inspection["local_path"]; reader=PdfReader(source); parts=[]; extracted_pages=0; page_errors=0
  for number,page in enumerate(reader.pages,1):
   try: text=(page.extract_text() or "").strip()
   except Exception as exc:
    page_errors+=1; text=f"[ERRO DE EXTRAÇÃO NA PÁGINA {number}: {type(exc).__name__}]"
   if text: extracted_pages+=1
   parts.append(f"\n\n===== PAGE {number} =====\n\n{text}")
  content="".join(parts).lstrip()
  content=content.encode("utf-8",errors="replace").decode("utf-8")
  target=destination/(source.stem+".txt"); target.write_text(content,encoding="utf-8")
  results.append({"record_id":record_id,"title":inspection["title"],"doi":doi,"pdf_path":str(source.relative_to(ROOT)),"text_path":str(target.relative_to(ROOT)),
   "pages":len(reader.pages),"pages_with_text":extracted_pages,"page_errors":page_errors,"characters":len(content),"text_sha256":hashlib.sha256(content.encode()).hexdigest(),
   "extraction_status":"complete" if extracted_pages==len(reader.pages) and page_errors==0 else "partial-page-coverage"})
  write_manifest()
 write_manifest()
 print(f"documents={len(results)} complete={sum(r['extraction_status']=='complete' for r in results)}")
if __name__=="__main__":main()
