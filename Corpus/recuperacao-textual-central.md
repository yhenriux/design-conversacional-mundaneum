---
tipo: controle-de-recuperacao-documental
escopo: fontes-centrais-sem-texto-analiticamente-suficiente
atualizado_em: 2026-09-19
regra_de_acesso: somente-fontes-legitimas-e-localizacoes-abertas
---

# Recuperação de texto para o corpus central

## Distinção de estados

As 178 fichas analíticas ainda não concluídas não estão, em sua maior parte, sem texto. Elas já dispõem de extração documental suficiente e dependem de leitura crítica e redação. A recuperação textual é uma frente separada: procura texto integral ou o trecho integral correspondente quando a fonte central ainda não o possui.

## Casos prioritários verificados

| Registro atual | Diagnóstico | Ação correta |
| --- | --- | --- |
| DCM-00103, *Studies in Conversational UX Design* | O PDF local contém apenas front matter e sumário. A edição integral é de acesso por assinatura. | Recuperar, quando houver acesso legítimo, capítulos identificados pelo sumário e registrá-los como capítulos, sem apresentar o livro completo como texto recuperado. |
| DCM-00264, *Erratum to: An approach to conversational agent design using semantic sentence similarity* | O arquivo de uma página é integral para uma errata, mas não contém o estudo empírico original. | Manter a errata como documento corretivo. Buscar o artigo original DCM-00250, DOI 10.1007/s10489-012-0349-9. |
| DCM-00792, *Erratum to: Natural language scripting within conversational agent design* | O arquivo de uma página é integral para uma errata, mas não contém o estudo original. | Manter a errata como documento corretivo. Buscar o artigo original DCM-00263, DOI 10.1007/s10489-012-0408-2. |

## Estratégia de busca em execução

1. Consultar OpenAlex por DOI e preservar todas as localizações abertas devolvidas.
2. Baixar somente URL que entregue arquivo com assinatura PDF, registrando URL, data, hash, licença declarada e versão.
3. Validar correspondência entre título, autores, DOI, número de páginas e arquivo recebido antes de promover o documento.
4. Extrair texto paginado e só então mudar o estado para texto suficiente.
5. Para livros fechados, buscar capítulos identificados e cópias autorizadas em repositórios institucionais, páginas de autores e anais. A ausência de acesso aberto não autoriza substituir a obra por cópia não verificada.

## Limite técnico registrado

Em 2026-09-19, a primeira execução do resolvedor local de OpenAlex foi bloqueada pela política local de rede. Foram preservadas 50 tentativas, sem resultado positivo, para permitir retomada com acesso de rede disponível. A busca de fontes públicas continua pela interface de pesquisa e pelos resolvedores já existentes no repositório.

## Referências de controle

- Página oficial do livro: https://doi.org/10.1007/978-3-319-95579-7
- Capítulo introdutório: https://doi.org/10.1007/978-3-319-95579-7_1
- Artigo original relacionado a DCM-00264: https://doi.org/10.1007/s10489-012-0349-9
- Artigo original relacionado a DCM-00792: https://doi.org/10.1007/s10489-012-0408-2
