---
corpus_id: DCM-03740
titulo: "Speech recognition assisted by large language models to command software orally -- Application to an augmented and virtual reality web app for immersive molecular graphics"
autores: "Fabio Cortés Rodríguez; Luciano A. Abriata"
ano: 2026
doi: ""
idioma: ""
status_coleta: arquivo-recebido
status_documento: pdf-recebido-a-validar
aderencia_ontologica: 3
triagem: nucleo-central
---

# Speech recognition assisted by large language models to command software orally -- Application to an augmented and virtual reality web app for immersive molecular graphics

## Ficha bibliográfica

- **ID:** DCM-03740
- **Autores:** Fabio Cortés Rodríguez; Luciano A. Abriata
- **Ano:** 2026
- **Tipo:** preprint
- **DOI:** 
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** http://arxiv.org/abs/2603.02901
- **URL de PDF:** https://arxiv.org/pdf/2603.02901
- **Status documental:** pdf-recebido-a-validar
- **Status de coleta:** arquivo-recebido

## Resumo disponível

This project successfully developed, evaluated and integrated a Voice User Interface (VUI) into a web application that we are developing for immersive molecular graphics. Said app provides augmented and virtual reality (AR and VR) environments where users manipulate molecules with their hands, but this means the hands can't be used to control the app through a regular mouse- and keyboard-based GUI. The speech-based VUI system developed here alleviates this problem, making it easy to control the app via natural spoken (or typed) commands. To achieve this VUI we evaluated two distinct Automated Speech Recognition (ASR) systems: Chrome's native Speech API and OpenAI's Whisper v3. While Whisper offered broader browser compatibility, its tendency to "hallucinate" with specialized scientific jargon proved very problematic. Consequently, we selected Chrome's ASR for its stability, speed, and reliability. For translating transcribed speech into software commands, we tested two Large Language Model (LLM)-driven approaches: either generating executable code, or calling predefined functions. The function call method, powered by OpenAI's GPT-4o-mini, was ultimately adopted due to its superior safety, efficiency, and reliability over the more complex and error-prone code-generation approach. The resulting VUI is then based on an integration of Chrome's ASR with our LLM-based function-calling module, enabling users to command the application using natural language as shown in a video linked inside this report. We provide links to live examples demonstrating all the intermediate components, and details on how we crafted the LLM's prompt in order to teach it the function calls as well as ways to clean up the transcribed speech and to explain itself while generating function calls. For best demonstration of the final system, we provide a video example.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** núcleo central
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
