"""Coleta paginada com checkpoints por consulta. Nenhum PDF é lido."""
import argparse,csv,hashlib,json,time
from datetime import datetime,timezone
from discover import ROOT,CONNECTORS,FIELDS,clean,score,load_json

def save(path,obj):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    temporary.replace(path)

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-id');p.add_argument('--apis',default='openalex,crossref');p.add_argument('--query');p.add_argument('--pages-per-query',type=int,default=0,help='0 percorre até esgotar a consulta');p.add_argument('--rows',type=int,default=100);a=p.parse_args()
    run=a.run_id or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    base=ROOT/'data/search-runs'/run;base.mkdir(parents=True,exist_ok=True);rawdir=base/'raw';rawdir.mkdir(exist_ok=True)
    cfg=load_json(ROOT/'config/search-queries.json');gate=load_json(ROOT/'config/ontology-gate.json')
    config={'apis':a.apis.split(','),'queries':[a.query] if a.query else cfg['precision_queries']+cfg['multilingual_queries'],'rows':a.rows,'query_config':cfg,'gate':gate}
    state_path=base/'pagination.json'
    if state_path.exists():state=load_json(state_path);config=state['config']
    else:state={'run_id':run,'config':config,'queries':{}}
    for api in config['apis']:
        for query in config['queries']:
            token=hashlib.sha256((api+'\n'+query).encode()).hexdigest()[:20]
            checkpoint=state['queries'].setdefault(token,{'api':api,'query':query,'cursor':'*','pages':0,'records':0,'complete':False,'attempts':[]})
            processed=0
            while not checkpoint['complete'] and (not a.pages_per_query or processed<a.pages_per_query):
                result=None
                for retry in range(3):
                    try:
                        result=CONNECTORS[api](query,config['rows'],'',checkpoint['cursor']);break
                    except Exception as exc:
                        checkpoint['attempts'].append({'at':datetime.now(timezone.utc).isoformat(),'cursor':checkpoint['cursor'],'error':repr(exc),'retry':retry});save(state_path,state)
                        if retry<2:time.sleep(5*(retry+1))
                if result is None:break
                url,records,raw=result;number=checkpoint['pages']+1;page=base/f'{token}-{number:06d}.csv'
                (rawdir/f'{token}-{number:06d}.json').write_bytes(raw)
                with page.open('w',encoding='utf-8-sig',newline='') as h:
                    writer=csv.DictWriter(h,fieldnames=FIELDS,extrasaction='ignore');writer.writeheader()
                    for record in records:
                        centrality,total,signal=score(record['title'],record['abstract'],config['gate'])
                        record.update(run_id=run,query_version=config['query_config']['version'],query=query,ontology_score=centrality,provisional_score=total,automatic_signal=signal,decision='candidato-por-metadados',decision_reason='Descoberta bibliográfica; análise posterior.')
                        writer.writerow({**record,'authors':clean(record.get('authors')),'abstract':clean(record.get('abstract'))})
                payload=json.loads(raw);meta=payload.get('meta',{}) if api=='openalex' else payload.get('message',{})
                next_cursor=meta.get('next_cursor') if api=='openalex' else meta.get('next-cursor')
                checkpoint['attempts'].append({'at':datetime.now(timezone.utc).isoformat(),'url':url,'page':number,'results':len(records),'sha256':hashlib.sha256(raw).hexdigest()})
                checkpoint.update(pages=number,records=checkpoint['records']+len(records),complete=not records or not next_cursor)
                checkpoint['cursor']=next_cursor;save(state_path,state);processed+=1;time.sleep(.5)
            checkpoint['status']='complete' if checkpoint['complete'] else 'pending';save(state_path,state)
    count=0
    with (base/'candidates.csv').open('w',encoding='utf-8-sig',newline='') as h:
        writer=csv.DictWriter(h,fieldnames=FIELDS);writer.writeheader()
        for path in sorted(base.glob('*-??????.csv')):
            with path.open(encoding='utf-8-sig',newline='') as source:
                for row in csv.DictReader(source):writer.writerow(row);count+=1
    summary={'run_id':run,'occurrences':count,'complete_queries':sum(q['complete'] for q in state['queries'].values()),'pending_queries':sum(not q['complete'] for q in state['queries'].values())}
    save(base/'run.json',summary);print(json.dumps(summary))

if __name__=='__main__':main()
