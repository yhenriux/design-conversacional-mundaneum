#!/usr/bin/env python3
"""Busca reproduzível. Conectores iniciais: OpenAlex e Crossref."""
from __future__ import annotations
import argparse, csv, hashlib, json, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "DesignConversacionalMundaneum/1.0 (systematic evidence mapping)"

def load_json(path): return json.loads(path.read_text(encoding="utf-8"))
def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as response: raw = response.read()
    return json.loads(raw), raw
def clean(value):
    if value is None: return ""
    if isinstance(value, list): return "; ".join(clean(x) for x in value if x)
    return re.sub(r"\s+", " ", str(value)).strip()
def openalex_abstract(index):
    return " ".join(word for _, word in sorted((pos, word) for word, positions in (index or {}).items() for pos in positions))
def score(title, abstract, gate):
    title, abstract = title or "", abstract or ""
    title_l, text_l = f" {title.lower()} ", f" {title} {abstract} ".lower()
    anchored = any(x in title_l for x in gate["title_anchors"])
    systems = sum(x in text_l for x in gate["system_terms"])
    products = sum(x in text_l for x in gate["product_design_terms"])
    ontology = 4 if anchored else (3 if systems and products else (2 if systems else 0))
    return ontology, ontology + min(3, products), "titulo-ancora" if anchored else f"sistema={systems};produto-design={products}"

def openalex(query, rows, mailto):
    fields = "id,doi,title,publication_year,type,authorships,abstract_inverted_index,primary_location,best_oa_location,open_access"
    params = {"search": query, "per-page": min(rows, 200), "select": fields}
    if mailto: params["mailto"] = mailto
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    data, raw = fetch_json(url); records = []
    for item in data.get("results", []):
        best, primary = item.get("best_oa_location") or {}, item.get("primary_location") or {}
        records.append({"source_api":"OpenAlex", "source_id":item.get("id",""), "doi":item.get("doi",""),
          "title":item.get("title",""), "year":item.get("publication_year",""),
          "authors":[x.get("author",{}).get("display_name","") for x in item.get("authorships",[])],
          "type":item.get("type",""), "abstract":openalex_abstract(item.get("abstract_inverted_index")),
          "landing_url":best.get("landing_page_url") or primary.get("landing_page_url") or "",
          "pdf_url":best.get("pdf_url") or "", "license":best.get("license") or "",
          "oa_status":(item.get("open_access") or {}).get("oa_status","")})
    return url, records, raw

def crossref(query, rows, mailto):
    params = {"query.bibliographic":query, "rows":min(rows,1000),
      "select":"DOI,title,author,published,type,abstract,URL,link,license"}
    if mailto: params["mailto"] = mailto
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    data, raw = fetch_json(url); records=[]
    for item in data.get("message",{}).get("items",[]):
        links=item.get("link") or []; dates=((item.get("published") or {}).get("date-parts") or [[]])[0]
        records.append({"source_api":"Crossref", "source_id":item.get("DOI",""), "doi":item.get("DOI",""),
          "title":clean(item.get("title",[])), "year":dates[0] if dates else "",
          "authors":[" ".join(filter(None,[x.get("given",""),x.get("family","")])) for x in item.get("author",[])],
          "type":item.get("type",""), "abstract":item.get("abstract",""), "landing_url":item.get("URL",""),
          "pdf_url":next((x.get("URL","") for x in links if x.get("content-type")=="application/pdf"),""),
          "license":clean([x.get("URL","") for x in item.get("license") or []]), "oa_status":""})
    return url, records, raw

CONNECTORS={"openalex":openalex,"crossref":crossref}
FIELDS=["run_id","query_version","query","source_api","source_id","doi","title","year","authors","type","abstract","landing_url","pdf_url","license","oa_status","ontology_score","provisional_score","automatic_signal","decision","decision_reason"]

def main():
    p=argparse.ArgumentParser(); p.add_argument("--apis",default="openalex,crossref"); p.add_argument("--rows",type=int,default=100)
    p.add_argument("--mailto",default=os.environ.get("SCHOLARLY_API_EMAIL","")); p.add_argument("--delay",type=float,default=.25); args=p.parse_args()
    queries_cfg=load_json(ROOT/"config"/"search-queries.json"); gate=load_json(ROOT/"config"/"ontology-gate.json")
    queries=queries_cfg["precision_queries"]+queries_cfg["multilingual_queries"]
    selected=[x.strip().lower() for x in args.apis.split(",") if x.strip()]
    unknown=sorted(set(selected)-set(CONNECTORS))
    if unknown: raise SystemExit("Conectores ainda não implementados: "+", ".join(unknown))
    run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"); run_dir=ROOT/"data"/"search-runs"/run_id; raw_dir=run_dir/"raw"; raw_dir.mkdir(parents=True)
    candidates=[]; log=[]
    for api in selected:
      for number,query in enumerate(queries,1):
        try:
          url,records,raw=CONNECTORS[api](query,args.rows,args.mailto); digest=hashlib.sha256(raw).hexdigest(); (raw_dir/f"{api}-{number:02d}.json").write_bytes(raw)
          for record in records:
            ontology,provisional,signal=score(record["title"],record["abstract"],gate)
            record.update({"run_id":run_id,"query_version":queries_cfg["version"],"query":query,"ontology_score":ontology,"provisional_score":provisional,"automatic_signal":signal,"decision":"screening-required","decision_reason":"Automação não substitui leitura ontológica."}); candidates.append(record)
          log.append({"api":api,"query":query,"url":url,"status":"ok","results":len(records),"sha256":digest})
        except Exception as exc:
          log.append({"api":api,"query":query,"status":"error","error":repr(exc)}); print(f"ERRO {api} {query}: {exc}",file=sys.stderr)
        time.sleep(args.delay)
    with (run_dir/"candidates.csv").open("w",encoding="utf-8-sig",newline="") as h:
      w=csv.DictWriter(h,fieldnames=FIELDS,extrasaction="ignore"); w.writeheader()
      for row in candidates: row={**row,"authors":clean(row.get("authors")),"abstract":clean(row.get("abstract"))}; w.writerow(row)
    (run_dir/"run.json").write_text(json.dumps({"run_id":run_id,"queries":log},ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"run_id":run_id,"candidates":len(candidates),"errors":sum(x["status"]=="error" for x in log)},ensure_ascii=False))
if __name__=="__main__": main()
