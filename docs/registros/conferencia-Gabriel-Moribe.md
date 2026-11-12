# Conferência cruzada: testes de Gabriel Moribe

Conferente designado: Gabriel Conti — pré-conferência feita por agente de IA, pendente de validação humana

Data: 12/11/2026 · Método: só arquivos versionados e git (nada reexecutado; patches lidos no contêiner apenas para C5/C7). Os 5 testes foram executados por agente, então esta conferência também é de agente e deve ser validada por humano.

## Resumo

| Teste | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | Resultado sugerido |
|---|---|---|---|---|---|---|---|---|---|
| Closure-32 | ok | ok | ok | ok | n/a | ok | ok | ok | ok:Gabriel Conti |
| Time-6 | ok | ok | ok | ok | ok (concordo) | n/a | ok | ok | ok:Gabriel Conti |
| Math-25 | ok | ok | ok | ok | ok (concordo) | n/a | ok | ok | ok:Gabriel Conti |
| Chart-14 | ok | ok | ok | ok | ok (concordo) | n/a | ok | ok | ok:Gabriel Conti |
| Lang-61 | ok | ok | ok | ok | n/a | ok | ok | ok | ok:Gabriel Conti |

Todos os itens passaram; nenhuma divergência. A coluna `conferencia` de `dados/registro.csv` NÃO foi alterada (a edição fica com o humano).

## Closure-32 (ordem 1, semente 425589020, commit 09fb468)

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | `ambiente-Gabriel-Moribe.md`, coluna do teste 1: A1-A10 e D1-D5 `ok` (D4 por evidência indireta, conforme decisão do usuário; `suites/logs/Closure.32f.log` mostra `-b 360` e `-s 425589020`). Datas coerentes: manifesto 06:56 -08:00 = 11:56 -03; commit 12:02. |
| C2 | ok | Manifesto: imagem `sha256:45031972...`, cpus_limite=2, memoria_limite=6g, memoria_cgroup=6442450944, Java 1.8.0_452, Defects4J a83e479, SHA do EvoSuite e da config (7349236d...) iguais aos dos demais testes; semente 425589020 = `atribuicao.csv`; orcamento_total_s=360 (1 classe). nproc_visto=10 esperado. |
| C3 | ok | Ordem 1 do pesquisador; manifesto e commit 09fb468 (12:02 -03) anteriores aos de Time-6, Math-25, Chart-14 e Lang-61. |
| C4 | ok | `bug_detection`: Pass, num_trigger 0 = `resultado_d4j=Pass`, `testes_reveladores=0`, `deteccao_automatica=0`. `coverage`: 968/359/621/193 = registro; 359/968 = 37,09%. 57 `@Test` na suíte = `testes_gerados=57`, removidos 0, finais 57. `cobertura_falha.txt`=nenhuma = registro. `tempos.csv` soma 339 s = `tempo_total_s`; todos os códigos de saída 0. |
| C5 | não se aplica | Sem detecção (`falso_positivo=nao_se_aplica`, `deteccao_confirmada=0`); não há arquivo de FP, o que está correto. |
| C6 | ok | `bug_detection`=Pass. `fix_test_suite.summary.log`: 0 não compilam, 0 falham; `fix_test_suite.run.log` e `.compile.log` vazios; sem remoção em massa. Os dois `trigger.log` vazios. |
| C7 | ok (classificada pelo script, conferida à mão) | Não é indeterminado, mas conferi a classificação `nenhuma` com o patch e o `32f.1.xml`: as 13 linhas-alvo (1358, 1365, 1384, 1392-1397, 1399, 1400, 1402 e 1429 pela regra 2 da seção 5.2, trecho só com `+`) aparecem todas com hits=0 no XML. Coerente com 37% de cobertura da classe. |
| C8 | ok | `git log -p` de `resultados/Closure-32` mostra um único commit (09fb468), só adições (22 arquivos); nenhuma alteração posterior; `git status` limpo para a pasta. |

