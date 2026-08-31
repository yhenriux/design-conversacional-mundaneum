#!/usr/bin/env python3
"""Busca preprints equivalentes no arXiv por títulos agrupados."""
import csv,json,re,time,unicodedata,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution";SOURCE=BASE/"document-status.csv";NS={"a":"http://www.w3.org/2005/Atom"}
def norm(v):return re.sub(r"[^a-z0-9]+"," ",unicodedata.normalize("NFKD",v or "").encode("ascii","ignore").decode().lower()).strip()
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h:rows=[r for r in csv.DictReader(h) if r["document_status"]!="pdf-integral-validado-local"]
 results=[]
 for start in range(0,len(rows),8):
  batch=rows[start:start+8];terms=[]
  for row in batch:terms.append('ti:"'+row["title"].replace('"','')+'"')
  url="https://export.arxiv.org/api/query?"+urllib.parse.urlencode({"search_query":" OR ".join(terms),"start":0,"max_results":50})
  try:
   req=urllib.request.Request(url,headers={"User-Agent":"DesignConversacionalMundaneum/1.0"})
   with urllib.request.urlopen(req,timeout=90) as response:root=ET.fromstring(response.read())
   for entry in root.findall("a:entry",NS):
    found=" ".join((entry.findtext("a:title",default="",namespaces=NS)).split());best=max(batch,key=lambda r:SequenceMatcher(None,norm(r["title"]),norm(found)).ratio());similarity=SequenceMatcher(None,norm(best["title"]),norm(found)).ratio()
    if similarity<.94:continue
    pdf=next((x.attrib.get("href","") for x in entry.findall("a:link",NS) if x.attrib.get("title")=="pdf"),"")
    results.append({"title":best["title"],"doi":best["doi"],"arxiv_title":found,"similarity":f"{similarity:.3f}","arxiv_id":entry.findtext("a:id",default="",namespaces=NS),"pdf_url":pdf,"error":""})
  except Exception as exc:
   for row in batch:results.append({"title":row["title"],"doi":row["doi"],"arxiv_title":"","similarity":"","arxiv_id":"","pdf_url":"","error":repr(exc)})
  time.sleep(3.1)
 fields=["title","doi","arxiv_title","similarity","arxiv_id","pdf_url","error"]
 with (BASE/"arxiv-resolution.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 summary={"queried":len(rows),"batches":(len(rows)+7)//8,"matches":sum(bool(r["pdf_url"]) for r in results),"errors":sum(bool(r["error"]) for r in results)}
 (BASE/"arxiv-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
