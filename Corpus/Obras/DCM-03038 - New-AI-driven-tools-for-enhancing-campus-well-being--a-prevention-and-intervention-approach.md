---
corpus_id: DCM-03038
titulo: "New AI-driven tools for enhancing campus well-being : a prevention and intervention approach"
autores: "Jinwen Tang"
ano: 2026
doi: "https://doi.org/10.32469/10355/112627"
idioma: ""
status_coleta: obra-descoberta
status_documento: sem-url-pdf-resolucao-pendente
aderencia_ontologica: 3
triagem: triagem-pendente
---

# New AI-driven tools for enhancing campus well-being : a prevention and intervention approach

## Ficha bibliográfica

- **ID:** DCM-03038
- **Autores:** Jinwen Tang
- **Ano:** 2026
- **Tipo:** dissertation
- **DOI:** https://doi.org/10.32469/10355/112627
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.48550/arxiv.2605.10804
- **URL de PDF:** 
- **Status documental:** sem-url-pdf-resolucao-pendente
- **Status de coleta:** obra-descoberta

## Resumo disponível

Campus well-being underpins the academic success and personal fulfillment of students, faculty, and staff, yet many universities lack effective methods for proactively monitoring satisfaction and detecting emerging mental health risks. These gaps highlight an urgent need for both preventive strategies, such as capturing nuanced, actionable feedback to improve the campus environment, and intervention tools that identify and support individuals experiencing psychological distress. By collecting richer data and personalizing engagement, institutions can more quickly and effectively respond to the evolving needs of their communities. Universities often contend with low response rates and superficial feedback in traditional campus climate surveys, limiting their ability to identify and address pressing issues. To overcome these shortcomings, we developed TigerGPT, a personalized survey chatbot, to engage users in deeper, context-aware conversations. Employing a theory-based engagement approach and leveraging large language models (LLMs), TigerGPT adapts its dialogues based on user roles and real-time inputs. Grounded in principles of conversational design and user engagement theory, it dynamically triggers and combines prompts to probe for deeper insights or clarifications, encourages comfortable sharing on sensitive topics, employs empathetic language and well-chosen emojis to foster trust and warmth, offers flexible topic selection to empower users, and incorporates visual elements such as bolded questions to reduce cognitive load. In a pilot study, TigerGPT demonstrated significant improvements over conventional methods, achieving a 75 percent usability rating and an 81 percent satisfaction score, with 50 percent of participants preferring it over traditional surveys. Despite these gains, the initial version suffered from repetitive prompts, limited topic diversity, superficial personalization, and low response quality. To address these issues, we introduced AURA, a reinforcement-learning framework that learns within a session to adapt follow-up question types using an LSDE quality signal (Length, Self-disclosure, Emotion, Specificity). AURA initializes expected gains from 96 prior campus-climate conversations (467 total chatbot-user exchanges) and updates them online via an ϵ-greedy policy over 10-15 exchanges, selecting among follow-up classes (e.g., validate, specify, reflect, probe) to optimize LSDE as the conversation unfolds. In controlled evaluations (n = 20 conversations per condition), AURA achieved a +0.12 mean gain in composite response quality with a statistically significant improvement over non-adaptive baselines (p = 0.044, d = 0.66), driven by a 63 percent reduction in specification prompts and a 10x increase in validation behavior. These results indicate that within-session reinforcement learning reduces repetition, increases response specificity and depth, and mitigates late-phase drop-off across heterogeneous campus users. While these enhancements substantially bolster campus feedback collection (Objective 1), they also underscore the need for specialized methods to detect and address mental health risks in a timely fashion (Objective 2). Current approaches to early mental health detection remain fragmented and often rely on short-text analysis or static screenings, overlooking deeper emotional and cognitive markers. To address this gap, we focus on Expressive Narrative Stories (ENS), longer, first-person narratives rich in psychological details, to uncover subtle signals that brief, generic posts typically miss. Our methodology evaluates advanced language models (BERT and MentalBERT) alongside traditional classifiers (SVM, Naive Bayes, Logistic Regression) by removing or replacing topic words and shuffling sentence order. Results reveal that conventional classifiers and MentalBERT depend heavily on explicit mental health terms (P-value < 0.05), which can be problematic when such terms are absent. In contrast, BERT(128) maintains robust accuracy even without keyword cues, demonstrating its effectiveness at capturing nuanced linguistic features. Both BERT and MentalBERT remain resilient under sentence shuffling (P-value < 0.05), a critical capability for analyzing extended narratives, particularly in ENS-based comparisons of individuals with and without self-declared mental health issues. These findings underscore ENS as a valuable resource for more nuanced mental health screening, highlighting how context-aware analyses can deepen our understanding of linguistic patterns in psychological distress. Although Expressive Narrative Stories (ENS) have improved classification in mental health screening, existing approaches often function as “black boxes,” providing minimal transparency into how they derive conclusions. This lack of explainability can undermine user trust and limit clinical validation. To address this challenge, we developed “PsychoGPT”, a specialized large language model tailored for psychological distress assessment. Built atop GPT-4 with adaptations from DSM-5 and PHQ-8 guidelines, PsychoGPT follows a multi-stage evaluation process: it first produces an initial classification of potential distress, then breaks down PHQ-8 criteria to score individual symptoms, and finally reconciles its own findings with external PHQ ratings for an independent validation step. This staged approach not only yields more granular insights but also enables stakeholders to review the system's reasoning line by line. Tested on datasets like DAIC-WOZ, PsychoGPT maintains high accuracy while generating clear, interpretable justifications for its decisions, thereby bridging the explainability gap in automated mental health screenings. While PsychoGPT enhances explainability, large language models can still produce inconsistent or erroneous outputs, particularly with extended, narrative-style data where “hallucinations” pose significant risks for mental health assessments. To address this, we developed a Stacked Multi-Model Reasoning (SMMR) framework, which layers multiple “expert” models to iteratively refine each other's outputs, rather than relying on a single GPT-based analysis. Early layers tackle simpler or more localized subtasks, while subsequent layers integrate and reconcile these partial findings. By systematically resolving discrepancies between models and consolidating complementary insights, SMMR reduces hallucinations and stabilizes results. Evaluations on the DAIC-WOZ dataset and curated case study narratives demonstrate that SMMR outperforms single-model GPT solutions in accuracy, F1-score, and PHQ-8 scoring accuracy. These improvements mark a key step toward more robust, reliable, and safer AI-driven mental health interventions in campus contexts. To unify the preventive strengths of TigerGPT and AURA with the advanced mental health detection tools, we propose a cohesive framework that seamlessly connects real-time survey feedback with targeted intervention analytics (Objective 3). This design allows insights from survey chatbot's adaptive dialogues, such as emerging student concerns or early signs of distress, to flow directly into specialized models like PsychoGPT or SMMR. By aligning both preventive and intervention strategies under one integrated system, administrators can simultaneously enhance campus-wide satisfaction initiatives and more swiftly identify and support individuals experiencing psychological challenges.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** aguarda triagem analítica
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