## Time-6 (ordem 2, semente 179721715, commit d6ca85f)

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 2 toda `ok`; A7 cita corretamente o commit 09fb468 da ordem 1; D4 indireto (`Time.6f.log` com `-b 360` e `-s 179721715`). |
| C2 | ok | Manifesto igual ao padrão (imagem, 2 CPUs, 6g, SHAs); semente 179721715 = `atribuicao.csv`; orçamento 360. |
| C3 | ok | Manifesto 08:42 -08:00 (13:42 -03), commit 13:49 -03, posteriores à ordem 1 (12:02) e anteriores à ordem 3 (14:48). Observação: o commit 9a5c348 (13:27, suporte a `substituicoes.csv` em `scripts/`) ocorreu entre a ordem 1 e a ordem 2; não afeta as saídas, mas a ordem 1 rodou com a versão anterior do script. |
| C4 | ok | `bug_detection`: Fail, num_trigger 2 = registro (`Fail`, 2 reveladores, detecção 1). `coverage`: 380/303/182/128 (79,74%) = registro. 40 `@Test` = `testes_gerados=40`, 0 removidos. `cobertura_falha.txt`=parcial = registro. `tempos.csv` soma 304 s = `tempo_total_s`. |
| C5 | concordo | Revisão independente. `6b.1.trigger.log` lista test10 (`Expecting exception: IllegalArgumentException`) e test36 (`expected:<-433475552740680> but was:<-433444016740680>`), que são os 2 reveladores; `6f.1.trigger.log` vazio. O patch (lido no contêiner) remove, da corrigida para a defeituosa, o bloco `Cutover too early` em `getInstance` (test10 espera exatamente essa mensagem) e o ajuste `year <= 0` / `wyear <= 0` nos dois métodos do `ImpreciseCutoverField` (test36, diferença de 31536000000 ms = 365 dias, compatível com `year().add(instant, -1)`). F1, F2, F4, F5 corretos. F3: test10 usa entradas fixas; test36 usa `DateTime.now`, mas a classe tem `mockJVMNonDeterminism=true` e o próprio teste afirma `getMillis()==1392409281320L`, ou seja, relógio mockado. Ressalva a confirmar por humano: o fuso America/Los_Angeles do contêiner entra no cálculo, mas é o mesmo nas duas versões e na geração. Decisão `falso_positivo=nao` aceita; `deteccao_confirmada` segue `pendente` até o humano. |
| C6 | não se aplica | Houve detecção. |
| C7 | ok (classificada pelo script, conferida à mão) | Recontei as linhas-alvo pelo patch: 196-198 (bloco removido em `getInstance`), 983-991 e 1016-1024 (blocos `weekyear`/`year`), 19 no total, 11 com hits>0 (3 + 4 + 4). Bate com `linhas_consideradas=19`, `linhas_cobertas=11`; `parcial` correto. |
| C8 | ok | Único commit na pasta (d6ca85f), só adições; sem alterações posteriores. |

## Math-25 (ordem 3, semente 621546919, commit a703045)

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 3 toda `ok`, com `cpus_limite=2`, `memoria_limite=6g` e nota de nproc 10 esperado; A7 cita 09fb468 e d6ca85f. |
| C2 | ok | Manifesto padrão; semente 621546919 = `atribuicao.csv`; orçamento 360. |
| C3 | ok | Manifesto 09:41 -08:00 (14:41 -03), commit 14:48 -03; posterior a d6ca85f (13:49) e anterior a 01cc3b7 (15:47). |
| C4 | ok | `bug_detection`: Fail, num_trigger 1 = registro. `coverage`: 95/94/30/29 (98,95%) = registro. 6 `@Test` = `testes_gerados=6`, 0 removidos. `cobertura_falha.txt`=total = registro. `tempos.csv` soma 315 s = `tempo_total_s`. |
| C5 | concordo | Revisão independente. `25b.1.trigger.log` tem só test5 (`Expecting exception: IllegalStateException`, `HarmonicFitter_ESTest.java:228`); `25f.1.trigger.log` vazio. O patch remove, na defeituosa, `if (c2 == 0) { throw new MathIllegalStateException(ZERO_DENOMINATOR); }` em `ParameterGuesser.guess()`; o teste monta 4 pontos fixos e chama `guess()`, esperando a exceção da corrigida. Determinístico (aritmética de ponto flutuante com entradas literais). Sem remoção na filtragem (summary com 0/0). Decisão `falso_positivo=nao` aceita. |
| C6 | não se aplica | Houve detecção. |
| C7 | ok (classificada pelo script, conferida à mão) | Linhas-alvo: 323 (`if (c2 == 0) {`) e 326 (`throw`); os comentários intermediários não são executáveis (regra 3). `cobertura_falha.txt`: 323 hits=2, 326 hits=1, `total` correto. |
| C8 | ok | Único commit na pasta (a703045), só adições; sem alterações posteriores. |

