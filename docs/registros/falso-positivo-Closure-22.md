# Falso positivo: Closure-22

- Executor: Gabriel Conti (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: com.google.javascript.jscomp.CheckSideEffects_ESTest::test5

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `22b.1.trigger.log`: `java.lang.NullPointerException at com.google.javascript.jscomp.NodeUtil.isExpressionResultUsed(NodeUtil.java:3113) at com.google.javascript.jscomp.CheckSideEffects.visit(CheckSideEffects.java:130) at ...CheckSideEffects_ESTest.test5(CheckSideEffects_ESTest.java:1437)`. `CheckSideEffects.visit` é o método alterado em `22.src.patch` (hunk `@@ -98,20 +98,44 @@`). O patch está no sentido corrigida -> defeituosa: a linha `-    if (n.isExprResult() \|\| n.isBlock()) {` (retorno antecipado, presente na corrigida) é substituída na defeituosa por checagens sobre `parent` (`parent.getType() == Token.COMMA`, `parent.getType() != Token.EXPR_RESULT && parent.getType() != Token.BLOCK`), e `NodeUtil.isExpressionResultUsed(n)` passa a ser alcançada onde antes havia o retorno. |
| F2 | Sim | O teste chama `checkSideEffects0.visit(nodeTraversal0, node0, node0)` com o nó retornado por `compiler0.parseInputs()` como `n` e como `parent`. Na corrigida, o retorno antecipado `n.isExprResult() \|\| n.isBlock()` evita a chamada e o teste passa (`22f.1.trigger.log` vazio, 0 bytes). Na defeituosa, esse retorno não existe e a execução segue até `NodeUtil.isExpressionResultUsed`, que lança `NullPointerException`. Ressalva: não executei o teste para confirmar o tipo do nó raiz; a coerência é inferida do patch e dos dois logs (corrigida sem falha; defeituosa com NPE em `CheckSideEffects.java:130`). |
| F3 | Sim | `test5` só cria `Compiler`, `CompilerOptions`, lista vazia e `NodeTraversal`, e chama `visit`. Não há uso de data/hora, fuso, locale, `HashMap`/`HashSet`, rede, arquivos ou memória no corpo do teste (busca por `Date`, `Random`, `Locale`, `HashMap` e `File` só encontra `LinkedList<JSSourceFile>`, o tipo da lista vazia). |
| F4 | Sim | `fix_test_suite.summary.log`: "Number of uncompilable test classes: 0", "Number of uncompilable tests: 0", "Number of failing tests: 0"; `fix_test_suite.run.log` e `fix_test_suite.compile.log` vazios (0 bytes), logo `test5` não foi removido. `22f.1.trigger.log` vazio. |
| F5 | Sim | A mensagem é `NullPointerException` em código do Closure (`NodeUtil`/`CheckSideEffects`), sem timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version". |

Observação: o trigger log tem um único teste (`test5`), então a análise cobre 100% dos reveladores.

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente: 
