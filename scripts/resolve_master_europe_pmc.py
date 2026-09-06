#!/usr/bin/env python3
"""Resolve DOI no Europe PMC e localiza PDFs no conjunto aberto PMC."""
import csv,json,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution"/"master";SOURCE=ROOT/"data"/"corpus"/"master-corpus.csv";OUTPUT=BASE/"europe-pmc-resolution.csv";UA="DesignConversacionalMundaneum/1.1"
def rows(path):
 with path.open(encoding="utf-8-sig",newline="") as h:return list(csv.DictReader(h))
def get(url,accept):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":accept})
 with urllib.request.urlopen(req,timeout=60) as response:return response.read()
def s3(pmcid):
 raw=get("https://pmc-oa-opendata.s3.amazonaws.com/?"+urllib.parse.urlencode({"list-type":"2","prefix":pmcid+"."}),"application/xml");root=ET.fromstring(raw);ns="{http://s3.amazonaws.com/doc/2006-03-01/}";keys=[x.text for x in root.findall(ns+"Contents/"+ns+"Key")];pdf=[k for k in keys if k and k.lower().endswith(".pdf")];return "https://pmc-oa-opendata.s3.amazonaws.com/"+urllib.parse.quote(pdf[0],safe="/") if pdf else ""
def resolve(row):
 out={"corpus_id":row["corpus_id"],"title":row["title"],"doi":row["doi"],"pmid":"","pmcid":"","is_oa":"","has_pdf":"","pdf_url":"","queried_at":datetime.now(timezone.utc).isoformat(),"error":""}
 try:
  url="https://www.ebi.ac.uk/europepmc/webservices/rest/search?"+urllib.parse.urlencode({"query":"DOI:"+row["doi"],"format":"json"});data=json.loads(get(url,"application/json"));found=(data.get("resultList") or {}).get("result") or []
  if found:
   item=found[0];out.update({"pmid":item.get("pmid") or "","pmcid":item.get("pmcid") or "","is_oa":item.get("isOpenAccess") or "","has_pdf":item.get("hasPDF") or ""})
   if out["pmcid"] and out["is_oa"]=="Y" and out["has_pdf"]=="Y":out["pdf_url"]=s3(out["pmcid"])
 except Exception as exc:out["error"]=repr(exc)
 return out
def main():
 selected=[x for x in rows(SOURCE) if x["document_status"]=="sem-url-pdf-resolucao-pendente" and x["doi"]];result=[]
 with ThreadPoolExecutor(max_workers=8) as pool:
  for future in as_completed([pool.submit(resolve,x) for x in selected]):result.append(future.result())
 result.sort(key=lambda x:x["corpus_id"]);fields=list(result[0]) if result else []
 with OUTPUT.open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(result)
 summary={"queried":len(result),"matched":sum(bool(x["pmid"] or x["pmcid"]) for x in result),"open_pdfs":sum(bool(x["pdf_url"]) for x in result),"errors":sum(bool(x["error"]) for x in result)};(BASE/"europe-pmc-resolution-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
