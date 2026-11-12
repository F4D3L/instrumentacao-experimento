# Conferência cruzada: testes de Guilherme Fadel

Conferente designado: Guilherme Celente — pré-conferência feita por agente de IA, pendente de validação humana

Data: 12/11/2026. Método: só arquivos versionados e `git`, nada reexecutado. Como todos os testes foram executados por agente, esta conferência também foi feita por agente, de forma cética. Esta pré-conferência não altera `dados/registro.csv`.

Resumo: Lang-37, Closure-37, Time-20 e Math-9 passaram em C1-C8. Chart-18 tem divergência em C5, porque o checklist de falso positivo não existe.

## Lang-37 (ordem 1) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | `ambiente-Guilherme-Fadel.md`, coluna do teste 1, itens A1-A10 e D1-D5 em `ok`. D4 por evidência indireta (decisão do usuário). |
| C2 | ok | `manifesto.txt`: imagem `sha256:45031972...`, cpus_limite 2, memoria_limite 6g, memoria_cgroup 6442450944, Java 1.8.0_452, Defects4J a83e479, `evosuite_config_sha256` = 7349236d...; semente 2053419074 = `atribuicao.csv`. `suites/logs/Lang.37f.log` mostra `-b 360 -s 2053419074`. |
| C3 | ok | Ordem 1; manifesto 06:35 -08:00 (11:35 -03), commit 22d958b às 11:42 -03. Primeira da sequência. |
| C4 | ok | `bug_detection`: Fail, num_trigger 1, igual ao registro (Fail, 1, deteccao_automatica 1). `coverage`: 957/954 linhas e 806/804 ramos, 99,69%, igual ao registro. `cobertura_falha.txt` = parcial (5 de 7), igual ao registro. `tempos.csv`: 212+40+26+18+0 = 296 s, igual a `tempo_total_s`. Todas as etapas com código 0. |
| C5 | ok (concordo) | `falso-positivo-Lang-37.md` completo (F1-F5 = Sim). Trigger log: `ArrayStoreException` em `ArrayUtils.addAll(ArrayUtils.java:2962)` (test331), método alterado no patch. `37f.1.trigger.log` vazio. test331 não está entre os removidos (só test345). Sem fator de ambiente (arrays em memória). Concordo com falso_positivo = nao. O campo "Conferente" do arquivo está em branco; é preciso preencher. |
| C6 | n/a | Detectou. |
| C7 | n/a | `cobertura_falha` = parcial, determinada pelo script. |
| C8 | ok | `git log -p resultados/Lang-37` tem um único commit (22d958b). Sem edição posterior. |

Observação: `testes_finais` = 365 > 364 gerados − 1 removido. É artefato do contador (stub de test345 com `@Test`), explicado em `observacoes`. Concordo com manter os valores gerados.

## Closure-37 (ordem 2) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 2 toda em `ok`; D3 720 = 360×2 classes; D4 indireta. |
| C2 | ok | Manifesto com os mesmos hashes e recursos; semente 1564608330 = `atribuicao.csv`; `Closure.37f.log` com `-b 720 -s 1564608330`; `classes_modificadas` com 2 classes, coerente com o orçamento. |
| C3 | ok | Ordem 2; manifesto 07:17 -08:00 (12:17 -03), commit 71cec15 às 12:29 -03, depois de 22d958b. |
| C4 | ok | `bug_detection`: Fail, num_trigger 1. `coverage`: 749/434 linhas, 387/172 ramos, 57,94%, igual ao registro. `cobertura_falha.txt` = parcial (3 de 4). `tempos.csv`: 402+81+48+32 = 563 s, igual ao registro. Todas as etapas com código 0. |
| C5 | ok (concordo) | `falso-positivo-Closure-37.md` completo. Trigger: `AssertionFailedError: Expecting exception: IllegalStateException` em `IRFactory_ESTest::test33`; o teste exercita `IRFactory.transformTree`, alterada no patch (a remoção de checagem torna a falha coerente com a versão defeituosa). `37f.1.trigger.log` vazio. test33 não está entre os 4 removidos (todos de `NodeTraversal_ESTest`). Teste determinístico, sem infraestrutura. Concordo com falso_positivo = nao. Ressalva já feita pelo executor: a asserção é fraca (só o tipo da exceção), mas coerente. O campo "Conferente" do arquivo está em branco. |
| C6 | n/a | Detectou. |
| C7 | n/a | `cobertura_falha` = parcial, pelo script. |
| C8 | ok | Um único commit (71cec15) em `resultados/Closure-37`. |

Observação: `testes_finais` 77 > 73 − 4: mesmo artefato do contador, explicado em `observacoes`. Os 4 removidos são de `NodeTraversal_ESTest`, falharam na corrigida (4 testes, não é remoção em massa por infraestrutura).

