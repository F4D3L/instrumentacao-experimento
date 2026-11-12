# Conferência cruzada: testes de Leonardo Ceccon

Conferente designado: Gabriel Moribe — pré-conferência feita por agente de IA, pendente de validação humana

Data: 12/11/2026. Método: só arquivos versionados e `git`, nada reexecutado (o docker foi usado só para ler os patches `.src.patch`). Como todos os testes foram executados por agente, esta conferência também foi feita por agente, de forma cética. Esta pré-conferência não altera `dados/registro.csv`.

Resumo: Closure-38 e Chart-11 passaram em C1-C8. Lang-46, Time-22 e Math-52 têm divergência em C1: na versão atual de `ambiente-Leonardo-Ceccon.md` a linha D1–D5 está em branco nas colunas dos testes 1, 2 e 3. As células estavam preenchidas nos commits de cada teste (de6d728, 631a608, 0ff6c4a) e foram apagadas no commit ec039a7 (Closure-38), que regravou a linha só com o teste 4. Isso é regressão do arquivo, não falha do teste; basta restaurar o texto das células. Os demais itens (C2-C8) passam nos três.

Observação geral: `nproc_visto` = 10 é esperado (decisão do usuário) e não foi tratado como divergência. D4 do checklist é por evidência indireta (decisão do usuário): em todos os testes `suites/logs/<P>.<id>f.log` mostra `-b 360` e `-s <semente de atribuicao.csv>`, e `evosuite_config_sha256` = 7349236d...

## Lang-46 (ordem 1) — resultado sugerido: divergente:C1

