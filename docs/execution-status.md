# Estado da execução do corpus mestre

## Ciclo 20260831T003810Z

### Corpus mestre

- Os 1.065 estudos únicos descobertos formam o corpus mestre, independentemente da disponibilidade de PDF.
- Uma descoberta brasileira suplementar da USP/SBC foi adicionada em 05 set. 2026, validada e extraída como PDF integral.
- A presença de documento integral é tratada como estado documental, não como critério de validade bibliográfica.
- 1.007 estudos possuem DOI e 387 apresentaram alguma URL de PDF nos metadados de descoberta.
- A fila de 341 URLs diretas foi integralmente testada. Duzentas entregaram PDFs; 190 corresponderam bibliograficamente aos estudos e dez foram rejeitadas por divergência ou erro estrutural.
- A rota OpenAlex consultou os 633 DOI que não possuíam URL documental. O serviço reconheceu 411 estudos, retornou 605 localizações e forneceu 69 URLs de PDF para 61 estudos.
- Das 69 URLs do OpenAlex, quarenta entregaram PDFs. Trinta e sete foram validados e três foram rejeitados por divergência bibliográfica.
- O corpus possui agora 297 PDFs integrais validados localmente.
- OpenAIRE, Semantic Scholar, DOAJ, HAL, Europe PMC e arXiv foram executados sobre os estudos pendentes. O arXiv localizou 22 correspondências por título, das quais 18 foram validadas como PDFs.
- Permanecem 447 estudos com DOI sem PDF localizado nas rotas já executadas e 26 estudos sem DOI para busca por título e por repositório institucional.

### Descoberta

- 1.246 ocorrências recuperadas por OpenAlex e Crossref.
- 1.064 candidatos únicos depois da deduplicação.
- 80 registros encaminhados à primeira triagem.

Uma auditoria posterior identificou que o primeiro corte exigia nota 7 antes de contabilizar os sinais documental e de aplicabilidade. Esse procedimento poderia retirar estudos ontologicamente centrais que alcançariam o limiar depois dessas duas verificações. O filtro foi corrigido sem rebaixar o requisito de centralidade.

### Triagem

- 67 inclusões provisórias.
- 8 casos que exigem leitura do texto integral.
- 3 exclusões ontológicas.
- 2 duplicatas documentais.

As inclusões são provisórias porque o resumo não substitui a confirmação no documento integral.

Uma correção conceitual retirou “produto conversacional” dos requisitos de inclusão. Design Conversacional passa a ser tratado como objeto autônomo de pesquisa e estudo. Produto, sistema, interface, serviço, educação e outros domínios são contextos possíveis, não fundamentos ontológicos. Um registro antes excluído por não ter produto conversacional foi devolvido à leitura integral.

### Triagem ampliada

- 274 candidatos adicionais possuem centralidade ontológica mínima de 3/4 e podem alcançar nota 7/10 depois dos sinais documental e de aplicabilidade.
- O conjunto foi dividido em seis lotes governáveis: cinco com cinquenta registros e um com vinte e quatro.
- O lote B01 foi lido por título e resumo: 42 inclusões provisórias, 2 casos para leitura integral, 4 exclusões ontológicas e 2 duplicatas.
- As inclusões do lote B01 ainda exigem obtenção legal e leitura do texto integral. Elas não foram incorporadas ao conjunto de evidências confirmadas.
- Entre os 44 registros selecionados do B01, 20 apresentavam URL de PDF nos metadados de origem. Seis URLs devolveram arquivos PDF.
- Cinco documentos corresponderam ao título esperado e foram extraídos integralmente: 83 páginas e 309.070 caracteres com marcadores de página.
- Uma URL foi rejeitada porque entregava um livreto relacionado ao tema, mas não o artigo bibliográfico esperado. As outras quatorze falharam por bloqueio, resposta não documental ou indisponibilidade.
- Os cinco textos extraídos continuam fora do Git e aguardam leitura analítica; os manifestos, hashes, licenças informadas e decisões de validação permanecem versionados.

### Resolução documental

- 74 registros já processados na resolução e 1 registro reclassificado que ainda precisa entrar nessa etapa.
- 70 identificadores resolvidos no OpenAlex.
- 43 registros identificados como acesso aberto.
- 29 localizações de PDF submetidas à recuperação.
- 23 PDFs integrais validados localmente.
- 23 extrações completas, com cobertura textual em todas as páginas.

### Pendências documentais

- 11 localizações continuam com bloqueio, página HTML, arquivo incorreto ou outra falha depois das resoluções complementares.
- 11 registros abertos ainda não oferecem URL direta de PDF validada.
- 26 não apresentam versão aberta localizada nos resolvedores executados.
- 4 permanecem como lacuna documental.

### Próxima ação

Consultar Semantic Scholar, OpenAIRE, CORE, DOAJ, HAL, Zenodo, OSF, arXiv, Europe PMC e NCBI para resolver as pendências. O Unpaywall será usado somente depois de autorização explícita para transmitir o e-mail exigido pelo serviço.

### Semantic Scholar

A primeira tentativa sem chave consultou 55 registros pendentes. Cinco foram resolvidos antes de o serviço aplicar limite de requisições, com três localizações abertas já conhecidas e nenhum PDF novo validado. As cinquenta respostas com código 429 permanecem registradas como limitação da execução, não como ausência documental. A próxima consulta deverá usar uma chave autorizada ou respeitar uma janela de espera maior.

### OpenAIRE

O OpenAIRE consultou 55 registros pendentes, resolveu 52 e ofereceu 43 ocorrências de URL aberta. Depois da deduplicação, quarenta endereços foram testados. Apenas um forneceu um PDF que correspondia ao título esperado. O resultado confirma que a indicação de acesso aberto de um agregador não substitui a validação do arquivo.

### Europe PMC e PubMed Central

O Europe PMC consultou 53 DOI pendentes e encontrou três registros biomédicos. Dois possuíam PDF no conjunto aberto do PubMed Central. Ambos foram recuperados e validados. A mesma rota corrigiu o artigo da JMIR cujo endereço anterior apontava para um suplemento. O acesso foi realizado pelo conjunto aberto oficial destinado à recuperação automatizada.

### DOAJ e HAL

DOAJ e HAL consultaram 51 DOI pendentes. Foram encontrados dois registros no DOAJ e um no HAL, sem nova URL direta de PDF. Os resultados foram preservados como evidência de cobertura e possíveis rotas para inspeção editorial posterior.

### Zenodo e OSF

Zenodo e OSF foram consultados por título para 56 registros. O limiar de correspondência foi fixado em 94%. Nenhuma nova versão documental foi localizada. Sete falhas de serviço foram registradas separadamente e poderão ser repetidas em outro ciclo.

### arXiv

A API do arXiv recebeu sete consultas agrupadas, cobrindo 56 títulos. Quatro preprints apresentaram correspondência exata. Todos foram baixados, validados e extraídos integralmente, elevando o conjunto documental para 22 fontes.

### Localizações alternativas do OpenAlex

As respostas integrais do OpenAlex foram reprocessadas para examinar todas as localizações, não somente a versão indicada como melhor. Dezesseis URLs alternativas foram testadas e duas corresponderam ao título esperado. Uma forneceu o artigo completo “Chatbot Design and Implementation: Towards an Operational Model for Chatbots”. A outra continha somente os elementos iniciais do livro “Voice User Interface Design” e foi retirada do conjunto integral. O saldo desta etapa foi de um novo documento validado, elevando o total para 23.
