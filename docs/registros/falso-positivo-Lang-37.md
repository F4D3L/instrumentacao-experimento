# Falso positivo: Lang-37

- Executor: Guilherme Fadel (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: org.apache.commons.lang3.ArrayUtils_ESTest::test331

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `37b.1.trigger.log`: `java.lang.ArrayStoreException at java.lang.System.arraycopy(Native Method)` seguido de `at org.apache.commons.lang3.ArrayUtils.addAll(ArrayUtils.java:2962)`. O patch (`37.src.patch`) altera exatamente `ArrayUtils.addAll(T[], T...)` (hunk `@@ -2959,16 +2959,8 @@`). O `src.patch` do Defects4J está no sentido corrigida -> defeituosa: as linhas `-` (bloco `try { System.arraycopy(array2, ...) } catch (ArrayStoreException ase) { ... throw new IllegalArgumentException("Cannot store "+type2.getName()+" in an array of "+type1.getName()); ... }`) existem só na versão corrigida; na defeituosa o `arraycopy` fica sem o try/catch, e a linha 2962 do trace é o `System.arraycopy(array2, 0, joinedArray, array1.length, array2.length)` sem proteção. |
| F2 | Sim | Na suíte filtrada (gerada sobre a corrigida), `test331` chama `ArrayUtils.addAll((Object[]) stringArray0, objectArray0)` com `String[]` vazio e `Object[8]` e espera `fail("Expecting exception: IllegalArgumentException")` / `catch(IllegalArgumentException e)` com mensagem "Cannot store java.lang.Object in an array of java.lang.String", que é a exceção do bloco catch presente só na corrigida (patch). Na defeituosa a exceção obtida é `ArrayStoreException` crua (trigger log), coerente com o código sem o try/catch. |
| F3 | Sim | O teste usa apenas arrays em memória (`EMPTY_STRING_ARRAY`, `new Object[8]`, `Boolean.FALSE`) e um único `System.arraycopy` determinístico; sem data/hora, fuso, locale, HashMap/HashSet, rede, arquivo ou memória. |
| F4 | Sim | `fix_test_suite.run.log` lista só `ArrayUtils_ESTest::test345` (`ClassCastException: [Ljava.lang.Object; cannot be cast to [Ljava.util.AbstractMap$SimpleImmutableEntry;`) e `fix_test_suite.summary.log` diz "Number of failing tests: 1". `test331` não aparece como removido. `37f.1.trigger.log` está vazio (0 bytes): nenhum teste falha na corrigida. O `test345` removido é outro teste (marcado "Defects4J: flaky method" no arquivo final) e não é o revelador. |
| F5 | Sim | A mensagem é `ArrayStoreException` em `ArrayUtils.addAll`, erro de lógica do código sob teste; não há timeout, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória no trigger log. `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version". |

Observação: o trigger log tem um único teste (`test331`), então a análise cobre 100% dos reveladores.

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente: 
