# Esqueleto do projeto — Web Recon CLI

> Leiam os dois antes de codar. Este é o **mapa**: o que cada arquivo faz, o que
> entra/sai dele, e quando está "pronto". A lógica de dentro é com vocês.

## O que a ferramenta faz (em uma frase)

Recebe uma URL, faz uma requisição, e relata a postura de segurança básica do
alvo: status HTTP, servidor, security headers presentes/ausentes, tecnologia
provável e paths comuns expostos.

## O fluxo de dados (o "pipeline")

Pensa na ferramenta como uma esteira. O dado entra cru e vai sendo enriquecido:

```
  URL (string)
     │
     ▼
 http_client ──► objeto de resposta ───┬──► headers ──►  achados de headers
                                       ├──► fingerprint ► tech provável
                                       └──► paths ──────► paths expostos
                                                              │
  todos os achados ───────────────────────────────────────►  report ──► texto/arquivo
```

Repara: **`http_client` faz a request UMA vez**, e os três analisadores
(`headers`, `fingerprint`, `paths`) consomem o resultado. `paths` é um caso
especial — ele faz requests *extras* (uma por path testado).

---

## ⚠️ DECISÃO PENDENTE — vocês definem (não eu)

**O que o `http_client.py` devolve pro resto do programa?** Tudo depende disso.
Três caminhos possíveis — escolham um e anotem aqui:

| Opção | O que devolve | Trade-off |
|---|---|---|
| A | O objeto `Response` do `requests` cru | Simples agora, mas acopla todo mundo na lib `requests` |
| B | Um dicionário próprio (`{"status": ..., "headers": ..., "body": ...}`) | Um pouco mais de trabalho, mas desacopla e fica fácil de testar |
| C | Uma `dataclass` própria (ex.: `FetchResult`) | Mais "Python de verdade", autodocumentado, testável |

> **Decisão da dupla:** _______________  (preencham antes de começar a Fase 1)

Toda a coluna "Recebe / Devolve" abaixo assume que vocês escolheram um formato e
o chamam de **`resultado`**. Troquem pelo nome real quando decidirem.

---

## Mapa dos arquivos

| Arquivo | Responsabilidade (uma só) | Recebe | Devolve | Pronto quando… | Bom pra |
|---|---|---|---|---|---|
| `recon/http_client.py` | Fazer o GET na URL e tratar erro de conexão/timeout | `url: str` | `resultado` (ver decisão) | dado uma URL válida, devolve o resultado; dada uma URL morta, não quebra — devolve erro tratado | **sênior** (define o contrato) |
| `recon/headers.py` | Dizer quais security headers existem e quais faltam | `resultado` | lista/dict de headers presentes e ausentes | passado um resultado, lista certo os headers de uma lista conhecida | **júnior** (isolado, testável, critério claro) |
| `recon/fingerprint.py` | Deduzir tecnologia pelos headers (`Server`, `X-Powered-By`…) | `resultado` | tech provável (string/lista) | identifica nginx/apache/php quando o header existe; diz "desconhecido" quando não | **júnior→sênior** |
| `recon/paths.py` | Testar paths comuns (`robots.txt`, `sitemap.xml`, `/.git/`) | `url: str` (base) | lista de paths e seus status | reporta quais paths responderam 200 vs 404 | **sênior** (faz requests próprias, mais lógica) |
| `recon/report.py` | Juntar todos os achados num relatório legível | os achados dos módulos acima | texto (e depois, arquivo) | monta um relatório lendo todos os achados, sem fazer request nenhuma | **júnior** (pura formatação, zero rede) |
| `main.py` | Orquestrar: ler args, chamar os módulos na ordem, imprimir | argumentos da linha de comando | exit code | `python main.py http://localhost` roda o pipeline ponta a ponta | **sênior** (cola tudo) |
| `tests/` | Um teste por módulo, isolado | — | — | cada módulo tem ao menos um teste que passa | a dupla, junto |

### Por que essa divisão

- **Uma responsabilidade por arquivo** = cada um pega um arquivo, ninguém edita
  o do outro, conflito no Git fica raro.
- **Os analisadores não fazem request** (exceto `paths`) — recebem o `resultado`
  pronto. Isso os torna **testáveis sem internet**: você fabrica um `resultado`
  falso no teste e verifica a lógica. Função que mistura rede + lógica é um
  inferno de testar.
- **`report` não toca na rede** — só formata. Se ele precisar de internet pra
  rodar, alguma responsabilidade vazou pra dentro dele.

---

## Ordem de ataque (as Fases viram branches)

Cada fase é uma branch + um Pull Request. Não pulem ordem — cada uma depende da anterior.

| Fase | Branch sugerida | Entrega |
|---|---|---|
| 1 | `feature/fase-1-http` | `http_client.py` + `main.py` mínimo que imprime status e `Server` |
| 2 | `feature/fase-2-headers` | `headers.py` plugado no pipeline |
| 3 | `feature/fase-3-fingerprint` | `fingerprint.py` |
| 4 | `feature/fase-4-paths` | `paths.py` |
| 5 | `feature/fase-5-report` | `report.py` + salvar em arquivo |
| 6 | `feature/fase-6-polish` | vários alvos, cor, config |

**Comecem pela Fase 1.** Ela força a decisão pendente lá em cima — e sem ela
nada anda.

## Regra ética (não-negociável)

A ferramenta roda **só em alvo próprio ou autorizado**. Treino: `localhost` ou um
alvo vulnerável que vocês mesmos subam. Nunca terceiro sem permissão.

## O que NÃO está aqui de propósito

A lógica de dentro de cada função. O esqueleto diz *o que* e *com qual contrato* —
o *como* é o trabalho de vocês. É aí que se aprende a programar de verdade.
