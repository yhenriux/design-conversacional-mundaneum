---
corpus_id: DCM-02765
titulo: "Revisiting clustering for efficient unsupervised dialogue structure induction"
autores: "Maarten De Raedt; Fréderic Godin; Chris Develder; Thomas Demeester"
ano: 2024
doi: "https://doi.org/10.1007/s10489-024-05455-5"
idioma: ""
status_coleta: arquivo-recebido
status_documento: pdf-recebido-a-validar
aderencia_ontologica: 3
triagem: nucleo-central
---

# Revisiting clustering for efficient unsupervised dialogue structure induction

## Ficha bibliográfica

- **ID:** DCM-02765
- **Autores:** Maarten De Raedt; Fréderic Godin; Chris Develder; Thomas Demeester
- **Ano:** 2024
- **Tipo:** article
- **DOI:** https://doi.org/10.1007/s10489-024-05455-5
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** http://dx.doi.org/10.1007/s10489-024-05455-5
- **URL de PDF:** https://link.springer.com/content/pdf/10.1007/s10489-024-05455-5.pdf
- **Status documental:** pdf-recebido-a-validar
- **Status de coleta:** arquivo-recebido

## Resumo disponível

Abstract In the development of a task-oriented dialogue system, defining the dialogue structure is a time-consuming task. Hence, several works have looked into automatically inferring it from data, e.g., actual conversations between a customer and a support agent. To recover such dialogue structure, recent methods based on discrete variational models learn to jointly encode and cluster utterances in dialogue states, but (i) represent utterances by only considering preceding dialogue context, and (ii) are slow to train since they are optimized with a compute-expensive decoding objective. We revisit and improve upon an existing efficient pipeline approach, commonly adopted as a baseline, that first encodes utterances and then clusters them with k-means to induce the dialogue structure. However, the existing approach represents utterances as bag-of-words or skip-thought vectors, which have been shown to perform poorly in semantic similarity tasks, and without considering dialogue context. We therefore first investigate the use of more powerful transformer-based encoders for encoding utterances. Next, we propose ellodar, a method for learning representations that capture both preceding and subsequent dialogue context, inspired by word-to-vec training strategies. ellodar is efficient since representations are learned directly in the encoding space by finetuning just a single linear layer on top of a frozen sentence encoder with a vector-to-vector regression training objective. Extensive experiments on representative datasets for dialogue structure induction (SimDial, Schema Guided Dialogues, DSTC2, and CamRest676) demonstrate that in terms of effectiveness to induce the correct dialogue structure, (i) clustering utterances represented by transformed-based encoders improves recent joint models by 13%–32% on standard cluster metrics, and (ii) clustering ellodar’s representations yields additional improvements ranging from +20% to +26%, with speedups of $$\times $$ × $$\textbf{10}$$ 10 – $$\textbf{10}^{\textbf{4}}$$ 10 4 compared to the recent joint models.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** núcleo central
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
