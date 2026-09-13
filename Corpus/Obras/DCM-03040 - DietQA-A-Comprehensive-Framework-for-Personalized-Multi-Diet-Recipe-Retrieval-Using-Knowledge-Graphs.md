---
corpus_id: DCM-03040
titulo: "DietQA: A Comprehensive Framework for Personalized Multi-Diet Recipe Retrieval Using Knowledge Graphs, Retrieval-Augmented Generation, and Large Language Models"
autores: "Ioannis Tsampos; Emmanouil Marakakis"
ano: 2025
doi: "https://doi.org/10.3390/computers14100412"
idioma: ""
status_coleta: transferencia-falhou
status_documento: recuperacao-tentada-sem-pdf-valido
aderencia_ontologica: 3
triagem: triagem-pendente
---

# DietQA: A Comprehensive Framework for Personalized Multi-Diet Recipe Retrieval Using Knowledge Graphs, Retrieval-Augmented Generation, and Large Language Models

## Ficha bibliográfica

- **ID:** DCM-03040
- **Autores:** Ioannis Tsampos; Emmanouil Marakakis
- **Ano:** 2025
- **Tipo:** article
- **DOI:** https://doi.org/10.3390/computers14100412
- **Fonte de descoberta:** OpenAlex
- **URL de registro:** https://doi.org/10.3390/computers14100412
- **URL de PDF:** https://www.mdpi.com/2073-431X/14/10/412/pdf?version=1759152441
- **Status documental:** recuperacao-tentada-sem-pdf-valido
- **Status de coleta:** transferencia-falhou

## Resumo disponível

Recipes available on the web often lack nutritional transparency and clear indicators of dietary suitability. While searching by title is straightforward, exploring recipes that meet combined dietary needs, nutritional goals, and ingredient-level preferences remains challenging. Most existing recipe search systems do not effectively support flexible multi-dietary reasoning in combination with user preferences and restrictions. For example, users may seek gluten-free and dairy-free dinners with suitable substitutions, or compound goals such as vegan and low-fat desserts. Recent systematic reviews report that most food recommender systems are content-based and often non-personalized, with limited support for dietary restrictions, ingredient-level exclusions, and multi-criteria nutrition goals. This paper introduces DietQA, an end-to-end, language-adaptable chatbot system that integrates a Knowledge Graph (KG), Retrieval-Augmented Generation (RAG), and a Large Language Model (LLM) to support personalized, dietary-aware recipe search and question answering. DietQA crawls Greek-language recipe websites to extract structured information such as titles, ingredients, and quantities. Nutritional values are calculated using validated food composition databases, and dietary tags are inferred automatically based on ingredient composition. All information is stored in a Neo4j-based knowledge graph, enabling flexible querying via Cypher. Users interact with the system through a natural language chatbot friendly interface, where they can express preferences for ingredients, nutrients, dishes, and diets, and filter recipes based on multiple factors such as ingredient availability, exclusions, and nutritional goals. DietQA supports multi-diet recipe search by retrieving both compliant recipes and those adaptable via ingredient substitutions, explaining how each result aligns with user preferences and constraints. An LLM extracts intents and entities from user queries to support rule-based Cypher retrieval, while the RAG pipeline generates contextualized responses using the user query and preferences, retrieved recipes, statistical summaries, and substitution logic. The system integrates real-time updates of recipe and nutritional data, supporting up-to-date, relevant, and personalized recommendations. It is designed for language-adaptable deployment and has been developed and evaluated using Greek-language content. DietQA provides a scalable framework for transparent and adaptive dietary recommendation systems powered by conversational AI.

## Triagem orientada pelo Design Conversacional

- **Centralidade ontológica:** 3/4
- **Classificação atual:** aguarda triagem analítica
- **Contribuição e relação com a obra:** a preencher após leitura analítica.
- **Limitações e contrapontos:** a preencher após leitura analítica.

## Ligações

- Capítulos relacionados: a definir
- Conceitos: a definir
- Autores: a definir
