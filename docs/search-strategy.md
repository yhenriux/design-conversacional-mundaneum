# Estratégia governada de busca e recuperação documental

## Pergunta operacional

Quais publicações tratam o Design Conversacional, as interfaces conversacionais ou o design de agentes e sistemas conversacionais como objeto central e oferecem conhecimento que pode orientar decisões de produto?

Uma publicação não entra apenas porque menciona chatbot, voz, inteligência artificial, conversa ou linguagem. A relação com Design Conversacional precisa organizar a pergunta, o método, a análise ou a contribuição do trabalho.

## Portão ontológico quantitativo

Cada resultado recebe quatro notas, com máximo de dez pontos:

| Dimensão | Pontos | Evidência exigida |
|---|---:|---|
| Centralidade ontológica | 0 a 4 | Design Conversacional ou o design de uma interface, agente ou sistema conversacional é objeto central |
| Relevância para produto | 0 a 3 | O estudo esclarece uma decisão sobre interação, conteúdo, comportamento, implementação, avaliação, acessibilidade, dados ou governança |
| Evidência documental | 0 a 2 | Metadados verificáveis e documento integral ou parte pertinente legalmente acessível |
| Contribuição aplicável | 0 a 1 | Há conceito, achado, método, padrão, crítica ou implicação utilizável |

O registro só é incorporado quando obtém pelo menos **3 de 4 em centralidade ontológica** e **7 de 10 no total**. Centralidade inferior a três causa exclusão automática, qualquer que seja a soma restante.

### Como atribuir centralidade

- **4 pontos:** uma expressão âncora aparece no título e corresponde ao objeto efetivamente estudado.
- **3 pontos:** título e resumo tratam explicitamente do design de uma interface, agente ou sistema conversacional, ainda que não usem a expressão “Design Conversacional”.
- **2 pontos:** o sistema conversacional é apenas contexto de adoção, desempenho, ensino, saúde ou comportamento.
- **1 ponto:** há somente menção lateral a conversa ou chatbot.
- **0 ponto:** não existe sistema conversacional projetado como objeto.

Resultados com zero, um ou dois pontos não entram no corpus. Também não são mantidos como uma fila temática paralela.

## Etapas da busca

1. **Busca de precisão:** executar as expressões exatas registradas em `config/search-queries.json` nas APIs de descoberta.
2. **Normalização:** converter os resultados para um esquema comum e preservar a resposta bruta, a consulta, a data, a API, a página ou cursor e o hash da resposta.
3. **Deduplicação:** usar, nesta ordem, DOI, PMID/PMCID, OpenAlex ID, Semantic Scholar ID, arXiv ID e título normalizado com ano.
4. **Triagem ontológica:** pontuar título e resumo. Casos limítrofes exigem leitura do texto integral antes da inclusão.
5. **Expansão controlada:** consultar referências citadas, trabalhos citantes, autores e veículos somente a partir de estudos aceitos. Cada novo candidato retorna ao passo 3 e passa pelo mesmo portão.
6. **Resolução documental:** consultar Unpaywall, OpenAlex, CORE, OpenAIRE, DOAJ, repositórios e APIs disciplinares para localizar versões legalmente acessíveis.
7. **Recuperação:** baixar somente arquivos oferecidos pelo titular, periódico, repositório ou serviço autorizado. Acesso institucional pode formar a biblioteca local, mas não autoriza publicação no GitHub.
8. **Validação do arquivo:** verificar assinatura `%PDF`, tipo MIME, tamanho, número de páginas, título, autoria, DOI e correspondência com o registro.
9. **Licença e destino:** registrar URL, data, licença e origem. Somente domínio público ou licença que permita redistribuição segue para `library/open-pdfs/`; os demais permanecem fora do Git.
10. **Catalogação:** atualizar registro, manifesto, estado documental, termos ontológicos e histórico da decisão.

## Famílias de consultas

### Núcleo explícito

`"conversation design" OR "conversational design" OR "design conversacional" OR "diseño conversacional"`

### Interfaces e experiência

`("conversational user interface" OR "conversational UX" OR "voice user interface") AND (design OR product OR interaction OR usability OR accessibility)`

### Agentes e sistemas

`("conversational agent" OR chatbot OR "dialogue system") AND (design OR "user experience" OR interaction OR interface)`

A sintaxe deve ser adaptada a cada API. A consulta executada, e não apenas a formulação conceitual, precisa ser preservada no histórico de busca.

## Exclusões substantivas

- conversa humana sem sistema ou produto conversacional projetado;
- aprendizagem conversacional entendida somente como técnica pedagógica;
- estudos genéricos de LLMs, inteligência artificial ou processamento de linguagem;
- adoção, satisfação ou desfecho de chatbot sem contribuição explícita para seu design;
- aplicação clínica, educacional ou comercial que apenas usa um chatbot como canal;
- “conversacional” empregado como estilo de escrita, marca ou metáfora;
- trabalhos sobre detecção de intenção, ASR ou geração de linguagem que não relacionam o resultado a uma decisão de experiência ou produto.

## Indicadores de cobertura

Cada ciclo publicará: APIs consultadas sobre as 20 mapeadas; consultas concluídas sobre as previstas; resultados brutos; duplicatas; registros avaliados; incluídos; exclusões por motivo; documentos integrais localizados; partes pertinentes localizadas; lacunas documentais; licenças redistribuíveis; falhas de API; e data da última atualização.

“Todos os PDFs possíveis” significa todos os documentos localizáveis por meios legais e reprodutíveis nas fontes conectadas. Não significa contornar autenticação, assinatura, embargo, robots.txt ou licença.
