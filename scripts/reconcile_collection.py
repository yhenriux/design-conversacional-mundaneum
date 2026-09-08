"""Associa históricos às identidades atuais usando apenas metadados."""
import csv
import json
from collections import defaultdict, Counter
from build_master_corpus import ROOT, read_rows, normalize_doi, normalize_title

def main():
    corpus = read_rows(ROOT/'data/corpus/master-corpus.csv')
    dois, titles = defaultdict(set), defaultdict(set)
    for row in corpus:
        if row['doi']: dois[normalize_doi(row['doi'])].add(row['corpus_id'])
        titles[normalize_title(row['title'])].add(row['corpus_id'])
    output=[]
    for manifest in sorted((ROOT/'data/document-resolution').rglob('*download-manifest.csv')):
        for number,row in enumerate(read_rows(manifest),2):
            doi=normalize_doi(row.get('doi',''))
            matches=dois.get(doi,set()) if doi else titles.get(normalize_title(row.get('title','')),set())
            current=next(iter(matches)) if len(matches)==1 else ''
            output.append({'corpus_id':current,'legacy_corpus_id':row.get('corpus_id',''),'match_basis':'doi' if doi and current else 'unique-title-metadata' if current else 'unresolved','manifest':manifest.relative_to(ROOT).as_posix(),'row':number,'title':row.get('title',''),'doi':doi,'url':row.get('url',''),'path':row.get('path',''),'sha256':row.get('sha256',''),'received':str(row.get('pdf_signature',row.get('valid_pdf','false'))=='true').lower(),'retrieved_at':row.get('retrieved_at',''),'error':row.get('error','')})
    destination=ROOT/'data/corpus/collection-history.csv'
    with destination.open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(output[0]));writer.writeheader();writer.writerows(output)
    summary={'attempt_occurrences':len(output),'matched':sum(bool(r['corpus_id']) for r in output),'unresolved':sum(not r['corpus_id'] for r in output),'renumbered_occurrences':sum(bool(r['corpus_id'] and r['legacy_corpus_id'] and r['corpus_id']!=r['legacy_corpus_id']) for r in output),'distinct_received_hashes':len({r['sha256'] for r in output if r['received']=='true' and r['sha256']})}
    (ROOT/'data/corpus/collection-reconciliation.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary))

if __name__=='__main__':main()
