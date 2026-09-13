---
corpus_id: DCM-02214
titulo: "Inaudible Backdoor Attack via Stealthy Frequency Trigger Injection in Audio Spectrogram"
autores: "Tianfang Zhang; Huy Phan; Zijie Tang; Cong Shi; Yan Wang; Bo Yuan; Yingying Chen"
ano: 2024
doi: "https://doi.org/10.1145/3636534.3649345"
idioma: ""
status_coleta: transferencia-falhou
status_documento: recuperacao-tentada-sem-pdf-valido
aderencia_ontologica: 3
triagem: triagem-pendente
---

# Inaudible Backdoor Attack via Stealthy Frequency Trigger Injection in Audio Spectrogram

## Ficha bibliográfica

- **ID:** DCM-02214
- **Autores:** Tianfang Zhang; Huy Phan; Zijie Tang; Cong Shi; Yan Wang; Bo Yuan; Yingying Chen
- **Ano:** 2024
- **Tipo:** conference-paper
- **DOI:** https://doi.org/10.1145/3636534.3649345
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.1145/3636534.3649345
- **URL de PDF:** 
- **Status documental:** recuperacao-tentada-sem-pdf-valido
- **Status de coleta:** transferencia-falhou

## Resumo disponível

Deep learning-enabled Voice User Interfaces (VUIs) have surpassed human-level performance in acoustic perception tasks. However, the significant cost associated with training these models compels users to rely on third-party data or outsource training services. Such emerging trends have drawn substantial attention to training-phase attacks, particularly backdoor attacks. Such attacks implant hidden trigger patterns (e.g., tones, environmental sounds) into the model during training, thereby manipulating the model's predictions in the inference phase. However, existing backdoor attacks can be easily undermined in practice as the inserted triggers are audible. Users may notice such attacks when listening to the training data and remaining alert for suspicious sounds. In this work, we present a novel audio backdoor attack that exploits completely inaudible triggers in the frequency domain of the audio spectrograms. Specifically, we optimize the trigger to be a frequency-domain pattern with the energy below the noise floor (e.g., background and hardware noises) at any given frequency, thereby rendering the trigger inaudible. To realize such attacks, we design a strategy that automatically generates inaudible triggers in the spectrum supported by commodity playback devices (e.g., smartphones and laptops). We further develop optimization techniques to enhance the trigger's robustness against speech content and onset variations. Experiments on hotword and speaker recognition indicate that our attack can achieve attack success rates of more than 98.2% and 81.0% under digital and physical attack scenarios. The results also demonstrate the trigger's inaudibility with a Signal-to-Noise Ratio (SNR) less than -3.54 dB against background noises. We further verify that our attack can successfully bypass state-of-the-art backdoor defense strategies based on learning and audio processing.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** aguarda triagem analítica
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
