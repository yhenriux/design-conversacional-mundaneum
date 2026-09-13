---
corpus_id: DCM-05540
titulo: "LLM-Powered Educational Conversational Agent for Open Educational Resources"
autores: "Renan Zafalon da Silva; Paulo Cesar Ramos Pinho; Ulian Gabriel Alff Ramires; Raymundo Carlos Machado Ferreira Filho; Tiago Thompen Primo"
ano: 2026
doi: "https://doi.org/10.5753/sbsi.2026.248280"
idioma: ""
status_coleta: transferencia-falhou
status_documento: recuperacao-tentada-sem-pdf-valido
aderencia_ontologica: 3
triagem: triagem-pendente
---

# LLM-Powered Educational Conversational Agent for Open Educational Resources

## Ficha bibliográfica

- **ID:** DCM-05540
- **Autores:** Renan Zafalon da Silva; Paulo Cesar Ramos Pinho; Ulian Gabriel Alff Ramires; Raymundo Carlos Machado Ferreira Filho; Tiago Thompen Primo
- **Ano:** 2026
- **Tipo:** conference-paper
- **DOI:** https://doi.org/10.5753/sbsi.2026.248280
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.5753/sbsi.2026.248280
- **URL de PDF:** https://sol.sbc.org.br/index.php/sbsi/article/download/41313/41083
- **Status documental:** recuperacao-tentada-sem-pdf-valido
- **Status de coleta:** transferencia-falhou

## Resumo disponível

Research Context: Educational repositories gather diverse Open Educational Resources (OER), yet sparse metadata and inconsistent terminology reduce findability. Large Language Models (LLMs) with retrieval-augmented generation (RAG) can bridge vocabulary gaps by capturing semantic similarity, thereby improving recall and user experience. Scientific and/or Practical Problem: The national OER repository (ProEdu) depends on a solely lexical engine. This dependence creates difficulties in handling synonyms, paraphrases, and domain shifts, resulting in suboptimal recall and inconsistent rankings. Proposed Solution and/or Analysis: We develop a prototype of an Educational Conversational Agent (ECA) that integrates retrieval and response generation. Three pipelines are evaluated: ProEdu, which employs a lexical approach; a field-weighted Elasticsearch (ES); and a semantic RAG system utilizing Sentence-Transformers (all-MiniLM-L6-v2) embeddings with a FAISS (Facebook AI Similarity Search) index and Llama for text generation, plus a lightweight reranking mechanism. Related IS Theory: We assert that AI-enhanced repositories diminish search obstacles and assist educators in effectively identifying suitable materials. Furthermore, the conversational interface alleviates the cognitive load by providing verified sources within context. Research Method: A comparative assessment involved 22 interdisciplinary prompts in ten domains. For each prompt, we established gold-standard datasets, formulated standardized queries, and calculated precision, recall, and F1-score. Summary of Results: The Llama/FAISS pipeline achieves the best coverage-relevance balance driven by high recall. ES attains a similar F1 through higher precision but lower recall. ProEdu performs poorly in F1. Error analysis shows semantic retrieval excels in cross-vocabulary matches and multi-facet intents. Contributions and Impact to IS area: We deliver a replicable benchmark for large-scale OER search (prompts, metrics, code) and a pragmatic architecture combining semantic RAG and ES to balance recall and precision on cost-efficient infrastructure. Prompt templates and evaluation scripts support adoption.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** aguarda triagem analítica
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
