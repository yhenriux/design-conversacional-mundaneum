#!/usr/bin/env python3
"""Busca versões por título no Zenodo e OSF, com correspondência estrita."""
import csv,json,re,time,unicodedata,urllib.parse,urllib.request
from difflib import SequenceMatcher
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution";SOURCE=BASE/"document-status.csv";UA="DesignConversacionalMundaneum/1.0"
def norm(v):return re.sub(r"[^a-z0-9]+"," ",unicodedata.normalize("NFKD",v or "").encode("ascii","ignore").decode().lower()).strip()
def get(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
 with urllib.request.urlopen(req,timeout=60) as response:return json.loads(response.read())
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h:rows=[r for r in csv.DictReader(h) if r["document_status"]!="pdf-integral-validado-local"]
 results=[]
 for row in rows:
  expected=norm(row["title"])
  try:
   data=get("https://zenodo.org/api/records?"+urllib.parse.urlencode({"q":'title:"'+row["title"]+'"',"size":5}))
   for item in (data.get("hits") or {}).get("hits") or []:
    found=(item.get("metadata") or {}).get("title") or "";similarity=SequenceMatcher(None,expected,norm(found)).ratio()
    if similarity<.94:continue
    for file in item.get("files") or []:
     if (file.get("key") or "").lower().endswith(".pdf"):
      results.append({"title":row["title"],"doi":row["doi"],"resolver":"Zenodo","matched_title":found,"similarity":f"{similarity:.3f}","landing_url":(item.get("links") or {}).get("html") or "","pdf_url":(file.get("links") or {}).get("content") or "","license":((item.get("metadata") or {}).get("license") or {}).get("id") or "","error":""})
  except Exception as exc:results.append({"title":row["title"],"doi":row["doi"],"resolver":"Zenodo","matched_title":"","similarity":"","landing_url":"","pdf_url":"","license":"","error":repr(exc)})
  try:
   url="https://api.osf.io/v2/preprints/?"+urllib.parse.urlencode({"filter[title]":row["title"]})
   data=get(url)
   for item in data.get("data") or []:
    attrs=item.get("attributes") or {};found=attrs.get("title") or "";similarity=SequenceMatcher(None,expected,norm(found)).ratio()
    if similarity<.94:continue
    related=(((item.get("relationships") or {}).get("primary_file") or {}).get("links") or {}).get("related",{}).get("href")
    file_data=(get(related).get("data") or {}) if related else {};download=(file_data.get("links") or {}).get("download") or ""
    results.append({"title":row["title"],"doi":row["doi"],"resolver":"OSF","matched_title":found,"similarity":f"{similarity:.3f}","landing_url":(item.get("links") or {}).get("html") or "","pdf_url":download,"license":"","error":""})
  except Exception as exc:results.append({"title":row["title"],"doi":row["doi"],"resolver":"OSF","matched_title":"","similarity":"","landing_url":"","pdf_url":"","license":"","error":repr(exc)})
  time.sleep(.2)
 fields=["title","doi","resolver","matched_title","similarity","landing_url","pdf_url","license","error"]
 with (BASE/"zenodo-osf-resolution.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 summary={"queried":len(rows),"zenodo_matches":sum(r["resolver"]=="Zenodo" and bool(r["pdf_url"]) for r in results),"osf_matches":sum(r["resolver"]=="OSF" and bool(r["pdf_url"]) for r in results),"pdf_urls":sum(bool(r["pdf_url"]) for r in results),"errors":sum(bool(r["error"]) for r in results)}
 (BASE/"zenodo-osf-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
