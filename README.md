# Design Conversacional Mundaneum

Repositório de mapeamento sistemático da literatura relacionada ao Design Conversacional como área interdisciplinar de produto.

## Compromisso documental

Cada registro deve estar associado a um destes estados:

1. `pdf-integral-validado`;
2. `pdf-parte-utilizada-validado`;
3. `pdf-local-a-validar-extensao`;
4. `lacuna-documental`.

O objetivo do levantamento massivo é eliminar os dois últimos estados. Nenhum registro é descrito como aguardando leitura. O controle informa o que existe documentalmente e o que ainda precisa ser localizado ou validado.

## Estrutura

- `records/`: um registro governado para cada fonte;
- `data/corpus-master.csv`: classificação fonte a fonte;
- `data/document-manifest.csv`: proveniência, licença e disponibilidade documental;
- `data/document-gaps.csv`: fila objetiva de lacunas documentais;
- `library/open-pdfs/`: PDFs cuja licença permite redistribuição;
- `docs/catalog.md`: navegação pelo corpus;
- `docs/methodology.md`: protocolo de inclusão, classificação e uso.
- `docs/api-map.md`: funções das vinte APIs de descoberta e recuperação;
- `docs/search-strategy.md`: consultas, portão ontológico e fluxo documental;
- `config/ontology-gate.json`: critérios quantitativos de inclusão;
- `config/search-queries.json`: famílias versionadas de consultas;
- `data/api-registry.csv`: requisitos e capacidade de cada conexão.

## Regra ontológica

Design Conversacional é o centro de inclusão, não apenas uma etiqueta temática. Uma fonte precisa tratar o design de uma interface, agente ou sistema conversacional como objeto central e contribuir para decisões de produto. Menções laterais a chatbots, conversa, voz ou inteligência artificial são excluídas.

## Direito autoral e proveniência

O repositório publica somente documentos com licença de redistribuição ou em domínio público. Fontes fechadas continuam catalogadas, mas seus arquivos não são enviados ao GitHub. O corpus local pode registrar exemplares fornecidos legalmente ou acessados por biblioteca, respeitando as condições de uso.

## Estado inicial

O primeiro ciclo migra 116 registros do corpus do Volume 1. A arquitetura futura da coleção será recalculada conforme o corpus crescer e as lacunas documentais forem eliminadas.

## Primeiro ciclo de descoberta

O piloto OpenAlex e Crossref produziu 1.064 candidatos únicos. O portão automático encaminhou 80 para triagem argumentada:

- 67 inclusões provisórias, dependentes de confirmação documental;
- 7 casos que exigem texto integral antes da decisão;
- 4 exclusões por ausência de centralidade ontológica;
- 2 ocorrências reunidas como duplicatas documentais.

A resolução combinada por OpenAlex, OpenAIRE e Europe PMC validou dezoito PDFs integrais. Todos tiveram seu texto extraído localmente com marcadores de página. Arquivos e textos sem licença de redistribuição confirmada permanecem fora do Git.

Consulte `data/screening/screening-summary.json` e `data/document-resolution/document-status-summary.json` para os resultados auditáveis do ciclo.
