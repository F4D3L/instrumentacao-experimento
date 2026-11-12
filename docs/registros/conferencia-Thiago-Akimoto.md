# Conferência cruzada: testes de Thiago Akimoto

Conferente designado: Lucas Reali — pré-conferência feita por agente de IA, pendente de validação humana

Data: 12/11/2026. Método: só arquivos versionados e `git`; nada foi reexecutado (o contêiner foi usado apenas para ler os patches `.src.patch` de C5/C7 e a suíte gerada foi descompactada fora do repositório para contar `@Test`). Como todos os testes foram executados por agente, esta conferência também foi feita por agente, de forma cética. Esta pré-conferência não altera `dados/registro.csv`.

Resumo: Lang-12, Time-13, Math-65 e Closure-108 passaram em C1-C8. Chart-17 tem divergência em C1: no checklist do ambiente, os itens A2 (ID da imagem) e A5 (repositório limpo e atualizado) da coluna do teste 3 estão em branco. O restante de Chart-17 confere (o manifesto mostra a imagem correta, então a divergência é de preenchimento, não de ambiente).

Observações gerais:
- Fuso: os manifestos estão em -08:00 e os commits em -03:00; os horários do checklist estão em -03:00. Ao converter, tudo é coerente.
- O campo "Conferente" dos arquivos `falso-positivo-*.md` está em branco; deve ser preenchido pelo conferente humano.
- `dados/registro.csv` está com `deteccao_confirmada = pendente` e `conferencia = pendente` nos três testes que detectaram, o que é esperado nesta etapa.

## Lang-12 (ordem 1) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | `ambiente-Thiago-Akimoto.md`, coluna do teste 1: A1-A10 e D1-D5 em `ok`; D4 por evidência indireta (decisão do usuário); nproc=10 explicado por cota de cgroup. |
| C2 | ok | Manifesto: imagem `sha256:45031972...` (igual aos demais), cpus_limite 2, memoria_limite 6g, memoria_cgroup 6442450944, Java 1.8.0_452, Defects4J a83e479, `evosuite_config_sha256` = 7349236d..., orçamento 360 (1 classe). Semente 728680798 = `atribuicao.csv`; `suites/logs/Lang.12f.log` com `-b 360 -s 728680798`. |
| C3 | ok | Ordem 1. Manifesto 07:07 -08:00 (12:07 -03); commit 532af0b às 12:11 -03; primeiro da sequência. |
| C4 | ok | `bug_detection`: Fail, num_trigger 1 = registro (Fail, 1, 1). `coverage`: 55/55 linhas e 54/54 ramos = registro (100,00%). `cobertura_falha.txt` = total = registro. `tempos.csv`: 69+25+23+17+0 = 134 s = `tempo_total_s`; todos os códigos 0. 20 `@Test` na suíte = `testes_gerados` 20. |
| C5 | ok (concordo) | `falso-positivo-Lang-12.md` completo (F1-F5 = Sim). Patch lido: remove da defeituosa a validação `chars.length == 0 -> IllegalArgumentException` e o tratamento `end = chars.length`. Trigger log: `ArrayIndexOutOfBoundsException: 0` em `RandomStringUtils.random(...:248)` no test09 (único revelador), que espera `IllegalArgumentException`. Corrigida passa (`12f.1.trigger.log` com 0 bytes). Entrada fixa, sem data/hora, locale, rede ou HashMap. Concordo com falso_positivo = nao. |
| C6 | n/a | Detectou. |
| C7 | n/a | `cobertura_falha` = total, determinada pelo script. Conferido mesmo assim: linhas 230, 231, 235, 236 são as linhas `-` executáveis do patch, e 247 é a próxima linha executável depois do `}` removido (regra 3); todas com hits > 0 no `12f.1.xml`. |
| C8 | ok | `git log -p resultados/Lang-12`: um único commit (532af0b), só adições; sem edição posterior. |

