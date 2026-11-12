# Conferência cruzada: testes de Guilherme Celente

Conferente designado: Leonardo Ceccon — pré-conferência feita por agente de IA, pendente de validação humana

- Data da pré-conferência: 12/11/2026
- Roteiro: `docs/roteiro-conferencia.md` (C1 a C8). Só arquivos versionados e `git`; nada foi reexecutado. O único uso do contêiner foi ler os patches do Defects4J (`cat` de `*.src.patch`) para C5/C7.
- Executor dos 5 testes: agente de IA (execução centralizada), portanto esta conferência também é de agente, sem independência humana. Sugestão: o conferente humano repetir, no mínimo, a leitura dos itens marcados com **divergente**.
- Resumo: Lang-50, Math-80, Chart-26 e Time-5 sem divergência. **Closure-42 divergente em C5** (checklist de falso positivo ausente).

| Teste | Ordem | Resultado sugerido para a coluna `conferencia` |
|---|---|---|
| Lang-50 | 1 | `ok:Leonardo Ceccon` |
| Math-80 (substituta de Math-101) | 2 | `ok:Leonardo Ceccon` |
| Closure-42 | 3 | `divergente:Leonardo Ceccon:C5` |
| Chart-26 | 4 | `ok:Leonardo Ceccon` |
| Time-5 | 5 | `ok:Leonardo Ceccon` |

Verificações gerais feitas uma vez:

- Sementes de `dados/sorteio/atribuicao.csv`: Lang-50 = 1768226709, Math-101 (herdada por Math-80) = 29410720, Closure-42 = 89868774, Chart-26 = 807160701, Time-5 = 1792588423. Todas iguais às dos manifestos e aos `-s` de `resultados/<Falha>/suites/logs/<P>.<id>f.log`.
- Valores de referência (manifestos dos 5 testes e do Math-101 idênticos entre si): imagem `sha256:45031972...499d446e` (igual ao ID de referência em `docs/03-semana3-instrumentacao.md`), Java 1.8.0_452, Defects4J `a83e4792...`, EvoSuite SHA `939c0c76...`, `evosuite_config_sha256` = `7349236d...` (igual ao `shasum -a 256 ambiente/evosuite.config` atual), TZ America/Los_Angeles, `cpus_limite=2`, `memoria_limite=6g`, `memoria_cgroup=6442450944`. `nproc_visto=10` é esperado (decisão do usuário).
- D4 por evidência indireta (decisão do usuário): `-b 360` com 1 classe modificada e `-s <semente>` em todos os `suites/logs/<P>.<id>f.log`, mais o SHA da configuração acima. Os `gerar.log` só têm mensagens `ERROR TestCluster - Failed to check cache ...` do EvoSuite (ruído conhecido, não é falha de infraestrutura).
- Contagem independente de `@Test` nas suítes (`*.tar.bz2` extraídas em pasta temporária): Lang-50 = 71, Math-80 = 41, Closure-42 = 46, Chart-26 = 59, Time-5 = 75, iguais a `testes_gerados` e `testes_finais` do registro (nenhum teste removido: `fix_test_suite.summary.log` com 0 e `compile.log`/`run.log` vazios nos cinco).
- `tempo_total_s` = soma dos `segundos` de `tempos.csv`: 268, 285, 359, 325 e 207, iguais ao registro. Todas as etapas com código 0 (coluna `etapas_com_erro` vazia).
- Ordem cronológica (manifestos em America/Los_Angeles; commits em UTC-3, diferença de 5 h entre os dois fusos neste dia): Lang-50 06:43 (commit cb5dc3c, 11:49) → Math-101 07:30 (e2f41ac, 13:26) → Math-80 08:30 (02d068e, 13:35) → Closure-42 09:26 (c018115, 14:33) → Chart-26 10:21 (85a78ce, 15:27) → Time-5 11:09 (bf7ab2b, 16:14). Crescente em todos os pares.
- As datas/horas do `ambiente-Guilherme-Celente.md` (11:43, 12:30, 13:30, 14:26, 15:21, 16:09) correspondem aos manifestos convertidos para o horário de Brasília.

