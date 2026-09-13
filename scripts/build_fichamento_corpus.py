import csv, json, re, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'data/corpus/master-corpus.csv'
OUT = ROOT / 'Corpus'

def safe(s, n=100):
    s = re.sub(r'[^\w\- ]+', '', s or '', flags=re.UNICODE).strip().replace(' ', '-')
    return (s[:n] or 'sem-titulo')

def main():
    rows = list(csv.DictReader(CORPUS.open(encoding='utf-8-sig')))
    (OUT/'Obras').mkdir(parents=True, exist_ok=True)
    (OUT/'Fichas-documentais').mkdir(parents=True, exist_ok=True)
    (OUT/'Fichas-analiticas').mkdir(parents=True, exist_ok=True)
    (OUT/'Autores').mkdir(parents=True, exist_ok=True)
    central = 0; received = 0
    index = []
    for r in rows:
        cid = r['corpus_id']; title = r['title'] or 'Sem título'
        status = r['collection_status']; received += status == 'arquivo-recebido'
        score = int(float(r.get('ontology_score') or 0))
        is_central = score >= 3 and status == 'arquivo-recebido'
        central += is_central
        note = f"""---\ncorpus_id: {cid}\ntitulo: \"{title.replace(chr(34), '')}\"\nautores: \"{r['authors']}\"\nano: {r['year']}\ndoi: \"{r['doi']}\"\nidioma: \"{r.get('language','')}\"\nstatus_coleta: {status}\nstatus_documento: {r['document_status']}\naderencia_ontologica: {score}\ntriagem: {'nucleo-central' if is_central else 'triagem-pendente'}\n---\n\n# {title}\n\n## Ficha bibliográfica\n\n- **ID:** {cid}\n- **Autores:** {r['authors']}\n- **Ano:** {r['year']}\n- **Tipo:** {r['type']}\n- **DOI:** {r['doi']}\n- **Fonte de descoberta:** {r['source_api']}\n- **URL de registro:** {r['landing_url']}\n- **URL de PDF:** {r['source_pdf_url']}\n- **Status documental:** {r['document_status']}\n- **Status de coleta:** {status}\n\n## Resumo disponível\n\n{r['abstract']}\n\n## Triagem orientada pelo Design Conversacional\n\n- **Centralidade ontológica:** {score}/4\n- **Classificação atual:** {'núcleo central' if is_central else 'aguarda triagem analítica'}\n- **Contribuição e relação com a obra:** a preencher após leitura analítica.\n- **Limitações e contrapontos:** a preencher após leitura analítica.\n\n## Ligações\n\n- Capítulos relacionados: a definir\n- Conceitos: a definir\n- Autores: a definir\n"""
        (OUT/'Obras'/f'{cid} - {safe(title)}.md').write_text(note, encoding='utf-8')
        if is_central:
            central_note = note + "\n## Ficha analítica\n\n- Pergunta ou problema: a extrair do texto integral.\n- Tese principal: a extrair do texto integral.\n- Método e corpus: a extrair do texto integral.\n- Resultados e limitações: a extrair do texto integral.\n- Citações paginadas: a inserir após verificação.\n- Grau de confiança: pendente de leitura humana/analítica.\n"
            (OUT/'Fichas-analiticas'/f'{cid} - {safe(title)}.md').write_text(central_note, encoding='utf-8')
        index.append({'corpus_id':cid,'title':title,'authors':r['authors'],'year':r['year'],'collection_status':status,'document_status':r['document_status'],'ontology_score':score,'central':bool(is_central)})
    (OUT/'indice-obras.json').write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    (OUT/'relatorio-fichamento.md').write_text(f"# Relatório de fichamento\n\n- Obras catalogadas: **{len(rows)}**\n- PDFs recebidos: **{received}**\n- Fontes centrais encaminhadas à ficha analítica: **{central}**\n- Fichas bibliográficas geradas: **{len(rows)}**\n- Fase: formação e triagem do corpus; análise integral posterior.\n", encoding='utf-8')
    print(json.dumps({'obras':len(rows),'recebidos':received,'centrais':central}, ensure_ascii=False))

if __name__ == '__main__': main()
