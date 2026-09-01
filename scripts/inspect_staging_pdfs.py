#!/usr/bin/env python3
"""Inspeciona estrutura e correspondência textual dos PDFs no estágio local."""
import argparse,csv,hashlib,re,unicodedata
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"document-resolution"/"download-manifest.csv"
OUTPUT=ROOT/"data"/"document-resolution"/"pdf-inspection.csv"
STOP={"the","a","an","of","for","to","and","in","on","with","as","is","or","de","da","do","das","dos","para","e","em"}
def tokens(value):
 value=unicodedata.normalize("NFKD",value or "").encode("ascii","ignore").decode().lower()
 return {x for x in re.findall(r"[a-z0-9]+",value) if len(x)>2 and x not in STOP}
def main():
 p=argparse.ArgumentParser(); p.add_argument("--source",type=Path,default=SOURCE); p.add_argument("--output",type=Path,default=OUTPUT); a=p.parse_args()
 with a.source.open(encoding="utf-8-sig",newline="") as h: rows=list(csv.DictReader(h))
 results=[]
 for row in rows:
  validity=row.get("valid_pdf",row.get("pdf_signature","false"))
  if validity!="true": continue
  path=ROOT/row["path"]; result={"corpus_id":row.get("corpus_id",""),"expanded_id":row.get("expanded_id",""),"title":row["title"],"doi":row["doi"],"path":row["path"],"pages":"","encrypted":"","metadata_title":"","title_token_coverage":"0","correspondence":"false","text_sha256":"","error":""}
  try:
   reader=PdfReader(path); result["pages"]=len(reader.pages); result["encrypted"]=str(reader.is_encrypted).lower(); meta=reader.metadata or {}; result["metadata_title"]=str(meta.get("/Title") or "")
   sample=" ".join((reader.pages[i].extract_text() or "") for i in range(min(3,len(reader.pages))))
   expected=tokens(row["title"]); observed=tokens(sample+" "+result["metadata_title"]); coverage=len(expected&observed)/len(expected) if expected else 0
   result["title_token_coverage"]=f"{coverage:.3f}"; result["correspondence"]=str(coverage>=.60).lower(); result["text_sha256"]=hashlib.sha256(sample.encode("utf-8")).hexdigest()
  except Exception as exc: result["error"]=repr(exc)
  results.append(result)
 fields=list(results[0]) if results else ["corpus_id","expanded_id","title","doi","path","pages","encrypted","metadata_title","title_token_coverage","correspondence","text_sha256","error"]
 a.output.parent.mkdir(parents=True,exist_ok=True)
 with a.output.open("w",encoding="utf-8-sig",newline="") as h:
  w=csv.DictWriter(h,fieldnames=fields); w.writeheader(); w.writerows(results)
 print(f"inspected={len(results)} correspondence={sum(r['correspondence']=='true' for r in results)} errors={sum(bool(r['error']) for r in results)}")
if __name__=="__main__": main()
