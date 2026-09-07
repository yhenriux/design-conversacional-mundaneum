# Expansão por citações

Em 7 de setembro de 2026 foram consultadas 20 sementes de alta aderência no OpenAlex. A rede retornou 345 candidatos entre referências citadas e trabalhos citantes.

Esses candidatos permanecem em `data/citation-runs/20260907T231123Z/candidates.csv`. Nesta fase eles são apenas obras descobertas por relação bibliográfica. O portão ontológico e a seleção para coleta de PDF serão aplicados em ciclo próprio, antes de incorporá-los ao corpus mestre.

O resultado não foi incorporado automaticamente porque os registros da expansão não trazem ainda a pontuação de centralidade exigida pelo processo de descoberta. Isso evita transformar uma relação de citação em evidência de aderência ao Design Conversacional.

O quarto ciclo, iniciado com 20 sementes em 7 de setembro de 2026, recebeu respostas HTTP 429 do OpenAlex e não produziu candidatos. O erro foi registrado no log bruto. A rotina deve respeitar um intervalo de espera progressivo antes da próxima tentativa; nenhum dado parcial será tratado como resultado.
