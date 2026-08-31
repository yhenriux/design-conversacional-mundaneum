#!/usr/bin/env python3
"""Consulta Semantic Scholar para registros sem PDF validado."""
import csv,json,time,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SOURCE=ROOT/"data"/"document-resolution"/"document-status.csv"; OUT=ROOT/"data"/"document-resolution"
UA="DesignConversacionalMundaneum/1.0 (systematic evidence mapping)"
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h: rows=[r for r in csv.DictReader(h) if r["document_status"]!="pdf-integral-validado-local" and r["doi"]]
 raw=OUT/"semantic-scholar-raw"; raw.mkdir(exist_ok=True); results=[]
 for number,row in enumerate(rows,1):
  result={"title":row["title"],"doi":row["doi"],"semantic_scholar_id":"","resolved":"false","open_access_pdf_url":"","open_access_status":"","landing_url":"","retrieved_at":datetime.now(timezone.utc).isoformat(),"error":""}
  try:
   ident=urllib.parse.quote("DOI:"+row["doi"],safe=":"); url=f"https://api.semanticscholar.org/graph/v1/paper/{ident}?fields=title,externalIds,url,openAccessPdf"
   req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
   with urllib.request.urlopen(req,timeout=45) as response:data=json.loads(response.read())
   (raw/f"{number:03d}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8"); oa=data.get("openAccessPdf") or {}
   result.update({"semantic_scholar_id":data.get("paperId") or "","resolved":"true","open_access_pdf_url":oa.get("url") or "","open_access_status":oa.get("status") or "","landing_url":data.get("url") or ""})
  except Exception as exc:result["error"]=repr(exc)
  results.append(result);time.sleep(.65)
 fields=list(results[0]) if results else []
 with (OUT/"semantic-scholar-resolution.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 summary={"records":len(results),"resolved":sum(r["resolved"]=="true" for r in results),"with_open_pdf":sum(bool(r["open_access_pdf_url"]) for r in results),"errors":sum(bool(r["error"]) for r in results)}
 (OUT/"semantic-scholar-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
