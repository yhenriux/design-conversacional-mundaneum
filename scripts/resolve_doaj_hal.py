#!/usr/bin/env python3
"""Resolve DOI em DOAJ e HAL e procura a URL documental declarada."""
import csv,html,json,re,time,urllib.parse,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/"data"/"document-resolution";SOURCE=BASE/"document-status.csv";UA="DesignConversacionalMundaneum/1.0"
def get(url,accept="application/json"):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":accept})
 with urllib.request.urlopen(req,timeout=60) as response:return response.read(),response.geturl()
def pdf_meta(url):
 try:
  raw,_=get(url,"text/html");text=raw.decode("utf-8","ignore")
  patterns=[r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)',r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url["\']']
  for pattern in patterns:
   match=re.search(pattern,text,re.I)
   if match:return html.unescape(match.group(1))
 except Exception:return ""
 return ""
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h:rows=[r for r in csv.DictReader(h) if r["document_status"]!="pdf-integral-validado-local" and r["doi"]]
 results=[]
 for row in rows:
  base={"title":row["title"],"doi":row["doi"]}
  try:
   url="https://doaj.org/api/search/articles/"+urllib.parse.quote("doi:"+row["doi"],safe=":/")+"?pageSize=5"
   data=json.loads(get(url)[0]);
   for item in data.get("results") or []:
    for link in (item.get("bibjson") or {}).get("link") or []:
     landing=link.get("url") or "";pdf=landing if "pdf" in (link.get("content_type") or "").lower() else pdf_meta(landing)
     results.append({**base,"resolver":"DOAJ","landing_url":landing,"pdf_url":pdf,"license":"","repository":(item.get("bibjson") or {}).get("journal",{}).get("title") or "","error":""})
  except Exception as exc:results.append({**base,"resolver":"DOAJ","landing_url":"","pdf_url":"","license":"","repository":"","error":repr(exc)})
  try:
   query='doiId_s:"'+row["doi"]+'"';params={"q":query,"fl":"title_s,doiId_s,fileMain_s,uri_s,license_s","wt":"json","rows":5}
   data=json.loads(get("https://api.archives-ouvertes.fr/search/?"+urllib.parse.urlencode(params))[0])
   for item in (data.get("response") or {}).get("docs") or []:
    results.append({**base,"resolver":"HAL","landing_url":item.get("uri_s") or "","pdf_url":item.get("fileMain_s") or "","license":item.get("license_s") or "","repository":"HAL","error":""})
  except Exception as exc:results.append({**base,"resolver":"HAL","landing_url":"","pdf_url":"","license":"","repository":"","error":repr(exc)})
  time.sleep(.15)
 fields=["title","doi","resolver","landing_url","pdf_url","license","repository","error"]
 with (BASE/"doaj-hal-resolution.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(results)
 summary={"queried":len(rows),"result_rows":len(results),"doaj_matches":sum(r["resolver"]=="DOAJ" and bool(r["landing_url"]) for r in results),"hal_matches":sum(r["resolver"]=="HAL" and bool(r["landing_url"]) for r in results),"pdf_urls":sum(bool(r["pdf_url"]) for r in results),"errors":sum(bool(r["error"]) for r in results)}
 (BASE/"doaj-hal-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
