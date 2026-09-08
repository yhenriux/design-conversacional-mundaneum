"""Gera catálogo público sem expor caminhos locais ou textos integrais."""
import csv
import json
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit
from collections import defaultdict
from build_master_corpus import key

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))

def safe_url(value):
    return value if urlsplit(value or '').scheme in ('http', 'https') else ''

def main():
    records = []
    transfers=defaultdict(list)
    for manifest in sorted((ROOT/'data/document-resolution').rglob('*download-manifest.csv')):
        for item in read(manifest):
            if item.get('pdf_signature',item.get('valid_pdf'))=='true':
                transfers[key(item)].append(item)
    for row in read(ROOT / 'data/corpus/master-corpus.csv'):
        documents = []
        for raw_path in row.get('document_manifest', '').split(';'):
            path = ROOT / raw_path.strip()
            if path.is_file() and path.suffix == '.csv':
                documents.extend(read(path))
        matches = [d for d in documents if key(d)==key(row)]
        pdf = next((safe_url(d.get('source_url', '')) for d in matches if safe_url(d.get('source_url', ''))), safe_url(row['source_pdf_url']))
        received=transfers.get(key(row),[])
        pdf=next((safe_url(d.get('url','')) for d in received if safe_url(d.get('url',''))),pdf)
        records.append(dict(id=row['corpus_id'], title=row['title'], authors=row['authors'], year=row['year'], type=row['type'], source=row['source_api'], status=row['document_status'], score=row['ontology_score'], screening=row['screening_state'], doi=safe_url(row['doi'] if row['doi'].startswith('http') else 'https://doi.org/'+row['doi']) if row['doi'] else '', url=safe_url(row['landing_url']), pdf=pdf, license=row['license']))
        records[-1]['collection_status']=row.get('collection_status','obra-descoberta')
        records[-1]['received_urls']=list(dict.fromkeys(safe_url(d.get('url','')) for d in received if safe_url(d.get('url',''))))
    destination = ROOT / 'site'
    destination.mkdir(exist_ok=True)
    (destination/'catalog.json').write_text(json.dumps({'generated':datetime.now(timezone.utc).isoformat(), 'records':records}, ensure_ascii=False), encoding='utf-8')
    with (destination/'catalog.csv').open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    print(f'{len(records)} registros; {sum(r["collection_status"]=="arquivo-recebido" for r in records)} arquivos recebidos.')

if __name__ == '__main__':
    main()
