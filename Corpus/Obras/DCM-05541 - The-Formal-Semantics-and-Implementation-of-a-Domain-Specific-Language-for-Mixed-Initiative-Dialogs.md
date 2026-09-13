---
corpus_id: DCM-05541
titulo: "The Formal Semantics and Implementation of a Domain-Specific Language for Mixed-Initiative Dialogs"
autores: "Zachary S. Rowland; Saverio Perugini"
ano: 2025
doi: "https://doi.org/10.22152/programming-journal.org/2026/10/7"
idioma: ""
status_coleta: transferencia-falhou
status_documento: recuperacao-tentada-sem-pdf-valido
aderencia_ontologica: 3
triagem: triagem-pendente
---

# The Formal Semantics and Implementation of a Domain-Specific Language for Mixed-Initiative Dialogs

## Ficha bibliográfica

- **ID:** DCM-05541
- **Autores:** Zachary S. Rowland; Saverio Perugini
- **Ano:** 2025
- **Tipo:** article
- **DOI:** https://doi.org/10.22152/programming-journal.org/2026/10/7
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.22152/programming-journal.org/2026/10/7
- **URL de PDF:** https://arxiv.org/pdf/2502.20529v1.pdf
- **Status documental:** recuperacao-tentada-sem-pdf-valido
- **Status de coleta:** transferencia-falhou

## Resumo disponível

Human-computer dialog plays a prominent role in interactions conducted at kiosks (e.g., withdrawing money from an atm or filling your car with gas), on smartphones (e.g., installing and configuring apps), and on the web (e.g., booking a flight).Some human-computer dialogs involve an exchange of system-initiated and user-initiated actions.These dialogs are called mixed-initiative dialogs and sometimes also involve the pursuit of multiple interleaved sub-dialogs, which are woven together in a manner akin to coroutines.However, existing dialog-authoring languages have difficulty expressing these dialogs concisely.In this work, we improve the expressiveness of a dialog-authoring language we call dialog specification language (dsl), which is based on the programming concepts of functional application, partial function application, currying, and partial evaluation, by augmenting it with additional abstractions to support concise specification of task-based, mixed-initiative dialogs that resemble concurrently executing coroutines.We also formalize the semantics of dsl-the process of simplifying and staging such dialogs specified in the language.We demonstrate that dialog specifications are compressed by to a higher degree when written in dsl using the new abstractions.We also operationalize the formal semantics of dsl in a Haskell functional programming implementation.The Haskell implementation of the simplification/staging rules provides a proof of concept that the formal semantics are sufficient to implement a dialog system specified with the language.We evaluate dsl from practical (i.e., case study), conceptual (i.e., comparisons to similar systems such as VoiceXML and State Chart XML), and theoretical perspectives.The practical applicability of the new language abstractions introduced in this work is demonstrated in a case study by using it to model portions of an online food ordering system that can be concurrently staged.Our results indicate that dsl enables concise representation of dialogs composed of multiple concurrent sub-dialogs and improves the compression of dialog expressions reported in prior research.We anticipate that the extension of our language and the formalization of the semantics can facilitate concise specification and smooth implementation of task-based, mixed-initiative, human-computer dialog systems across various domains such as atms and interactive, voice-response systems.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** aguarda triagem analítica
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
