# Falso positivo: Math-63

- Executor: Lucas Reali (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: org.apache.commons.math.util.MathUtils_ESTest::test057 (único revelador)

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim (indireto) | `63b.1.trigger.log`: `--- org.apache.commons.math.util.MathUtils_ESTest::test057` / `junit.framework.AssertionFailedError` / `at org.junit.Assert.assertFalse(Assert.java:74)` / `at org.apache.commons.math.util.MathUtils_ESTest.test057(MathUtils_ESTest.java:473)`. O topo da pilha é a asserção do teste, não o método alterado. O patch `63.src.patch` altera `MathUtils.equals(double x, double y)` (hunk `@@ -414,7 +414,7 @@`). O teste chama `MathUtils.equals(double[], double[])` (`MathUtils_ESTest.java:472`), que na versão defeituosa (checkout `63b`, `MathUtils.java:530`) executa `if (!equals(x[i], y[i]))`, ou seja, delega ao método alterado. A ligação com o patch vem da leitura do código, não da pilha. |
| F2 | Sim | Teste: `doubleArray0[0] = (double) Float.NaN; boolean boolean0 = MathUtils.equals(doubleArray0, doubleArray0); assertFalse(boolean0);`. O patch (da corrigida para a defeituosa) troca `-        return equals(x, y, 1);` por `+        return (Double.isNaN(x) && Double.isNaN(y)) \|\| x == y;`. Na corrigida, `equals(NaN, NaN)` com `equals(x, y, 1)` dá `false`, como o `assertFalse` espera. Na defeituosa, NaN e NaN dão `true`, e a asserção falha. Esperado = corrigida; obtido = defeituosa. Coerente com `63f.1.trigger.log` vazio (0 bytes). |
| F3 | Sim | A falha vem da comparação de `NaN` com `NaN`, sem relação com data/hora, fuso, locale, ordem de `HashMap`/`HashSet`, rede, arquivo ou memória. O teste usa só um `double[1]` local e é puramente determinístico (a classe usa `mockJVMNonDeterminism = true`). |
| F4 | Sim | `test057` não aparece no `fix_test_suite.run.log`. O log remove apenas `MathUtils_ESTest::test078` (`MathUtils.lcm(...)`, marcado `// Defects4J: flaky method`), que não é o revelador. `63f.1.trigger.log` tem 0 bytes (nenhuma falha na corrigida). `fix_test_suite.summary.log`: `Number of uncompilable tests: 0`, `Number of failing tests: 1`. `run_bug_detection.pl.log`: `Found 1 failing tests on buggy version`. |
| F5 | Sim | A mensagem é `junit.framework.AssertionFailedError` numa asserção de valor. Não é timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. |

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente:  · Data:  · Concorda?
