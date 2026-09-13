---
corpus_id: DCM-01795
titulo: "Lead Generation System Using AI and Retrieval Augmented Generation for Customer Interaction"
autores: "Dr.Karthik B; Prashanth K"
ano: 2026
doi: "https://doi.org/10.22214/ijraset.2026.83306"
idioma: ""
status_coleta: arquivo-recebido
status_documento: pdf-recebido-a-validar
aderencia_ontologica: 3
triagem: nucleo-central
---

# Lead Generation System Using AI and Retrieval Augmented Generation for Customer Interaction

## Ficha bibliográfica

- **ID:** DCM-01795
- **Autores:** Dr.Karthik B; Prashanth K
- **Ano:** 2026
- **Tipo:** article
- **DOI:** https://doi.org/10.22214/ijraset.2026.83306
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.22214/ijraset.2026.83306
- **URL de PDF:** https://doi.org/10.22214/ijraset.2026.83306
- **Status documental:** pdf-recebido-a-validar
- **Status de coleta:** arquivo-recebido

## Resumo disponível

This paper presents the design and development of an AI-driven lead generation platform that combines a Retrieval Augmented Generation (RAG) pipeline with a stateful conversational agent to automate customer qualification for a technology services company. The system operates through a two-phase dialogue strategy: in the first phase, the agent engages website visitors with concise product overviews without accessing the knowledge base; in the second phase, after contact details are captured, the agent retrieves contextually relevant content from a company PDF document using dense semantic embeddings and responds with detailed, document-grounded answers. Captured lead data is simultaneously persisted to a PostgreSQL database and dispatched as an HTML email notification to the sales team via a Model Context Protocol (MCP) server running concurrent threads. The backend is built on FastAPI with a LangGraph agent maintaining per-session conversation memory through InMemorySaver, while the frontend delivers a seamless floating chat experience through a Next.js 14 widget. Experimental evaluation demonstrates that the gated RAG strategy reduces hallucination, improves answer relevance, and increases lead conversion efficiency compared to conventional chatbot approaches. The paper describes the system architecture, agent design, RAG pipeline, MCP tool orchestration, and key implementation decisions

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** núcleo central
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