## Time-13 (ordem 2) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 2: todos os itens `ok`; D3 360 = 360 × 1 classe; D4 indireta. |
| C2 | ok | Mesmos hashes e recursos; semente 1784624022 = `atribuicao.csv`; `Time.13f.log` com `-b 360 -s 1784624022`; `classes_modificadas` = `PeriodFormatterBuilder` (1 classe). |
| C3 | ok | Ordem 2. Manifesto 09:03 -08:00 (14:03 -03), commit 9f797d9 às 14:09 -03, depois de 532af0b e do manifesto da ordem 1. |
| C4 | ok | Fail, num_trigger 1 = registro. 665/651 linhas (97,89%) e 458/448 ramos = registro. `cobertura_falha` = total = registro. Tempos: 202+46+31+23+0 = 302 s = registro. 126 `@Test` = `testes_gerados` 126; summary sem removidos (testes_finais 126). |
| C5 | ok (concordo) | `falso-positivo-Time-13.md` completo. Patch lido (corrigida -> defeituosa): a defeituosa perde o `buf.insert(bufLen, '-')` para `-1000 < valueLong < 0` em `FieldFormatter.printTo`. Trigger log: `AssertionFailedError: expected:<[-]0.024> but was:<[]0.024>` no test074 (único revelador), exatamente o efeito do patch. Corrigida passa (`13f.1.trigger.log` vazio). Ressalvas do executor (trace só mostra o frame do teste; locale não reexecutado) são honestas; o valor `-24 ms` e o formatador numérico sem locale tornam a dependência de ambiente improvável. Concordo com falso_positivo = nao. |
| C6 | n/a | Detectou. |
| C7 | n/a | `cobertura_falha` = total pelo script. Conferido: linhas 1098, 1133, 1143, 1144 = linhas `-` executáveis dos 3 trechos do patch. |
| C8 | ok | Um único commit (9f797d9) em `resultados/Time-13`, só adições. |

## Chart-17 (ordem 3) — resultado sugerido: divergente:C1

| # | Resultado | Evidência |
|---|---|---|
| C1 | **problema** | Na coluna do teste 3 de `ambiente-Thiago-Akimoto.md`, **A2 (ID da imagem) e A5 (repositório limpo e atualizado) estão em branco** (outros itens preenchidos). Os demais itens estão `ok` e D1-D5 conferem. O manifesto mostra a imagem correta (`45031972...`), então não há indício de problema real de ambiente; falta o executor preencher A2 e A5 (com a ressalva de que esse preenchimento seria posterior ao teste) ou o grupo aceitar a exceção justificada. |
| C2 | ok | Mesmos hashes e recursos; semente 83094516 = `atribuicao.csv`; `Chart.17f.log` com `-b 360 -s 83094516`; `classes_modificadas` = `TimeSeries` (1 classe). |
| C3 | ok | Ordem 3. Manifesto 09:56 -08:00 (14:56 -03), commit 5e57fcf às 15:04 -03, depois de 9f797d9. |
| C4 | ok | Fail, num_trigger 1 = registro. 280/267 linhas (95,36%) e 138/135 ramos = registro. `cobertura_falha` = total = registro. Tempos: 210+73+45+32+1 = 361 s = registro. 57 `@Test` = `testes_gerados` 57; summary sem removidos. |
| C5 | ok (concordo) | `falso-positivo-Chart-17.md` completo. Patch lido: a corrigida faz `super.clone()` + `deepClone`; a defeituosa usa `createCopy(0, getItemCount() - 1)`. Trigger log: `Requires start <= end.` em `createCopy(TimeSeries.java:880)` chamado por `clone(:857)` no test50 (único revelador), com série vazia (`createCopy(0, -1)`). Corrigida passa (`17f.1.trigger.log` vazio). Determinístico (relógio mockado, sem locale/rede). Concordo com falso_positivo = nao. |
| C6 | n/a | Detectou. |
| C7 | n/a | `cobertura_falha` = total pelo script. Conferido: linhas 857 e 858 = as duas linhas `-` do patch; hits 3 e 3. |
| C8 | ok | Um único commit (5e57fcf) em `resultados/Chart-17`, só adições. |

