#!/usr/bin/env python3
"""Registra a primeira triagem argumentada dos 80 candidatos do piloto."""
import csv, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
RUN="20260831T003810Z"
SOURCE=ROOT/"data"/"search-runs"/RUN/"screening-queue.csv"
OUT=ROOT/"data"/"screening"

EXCLUDE_ONTOLOGY={
  12:"A expressão descreve um processo de projeto arquitetônico mediado por IA; não trata o design de uma interface, agente ou sistema conversacional.",
  24:"O resumo concentra-se em percepção de marca e marketing, sem demonstrar contribuição explícita para decisões de Design Conversacional.",
  73:"O objeto é a arquitetura algorítmica LSTM e sua acurácia. Não há contribuição demonstrada para interação, conteúdo ou experiência conversacional."
}
EXCLUDE_DUPLICATE={
  14:"Preprint da mesma pesquisa publicada no registro 11; deve integrar a mesma família documental.",
  75:"Ocorrência Crossref da tese registrada no item 3; deve integrar a mesma família documental."
}
FULL_TEXT={
  7:"O estudo usa interação conversacional para organizar a crítica de interfaces; o texto integral deve mostrar se Design Conversacional é objeto de pesquisa ou apenas modalidade operacional.",
  25:"O registro não oferece resumo nem identificador suficiente para confirmar se a contribuição industrial é de Design Conversacional.",
  42:"O título indica uma CUI aplicada, mas é necessário verificar se a contribuição trata decisões de design ou apenas a aplicação setorial.",
  45:"A integração entre recomendação e CUI pode ser predominantemente arquitetural; o texto integral deve demonstrar uma contribuição própria para Design Conversacional.",
  50:"Título sem DOI e sem resumo. É necessário identificar autoria, edição e conteúdo antes da decisão.",
  52:"Título sem DOI e sem resumo. É necessário identificar a obra e distinguir o padrão documental de outras fontes sobre VUI.",
  67:"O título sugere implementação em plataforma empresarial, mas é preciso verificar se há contribuição para Design Conversacional além da automação técnica.",
  77:"O título é aderente, porém a ausência de resumo impede avaliar método, contribuição e alcance das heurísticas."
}

FIELDS_EXTRA=["manual_centrality","manual_field_relevance","manual_documentary_evidence","manual_actionable_contribution","manual_total","screening_decision","screening_reason","evidence_basis","reviewer","review_date","author_review"]

def main():
  with SOURCE.open(encoding="utf-8-sig",newline="") as h: rows=list(csv.DictReader(h))
  if len(rows)!=80: raise SystemExit(f"A fila esperada tem 80 registros; foram encontrados {len(rows)}.")
  output=[]
  for index,row in enumerate(rows,1):
    row.pop("manual_product_relevance",None)
    has_abstract=bool((row.get("abstract") or "").strip()); has_pdf=bool((row.get("pdf_url") or "").strip())
    if index in EXCLUDE_ONTOLOGY:
      decision="exclude-ontology"; reason=EXCLUDE_ONTOLOGY[index]; centrality=2; field_relevance=1; actionable=0; author_review="sample-audit"
    elif index in EXCLUDE_DUPLICATE:
      decision="exclude-duplicate"; reason=EXCLUDE_DUPLICATE[index]; centrality=4; field_relevance=3; actionable=1; author_review="not-required"
    elif index in FULL_TEXT:
      decision="full-text-review"; reason=FULL_TEXT[index]; centrality=3; field_relevance=2; actionable=0; author_review="required"
    else:
      decision="provisional-include"; centrality=4 if int(row.get("ontology_score") or 0)==4 else 3
      field_relevance=3 if any(x in ((row.get("title") or "").lower()) for x in ["design","guideline","principle","framework","pattern","usability","accessible","error","ethic","evaluation"]) else 2
      actionable=1
      reason="Título e resumo tratam Design Conversacional, sua avaliação ou suas consequências como contribuição central. A decisão será confirmada no documento."
      author_review="required-if-central-claim"
    documentary=2 if has_pdf else 1
    total=centrality+field_relevance+documentary+actionable
    row.update({"manual_centrality":centrality,"manual_field_relevance":field_relevance,"manual_documentary_evidence":documentary,
      "manual_actionable_contribution":actionable,"manual_total":total,"screening_decision":decision,"screening_reason":reason,
      "evidence_basis":"title+abstract" if has_abstract else "title+metadata","reviewer":"Codex: primeira passagem governada",
      "review_date":"2026-08-30","author_review":author_review})
    output.append(row)
  OUT.mkdir(parents=True,exist_ok=True); fields=list(rows[0])+[x for x in FIELDS_EXTRA if x not in rows[0]]
  for filename,predicate in {
    "screening-decisions.csv":lambda r:True,
    "provisional-inclusions.csv":lambda r:r["screening_decision"]=="provisional-include",
    "full-text-review.csv":lambda r:r["screening_decision"]=="full-text-review",
    "exclusions.csv":lambda r:r["screening_decision"].startswith("exclude-")}.items():
    with (OUT/filename).open("w",encoding="utf-8-sig",newline="") as h:
      w=csv.DictWriter(h,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows([r for r in output if predicate(r)])
  counts=Counter(r["screening_decision"] for r in output)
  report={"run_id":RUN,"records":len(output),"decisions":dict(counts),"provisional_not_final":True,
    "next_gate":"document-resolution-and-full-text-confirmation"}
  (OUT/"screening-summary.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
  print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__": main()
