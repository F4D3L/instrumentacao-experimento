# Falso positivo: Chart-8

- Executor: Gabriel Conti (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: org.jfree.data.time.Week_ESTest::test12 (único revelador)

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `8b.1.trigger.log`: `--- org.jfree.data.time.Week_ESTest::test12` / `junit.framework.AssertionFailedError: Expecting exception: IllegalArgumentException` / `at org.junit.Assert.fail(Assert.java:88)` / `at org.jfree.data.time.Week_ESTest.test12(Week_ESTest.java:357)`. O stack trace não contém frame de `Week`, pois a falha é o `fail(...)` do próprio teste, logo após a chamada `new Week(mockDate0, (TimeZone) null)` (linha 356), que é o construtor `Week(Date, TimeZone)` alterado pelo patch `8.src.patch` (`source/org/jfree/data/time/Week.java`, hunk `@@ -172,7 +172,7 @@`): `-        this(time, zone, Locale.getDefault());` / `+        this(time, RegularTimePeriod.DEFAULT_TIME_ZONE, Locale.getDefault());`. |
| F2 | Sim | O teste espera `IllegalArgumentException` com a mensagem "Null 'zone' argument." ao passar zona `null`. Na versão corrigida (linha `-` do patch; no D4J o `.src.patch` vai da corrigida para a defeituosa) a zona `null` é repassada ao construtor de 3 argumentos, que a rejeita, lançando a exceção esperada (a suíte foi gerada sobre a corrigida e passa nela). Na defeituosa (linha `+`) a zona informada é ignorada e substituída por `DEFAULT_TIME_ZONE`, então nenhuma exceção é lançada e o teste chega ao `fail(...)` (obtido). |
| F3 | Sim | O resultado não depende de relógio, fuso real, locale, `HashMap`/`HashSet`, rede, arquivos ou memória: o teste usa `MockDate` (data simulada pelo EvoSuite) e zona `null` fixa; o desfecho depende só de o argumento `null` ser validado ou descartado. Há `TimeZone.getDefault()` apenas em outro teste (linha 372, não revelador). |
| F4 | Sim | `fix_test_suite.run.log` e `fix_test_suite.compile.log` vazios (0 bytes); `fix_test_suite.summary.log`: `Number of uncompilable tests: 0` e `Number of failing tests: 0`. `8f.1.trigger.log` vazio (nenhuma falha na corrigida); `run_bug_detection.pl.log`: `Found 1 failing tests on buggy version`. test12 não foi removido. |
| F5 | Sim | A falha é `junit.framework.AssertionFailedError` ("Expecting exception: IllegalArgumentException"), uma asserção de comportamento, e não timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. |

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente:  · Data:  · Concorda?
