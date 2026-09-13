---
corpus_id: DCM-01926
titulo: "Hold the Phone: Conversational Man-in-the-Middle Attacks on LLM Chat Interfaces via Multi-Turn UI Spoofing"
autores: "Kase Branham"
ano: 2026
doi: "https://doi.org/10.5281/zenodo.19421883"
idioma: ""
status_coleta: obra-descoberta
status_documento: sem-url-pdf-resolucao-pendente
aderencia_ontologica: 3
triagem: triagem-pendente
---

# Hold the Phone: Conversational Man-in-the-Middle Attacks on LLM Chat Interfaces via Multi-Turn UI Spoofing

## Ficha bibliográfica

- **ID:** DCM-01926
- **Autores:** Kase Branham
- **Ano:** 2026
- **Tipo:** article
- **DOI:** https://doi.org/10.5281/zenodo.19421883
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.5281/zenodo.19421883
- **URL de PDF:** 
- **Status documental:** sem-url-pdf-resolucao-pendente
- **Status de coleta:** obra-descoberta

## Resumo disponível

We identify a novel class of prompt injection attack—the Conversational ProtocolMan-in-the-Middle (CP-MITM)—that hijacks multi-turn LLM chat sessions without requiringagentic tool access, memory manipulation, or network-layer interception. The attack sits atthe intersection of three established threat categories: indirect prompt injection, socialengineering, and conversational UX hijacking. It exploits a structural gap in existing threatmodels: no authentication mechanism exists within the conversational protocol between auser and an AI assistant to verify that a given response originated from the intended model.By injecting content that mimics the AI assistant’s own interaction patterns—includingfabricated clarifying questions with selectable options—the attacker creates achoose-your-own-adventure loop in which every user choice triggers a fetch of the nextattacker-controlled payload. In its most sophisticated variant, the attacker relays genuine AIresponses alongside hidden parasitic instructions, rendering the hijack resistant to casualdetection. We term this the “Hold-the-Phone” attack, by analogy to classic telephonyhijacking. We show that this attack extends the Promptware Kill Chain (Nassi, Schneier,and Brodt, 2026) by introducing a new persistence mechanism—the user-as-loop—thatrequires no memory poisoning and leaves response latency as the primary observablesignal. While partial defenses exist at the model and platform levels, no current mitigationaddresses the protocol-layer vulnerability directly. We propose an initial taxonomy ofdefenses and identify conversational protocol authentication as an urgent open problem inLLM security.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** aguarda triagem analítica
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