---

## Teste 1: Lang-50 (ordem 1)

| # | Verificação | Resultado | Evidência |
|---|---|---|---|
| C1 | Checklist do ambiente | ok | Coluna "Teste 1: Lang-50" com A1 a A10, D1 a D5, máquina e observações preenchidos, todos `ok`. Ressalva menor: A6 registra "cgroup 2 CPUs, 6 GiB" sem o valor literal de `cpu.max` nem a `availableProcessors` da JVM; o manifesto tem `cpus_limite=2` e `memoria_cgroup=6442450944`, então a evidência fecha. |
| C2 | Manifesto | ok | Imagem, versões, SHA-256, recursos e semente 1768226709 conforme as verificações gerais. `classes_modificadas` = `org.apache.commons.lang.time.FastDateFormat` (1 classe, `orcamento_total_s=360`). |
| C3 | Ordem | ok | Primeiro teste de Celente: manifesto 06:43 e commit cb5dc3c (11:49), anteriores a todos os demais dele. |
| C4 | Registro x saídas | ok | `bug_detection`: Pass, `num_trigger=0` → `resultado_d4j=Pass`, `testes_reveladores=0`, `deteccao_automatica=0`. `coverage`: 455/426 linhas e 228/186 ramos; 426/455 = 93,63% (confere). `cobertura_falha.txt` = total (8/8) → `cobertura_falha=total`. |
| C5 | Falso positivo | n/a | Não detectou (`deteccao_automatica=0`; `falso_positivo=nao_se_aplica`). |
| C6 | Não detectou com testes gerados | ok | `bug_detection` = Pass (não Broken). `fix_test_suite.summary.log`: 0 não compiláveis e 0 falhando; `compile.log` e `run.log` vazios (nenhuma remoção em massa). `5b.1.trigger.log` vazio. 71 testes finais. |
| C7 | Cobertura da falha indeterminada/manual | n/a | Classificada automaticamente como `total`. Conferi mesmo assim contra `Lang/50.src.patch`: trechos `-` nas linhas 285-286 e 289 (primeiro método) e 463-464 e 466 (segundo); os dois trechos só com `+` (bloco `if (locale == null)` dentro de `if (format == null)`) mapeiam, pelas regras 2 e 3, para 294 e 471 (primeira linha executável depois de `try {`). São 8 linhas, igual às 8 consideradas, todas com hits > 0 no `50f.1.xml`. |
| C8 | Logs não editados | ok | `git log --name-status -- resultados/Lang-50` mostra só o commit cb5dc3c (22 arquivos `A`, nenhuma modificação posterior). Nota: o commit 1c1c3f8 mexeu em `dados/registro.csv` (aspas na coluna `observacoes` de Lang-50 e Closure-37, documentado em `04-semana4-resultados.md`); não afeta logs nem valores. |

Resultado: **ok**.

---

## Teste 2: Math-80 (ordem 2; substituta de Math-101)

