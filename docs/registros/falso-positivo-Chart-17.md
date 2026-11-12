# Falso positivo: Chart-17

- Executor: Thiago Akimoto (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: org.jfree.data.time.TimeSeries_ESTest::test50 (único revelador)

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `17b.1.trigger.log`: `--- org.jfree.data.time.TimeSeries_ESTest::test50` / `MockIllegalArgumentException: Requires start <= end.` / `at org.jfree.data.time.TimeSeries.createCopy(TimeSeries.java:880)` / `at org.jfree.data.time.TimeSeries.clone(TimeSeries.java:857)`. O patch `17.src.patch` altera `source/org/jfree/data/time/TimeSeries.java`, método `clone()` (hunk `@@ -854,8 +854,7 @@`): linhas `-` `TimeSeries clone = (TimeSeries) super.clone(); clone.data = (List) ObjectUtilities.deepClone(this.data);` e `+` `Object clone = createCopy(0, getItemCount() - 1);`. A pilha passa por `clone()`, o método alterado. |
| F2 | Sim | O teste (linha 3385) cria `new TimeSeries(day0)` vazia (`getItemCount() == 0`) e chama `timeSeries0.clone()`, esperando uma cópia com 0 itens (`assertEquals(0, timeSeries1.getItemCount())`, `assertTrue(timeSeries1.equals(timeSeries0))`), o que corresponde à `clone()` da versão corrigida (`super.clone()` + `deepClone`). Na defeituosa, `clone()` chama `createCopy(0, getItemCount() - 1)` = `createCopy(0, -1)`, que lança `IllegalArgumentException: Requires start <= end.` (start 0 > end -1). Esperado = corrigida; obtido = defeituosa. Nota: no D4J o `.src.patch` é aplicado da versão corrigida para a defeituosa, por isso as linhas `-` são o código da corrigida. |
| F3 | Sim | A falha vem de aritmética fixa (série vazia, `createCopy(0, -1)`). `new Day()` aparece no teste, mas o EvoSuite o executa com relógio simulado (`mockJVMNonDeterminism = true`; `getFirstMillisecond() == 1392409281320L` fixo nas asserções), e a data não influencia a exceção. Sem rede, arquivo, locale, `HashMap`/`HashSet` ou memória no caminho da falha. |
| F4 | Sim | `fix_test_suite.run.log` e `fix_test_suite.compile.log` vazios (0 bytes); `fix_test_suite.summary.log`: `Number of uncompilable tests: 0` e `Number of failing tests: 0`. test50 não foi removido; testes_removidos_* = 0 no registro. `17f.1.trigger.log` vazio (nenhuma falha na corrigida) e `run_bug_detection.pl.log`: `Found 1 failing tests on buggy version`. |
| F5 | Sim | A mensagem é `Requires start <= end.`, erro lógico do código sob teste (validação de argumentos em `createCopy`), não timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. A pilha termina em `TimeSeries_ESTest.test50(TimeSeries_ESTest.java:3385)`. |

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente:  · Data:  · Concorda?
