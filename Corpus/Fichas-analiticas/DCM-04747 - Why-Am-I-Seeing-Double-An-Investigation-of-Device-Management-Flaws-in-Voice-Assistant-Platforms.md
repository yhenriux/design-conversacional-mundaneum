---
corpus_id: DCM-04747
titulo: "Why Am I Seeing Double? An Investigation of Device Management Flaws in Voice Assistant Platforms"
autores: "Muslum Ozgur Ozmen; Mehmet Oguz Sakaoglu; Jackson Bizjak; Jianliang Wu; Antonio Bianchi; Dave Tian; Z. Berkay Celik"
ano: 2025
doi: "https://doi.org/10.56553/popets-2025-0084"
idioma: ""
status_coleta: arquivo-recebido
status_documento: pdf-recebido-a-validar
aderencia_ontologica: 3
triagem: nucleo-central
---

# Why Am I Seeing Double? An Investigation of Device Management Flaws in Voice Assistant Platforms

## Ficha bibliográfica

- **ID:** DCM-04747
- **Autores:** Muslum Ozgur Ozmen; Mehmet Oguz Sakaoglu; Jackson Bizjak; Jianliang Wu; Antonio Bianchi; Dave Tian; Z. Berkay Celik
- **Ano:** 2025
- **Tipo:** article
- **DOI:** https://doi.org/10.56553/popets-2025-0084
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.56553/popets-2025-0084
- **URL de PDF:** https://petsymposium.org/popets/2025/popets-2025-0084.pdf
- **Status documental:** pdf-recebido-a-validar
- **Status de coleta:** arquivo-recebido

## Resumo disponível

In Voice Assistant (VA) platforms, when users add devices to their accounts and give voice commands, complex interactions occur between the devices, skills, VA clouds, and vendor clouds. These interactions are governed by the device management capabilities (DMC) of VA platforms, which rely on device names, types, and associated skills in the user account. Prior work studied vulnerabilities in specific VA components, such as hidden voice commands and bypassing skill vetting. However, the security and privacy implications of device management flaws have largely been unexplored. In this paper, we introduce DMC-Xplorer, a testing framework for the automated discovery of VA device management flaws. We first introduce VA description language (VDL), a new domain-specific language to create VA environments for testing, using VA and skill developer APIs. DMC-Xplorer then selects VA parameters (device names, types, vendors, actions, and skills) in a combinatorial approach and creates VA environments with VDL. It issues real voice commands to the environment via developer APIs and logs event traces. It validates the traces against three formal security properties that define the secure operation of VA platforms. Lastly, DMC-Xplorer identifies the root cause of property violations through intervention analysis to identify VA device management flaws. We exercised DMC-Xplorer on Amazon Alexa and Google Home and discovered two design flaws that can be exploited to launch four attacks. We show that malicious skills with default permissions can eavesdrop on privacy-sensitive device states, prevent users from controlling their devices, and disrupt the services on the VA cloud.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** núcleo central
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir

## Ficha analítica

- Pergunta ou problema: a extrair do texto integral.
- Tese principal: a extrair do texto integral.
- Método e corpus: a extrair do texto integral.
- Resultados e limitações: a extrair do texto integral.
- Citações paginadas: a inserir após verificação.
- Grau de confiança: pendente de leitura humana/analítica.