| # | Verificação | Resultado | Evidência |
|---|---|---|---|
| C1 | Checklist do ambiente | ok | Há duas colunas: "Teste 2: Math-101" e "Teste 2 (substituta): Math-80". A da substituta está completa e `ok`. A da original marca "NÃO OK" em D4/D5 (`gerar` falhou, código 1), o que é coerente com `tempos.csv` do Math-101 e foi tratado pela regra de substituição. Ressalva menor: A5 da Math-80 afirma "sem alterações em scripts/", mas o `scripts/executar_teste.sh` foi alterado de forma autorizada no commit 9a5c348 (antes da execução da Math-80), e o commit está no histórico; Lang-50 rodou com a versão anterior do script (a diferença só acrescenta a leitura de `substituicoes.csv`, sem tocar nas etapas do tratamento). |
| C2 | Manifesto | ok | Semente 29410720 = semente de Math-101 em `atribuicao.csv` = `substituicoes.csv`. `classes_modificadas` = `org.apache.commons.math.linear.EigenDecompositionImpl` (1 classe). Demais campos de referência iguais. |
| C3 | Ordem | ok | Manifesto 08:30, depois de Lang-50 (06:43) e Math-101 (07:30), antes de Closure-42 (09:26). Commits cb5dc3c < e2f41ac < 9a5c348 < 02d068e < c018115. |
| C4 | Registro x saídas | ok | `bug_detection`: Pass, 0 triggers → `Pass`/0/0. `coverage`: 839/748 linhas, 414/350 ramos; 748/839 = 89,15% (confere). `cobertura_falha.txt` = total (1/1). A coluna `observacoes` do registro está vazia; a linha não menciona que é substituta (a informação está em `substituicoes.csv`, `registro-substituidas.csv` e `04-semana4-resultados.md`). Sugestão, sem bloquear: anotar "substituta de Math-101" em `observacoes`. |
| C5 | Falso positivo | n/a | Não detectou. |
| C6 | Não detectou com testes gerados | ok | `bug_detection` = Pass; 0 removidos (`summary.log` com 0/0, `compile.log` e `run.log` vazios); `80b.1.trigger.log` vazio; 41 testes finais. |
| C7 | Cobertura da falha | n/a | Automática (`total`). Conferi contra `Math/80.src.patch`: única linha `-` é `int j = 4 * (n - 1);` na versão corrigida (`EigenDecompositionImpl.java:1135`), com hits=4 no `80f.1.xml`. Confere. |
| C8 | Logs não editados | ok | `git log -- resultados/Math-80` só tem 02d068e (22 `A`); `resultados/Math-101` só tem e2f41ac (5 `A`). |

Verificação da substituição Math-101 → Math-80:

- `dados/sorteio/substituicoes.csv` tem a linha Celente, ordem 2, Math-101 → Math-80, `posicao_reserva=8`, semente 29410720, conferente Leonardo Ceccon. Em `amostra.csv`, Math-80 é a posição 8 e a primeira reserva de Math (depois vêm Math-32 e Math-40), então a escolha segue a ordem da regra da seção 8. Semente e conferente herdados corretamente.
- `resultados/Math-101` preservada (manifesto, `tempos.csv`, `gerar.log`, `cobertura_falha.*`; sem suíte). `tempos.csv`: `gerar` com código 1 em 6 s. `logs/gerar.log` termina em `Cannot compile! at /defects4j/framework/bin/gen_tests.pl line 230.`, com 4 ocorrências de `error: unmappable character for encoding ASCII` (em `MultivariateSummaryStatistics.java:65` e `SynchronizedMultivariateSummaryStatistics.java:32`, comentários `@version ... févr. 2008`), `BUILD FAILED` e "Compile failed". O checkout, a aplicação do patch e o `Check out program version: Math-101f` terminaram `OK`; a falha é só do `javac`.
- Conclusão sobre a causa: o log sustenta "o projeto não compila no ambiente (javac com codificação ASCII)", que é o motivo registrado em `substituicoes.csv`, em `registro-substituidas.csv` e em `docs/04-semana4-resultados.md`. É um impedimento técnico alheio à ferramenta, não uma falha do EvoSuite (que nem chegou a rodar). Observação para a análise: a causa é a codificação padrão do contêiner (imagem sem `LANG`), não um defeito da falha em si; isso foi decidido pelo usuário (manter o ambiente homogêneo) e já está anotado como viés de seleção pequeno. Mantenho como ameaça à validade a registrar no relatório.
- `dados/registro-substituidas.csv` contém a linha Math-101 (`sem_suite`, `etapas_com_erro=gerar`, `nao_se_aplica`, `conferencia=pendente`), com texto de `observacoes` explicando a causa. `dados/registro.csv` não tem mais Math-101 (e tem Math-80), mantendo n = 35 por tamanho de amostra. Linha de Closure-88 também está em `registro-substituidas.csv` (fora do escopo desta conferência).
- Documentação: decisões registradas em `docs/03-semana3-instrumentacao.md` e `docs/04-semana4-resultados.md` (commit 9a5c348).

