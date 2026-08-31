#!/usr/bin/env python3
"""Recupera instâncias abertas do OpenAIRE e rejeita associações documentais incorretas."""
import csv,hashlib,json,re,time,unicodedata,urllib.request
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]; SOURCE=ROOT/"data"/"document-resolution"/"openaire-resolution.csv"; DEST=ROOT/"library"/"staging"/"openaire"; OUT=ROOT/"data"/"document-resolution"
UA="DesignConversacionalMundaneum/1.0";STOP={"the","a","an","of","for","to","and","in","on","with","as","is","or","de","da","do","das","dos","para","e","em"}
def tokens(value):
 value=unicodedata.normalize("NFKD",value or "").encode("ascii","ignore").decode().lower()
 return {x for x in re.findall(r"[a-z0-9]+",value) if len(x)>2 and x not in STOP}
def filename(doi,url):return re.sub(r"[^a-zA-Z0-9._-]+","-",doi).strip("-")+"-"+hashlib.sha256(url.encode()).hexdigest()[:10]+".pdf"
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h: rows=list(csv.DictReader(h))
 candidates=[];seen=set()
 for row in rows:
  key=(row["doi"],row["candidate_url"])
  if row["is_open"]=="true" and row["candidate_url"] and key not in seen:candidates.append(row);seen.add(key)
 DEST.mkdir(parents=True,exist_ok=True);results=[]
 for row in candidates:
  target=DEST/filename(row["doi"],row["candidate_url"]); result={"title":row["title"],"doi":row["doi"],"url":row["candidate_url"],"valid_pdf":"false","correspondence":"false","coverage":"0","pages":"","bytes":"0","sha256":"","local_path":"","license":row["license"],"hosted_by":row["hosted_by"],"error":""}
  try:
   req=urllib.request.Request(row["candidate_url"],headers={"User-Agent":UA,"Accept":"application/pdf,*/*;q=.5"})
   with urllib.request.urlopen(req,timeout=90) as response:data=response.read()
   result["bytes"]=len(data);result["sha256"]=hashlib.sha256(data).hexdigest()
   if not data.startswith(b"%PDF-"):raise ValueError("response-is-not-pdf")
   target.write_bytes(data);reader=PdfReader(target);sample=" ".join((reader.pages[i].extract_text() or "") for i in range(min(3,len(reader.pages))))
   expected=tokens(row["title"]);observed=tokens(sample);coverage=len(expected&observed)/len(expected) if expected else 0
   result.update({"valid_pdf":"true","coverage":f"{coverage:.3f}","pages":len(reader.pages),"correspondence":str(coverage>=.60).lower()})
   if coverage>=.60:result["local_path"]=str(target.relative_to(ROOT))
   else:target.unlink(missing_ok=True);result["error"]="title-mismatch"
  except Exception as exc:result["error"]=repr(exc) if not result["error"] else result["error"];target.unlink(missing_ok=True)
  results.append(result);time.sleep(.2)
 fields=list(results[0]) if results else []
 with (OUT/"openaire-download-manifest.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 summary={"attempted":len(results),"pdf_responses":sum(r["valid_pdf"]=="true" for r in results),"matched_documents":sum(r["correspondence"]=="true" for r in results),"title_mismatches":sum(r["error"]=="title-mismatch" for r in results),"errors":sum(bool(r["error"]) for r in results)}
 (OUT/"openaire-download-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
