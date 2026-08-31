#!/usr/bin/env python3
"""Baixa e valida todas as localizações alternativas retornadas pelo OpenAlex."""
import csv,hashlib,json,re,unicodedata,urllib.request
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution";DEST=ROOT/"library"/"staging"/"openalex-alt";STOP={"the","a","an","of","for","to","and","in","on","with","as","is","or","de","da","do","das","dos","para","e","em"}
def tokens(v):
 v=unicodedata.normalize("NFKD",v or "").encode("ascii","ignore").decode().lower();return {x for x in re.findall(r"[a-z0-9]+",v) if len(x)>2 and x not in STOP}
def main():
 with (BASE/"openalex-all-locations.csv").open(encoding="utf-8-sig",newline="") as h:rows=list(csv.DictReader(h))
 DEST.mkdir(parents=True,exist_ok=True);results=[]
 for row in rows:
  suffix=hashlib.sha256(row["pdf_url"].encode()).hexdigest()[:10];target=DEST/(re.sub(r"[^a-zA-Z0-9._-]+","-",row["doi"])+"-"+suffix+".pdf");result={**row,"valid_pdf":"false","correspondence":"false","coverage":"0","pages":"","bytes":"0","sha256":"","local_path":"","error":""}
  try:
   req=urllib.request.Request(row["pdf_url"],headers={"User-Agent":"DesignConversacionalMundaneum/1.0","Accept":"application/pdf,*/*;q=.5"})
   with urllib.request.urlopen(req,timeout=90) as response:data=response.read()
   if not data.startswith(b"%PDF-"):raise ValueError("response-is-not-pdf")
   target.write_bytes(data);reader=PdfReader(target);sample=" ".join((reader.pages[i].extract_text() or "") for i in range(min(3,len(reader.pages))))
   expected=tokens(row["title"]);coverage=len(expected&tokens(sample))/len(expected) if expected else 0;matched=coverage>=.60
   result.update({"valid_pdf":"true","correspondence":str(matched).lower(),"coverage":f"{coverage:.3f}","pages":len(reader.pages),"bytes":len(data),"sha256":hashlib.sha256(data).hexdigest(),"local_path":str(target.relative_to(ROOT)) if matched else ""})
   if not matched:target.unlink(missing_ok=True);result["error"]="title-mismatch"
  except Exception as exc:target.unlink(missing_ok=True);result["error"]=repr(exc)
  results.append(result)
 fields=list(results[0]) if results else []
 with (BASE/"openalex-alt-download-manifest.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 summary={"attempted":len(results),"matched_documents":sum(r["correspondence"]=="true" for r in results),"unique_matched_doi":len({r["doi"] for r in results if r["correspondence"]=="true"}),"errors":sum(bool(r["error"]) for r in results)}
 (BASE/"openalex-alt-download-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
