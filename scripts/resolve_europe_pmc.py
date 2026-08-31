#!/usr/bin/env python3
"""Resolve DOI biomédico em Europe PMC e localiza PDF no conjunto aberto PMC."""
import csv,json,time,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution";SOURCE=BASE/"document-status.csv";UA="DesignConversacionalMundaneum/1.0"
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json,application/xml"})
 with urllib.request.urlopen(req,timeout=60) as r:return r.read()
def s3_pdf(pmcid):
 raw=get("https://pmc-oa-opendata.s3.amazonaws.com/?"+urllib.parse.urlencode({"list-type":"2","prefix":pmcid+"."}))
 root=ET.fromstring(raw); keys=[node.text for node in root.findall("{http://s3.amazonaws.com/doc/2006-03-01/}Contents/{http://s3.amazonaws.com/doc/2006-03-01/}Key")]
 preferred=[k for k in keys if k.lower().endswith(".pdf") and k.rsplit("/",1)[-1].lower().startswith(pmcid.lower()+".")]
 return "https://pmc-oa-opendata.s3.amazonaws.com/"+urllib.parse.quote(preferred[0],safe="/") if preferred else ""
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h:rows=[r for r in csv.DictReader(h) if r["document_status"]!="pdf-integral-validado-local" and r["doi"]]
 results=[]
 for row in rows:
  result={"title":row["title"],"doi":row["doi"],"pmid":"","pmcid":"","is_oa":"","has_pdf":"","pmc_pdf_url":"","error":""}
  try:
   url="https://www.ebi.ac.uk/europepmc/webservices/rest/search?"+urllib.parse.urlencode({"query":"DOI:"+row["doi"],"format":"json"})
   data=json.loads(get(url));found=(data.get("resultList") or {}).get("result") or []
   if found:
    item=found[0];pmcid=item.get("pmcid") or "";result.update({"pmid":item.get("pmid") or "","pmcid":pmcid,"is_oa":item.get("isOpenAccess") or "","has_pdf":item.get("hasPDF") or ""})
    if pmcid and item.get("isOpenAccess")=="Y" and item.get("hasPDF")=="Y":result["pmc_pdf_url"]=s3_pdf(pmcid)
  except Exception as exc:result["error"]=repr(exc)
  results.append(result);time.sleep(.15)
 fields=list(results[0]);
 with (BASE/"europe-pmc-resolution.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 summary={"queried":len(results),"matched":sum(bool(r["pmid"] or r["pmcid"]) for r in results),"open_pdfs":sum(bool(r["pmc_pdf_url"]) for r in results),"errors":sum(bool(r["error"]) for r in results)}
 (BASE/"europe-pmc-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