Resultado: **ok**.

---

## Teste 3: Closure-42 (ordem 3)

| # | Verificação | Resultado | Evidência |
|---|---|---|---|
| C1 | Checklist do ambiente | ok | Coluna "Teste 3: Closure-42" completa e `ok` (A6 com `cpu.max 200000/100000` e `memory.max 6442450944`; D1 a D5 detalhados). |
| C2 | Manifesto | ok | Semente 89868774. `classes_modificadas` = `com.google.javascript.jscomp.parsing.IRFactory` (1 classe, `orcamento_total_s=360`). Demais campos de referência iguais. |
| C3 | Ordem | ok | Manifesto 09:26; depois de Math-80 (08:30) e antes de Chart-26 (10:21). Commit c018115 entre 02d068e e 85a78ce. |
| C4 | Registro x saídas | ok | `bug_detection`: Fail, `num_trigger=1` → `Fail`/1/`deteccao_automatica=1`. `coverage`: 528/221 linhas, 281/87 ramos; 221/528 = 41,86% (confere). `cobertura_falha.txt` = parcial (2 de 3 linhas: 568 hits=2, 569 hits=1, 575 hits=0) → `parcial`. Conferi contra `Closure/42.src.patch`: as linhas `-` são o bloco `if (loopNode.isForEach()) { errorReporter.error(...); return newNode(EXPR_RESULT, ...); }` (568-569 e 575 são as executáveis; 570-572 são argumentos e 576 é `}`), todas presentes no `42f.1.xml` como 568, 569 e 575. A linha 575 sem hits é coerente com o teste: na versão corrigida `errorReporter.error` lança `UnsupportedOperationException` (ErrorCollector) antes do `return`. |
| C5 | Falso positivo | **divergente** | **Não existe `docs/registros/falso-positivo-Closure-42.md`**: não está no commit c018115, nem em qualquer outro commit, nem no disco. No registro, `falso_positivo=pendente`, `deteccao_confirmada=pendente`, `conferencia=pendente` e `observacoes` vazio. O checklist é obrigatório quando `deteccao_automatica=1` (manual, passo 5 da seção 7). Avaliação independente abaixo. |
| C6 | Não detectou | n/a | Detectou. (Só para registro: nenhum teste removido; `summary.log` com 0/0, `compile.log` e `run.log` vazios; 46 testes finais.) |
| C7 | Cobertura da falha indeterminada/manual | n/a | Automática (`parcial`); verificada em C4. |
| C8 | Logs não editados | ok | `git log -- resultados/Closure-42` só tem c018115 (22 `A`). |

Avaliação independente de falso positivo (Closure-42), para o executor preencher/confirmar:

