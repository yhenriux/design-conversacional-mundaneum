#!/usr/bin/env python3
"""Busca por título no arXiv os estudos ainda sem PDF validado."""
import csv,json,re,time,unicodedata,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution"/"master";SOURCE=ROOT/"data"/"corpus"/"master-corpus.csv";OUTPUT=BASE/"arxiv-resolution.csv";NS={"a":"http://www.w3.org/2005/Atom"}
def norm(v):return re.sub(r"[^a-z0-9]+"," ",unicodedata.normalize("NFKD",v or "").encode("ascii","ignore").decode().lower()).strip()
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h:rows=[x for x in csv.DictReader(h) if x["document_status"]!="pdf-integral-validado-local"]
 results=[];errors=0
 for start in range(0,len(rows),10):
  batch=rows[start:start+10];query=" OR ".join('ti:"'+x["title"].replace('"','')+'"' for x in batch);url="https://export.arxiv.org/api/query?"+urllib.parse.urlencode({"search_query":query,"start":0,"max_results":50})
  try:
   req=urllib.request.Request(url,headers={"User-Agent":"DesignConversacionalMundaneum/1.1"})
   with urllib.request.urlopen(req,timeout=90) as response:root=ET.fromstring(response.read())
   for entry in root.findall("a:entry",NS):
    title=" ".join(entry.findtext("a:title",default="",namespaces=NS).split());best=max(batch,key=lambda x:SequenceMatcher(None,norm(x["title"]),norm(title)).ratio());score=SequenceMatcher(None,norm(best["title"]),norm(title)).ratio()
    if score<.94:continue
    pdf=next((x.attrib.get("href","") for x in entry.findall("a:link",NS) if x.attrib.get("title")=="pdf"),"");results.append({"corpus_id":best["corpus_id"],"title":best["title"],"doi":best["doi"],"arxiv_title":title,"similarity":f"{score:.3f}","arxiv_id":entry.findtext("a:id",default="",namespaces=NS),"pdf_url":pdf,"error":""})
  except Exception as exc:errors+=1
  time.sleep(3.1)
 fields=["corpus_id","title","doi","arxiv_title","similarity","arxiv_id","pdf_url","error"]
 with OUTPUT.open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 summary={"queried":len(rows),"batches":(len(rows)+9)//10,"matches":sum(bool(x["pdf_url"]) for x in results),"batch_errors":errors};(BASE/"arxiv-resolution-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
