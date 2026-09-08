# Ciclo trimestral de atualização do corpus

## Cadência

O ciclo ocorre a cada três meses, com execução extraordinária quando uma fonte passa a oferecer nova API, coleção ou exportação aberta relevante.

## Sequência

1. Executar todas as consultas de `config/search-queries.json` e preservar respostas brutas, consultas, hashes e falhas.
2. Executar as rotas territoriais e registrar país, instituição, região e idioma quando identificáveis.
3. Deduplicar contra o corpus mestre; candidatos novos passam pelo portão ontológico antes de qualquer síntese.
4. Rodar expansão por citações em lotes limitados, registrando sementes, relação citante ou referenciada e cobertura por ciclo.
5. Resolver PDFs por fontes abertas, validar correspondência bibliográfica e extrair texto de forma retomável.
6. Atualizar a classificação de centralidade, tipo documental, método, acesso, força de evidência e lacunas.
7. Publicar um comparativo entre ciclos: novos estudos, PDFs recuperados, duplicatas, exclusões, regiões e idiomas cobertos, rotas que falharam e lacunas remanescentes.

## Regra de comparabilidade

Uma alteração de vocabulário, limiar ontológico, conector ou política de PDF abre uma nova versão metodológica. Os resultados anteriores permanecem preservados, sem reescrever o histórico.
