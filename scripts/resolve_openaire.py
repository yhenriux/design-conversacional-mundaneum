#!/usr/bin/env python3
"""Localiza instâncias abertas no OpenAIRE para registros ainda pendentes."""
import csv,json,time,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SOURCE=ROOT/"data"/"document-resolution"/"document-status.csv"; OUT=ROOT/"data"/"document-resolution"; UA="DesignConversacionalMundaneum/1.0"
def main():
 with SOURCE.open(encoding="utf-8-sig",newline="") as h: source=[r for r in csv.DictReader(h) if r["document_status"]!="pdf-integral-validado-local" and r["doi"]]
 raw=OUT/"openaire-raw";raw.mkdir(exist_ok=True);results=[];records=0;errors=0
 for number,row in enumerate(source,1):
  try:
   url="https://api.openaire.eu/graph/v3/research-products?"+urllib.parse.urlencode({"pid":row["doi"],"pageSize":5})
   req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"application/json"})
   with urllib.request.urlopen(req,timeout=60) as response:data=json.loads(response.read())
   (raw/f"{number:03d}.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
   found=data.get("results") or []; records+=bool(found)
   for product in found:
    for instance in product.get("instances") or []:
     access=instance.get("accessRight") or {}; is_open=access.get("label") in {"OPEN","Open Access"}
     for candidate in instance.get("urls") or []:
      results.append({"title":row["title"],"doi":row["doi"],"openaire_id":product.get("id") or "","candidate_url":candidate,
       "is_open":str(is_open).lower(),"access_label":access.get("label") or "","oa_route":access.get("openAccessRoute") or "",
       "license":instance.get("license") or "","version":instance.get("type") or "","hosted_by":(instance.get("hostedBy") or {}).get("value") or "",
       "collected_from":(instance.get("collectedFrom") or {}).get("value") or "","resolved_at":datetime.now(timezone.utc).isoformat()})
  except Exception as exc:
   errors+=1;results.append({"title":row["title"],"doi":row["doi"],"openaire_id":"","candidate_url":"","is_open":"","access_label":"","oa_route":"","license":"","version":"","hosted_by":"","collected_from":"","resolved_at":datetime.now(timezone.utc).isoformat(),"error":repr(exc)})
  time.sleep(.2)
 fields=["title","doi","openaire_id","candidate_url","is_open","access_label","oa_route","license","version","hosted_by","collected_from","resolved_at","error"]
 with (OUT/"openaire-resolution.csv").open("w",encoding="utf-8-sig",newline="") as h:w=csv.DictWriter(h,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(results)
 summary={"queried":len(source),"records_resolved":records,"instances":len(results),"open_urls":sum(r.get("is_open")=="true" and bool(r.get("candidate_url")) for r in results),"errors":errors}
 (OUT/"openaire-summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
