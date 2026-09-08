# Priorização das falhas de coleta

Atualizado em 8 de setembro de 2026 a partir do manifesto de URLs do corpus mestre. Esta classificação trata apenas da resposta de rede; não avalia o conteúdo dos arquivos.

| Categoria | Registros | Ação recomendada |
|---|---:|---|
| Arquivo recebido sem erro | 2.249 | manter no acervo local |
| HTTP 403 | 1.042 | procurar repositório ou cópia aberta alternativa |
| Bloqueio de rede local | 671 | repetir em ambiente com rede autorizada |
| Resposta não PDF | 369 | resolver página de obra e novo bitstream |
| HTTP 404 | 55 | procurar versão atualizada ou identificador alternativo |
| Timeout | 47 | repetir com limite maior e recuo |
| Erro SSL | 24 | buscar endpoint HTTPS alternativo |
| HTTP 429 | 19 | aplicar espera progressiva |
| DNS, conexão ou reset | 30 | reprocessar em ciclo posterior |
| HTTP 500 | 6 | repetir e registrar persistência |

As prioridades são: 403, respostas que não são PDF e registros com DOI sem endereço. A fila não será considerada encerrada enquanto houver rotas públicas razoáveis a testar.
