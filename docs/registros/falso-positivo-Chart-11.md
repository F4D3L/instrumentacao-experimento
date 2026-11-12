# Falso positivo: Chart-11

- Executor: Leonardo Ceccon (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 4
- Testes analisados: org.jfree.chart.util.ShapeUtilities_ESTest::test44, org.jfree.chart.util.ShapeUtilities_ESTest::test45, org.jfree.chart.util.ShapeUtilities_ESTest::test46 (amostra de 3 dos 4; test47 tem o mesmo padrão: falha em `assertFalse` na linha 1826)

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `11b.1.trigger.log`: `--- org.jfree.chart.util.ShapeUtilities_ESTest::test44` / `junit.framework.AssertionFailedError` / `at org.junit.Assert.assertFalse(Assert.java:74)` / `at org.jfree.chart.util.ShapeUtilities_ESTest.test44(ShapeUtilities_ESTest.java:1470)`; idem test45 (linha 1663) e test46 (linha 1699). O stack trace não contém frame de `ShapeUtilities` porque a asserção falha no próprio teste, logo após a chamada `ShapeUtilities.equal(generalPath0, generalPath1)` (sobrecarga com `GeneralPath`). O patch `11.src.patch` altera `source/org/jfree/chart/util/ShapeUtilities.java` nesse método (hunk `@@ -272,7 +272,7 @@`): `-        PathIterator iterator2 = p2.getPathIterator(null);` / `+        PathIterator iterator2 = p1.getPathIterator(null);`. A asserção que falha depende diretamente do retorno do método alterado. |
| F2 | Sim | Os testes comparam dois `GeneralPath` diferentes (test44: `createDiagonalCross(0.0F, 0.0F)` vs `new GeneralPath()`; asserções prévias `assertFalse(generalPath0.equals(generalPath1))`) e esperam `assertFalse(boolean0)`, isto é, `equal(...) == false`. Na versão corrigida (linhas `-` do patch, que usam `p2.getPathIterator`) os dois caminhos são comparados e diferem, retornando false (esperado). Na defeituosa (linhas `+`), `iterator2` vem de `p1`, então p1 é comparado consigo mesmo e `equal` retorna true, o que faz `assertFalse` falhar (obtido). Nota: no D4J o `.src.patch` é aplicado da corrigida para a defeituosa, por isso `-` é o código correto. |
| F3 | Sim | Nenhum dos testes usa data/hora, locale, `HashMap`/`HashSet`, rede, arquivos ou memória (busca por `Random`, `System.`, `File`, `Date`, `Locale` em `ShapeUtilities_ESTest.java` sem ocorrências). Entradas são formas geométricas construídas deterministicamente (`new GeneralPath()`, `createDiagonalCross(0.0F, 0.0F)`, `Line2D.Float`), e o resultado depende só da comparação de `PathIterator`s. |
| F4 | Sim | `fix_test_suite.run.log` e `fix_test_suite.compile.log` vazios (0 bytes); `fix_test_suite.summary.log`: `Number of uncompilable tests: 0` e `Number of failing tests: 0`. test44 a test47 não foram removidos; `11f.1.trigger.log` vazio (nenhuma falha na corrigida); `run_bug_detection.pl.log`: `Found 4 failing tests on buggy version`. |
| F5 | Sim | A falha é `junit.framework.AssertionFailedError` em `assertFalse`, uma asserção de valor, e não timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. |

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente:  · Data:  · Concorda?
