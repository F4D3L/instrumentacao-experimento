# Falso positivo: Math-45

- Executor: Gabriel Conti (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: org.apache.commons.math.linear.OpenMapRealMatrix_ESTest::test3

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `45b.1.trigger.log`: `AssertionFailedError: Expecting exception: IllegalArgumentException` em `OpenMapRealMatrix_ESTest.test3(OpenMapRealMatrix_ESTest.java:77)`. O teste chama `new OpenMapRealMatrix(2145707400, 492)`, o construtor `OpenMapRealMatrix(int, int)` alterado em `45.src.patch` (hunk `@@ -47,11 +47,6 @@`). O patch está no sentido corrigida -> defeituosa: as linhas `-` (`long lRow = (long) rowDimension; ... if (lRow * lCol >= (long) Integer.MAX_VALUE) { throw new NumberIsTooLargeException(lRow * lCol, Integer.MAX_VALUE, false); }`) existem na corrigida e foram removidas na defeituosa. |
| F2 | Sim | Na suíte filtrada (gerada sobre a corrigida), `test3` espera `IllegalArgumentException` e comenta "1,055,688,040,800 is larger than, or equal to, the maximum (2,147,483,647)", que é a mensagem de `NumberIsTooLargeException` da checagem `lRow * lCol >= Integer.MAX_VALUE` presente só na corrigida (2145707400 * 492 = 1.055.688.040.800). Na defeituosa, a checagem não existe: o construtor retorna sem exceção e o `fail(...)` da linha 77 é executado. |
| F3 | Sim | O teste só invoca um construtor com argumentos inteiros literais; não usa data/hora, fuso, locale, ordem de `HashMap`/`HashSet`, rede, arquivos nem memória. O resultado (exceção lançada ou não) depende apenas da aritmética `long` do produto das dimensões. |
| F4 | Sim | `fix_test_suite.summary.log`: "Number of uncompilable tests: 0" e "Number of failing tests: 0"; `fix_test_suite.run.log` e `fix_test_suite.compile.log` vazios (0 bytes), logo `test3` não foi removido. `45f.1.trigger.log` vazio (0 bytes): nenhum teste falha na corrigida. |
| F5 | Sim | A falha é uma `AssertionFailedError` ("Expecting exception") gerada pelo `fail(...)` do teste, sem timeout, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version". |

Observação: o trigger log tem um único teste (`test3`), então a análise cobre 100% dos reveladores.

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente: 