## Math-65 (ordem 4) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 4: todos os itens `ok`; A6 inclui JVM availableProcessors=2; D3 360 = 360 × 1 classe; D4 indireta. |
| C2 | ok | Mesmos hashes e recursos; semente 1098537342 = `atribuicao.csv`; `Math.65f.log` com `-b 360 -s 1098537342`; `classes_modificadas` = `AbstractLeastSquaresOptimizer` (1 classe). |
| C3 | ok | Ordem 4. Manifesto 10:51 -08:00 (15:51 -03; checklist diz 15:50), commit 713e954 às 15:56 -03, depois de 5e57fcf. |
| C4 | ok | `bug_detection`: Pass, num_trigger 0 = registro (Pass, 0, 0). 87/61 linhas (70,11%) e 28/14 ramos = registro. `cobertura_falha` = parcial = registro. Tempos: 195+39+30+22+0 = 286 s = registro. 14 `@Test` = `testes_gerados` 14; summary sem removidos. |
| C5 | n/a | Não detectou; não há checklist de falso positivo (e o registro tem `nao_se_aplica`). |
| C6 | ok | `bug_detection` = Pass (não Broken); `65b.1.trigger.log` e `65f.1.trigger.log` vazios; `run_bug_detection.pl.log` sem "failing tests". `fix_test_suite.summary.log`: 0 classes e 0 testes não compiláveis, 0 testes falhando; `run.log` e `compile.log` com 0 bytes. Nenhuma remoção em massa. |
| C7 | n/a (conferido) | `cobertura_falha` = parcial, determinada pelo script, sem `indeterminado`. Verificação independente: o patch tem 2 trechos com linhas `-` (`return Math.sqrt(getChiSquare() / rows);` e `chiSquare += residual * residual * residualsWeights[i];`), que são as linhas 240 e 253 da corrigida. No `65f.1.xml`: linha 240 hits 26, linha 253 hits 0 (linha 252 hits 1). Resultado parcial (1 de 2) correto pela regra 4 da seção 5.2. |
| C8 | ok | Um único commit (713e954) em `resultados/Math-65`, só adições. |

## Closure-108 (ordem 5) — resultado sugerido: ok

| # | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna do teste 5: todos os itens `ok`. A5 menciona "git pull não executado nesta rodada" (execução centralizada, repositório local sem upstream), aceitável e coerente com os demais testes. |
| C2 | ok | Mesmos hashes e recursos; semente 682286618 = `atribuicao.csv`; `Closure.108f.log` com `-b 360 -s 682286618`; `classes_modificadas` = `ScopedAliases` (1 classe). |
| C3 | ok | Ordem 5. Manifesto 11:31 -08:00 (16:31 -03), commit cfa3e54 às 16:37 -03, depois de 713e954; é o último da sequência. |
| C4 | ok | Pass, num_trigger 0 = registro. 248/52 linhas (20,97%) e 152/22 ramos = registro. `cobertura_falha` = parcial = registro. Tempos: 207+52+42+28+0 = 329 s = registro. 4 `@Test` = `testes_gerados` 4; summary sem removidos. |
| C5 | n/a | Não detectou. |
| C6 | ok | `bug_detection` = Pass; trigger logs vazios; summary com 0 não compiláveis e 0 falhando; `run.log`/`compile.log` com 0 bytes. Nenhuma remoção em massa. A suíte é pequena (4 testes, cobertura 20,97%), mas isso é resultado da geração (log do gen_tests sem erro), não de infraestrutura. |
| C7 | n/a (conferido) | `cobertura_falha` = parcial pelo script. Verificação independente: o patch tem 4 trechos com linhas `-` (declaração `injectedDecls` 259; `injectedDecls.clear()` 317; `injectedDecls.add(...)` 434; `!injectedDecls.contains(n)` 584). No `108f.1.xml`: 259 hits 4; 317, 434 e 584 hits 0. Parcial (1 de 4), correto. |
| C8 | ok | Um único commit (cfa3e54) em `resultados/Closure-108`, só adições. |

## Notas para o conferente humano

- Para Chart-17, pedir ao executor o preenchimento de A2 e A5 (ou registrar a exceção justificada) antes de marcar `ok`.
- Preencher o campo "Conferente" e "Concorda?" nos três arquivos de falso positivo (Lang-12, Time-13, Chart-17) se concordar com a análise acima.
- Sugestão de coluna `conferencia`: `ok:Lucas Reali` para Lang-12, Time-13, Math-65 e Closure-108; `divergente:Lucas Reali:C1` para Chart-17 até a correção do checklist.
