# Expansão por citações

Em 7 de setembro de 2026 foram consultadas 20 sementes de alta aderência no OpenAlex. A rede retornou 345 candidatos entre referências citadas e trabalhos citantes.

Esses candidatos permanecem em `data/citation-runs/20260907T231123Z/candidates.csv`. Nesta fase eles são apenas obras descobertas por relação bibliográfica. O portão ontológico e a seleção para coleta de PDF serão aplicados em ciclo próprio, antes de incorporá-los ao corpus mestre.

O resultado não foi incorporado automaticamente porque os registros da expansão não trazem ainda a pontuação de centralidade exigida pelo processo de descoberta. Isso evita transformar uma relação de citação em evidência de aderência ao Design Conversacional.
