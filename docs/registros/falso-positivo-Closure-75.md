# Falso positivo: Closure-75

- Executor: Lucas Reali (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: com.google.javascript.jscomp.NodeUtil_ESTest::test069 (único revelador)

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `75b.1.trigger.log` (linhas 1-7): `--- com.google.javascript.jscomp.NodeUtil_ESTest::test069` / `junit.framework.AssertionFailedError: expected null, but was:<0.0>` em `assertNull`, `at ...NodeUtil_ESTest.test069(NodeUtil_ESTest.java:15619)`. O teste (linhas 15617-15620 da suíte filtrada) chama `NodeUtil.getStringNumberValue("\u000B")`, método de `NodeUtil` alterado em `75.src.patch` (hunk `@@ -310,10 +310,7 @@`). O patch está no sentido corrigida -> defeituosa: as linhas `-` `if (rawJsString.contains("\u000b")) { return null; }` existem só na corrigida. O segundo hunk (`@@ -375,7 +372,7 @@`) troca, em `isStrWhiteSpaceChar`, `case '\u000B': return TernaryValue.UNKNOWN` (corrigida) por `return TernaryValue.TRUE` (defeituosa). `NodeUtil` é a única classe modificada (`manifesto.txt`: `classes_modificadas: com.google.javascript.jscomp.NodeUtil`). |
| F2 | Sim | Na suíte filtrada (gerada sobre a corrigida), `test069` faz `assertNull(double0)` para a entrada `"\u000B"` (tabulação vertical), coerente com o `return null` da checagem `contains("\u000b")` presente só na corrigida. Na defeituosa, sem essa checagem e com `\u000B` tratado como espaço em branco (`TernaryValue.TRUE`), a string é aparada e o método devolve um número; o valor obtido registrado no log é `0.0`. Esperado = corrigida; obtido = defeituosa. |
| F3 | Sim | Entrada literal fixa (`"\u000B"`) e chamada estática pura a `getStringNumberValue`; não usa data/hora, fuso, locale, ordem de `HashMap`/`HashSet`, rede, arquivos nem memória. A suíte roda com `@EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true)` (linha 52). |
| F4 | Sim | `fix_test_suite.summary.log`: "Number of uncompilable test classes: 0", "Number of uncompilable tests: 0" e "Number of failing tests: 0"; `fix_test_suite.run.log` e `fix_test_suite.compile.log` vazios (0 bytes), logo `test069` não foi removido nas 5 execuções (`logs/filtrar.log` mostra 5 pares `compile.gen.tests`/`run.gen.tests` OK). `75f.1.trigger.log` vazio (0 bytes): nenhum teste falha na corrigida. |
| F5 | Sim | A falha é uma `AssertionFailedError` de valor (`expected null, but was:<0.0>`), sem timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version"; `deteccao/bug_detection`: `Closure,75f,evosuite,1,Fail,1`. |

Observação: o trigger log tem um único teste (`test069`), então a análise cobre 100% dos reveladores. A conclusão coincide com a avaliação preliminar do conferente (item C5 de `conferencia-Lucas-Reali.md`), mas foi verificada de forma independente a partir do trigger log, da suíte extraída e do patch lido no contêiner.

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente: Guilherme Fadel · Data:  · Concorda? 
