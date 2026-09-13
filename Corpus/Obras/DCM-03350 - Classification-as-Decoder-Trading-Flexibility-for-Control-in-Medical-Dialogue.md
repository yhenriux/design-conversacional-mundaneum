---
corpus_id: DCM-03350
titulo: "Classification as Decoder: Trading Flexibility for Control in Medical Dialogue"
autores: "Sam Shleifer; Manish Chablani; Anitha Kannan; Namit Katariya; Xavier Amatriain"
ano: 2019
doi: "https://doi.org/10.48550/arxiv.1911.08554"
idioma: ""
status_coleta: arquivo-recebido
status_documento: pdf-recebido-a-validar
aderencia_ontologica: 3
triagem: nucleo-central
---

# Classification as Decoder: Trading Flexibility for Control in Medical Dialogue

## Ficha bibliográfica

- **ID:** DCM-03350
- **Autores:** Sam Shleifer; Manish Chablani; Anitha Kannan; Namit Katariya; Xavier Amatriain
- **Ano:** 2019
- **Tipo:** preprint
- **DOI:** https://doi.org/10.48550/arxiv.1911.08554
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** http://arxiv.org/abs/1911.08554
- **URL de PDF:** https://arxiv.org/pdf/1911.08554
- **Status documental:** pdf-recebido-a-validar
- **Status de coleta:** arquivo-recebido

## Resumo disponível

Generative seq2seq dialogue systems are trained to predict the next word in dialogues that have already occurred. They can learn from large unlabeled conversation datasets, build a deeper understanding of conversational context, and generate a wide variety of responses. This flexibility comes at the cost of control, a concerning tradeoff in doctor/patient interactions. Inaccuracies, typos, or undesirable content in the training data will be reproduced by the model at inference time. We trade a small amount of labeling effort and some loss of response variety in exchange for quality control. More specifically, a pretrained language model encodes the conversational context, and we finetune a classification head to map an encoded conversational context to a response class, where each class is a noisily labeled group of interchangeable responses. Experts can update these exemplar responses over time as best practices change without retraining the classifier or invalidating old training data. Expert evaluation of 775 unseen doctor/patient conversations shows that only 12% of the discriminative model's responses are worse than the what the doctor ended up writing, compared to 18% for the generative model.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** núcleo central
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
