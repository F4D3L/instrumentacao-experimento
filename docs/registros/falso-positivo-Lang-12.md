# Falso positivo: Lang-12

- Executor: Thiago Akimoto (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: org.apache.commons.lang3.RandomStringUtils_ESTest::test09 (único revelador)

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `12b.1.trigger.log`: `--- org.apache.commons.lang3.RandomStringUtils_ESTest::test09` / `java.lang.ArrayIndexOutOfBoundsException: 0` / `at org.apache.commons.lang3.RandomStringUtils.random(RandomStringUtils.java:248)`. O patch `12.src.patch` altera `src/main/java/org/apache/commons/lang3/RandomStringUtils.java` no método `random(...)` (hunk `@@ -227,21 +227,14 @@`): remove o bloco `if (chars != null && chars.length == 0) { throw new IllegalArgumentException("The chars array must not be empty"); }` (e o tratamento de `chars` em `end = chars.length`). A pilha passa por `RandomStringUtils.random`, método alterado. |
| F2 | Sim | O teste (`RandomStringUtils.random(57343, "")`) espera `IllegalArgumentException` com a mensagem "The chars array must not be empty" (`fail("Expecting exception: IllegalArgumentException")` + `verifyException`). Isso é exatamente o bloco de validação que o patch mostra como diferença entre as versões (linhas `-` do patch, presentes na versão corrigida). Na defeituosa, sem a validação, o código segue e lança `ArrayIndexOutOfBoundsException: 0` por indexar `chars` vazio. Esperado = corrigida; obtido = defeituosa. |
| F3 | Sim | Entrada fixa (`count = 57343`, `chars = ""`); a exceção vem de uma checagem de argumento vazio, sem uso de data/hora, fuso, locale, `HashMap`/`HashSet`, rede, arquivo ou memória no trecho da falha. O `fix_test_suite.summary.log` indica 0 testes falhando na corrigida, o que reforça o determinismo. |
| F4 | Sim | `fix_test_suite.run.log` está vazio (0 bytes) e `fix_test_suite.summary.log` registra `Number of failing tests: 0` e `Number of uncompilable tests: 0`; test09 não foi removido na filtragem. `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version". |
| F5 | Sim | A mensagem é `ArrayIndexOutOfBoundsException: 0` (erro lógico do código sob teste), não timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. A pilha termina em `RandomStringUtils_ESTest.test09(RandomStringUtils_ESTest.java:92)`. Observação: o `12f.1.trigger.log` está vazio (0 bytes), ou seja, nenhum teste falhou na corrigida. |

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente:  · Data:  · Concorda? 
