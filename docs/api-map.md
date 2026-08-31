# Mapa das 20 APIs

As vinte APIs formam uma rede de serviços complementares. Nenhuma delas, isoladamente, oferece cobertura completa e arquivo integral de toda a literatura.

## Camada 1: descoberta interdisciplinar e identificação

1. **OpenAlex:** índice principal, relações entre obras e localizações abertas.
2. **Crossref:** DOI, referência bibliográfica, licença e links depositados pelos editores.
3. **Semantic Scholar:** relações de citação e campo `openAccessPdf`.
4. **DataCite:** DOI de repositórios, relatórios, livros, preprints e literatura cinzenta.
5. **OpenCitations:** expansão transparente de referências e citações.

## Camada 2: resolução de acesso aberto e repositórios

6. **Unpaywall:** melhor versão aberta conhecida para um DOI.
7. **CORE:** agregação de repositórios e, quando autorizado, texto integral.
8. **OpenAIRE Graph:** publicações, repositórios, projetos e localizações de acesso.
9. **DOAJ:** artigos em periódicos de acesso aberto e informação de licença.
10. **HAL:** versões depositadas por autores e instituições.
11. **Zenodo:** artigos, relatórios, livros, apresentações, dados e arquivos.
12. **OSF:** preprints, projetos e arquivos públicos.
13. **arXiv:** preprints e PDF direto, especialmente em computação e HCI.

## Camada 3: cobertura disciplinar

14. **Europe PMC:** aplicações biomédicas, resumo, texto integral e ligações de citação.
15. **NCBI E-utilities:** PubMed, PubMed Central e ligação PMID-PMC.
16. **IEEE Xplore:** computação, engenharia, voz, HCI e sistemas de diálogo.

## Camada 4: índices e plataformas licenciadas

17. **Springer Nature:** periódicos, livros e capítulos.
18. **Scopus:** descoberta, cobertura e citações mediante credenciais.
19. **ScienceDirect:** conteúdo Elsevier conforme os direitos da instituição ou do usuário.
20. **Web of Science:** descoberta e rastreamento de citações mediante assinatura.

O registro operacional completo, com autenticação, função, cobertura, capacidade documental e documentação oficial, está em `data/api-registry.csv`.

## Ordem de conexão

O primeiro ciclo usa serviços públicos ou com cadastro gratuito: OpenAlex, Crossref, Unpaywall, Semantic Scholar, OpenAIRE, Europe PMC, NCBI, arXiv, DOAJ, HAL, Zenodo, OSF, DataCite e OpenCitations. CORE entra assim que a chave for configurada. IEEE, Springer Nature, Scopus, ScienceDirect e Web of Science entram quando houver credenciais e, nos casos aplicáveis, acesso institucional.

As credenciais serão lidas apenas de variáveis de ambiente. Chaves, tokens e cookies nunca serão gravados no repositório.
