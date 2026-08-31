#!/usr/bin/env python3
"""Baixa e valida os preprints encontrados no arXiv."""
import csv,hashlib,json,re,unicodedata,urllib.request
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution";DEST=ROOT/"library"/"staging"/"arxiv";STOP={"the","a","an","of","for","to","and","in","on","with","as","is","or","de","da","do","das","dos","para","e","em"}
def tokens(v):
 v=unicodedata.normalize("NFKD",v or "").encode("ascii","ignore").decode().lower();return {x for x in re.findall(r"[a-z0-9]+",v) if len(x)>2 and x not in STOP}
def main():
 with (BASE/"arxiv-resolution.csv").open(encoding="utf-8-sig",newline="") as h:rows=[r for r in csv.DictReader(h) if r["pdf_url"]]
 DEST.mkdir(parents=True,exist_ok=True);results=[]
 for row in rows:
  aid=row["arxiv_id"].rsplit("/",1)[-1];target=DEST/(aid+".pdf");result={"title":row["title"],"doi":row["doi"],"arxiv_id":row["arxiv_id"],"url":row["pdf_url"],"valid_pdf":"false","correspondence":"false","coverage":"0","pages":"","bytes":"0","sha256":"","local_path":"","license":"arXiv-distribution","error":""}
  try:
   req=urllib.request.Request(row["pdf_url"],headers={"User-Agent":"DesignConversacionalMundaneum/1.0","Accept":"application/pdf"})
   with urllib.request.urlopen(req,timeout=90) as response:data=response.read()
   if not data.startswith(b"%PDF-"):raise ValueError("response-is-not-pdf")
   target.write_bytes(data);reader=PdfReader(target);sample=" ".join((reader.pages[i].extract_text() or "") for i in range(min(3,len(reader.pages))))
   expected=tokens(row["title"]);coverage=len(expected&tokens(sample))/len(expected) if expected else 0;matched=coverage>=.60
   result.update({"valid_pdf":"true","correspondence":str(matched).lower(),"coverage":f"{coverage:.3f}","pages":len(reader.pages),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"local_path":str(target.relative_to(ROOT)) if matched else ""})
   if not matched:target.unlink(missing_ok=True);result["error"]="title-mismatch"
  except Exception as exc:target.unlink(missing_ok=True);result["error"]=repr(exc)
  results.append(result)
 fields=list(results[0]) if results else []
 with (BASE/"arxiv-download-manifest.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 summary={"attempted":len(results),"matched_documents":sum(r["correspondence"]=="true" for r in results),"errors":sum(bool(r["error"]) for r in results)}
 (BASE/"arxiv-download-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
