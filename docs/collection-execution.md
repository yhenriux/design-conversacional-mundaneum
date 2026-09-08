# Execução da formação do corpus

Escopo vigente: descoberta bibliográfica, recuperação legal de PDFs e catalogação. Não executar inspeção de páginas, correspondência de título dentro do PDF, extração textual ou avaliação científica nesta fase.

## Entregas e estado

- [x] Ler o planejamento autoral de formação do corpus.
- [x] Registrar identificadores persistentes a partir do inventário existente.
- [x] Deduplicar DOI independentemente do título e preservar Unicode.
- [x] Registrar ocorrências das fontes de entrada em manifesto próprio.
- [x] Acrescentar estados operacionais de coleta sem apagar estados históricos.
- [ ] Migrar consumidores dos identificadores e reconciliar associações históricas por metadados.
- [ ] Recuperar proveniência adicional dos resultados brutos previamente deduplicados.
- [ ] Manter múltiplos arquivos e versões por obra, com todas as localizações disponíveis.
- [ ] Implementar paginação, retomada e registro de falhas nas consultas multilíngues.
- [ ] Executar coleta brasileira nas cinco regiões com acompanhamento das 27 unidades federativas.
- [ ] Executar América Latina e Caribe, Europa, África, Ásia, América do Norte e Oceania.
- [ ] Corrigir e ampliar expansão por citações, autores, grupos e eventos.
- [ ] Recuperar todas as URLs disponíveis dos candidatos elegíveis pelos metadados.
- [ ] Publicar catálogo com estados de coleta, proveniência e atualização automática.
- [ ] Produzir relatório por ciclo com cobertura, falhas, limites e novidade.
- [ ] Agendar atualização trimestral após integração do processo.

## Primeira passagem

O inventário passou de 1.626 para 1.622 registros após reunir DOI repetidos. Nenhum PDF foi removido. Os identificadores sobreviventes são preservados no registro persistente. Estados antigos de validação permanecem apenas como histórico; `collection_status` é o campo operacional desta fase.

A estabilidade começa no registro persistente criado nesta passagem. Associações anteriores que utilizaram numeração recalculada ainda exigem reconciliação por metadados, sem abrir os documentos.

## Retomada em 7 de setembro de 2026

- Criado `data/corpus/collection-history.csv`, associando históricos por DOI ou título único nos metadados. Após o lote: 1.042 ocorrências de transferência, 1.034 associadas e oito sem associação segura. Há 301 ocorrências com identificador histórico diferente do atual.
- O coletor de URLs diretas usa metadados e URL para retomada, mantém falhas anteriores e distingue nomes de arquivos por URL.
- Executadas 23 tentativas adicionais de URLs diretas, sem novo PDF recebido. As falhas foram preservadas.
- Corrigida a consulta de referências citadas para usar a API OpenAlex. Relações de múltiplas sementes são mantidas. Seleção das sementes utiliza metadados, sem exigir PDF ou leitura.
- O ciclo `20260907T171138Z` recuperou 82 relações candidatas a partir de três sementes. Continua sendo um lote limitado; paginação completa, avanço persistente entre sementes e integração dos resultados ainda estão pendentes.
- Não houve inspeção de conteúdo, extração textual ou análise científica nesta passagem.

## Paginação e retomada

Implementado `scripts/discover_paginated.py` para OpenAlex e Crossref, com cursor por consulta, configuração congelada por ciclo, tentativas registradas, respostas brutas e CSV por página. O limite de páginas por execução mantém consultas abertas; somente ausência de resultados ou de próximo cursor sinaliza conclusão. O valor zero solicita esgotamento da consulta.

O ciclo `20260907T171406Z` concluiu a expressão portuguesa "design conversacional" no OpenAlex com 21 ocorrências. O ciclo multilíngue `20260907T171423Z` foi iniciado com duas páginas por consulta e 100 resultados por página. Sua conclusão deve ser consultada em `pagination.json`; encerrar um lote não equivale a esgotar as consultas.

O integrador dos ciclos passou a usar a mesma identidade persistente por DOI ou identificador de fonte da base principal, preservando caracteres Unicode.

O integrador também preserva descobertas anteriores ao reexecutar o mesmo ciclo, evitando perda de registros já incorporados. O resumo do corpus passa a informar os estados de coleta separadamente dos estados históricos.
