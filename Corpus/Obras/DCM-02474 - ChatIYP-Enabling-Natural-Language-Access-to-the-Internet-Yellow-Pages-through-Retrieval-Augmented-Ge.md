---
corpus_id: DCM-02474
titulo: "ChatIYP: Enabling Natural Language Access to the Internet Yellow Pages through Retrieval-Augmented Generation"
autores: "Ανδριτσούδης, Βασίλης Β."
ano: 2025
doi: "https://doi.org/10.26262/heal.auth.ir.367999"
idioma: ""
status_coleta: obra-descoberta
status_documento: sem-url-pdf-resolucao-pendente
aderencia_ontologica: 3
triagem: triagem-pendente
---

# ChatIYP: Enabling Natural Language Access to the Internet Yellow Pages through Retrieval-Augmented Generation

## Ficha bibliográfica

- **ID:** DCM-02474
- **Autores:** Ανδριτσούδης, Βασίλης Β.
- **Ano:** 2025
- **Tipo:** article
- **DOI:** https://doi.org/10.26262/heal.auth.ir.367999
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.26262/heal.auth.ir.367999
- **URL de PDF:** 
- **Status documental:** sem-url-pdf-resolucao-pendente
- **Status de coleta:** obra-descoberta

## Resumo disponível

Large Language Models (LLMs) have transformed natural language processing by enabling machines to generate and comprehend human-like text; however, they often struggle with factual consistency, particularly when up-to-date or structured information is required. Retrieval-Augmented Generation (RAG) addresses this limitation by enhancing LLMs with the ability to retrieve relevant external data during inference. This thesis introduces ChatIYP, a RAG-based conversational agent designed to interact with the Internet Yellow Pages (IYP), a vast knowledge graph comprising over 26 million nodes and 160 million edges, aggregating structured data from diverse internet sources. Unlike traditional LLMs that depend solely on pre-trained knowledge, ChatIYP retrieves real-time, contextually relevant information from the IYP graph and grounds its responses in this data, generating both natural language answers and corresponding Cypher queries. This dual-output system increases transparency, allows traceability of information sources, and supports integration with downstream applications. The research begins by examining the evolution of RAG systems—from early neural retrieval methods to current models that integrate structured and unstructured sources—and analyzes the structural and semantic properties of the IYP graph to assess its suitability for integration with LLMs. Existing RAG toolkits such as LangChain and LlamaIndex are evaluated for performance, flexibility, and compatibility with Cypher query generation, informing the architecture of ChatIYP. The system is organized into four main stages: input interpretation, multi-source retrieval, natural language generation, and output delivery. Emphasis is placed on graph reduction strategies, hybrid retrieval configurations, and prompt engineering techniques to improve factual accuracy and query precision. Due to the lack of established benchmarks for RAG systems over large graphs, a custom evaluation framework was developed using CypherEval, a dataset that pairs prompts with ground-truth Cypher queries tailored to the IYP graph. The evaluation employs automatic metrics including BLEU, ROUGE, BERTScore, and G-Eval, with the latter proving most effective for assessing semantic fidelity in graph-grounded language generation. Experimental results are analyzed across varying levels of prompt complexity and domain-specific contexts, offering detailed insights into the model’s performance under different conditions. The final implementation of ChatIYP is accessible through an interactive web interface that allows users to input natural language queries and receive both explanatory responses and executable graph queries. This work demonstrates the feasibility and effectiveness of RAG systems for interacting with structured knowledge graphs at scale and highlights the importance of hybrid retrieval strategies, domain-specific prompt engineering, and robust evaluation methods. The contributions of this thesis span theoretical insights, architectural design, empirical evaluation, and practical deployment, laying the groundwork for future enhancements such as adaptive graph reduction, fallback mechanisms for retrieval robustness, and fine-tuning based on evaluation feedback.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** aguarda triagem analítica
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
