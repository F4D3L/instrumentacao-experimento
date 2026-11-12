# Falso positivo: Math-25

- Executor: Gabriel Moribe (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: org.apache.commons.math3.optimization.fitting.HarmonicFitter_ESTest::test5

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `25b.1.trigger.log`: `AssertionFailedError: Expecting exception: IllegalStateException` em `HarmonicFitter_ESTest.test5(HarmonicFitter_ESTest.java:228)`. O teste chama `new HarmonicFitter.ParameterGuesser(pontos).guess()`, método da classe `HarmonicFitter$ParameterGuesser` alterada em `25.src.patch` (hunk `@@ -320,11 +320,8 @@`). O patch está no sentido corrigida -> defeituosa: as linhas `-` (`if (c2 == 0) { ... throw new MathIllegalStateException(LocalizedFormats.ZERO_DENOMINATOR); }`) existem na corrigida e foram removidas na defeituosa. |
| F2 | Sim | Na suíte filtrada (gerada sobre a corrigida), `test5` espera `IllegalStateException` com comentário "denominator must be different from 0" e `verifyException("...HarmonicFitter$ParameterGuesser", e)`, que é a mensagem de `LocalizedFormats.ZERO_DENOMINATOR` lançada pela checagem `c2 == 0` presente só na corrigida. Na defeituosa, a checagem não existe: `guess()` segue para `a = FastMath.sqrt(c1 / c2)` sem exceção e o `fail("Expecting exception: IllegalStateException")` da linha 228 é executado. |
| F3 | Sim | O teste só constrói 4 `WeightedObservedPoint` com valores `double` literais e chama `guess()`; não usa data/hora, fuso, locale, ordem de `HashMap`/`HashSet`, rede, arquivos nem memória. O resultado depende apenas da aritmética em ponto flutuante determinística sobre as entradas fixas (c2 == 0). |
| F4 | Sim | `fix_test_suite.summary.log`: "Number of uncompilable tests: 0" e "Number of failing tests: 0"; `fix_test_suite.run.log` e `fix_test_suite.compile.log` vazios (0 bytes), logo `test5` não foi removido. `25f.1.trigger.log` vazio (0 bytes): nenhum teste falha na corrigida. |
| F5 | Sim | A falha é uma `AssertionFailedError` ("Expecting exception") gerada pelo `fail(...)` do teste, sem timeout, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version". |

Observação: o trigger log tem um único teste (`test5`), então a análise cobre 100% dos reveladores. Detalhe: no patch, a remoção do `if (c2 == 0)` é a única alteração de código (sobraram só comentários).

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente: 