- Teste revelador: `com.google.javascript.jscomp.parsing.IRFactory_ESTest::test32` (único; `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version").
- F1 sim: o trace da versão defeituosa passa por `IRFactory$TransformDispatcher.processForInLoop(IRFactory.java:570)`, o método alterado pelo patch (que remove o tratamento de `for each`).
- F2 sim: o teste cria um `ArrayComprehensionLoop` com `setIsForEach(true)` dentro de um `AstRoot`, chama `IRFactory.transformTree(...)` e espera `UnsupportedOperationException` vinda de `ErrorCollector` (comportamento da corrigida: `errorReporter.error("unsupported language extension: for each")`). Na defeituosa o `if (isForEach())` não existe e a execução segue para `transform(loopNode.getIterator())`, gerando `NullPointerException` em `TypeSafeDispatcher.process(TypeSafeDispatcher.java:119)`. Valor esperado coerente com a corrigida, obtido coerente com a defeituosa.
- F3 sim (não depende): só objetos do Rhino/Closure construídos em memória, entrada fixa; sem data/hora, fuso, locale, `HashMap`/`HashSet`, rede ou arquivos.
- F4 sim: `fix_test_suite.summary.log` com 0 não compiláveis e 0 falhando, `run.log` vazio; `42f.1.trigger.log` vazio (passa na corrigida).
- F5 sim: `NullPointerException` de lógica do produto, não é timeout, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória.
- Conclusão: concordo que o resultado é `falso_positivo = nao` e `deteccao_confirmada = 1`. A divergência é só de processo (arquivo de registro ausente e colunas `pendente`), não de mérito. Para fechar: o executor precisa criar `docs/registros/falso-positivo-Closure-42.md` com o modelo da seção 3 de `docs/checklist-falso-positivo.md`, atualizar `falso_positivo` e `deteccao_confirmada` em `dados/registro.csv` (módulo `csv`) e registrar o commit; depois a conferência passa a `ok`.

Resultado: **divergente:Leonardo Ceccon:C5**.

---

## Teste 4: Chart-26 (ordem 4)

| # | Verificação | Resultado | Evidência |
|---|---|---|---|
| C1 | Checklist do ambiente | ok | Coluna "Teste 4: Chart-26" completa e `ok` (A6 com `cpu.max` e `memory.max`; D1 a D5 detalhados). |
| C2 | Manifesto | ok | Semente 807160701. `classes_modificadas` = `org.jfree.chart.axis.Axis` (1 classe, `orcamento_total_s=360`). Demais campos de referência iguais. |
| C3 | Ordem | ok | Manifesto 10:21; depois de Closure-42 (09:26) e antes de Time-5 (11:09). Commit 85a78ce entre c018115 e bf7ab2b. |
| C4 | Registro x saídas | ok | `bug_detection`: Pass, 0 triggers → `Pass`/0/0. `coverage`: 329/299 linhas, 136/127 ramos; 299/329 = 90,88% (confere). `cobertura_falha.txt` = total (2/2: 1192 hits=9 e 1200 hits=12) → `total`. |
| C5 | Falso positivo | n/a | Não detectou. |
| C6 | Não detectou com testes gerados | ok | `bug_detection` = Pass; 0 removidos (`summary.log` 0/0, `compile.log`/`run.log` vazios); `26b.1.trigger.log` vazio; 59 testes finais. Observação de mérito: a linha-alvo 1192 (`if (owner != null)`) tem apenas 1 de 2 ramos cobertos no `26f.1.xml`; a suíte nunca exerceu `owner == null`, que é o caso que a defeituosa não trata. A ausência de detecção é, portanto, plausível (falha legítima do EvoSuite, não da infraestrutura). |
| C7 | Cobertura da falha indeterminada/manual | n/a | Automática (`total`). Conferi contra `Chart/26.src.patch`: duas linhas `-`, `if (owner != null) {` (1192, executável) e o `}` correspondente (não executável), que pela regra 3 desloca para a próxima executável, `return state;` (1200). Ambas aparecem no `26f.1.xml` com hits > 0. Confere. |
| C8 | Logs não editados | ok | `git log -- resultados/Chart-26` só tem 85a78ce (22 `A`). |

Resultado: **ok**.

---

## Teste 5: Time-5 (ordem 5)

| # | Verificação | Resultado | Evidência |
|---|---|---|---|
| C1 | Checklist do ambiente | ok | Coluna "Teste 5: Time-5" completa e `ok` (A7 lista os commits das ordens 1 a 4; D1 a D5 detalhados). |
| C2 | Manifesto | ok | Semente 1792588423. `classes_modificadas` = `org.joda.time.Period` (1 classe, `orcamento_total_s=360`). Demais campos de referência iguais. |
| C3 | Ordem | ok | Manifesto 11:09, o último de Celente; commit bf7ab2b (16:14) é o último dele. |
| C4 | Registro x saídas | ok | `bug_detection`: Fail, `num_trigger=2` → `Fail`/`testes_reveladores=2`/`deteccao_automatica=1`. `coverage`: 288/277 linhas, 64/64 ramos; 277/288 = 96,18% (confere). `cobertura_falha.txt` = total (11/11, linhas 1628-1640 de `Period.java`) → `total`. Conferi contra `Time/5.src.patch`: as linhas `-` do hunk `@@ -1625,19 +1625,13 @@` vão de 1628 a 1640, com 11 executáveis (as chaves 1633 e 1638 não contam), igual às 11 consideradas. |
| C5 | Falso positivo | ok (concordo) | `docs/registros/falso-positivo-Time-5.md` existe, com F1 a F5 preenchidos e justificados, no commit bf7ab2b. Revisão independente abaixo. Pendências formais: o campo "Conferente / Data / Concorda?" está em branco (a ser preenchido pelo conferente humano) e `deteccao_confirmada=pendente` / `conferencia=pendente` no registro (aguardam a validação humana; `observacoes` já diz "FP pré-avaliado por agente"). |
| C6 | Não detectou | n/a | Detectou. (Nenhum teste removido; 75 testes finais.) |
| C7 | Cobertura da falha indeterminada/manual | n/a | Automática (`total`); verificada em C4. |
| C8 | Logs não editados | ok | `git log -- resultados/Time-5` só tem bf7ab2b (22 `A`). |

Revisão independente do falso positivo (Time-5), testes `Period_ESTest::test74` e `test33`, que são os 2 reveladores:

- F1 sim: o trace de `test33` é `PeriodType.setIndexedField(PeriodType.java:690)` ← `Period.withYears(Period.java:896)` ← `Period.normalizedStandard(Period.java:1631)`, e `normalizedStandard` é o método alterado pelo patch. O de `test74` falha em `EvoAssertions.assertThrownBy` porque a exceção veio de `PeriodType.setIndexedField` em vez de `Period`, no mesmo fluxo.
- F2 sim: `test74` (`new Period(117,29,117,29,29,0,0,117).normalizedStandard(PeriodType.weeks())`) espera `UnsupportedOperationException` com a mensagem "Unable to normalize as PeriodType is missing either years or months...", que só existe na versão corrigida (linhas `-` do patch). `test33` (`Period.months(-2150).normalizedStandard(PeriodType.months())`) espera retorno normal; a defeituosa chama `withYears` em um tipo sem anos e lança `Field is not supported`. Sentido do patch (corrigida → defeituosa) entendido corretamente pelo executor.
- F3 sim: apenas construtores e métodos puros de `Period`/`PeriodType` com valores fixos.
- F4 sim: `summary.log` 0/0, `run.log` e `compile.log` vazios, `5f.1.trigger.log` vazio.
- F5 sim: `UnsupportedOperationException`/`AssertionFailedError` de lógica do produto, sem sinais de infraestrutura.
- Concordo com `falso_positivo = nao` e `deteccao_confirmada = 1` (a ser gravada pelo humano).

Resultado: **ok** (com as pendências formais acima, que dependem da validação humana e não são divergência).

---

## Pendências e sugestões

1. Closure-42: criar o checklist de falso positivo e atualizar `falso_positivo`/`deteccao_confirmada` no registro (único item divergente).
2. Math-80: sugerir anotar "substituta de Math-101 (regra da seção 8)" em `observacoes` de `dados/registro.csv`.
3. Time-5: preencher o campo "Conferente / Data / Concorda?" do `falso-positivo-Time-5.md` e atualizar `deteccao_confirmada` quando o humano validar.
4. Esta pré-conferência foi feita por agente sobre um experimento executado por agente: a validação humana do Leonardo Ceccon continua necessária antes de gravar `ok:Leonardo Ceccon` em `conferencia` (nenhuma coluna `conferencia` foi alterada).