## Time-20 (ordem 3) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 3 toda em `ok`; D3 360 = 360×1 classe; D4 indireta. |
| C2 | ok | Manifesto com os mesmos hashes e recursos; semente 1509347447 = `atribuicao.csv`; `Time.20f.log` com `-b 360 -s 1509347447`. |
| C3 | ok | Ordem 3; manifesto 09:18 -08:00 (14:18 -03), commit 1b5e725 às 14:25 -03, depois de 71cec15. |
| C4 | ok | `bug_detection`: Pass, num_trigger 0; registro Pass, 0, deteccao_automatica 0. `coverage`: 1034/968 linhas, 595/548 ramos, 93,62%. `cobertura_falha.txt` = total (6 de 6), igual ao registro. `tempos.csv`: 226+81+39+28 = 374 s. |
| C5 | n/a | Não detectou (`falso_positivo = nao_se_aplica`, `deteccao_confirmada = 0`). |
| C6 | ok | `bug_detection` = Pass; `20b.1.trigger.log` e `20f.1.trigger.log` vazios. Um único teste removido, `DateTimeFormatterBuilder_ESTest::test121` (`expected:<3> but was:<2>`), por falhar na versão corrigida; sem erro de compilação (0 não compiláveis), sem remoção em massa por infraestrutura. |
| C7 | n/a | `cobertura_falha` = total, pelo script. |
| C8 | ok | Um único commit (1b5e725). |

Observação: `observacoes` está vazio, mas `testes_finais` 192 > 191 − 1 mostra o mesmo artefato do contador dos testes 1 e 2. Sugere-se anotar isso em `observacoes` (não bloqueia a conferência). A causa do `expected:<3> but was:<2>` em test121 não foi investigada (o log não permite ver); não afeta o resultado.

## Chart-18 (ordem 4) — resultado sugerido: divergente:C5

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 4 toda em `ok`; D3 720 = 360×2 classes; D4 indireta. |
| C2 | ok | Manifesto com os mesmos hashes e recursos; semente 1318002706 = `atribuicao.csv`; `Chart.18f.log` com `-b 720 -s 1318002706`. |
| C3 | ok | Ordem 4; manifesto 10:11 -08:00 (15:11 -03), commit b5a4a6f às 15:20 -03, depois de 1b5e725. |
| C4 | ok | `bug_detection`: Fail, num_trigger 4; o `18b.1.trigger.log` lista 4 testes (`DefaultKeyedValues2D_ESTest::test20`, `test21`, `DefaultKeyedValues_ESTest::test15`, `test01`), igual ao registro (Fail, 4, deteccao_automatica 1). `coverage`: 268/261 linhas, 126/122 ramos, 97,39%. `cobertura_falha.txt` = total (10 de 10). `tempos.csv`: 382+38+43+22 = 485 s. |
| C5 | DIVERGENTE | Houve detecção (deteccao_automatica = 1), mas não existe `docs/registros/falso-positivo-Chart-18.md` (não está na árvore, nem no commit b5a4a6f nem em outro). O registro mantém `falso_positivo = pendente` e `deteccao_confirmada = pendente`, e `observacoes` diz "deteccao automatica = 1 pendente de conferencia". Não há análise de F1-F5 para eu concordar ou discordar. Evidência preliminar do conferente (não substitui o checklist): 3 dos 4 reveladores falham com `Expecting exception: IllegalArgumentException` e `test01` com `expected:<0> but was:<1>`; `18f.1.trigger.log` vazio e `fix_test_suite` sem testes removidos (0 falhando). Seria preciso o executor preencher o checklist (incluindo a leitura do patch `18.src.patch`) antes da confirmação. |
| C6 | n/a | Detectou. |
| C7 | n/a | `cobertura_falha` = total, pelo script. |
| C8 | ok | Um único commit (b5a4a6f). |

Pendência para o executor: criar `docs/registros/falso-positivo-Chart-18.md` (modelo da seção 3 do checklist, 4 reveladores, amostra de até 3) e só então definir `falso_positivo` e `deteccao_confirmada`.

## Math-9 (ordem 5) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 5 toda em `ok`; D3 360 = 360×1 classe; D4 indireta. |
| C2 | ok | Manifesto com os mesmos hashes e recursos; semente 1796075699 = `atribuicao.csv`; `Math.9f.log` com `-b 360 -s 1796075699`. |
| C3 | ok | Ordem 5; manifesto 11:06 -08:00 (16:06 -03), commit 680800f às 16:08 -03, depois de b5a4a6f. |
| C4 | ok | `bug_detection`: Pass, num_trigger 0. `coverage`: 47/46 linhas, 16/16 ramos, 97,87%. `cobertura_falha.txt` = total (2 de 2). `tempos.csv`: 20+34+31+20 = 105 s. |
| C5 | n/a | Não detectou (`nao_se_aplica`, `deteccao_confirmada = 0`). |
| C6 | ok | Pass, os dois trigger logs vazios, `fix_test_suite.summary.log` com 0 não compiláveis e 0 falhando (nada removido). 14 testes gerados e 14 finais. |
| C7 | n/a | `cobertura_falha` = total, pelo script. |
| C8 | ok | Um único commit (680800f). |

## Resultado sugerido para a coluna `conferencia`

| Falha | Sugestão |
|---|---|
| Lang-37 | `ok:Guilherme Celente` |
| Closure-37 | `ok:Guilherme Celente` |
| Time-20 | `ok:Guilherme Celente` |
| Chart-18 | `divergente:Guilherme Celente:C5` |
| Math-9 | `ok:Guilherme Celente` |

Todas as sugestões dependem de validação humana. Comentário geral: o parâmetro de cgroup/CPU (`nproc_visto` = 10) é esperado conforme a decisão do usuário e não foi tratado como divergência.