## Chart-14 (ordem 4, semente 1583597775, commit 01cc3b7)

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 4 toda `ok`; D3 orçamento 720 = 360 x 2 classes; D4 indireto (`Chart.14f.log` com `-b 720` e `-s 1583597775`). |
| C2 | ok | Manifesto padrão; semente 1583597775 = `atribuicao.csv`; `orcamento_total_s=720`, `classes_modificadas` com CategoryPlot e XYPlot (n_classes=2). |
| C3 | ok | Manifesto 10:35 -08:00 (15:35 -03), commit 15:47 -03; posterior a a703045 (14:48) e anterior a 5ae64fc (16:24). |
| C4 | ok | `bug_detection`: Fail, num_trigger 7 = registro. `coverage`: 2643/2196/1444/1069 (83,09%) = registro. 192 (XYPlot) + 164 (CategoryPlot) = 356 `@Test` = `testes_gerados`, 0 removidos. `cobertura_falha.txt`=total = registro. `tempos.csv` soma 576 s = `tempo_total_s`. |
| C5 | concordo | Revisão independente. `14b.1.trigger.log` lista 7 reveladores (CategoryPlot test038, test001, test011; XYPlot test017, test111, test102, test000), todos `NullPointerException` em `removeDomainMarker`/`removeRangeMarker`; `14f.1.trigger.log` vazio e o run_bug_detection registra 7 falhas na defeituosa. O patch remove, em 4 pontos de CategoryPlot e XYPlot, o guard `if (markers == null) return false;` antes de `markers.remove(marker)`. O topo da pilha de test038 (linha 2166) cai exatamente no ponto do patch. A amostra de 3 de 7 do executor é permitida pelo checklist e o padrão de pilha é o mesmo nos 7. Causa é referência nula (determinística), não infraestrutura. Decisão `falso_positivo=nao` aceita. |
| C6 | não se aplica | Houve detecção. |
| C7 | ok (classificada pelo script, conferida à mão) | 8 linhas-alvo (2166-2167 e 2451-2452 em CategoryPlot; 2293-2294 e 2532-2533 em XYPlot), todas com hits>0 em `cobertura_falha.txt`; bate com as linhas removidas pelo patch, `total` correto. |
| C8 | ok | Único commit na pasta (01cc3b7), só adições; sem alterações posteriores. |

## Lang-61 (ordem 5, semente 639934461, commit 5ae64fc)

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 5 toda `ok`; A7 cita os commits das ordens 1 a 4 (09fb468, d6ca85f, a703045, 01cc3b7), todos existentes no git; D4 indireto (`Lang.61f.log` com `-b 360` e `-s 639934461`). |
| C2 | ok | Manifesto padrão; semente 639934461 = `atribuicao.csv`; orçamento 360. |
| C3 | ok | Manifesto 11:18 -08:00 (16:18 -03), commit 16:24 -03; posterior a todas as ordens 1 a 4 do pesquisador. |
| C4 | ok | `bug_detection`: Pass, num_trigger 0 = registro (`Pass`, 0, 0). `coverage`: 656/650/464/463 (99,09%) = registro. 227 `@Test` = `testes_gerados`, 0 removidos. `cobertura_falha.txt`=total = registro. `tempos.csv` soma 278 s = `tempo_total_s`. |
| C5 | não se aplica | Sem detecção (`nao_se_aplica`); não há arquivo de FP, o que está correto. |
| C6 | ok | `bug_detection`=Pass; `fix_test_suite.summary.log` com 0 não compilam e 0 falham; `.run.log` e `.compile.log` vazios; `trigger.log` de b e f vazios. Cobertura total da linha-alvo sem detecção é plausível (falha de limite em `indexOf`, que depende de `buffer.length` > `size`), sem indício de problema de infraestrutura. |
| C7 | ok (classificada pelo script, conferida à mão) | Linha-alvo única: 1776 (`int len = size - strLen + 1;`, a linha `-` do patch); hits=5, `total` correto. |
| C8 | ok | Único commit na pasta (5ae64fc), só adições; sem alterações posteriores. |

## Observações para o humano

- Os três arquivos de falso positivo (Time-6, Math-25, Chart-14) foram preenchidos por agente; a revisão independente concorda, mas `deteccao_confirmada` continua `pendente` e o campo "Conferente" desses arquivos está em branco. A validação final é humana.
- Time-6, F3: ressalva sobre o fuso do contêiner no test36 (relógio mockado pelo EvoSuite, fuso igual nas duas versões); decidir se é aceitável.
- D4 foi aceito por evidência indireta (`-b`, `-s` nos logs de `suites/logs` e SHA da configuração), conforme decisão do usuário.
- Math-25: a nota anterior do usuário dizia que Math-25 "não compila"; neste teste o pipeline compilou e rodou todas as etapas com código 0 (`cobrir.log`, `detectar.log` com `compile` OK). Não há motivo nos arquivos para substituí-la; `dados/sorteio/substituicoes.csv` não a lista. Fica a observação caso o diagnóstico prévio precise ser revisto.
- O commit 9a5c348 (alteração em `scripts/` para suportar substituições) foi feito entre a ordem 1 e a ordem 2; o manifesto não registra a versão dos scripts, então não dá para provar por arquivo que ela não alterou o pipeline, mas as saídas dos 5 testes têm o mesmo formato.
