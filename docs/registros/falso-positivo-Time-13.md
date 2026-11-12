# Falso positivo: Time-13

- Executor: Thiago Akimoto (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: org.joda.time.format.PeriodFormatterBuilder_ESTest::test074

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `13b.1.trigger.log`: `junit.framework.AssertionFailedError: expected:<[-]0.024> but was:<[]0.024> at org.joda.time.format.PeriodFormatterBuilder_ESTest.test074(PeriodFormatterBuilder_ESTest.java:2064)`. O teste chama `periodFormatterBuilder_Separator0.printTo(stringBuffer0, period1, locale0)`, que delega ao printer de segundos/milissegundos de `PeriodFormatterBuilder.FieldFormatter`, a classe alterada em `13.src.patch` (hunks `@@ -1095,7 +1095,7 @@` e `@@ -1130,7 +1130,6 @@`/`@@ -1140,9 +1139,6 @@`). O patch está no sentido corrigida -> defeituosa: as linhas `-                    if (valueLong < 0 && valueLong > -DateTimeConstants.MILLIS_PER_SECOND) {` / `-                        buf.insert(bufLen, '-');` (presentes na corrigida) são removidas na defeituosa. Ressalva: o stack trace do log só mostra o frame do teste (as demais linhas são JUnit/reflexão), então a passagem pelo método alterado é inferida do teste e do patch, não vista no trace. |
| F2 | Sim | O teste cria `Period` de zero (`new Period(mutableDateTime0, mutableDateTime0, PeriodType.time())`), aplica `withMillis(-24)` e espera `assertEquals("-0.024", stringBuffer0.toString())`. A corrigida insere o `-` quando `valueLong < 0 && valueLong > -MILLIS_PER_SECOND` (-24 ms), logo imprime `-0.024`, o esperado. Na defeituosa essa inserção não existe e imprime `0.024`, exatamente o valor obtido no log (`but was:<[]0.024>`). O trigger log da corrigida (`13f.1.trigger.log`) tem 0 bytes. |
| F3 | Sim | O resultado depende só do valor `-24` ms passado a `withMillis`. `MutableDateTime.now()` aparece, mas é usado nas duas pontas do `Period` (período zero, independente do instante; EvoSuite ainda mocka o tempo: `getMillis()` = 1392409281320L, com `mockJVMNonDeterminism = true`). O `Locale.SIMPLIFIED_CHINESE` é passado ao `printTo`, mas a formatação usa `FormatUtils.appendUnpaddedInteger`/`appendPaddedInteger`, sem formatação dependente de locale. Não há `HashMap`/`HashSet`, rede, arquivos nem uso de memória relevante. Ressalva: a conclusão sobre o locale vem da leitura do trecho do patch e do teste, não de reexecução com outro locale. |
| F4 | Sim | `fix_test_suite.summary.log`: "Number of uncompilable test classes: 0", "Number of uncompilable tests: 0", "Number of failing tests: 0"; `fix_test_suite.run.log` e `fix_test_suite.compile.log` com 0 bytes. `test074` não aparece como removido e a suíte filtrada contém `test074`. `13f.1.trigger.log` vazio. |
| F5 | Sim | A falha é `AssertionFailedError` de valor (`expected:<[-]0.024> but was:<[]0.024>`), sem timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version". |

Observação: o trigger log da defeituosa tem um único teste (`test074`), então a análise cobre 100% dos reveladores.

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente: 
