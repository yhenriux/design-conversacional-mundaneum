---
corpus_id: DCM-03380
titulo: "A conversational agent for providing personalized PrEP support – Protocol for chatbot implementation and evaluation"
autores: "Fatima Sayed; Albert Park; Patrick S. Sullivan; Yaorong Ge"
ano: 2025
doi: "https://doi.org/10.1101/2025.05.02.25326894"
idioma: ""
status_coleta: transferencia-falhou
status_documento: recuperacao-tentada-sem-pdf-valido
aderencia_ontologica: 3
triagem: triagem-pendente
---

# A conversational agent for providing personalized PrEP support – Protocol for chatbot implementation and evaluation

## Ficha bibliográfica

- **ID:** DCM-03380
- **Autores:** Fatima Sayed; Albert Park; Patrick S. Sullivan; Yaorong Ge
- **Ano:** 2025
- **Tipo:** preprint
- **DOI:** https://doi.org/10.1101/2025.05.02.25326894
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.1101/2025.05.02.25326894
- **URL de PDF:** https://www.medrxiv.org/content/medrxiv/early/2025/05/05/2025.05.02.25326894.full.pdf
- **Status documental:** recuperacao-tentada-sem-pdf-valido
- **Status de coleta:** transferencia-falhou

## Resumo disponível

Abstract Background Chatbots have the potential to reduce barriers to pre-exposure prophylaxis (PrEP), including lack of awareness, misconceptions, and stigma, by providing anonymous and continuous support. However, in the context of PrEP chatbots are still nascent; they lack personalized informational expertise, peer experiential expertise, and human-like emotional support to promote PrEP uptake and retention. Tailoring information, providing relatable peer experiences, and offering effective emotional support are all crucial for increasing engagement, influencing health decisions, and fostering resilience and well-being. Objective In this paper, we describe the iterative development of a RAG chatbot for providing personalized information, peer experiential expertise, and human-like emotional support to PrEP candidates. Methods We employed an iterative design process consisting of two phases – prototype conceptualization and iterative chatbot development. In the conceptualization phase, we identified real-world PrEP needs and designed a functional dialog flow diagram for PrEP support. Chatbot development included developing 2 components – a query preprocessor and a RAG module. The preprocessor uses the Segment Any Text (SAT) tool for query segmentation and a Gemma 2 fine-tuned support classifier to identify informational, emotional, and contextual data from real-world queries. To implement the RAG module, we used information retrieval techniques, employing Sentence-BERT (SBERT) embeddings with cosine similarity for semantic similarity and performing topic matching to identify topically relevant documents based on query topic to support document retrieval. Extensive prompt engineering is used to guide the large language model (LLM), Gemini-2.0-Flash, in generating tailored responses. We conducted 10 rounds of internal evaluations to assess the chatbot responses based on 10 criteria: clarity, accuracy, actionability, relevancy, information detail, tailored information, comprehensiveness, language suitability, tone, and empathy. The iterative feedback was used to refine the LLM prompts to enhance the quality of chatbot responses. Results We developed a RAG chatbot and iteratively refined it based on the internal evaluation feedback. Prompt engineering is essential in guiding the LLM to generate responses tailored to information, experiential, and emotional user needs. We found that prompt effectiveness varied with task complexity; this was likely due to LLM sensitivity to the structure of prompts and to linguistic variability. For tasks requiring diverse perspectives, fine-tuning LLMs on annotated datasets provided better results compared to few-shot prompting techniques. Prompt decomposition and segmenting prompt instructions helped improve comprehensiveness and relevancy for complex and long queries. For tasks with high decision variance, condensed prompts that summarize the main concept or idea were more effective in reducing ambiguity in LLM decisions compared to decomposed prompts. Conclusion Our RAG chatbot leverages social media data to provide personalized information, peer experiences, and human-like emotional support; these elements are essential in effectively reducing PrEP misconceptions and promoting self-efficacy. Further analysis incorporating expert and user feedback will be conducted to help validate and improve the chatbot’s potential.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** aguarda triagem analítica
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
