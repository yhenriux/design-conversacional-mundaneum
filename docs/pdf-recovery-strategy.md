# Estratégia de localização e recuperação documental do corpus mestre

## Unidade do corpus

O corpus mestre contém todos os estudos únicos descobertos e deduplicados. A existência de PDF não determina a validade bibliográfica do estudo. Ela determina somente seu estado documental.

Cada estudo recebe um dos seguintes estados: PDF integral validado localmente; PDF recebido e ainda não validado; recuperação tentada sem PDF válido; URL de PDF ainda não testada; resolução por DOI pendente; ou busca por título pendente.

## Ordem das rotas

1. Testar a URL de PDF fornecida pela fonte de descoberta.
2. Resolver o DOI em OpenAlex, Crossref, Unpaywall, OpenAIRE, Semantic Scholar e CORE.
3. Consultar bases de acesso aberto: DOAJ, HAL, Zenodo, OSF, arXiv e BASE.
4. Consultar bases disciplinares: Europe PMC, PubMed Central, ERIC, SciELO, Redalyc e LA Referencia.
5. Examinar todas as localizações registradas no OpenAlex, não apenas a localização classificada como principal.
6. Pesquisar título exato, título normalizado e combinações de título com primeiro autor em repositórios institucionais.
7. Procurar versões aceitas, preprints, capítulos e partes pertinentes quando a obra integral não estiver legalmente disponível.
8. Registrar o motivo de cada falha e repetir somente rotas transitórias, como limite de requisições ou indisponibilidade do serviço.

## Critérios de aceitação do arquivo

Uma resposta só recebe o estado de PDF validado depois de cumprir todos os critérios aplicáveis:

- assinatura `%PDF` e tipo documental legível;
- correspondência entre título, autoria, DOI ou outro identificador;
- número de páginas compatível com artigo, capítulo, tese, livro ou parte utilizada;
- ausência de indícios de suplemento, elementos iniciais ou obra diferente;
- hash SHA-256 e URL de origem registrados;
- licença e permissão de redistribuição documentadas;
- extração textual com marcadores de página.

## Armazenamento no repositório

Todos os documentos legalmente obtidos ficam dentro da árvore do repositório local. PDFs com licença compatível com redistribuição podem entrar em `library/open-pdfs`. PDFs obtidos legalmente, mas sem autorização de redistribuição, ficam em `library/local-only` e são ignorados pelo Git. Seus metadados, hashes, origem, licença e estado permanecem versionados. Essa separação permite governança sem publicar cópias não autorizadas.

## Saturação documental

Uma fonte só recebe o estado de lacuna documental depois que as rotas compatíveis com seu identificador, tipo e área forem executadas. O relatório de saturação deve informar as APIs consultadas, consultas realizadas, datas, respostas, falhas transitórias e última tentativa. “Não localizado” significa que não foi encontrada uma cópia legal nas rotas documentadas, não que o documento inexista.