| # | Resultado | Evidência |
|---|---|---|
| C1 | **problema** | Colunas do teste 1 em A1-A10 preenchidas e `ok`. Mas a célula D1–D5 do teste 1 está em branco no arquivo atual (estava preenchida em de6d728: D2 semente 1936996271, D3 360 = 360×1, D4 indireta, D5 códigos 0). Precisa ser restaurada. |
| C2 | ok | Imagem `sha256:45031972...` (igual ao registro), cpus_limite 2, memoria_limite 6g, memoria_cgroup 6442450944, Defects4J a83e479, evosuite_sha256 939c0c76..., config 7349236d...; semente 1936996271 = `atribuicao.csv`. `Lang.46f.log`: `-b 360 -s 1936996271`; `classes_modificadas` com 1 classe. |
| C3 | ok | Ordem 1; manifesto 06:50 -08:00 (11:50 -03), commit de6d728 às 11:55 -03; primeira da sequência. |
| C4 | ok | `bug_detection`: Fail, num_trigger 1 = registro (Fail, 1, deteccao 1). `coverage`: 222/169 linhas, 109/93 ramos, 76,13% = registro. `cobertura_falha.txt` = total (9 de 9) = registro. `tempos.csv`: 197+27+23+16+0 = 263 s = `tempo_total_s`. Todas as etapas com código 0. 47 `@Test` na suíte = testes_gerados 47, finais 47. |
| C5 | ok (concordo) | `falso-positivo-Lang-46.md` completo (F1-F5 = Sim). Conferi de forma independente: o trigger log tem só `StringEscapeUtils_ESTest::test06` (`expected:<h.[]/&...> but was:<h.[\]/&...>`); na suíte, `test06` chama `escapeJava("h./&\"re\f x!T(B#J")` e espera `/` sem barra. O `46.src.patch` (corrigida -> defeituosa) mostra que na corrigida `escapeJava` passa `escapeForwardSlash=false` e o `case '/'` só escreve `\` sob `if (escapeForwardSlash)`; na defeituosa o `\` é sempre escrito. Valor esperado = corrigida, obtido = defeituosa. Teste determinístico (string literal), sem data/locale/hash/arquivos. `fix_test_suite.summary.log`: 0 não compiláveis e 0 falhando; `46f.1.trigger.log` com 0 bytes. Falha é de valor, não de infraestrutura. Concordo com falso_positivo = nao. O campo "Conferente" do arquivo está em branco; é preciso preencher. |
| C6 | n/a | Detectou. |
| C7 | n/a | `cobertura_falha` = total, pelo script. Por sanidade: as linhas-alvo (`-` do patch, mapeando não executáveis para a próxima executável: 86, 102, 127, 143, 155, 160, 180, 245, 248) batem com as 9 linhas do arquivo e todas têm hits > 0 no `46f.1.xml`. |
| C8 | ok | `git log -p resultados/Lang-46`: um único commit (de6d728). |

## Time-22 (ordem 2) — resultado sugerido: divergente:C1

| # | Resultado | Evidência |
|---|---|---|
| C1 | **problema** | A1-A10 do teste 2 em `ok`. Célula D1–D5 do teste 2 em branco no arquivo atual (estava preenchida em 631a608 e 0ff6c4a, apagada em ec039a7). |
| C2 | ok | Manifesto com os mesmos hashes e recursos; semente 1945184215 = `atribuicao.csv`; `Time.22f.log`: `-b 360 -s 1945184215`. |
| C3 | ok | Ordem 2; manifesto 08:36 -08:00 (13:36 -03), commit 631a608 às 13:42 -03, depois de de6d728. |
| C4 | ok | `bug_detection`: Pass, num_trigger 0 = registro (Pass, 0, deteccao 0). `coverage`: 174/172 linhas, 58/57 ramos, 98,85% = registro. `cobertura_falha.txt` = total (6 de 6) = registro. `tempos.csv`: 198+39+30+21+0 = 288 s. Etapas com código 0. 35 `@Test` = gerados 35, finais 35. |
| C5 | n/a | Não detectou (`nao_se_aplica`, `deteccao_confirmada = 0`). |
| C6 | ok | Pass; `22b.1.trigger.log` e `22f.1.trigger.log` com 0 bytes; `fix_test_suite.summary.log` com 0 não compiláveis e 0 falhando; `fix_test_suite.run.log` e `.compile.log` vazios. Nada removido, sem remoção em massa. |
| C7 | n/a | `cobertura_falha` = total, pelo script. Sanidade: o patch remove 222 e 224-228 (construtor `BasePeriod(long)`), exatamente as 6 linhas consideradas, todas com hits 1. |
| C8 | ok | Um único commit (631a608) em `resultados/Time-22`. |

## Math-52 (ordem 3) — resultado sugerido: divergente:C1

| # | Resultado | Evidência |
|---|---|---|
| C1 | **problema** | A1-A10 do teste 3 em `ok`. Célula D1–D5 do teste 3 em branco no arquivo atual (estava preenchida em 0ff6c4a, apagada em ec039a7). |
| C2 | ok | Manifesto com os mesmos hashes e recursos; semente 775229953 = `atribuicao.csv`; `Math.52f.log`: `-b 360 -s 775229953`. |
| C3 | ok | Ordem 3; manifesto 09:33 -08:00 (14:33 -03), commit 0ff6c4a às 14:40 -03, depois de 631a608. |
| C4 | ok | `bug_detection`: Pass, 0 = registro. `coverage`: 327/326 linhas, 122/121 ramos, 99,69% = registro. `cobertura_falha.txt` = total (4 de 4) = registro. `tempos.csv`: 213+74+45+28+0 = 360 s. Etapas com código 0. 64 `@Test` = gerados 64, finais 64. |
| C5 | n/a | Não detectou. |
| C6 | ok | Pass; trigger logs vazios; `fix_test_suite.summary.log` com 0 não compiláveis e 0 falhando; logs de run/compile vazios. |
| C7 | n/a | `cobertura_falha` = total, pelo script. Sanidade: o patch tem `-` nas linhas 344-345, 354 e 360 (as 4 consideradas), todas com hits > 0. |
| C8 | ok | Um único commit (0ff6c4a) em `resultados/Math-52`. |

## Closure-38 (ordem 4) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 4 toda preenchida e em `ok`, inclusive D1–D5 (D4 indireta). |
| C2 | ok | Manifesto com os mesmos hashes e recursos; semente 1667632258 = `atribuicao.csv`; `Closure.38f.log`: `-b 360 -s 1667632258`; 1 classe modificada (`CodeConsumer`). |
| C3 | ok | Ordem 4; manifesto 10:28 -08:00 (15:28 -03), commit ec039a7 às 15:34 -03, depois de 0ff6c4a. |
| C4 | ok | `bug_detection`: Pass, 0 = registro. `coverage`: 109/2 linhas, 66/9 ramos, 1,83% = registro. `cobertura_falha.txt` = nenhuma (0 de 1) = registro. `tempos.csv`: 201+49+44+30+0 = 324 s. Etapas com código 0. 6 `@Test` = gerados 6, finais 6. |
| C5 | n/a | Não detectou. |
| C6 | ok | Pass; trigger logs vazios; `fix_test_suite.summary.log` com 0 não compiláveis e 0 falhando; run/compile vazios. Cobertura muito baixa, mas explicável: os 6 testes só chamam métodos estáticos (`isNegativeZero`, `isWordChar`) da classe abstrata `CodeConsumer`; a geração terminou em ~201 s sem erro (`gerar.log` termina em "Moving test suite archive ... OK"). Não há indício de falha de infraestrutura; é limitação do EvoSuite, e vale como está. |
| C7 | n/a | `cobertura_falha` = nenhuma, pelo script. Verificado: o patch tem um único `-` (`if ((x < 0 \|\| negativeZero) && prev == '-')`, linha 245), executável, com hits="0" no `38f.1.xml`; pela regra 4 da seção 5.2 é "nenhuma". |
| C8 | ok | Um único commit (ec039a7) em `resultados/Closure-38`. |

## Chart-11 (ordem 5) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 5 toda preenchida e em `ok` (D4 indireta). |
| C2 | ok | Manifesto com os mesmos hashes e recursos; semente 685850782 = `atribuicao.csv`; `Chart.11f.log`: `-b 360 -s 685850782`. |
| C3 | ok | Ordem 5; manifesto 11:14 -08:00 (16:14 -03), commit 3d7247c às 16:18 -03, depois de ec039a7. |
| C4 | ok | `bug_detection`: Fail, num_trigger 4 = registro (Fail, 4, deteccao 1). `coverage`: 193/185 linhas, 116/116 ramos, 95,85% = registro. `cobertura_falha.txt` = total (1 de 1, linha 275, hits 6) = registro. `tempos.csv`: 54+30+26+18+0 = 128 s. Etapas com código 0. 66 `@Test` = gerados 66, finais 66. |
| C5 | ok (concordo) | `falso-positivo-Chart-11.md` completo (F1-F5 = Sim, amostra de 3 dos 4). Conferi de forma independente: o trigger log lista test44-47, todos `AssertionFailedError` em `assertFalse` (linhas 1470, 1663, 1699, 1826). No `11.src.patch`, o `-` é `p2.getPathIterator(null)` (corrigida) e o `+` é `p1.getPathIterator(null)` (defeituosa), em `ShapeUtilities.equal(GeneralPath, GeneralPath)`. Nos testes, `ShapeUtilities.equal` é chamado com dois `GeneralPath` diferentes (por exemplo test44: `new GeneralPath()` vs `createDiagonalCross(0.0F,0.0F)`) e se espera `false`; na defeituosa o caminho é comparado consigo mesmo e retorna `true`, o que explica a falha. Sem aleatoriedade/data/arquivos. `fix_test_suite.summary.log`: 0 removidos; `11f.1.trigger.log` vazio. Falha é de valor, não de infraestrutura. Concordo com falso_positivo = nao. Pequena imprecisão no registro: em test44 a chamada é `equal(generalPath1, generalPath0)` (não `(generalPath0, generalPath1)`), sem efeito na conclusão. O campo "Conferente" do arquivo está em branco; é preciso preencher. |
| C6 | n/a | Detectou. |
| C7 | n/a | `cobertura_falha` = total, pelo script (linha 275 é o `-` do patch, executável, hits 6). |
| C8 | ok | Um único commit (3d7247c) em `resultados/Chart-11`. Nota: esse commit reescreveu `dados/registro.csv` inteiro por mudança de fim de linha (de CRLF para LF); o conteúdo diff ignorando `\r` é só a linha nova do Chart-11. Não afeta os logs. |

## Resultado sugerido para a coluna `conferencia`

| Falha | Sugestão |
|---|---|
| Lang-46 | `divergente:Gabriel Moribe:C1` |
| Time-22 | `divergente:Gabriel Moribe:C1` |
| Math-52 | `divergente:Gabriel Moribe:C1` |
| Closure-38 | `ok:Gabriel Moribe` |
| Chart-11 | `ok:Gabriel Moribe` |

Ação para o executor: restaurar as células D1–D5 dos testes 1, 2 e 3 em `docs/registros/ambiente-Leonardo-Ceccon.md` (o texto original está nos commits de6d728, 631a608 e 0ff6c4a) e preencher o campo "Conferente" nos registros de falso positivo de Lang-46 e Chart-11. Todas as sugestões dependem de validação humana.
