---
corpus_id: DCM-05239
titulo: "DEVELOPMENT OF A RAG-BASED SCHOLARLY RESEARCH CHATBOT WITH FINE-TUNED DENSE RETRIEVAL"
autores: "Abiodun Oguntimilehin; OS Balogun"
ano: 2026
doi: "https://doi.org/10.67358/njt.2026.5975"
idioma: ""
status_coleta: arquivo-recebido
status_documento: pdf-recebido-a-validar
aderencia_ontologica: 3
triagem: nucleo-central
---

# DEVELOPMENT OF A RAG-BASED SCHOLARLY RESEARCH CHATBOT WITH FINE-TUNED DENSE RETRIEVAL

## Ficha bibliográfica

- **ID:** DCM-05239
- **Autores:** Abiodun Oguntimilehin; OS Balogun
- **Ano:** 2026
- **Tipo:** article
- **DOI:** https://doi.org/10.67358/njt.2026.5975
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.67358/njt.2026.5975
- **URL de PDF:** https://www.nijotech.com/index.php/nijotech/article/download/5975/2316
- **Status documental:** pdf-recebido-a-validar
- **Status de coleta:** arquivo-recebido

## Resumo disponível

Foundation models, particularly Large Language Models (LLMs), show promise for chatbots for scholarly research chatbots but suffer from “hallucinations” and limited domain knowledge. This work addresses these reliability issues by developing a Retrieval-Augmented Generation (RAG) chatbot designed explicitly for scholarly research interactions within the Natural Language Processing (NLP) domain. The system utilizes a domain-specific corpus from the Association of Computational Linguistics (ACL) Anthology. The corpus was processed into text chunks and indexed using a high-dimensional vector database to facilitate efficient information retrieval. The generation component comprises an instruct-tuned LLM; Mixtral 8x7b, which synthesizes the retrieved context into coherent, evidence-based responses while maintaining the original semantic integrity of the scholarly source. Retrieval is performed using semantic similarity search. To improve dense retrieval precision, the BAAI/bge-large Sentence Transformer model was fine-tuned on a synthetic dataset generated from the corpus. Results show that fine-tuning and integrating the BAAI/bge-large model significantly improves the chatbot's ability to retrieve relevant information. Compared to the base model, retrieval accuracy of the fine-tuned model increases by up to 15% across different metrics: Accuracy@k, Precision@k, Recall@k, where k represents the count of retrieved chunks considered for evaluation, and Mean Reciprocal Rank (MRR@10). Notably, accuracy reaches an impressive 97%, demonstrating a significant boost in retrieving the most relevant scholarly information for user queries. These findings underscore the efficacy of fine-tuned Retrieval-Augmented Generation (RAG) systems in developing reliable, grounded chatbots for academic environments.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** núcleo central
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
