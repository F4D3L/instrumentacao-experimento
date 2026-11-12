# Falso positivo: Closure-37

- Executor: Guilherme Fadel (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: com.google.javascript.jscomp.parsing.IRFactory_ESTest::test33

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `37b.1.trigger.log`: `--- com.google.javascript.jscomp.parsing.IRFactory_ESTest::test33` / `junit.framework.AssertionFailedError: Expecting exception: IllegalStateException`, em `IRFactory_ESTest.test33(IRFactory_ESTest.java:13135)`. O teste chama `IRFactory.transformTree(...)`, e o patch (`37.src.patch`) altera `IRFactory.java` no hunk `@@ -664,13 +664,9 @@`. O `src.patch` está no sentido corrigida -> defeituosa: as linhas `-` (`if (!bodyNode.isBlock()) {`, `Preconditions.checkState(config.isIdeMode);`, `bodyNode = IR.block();`, `}`) existem só na versão corrigida; na defeituosa o bloco foi removido. O patch também altera `NodeTraversal.java` (`Preconditions.checkState(body.getNext() == null && body.isBlock(), body)` na corrigida), mas esse arquivo não aparece no trace do teste revelador. |
| F2 | Sim | Na suíte filtrada (gerada sobre a corrigida), `test33` monta um `FunctionNode` cujo corpo é um `Name` (não é bloco), com `Config(..., false, ECMASCRIPT3, false)` (modo IDE desligado), e espera `fail("Expecting exception: IllegalStateException")` / `catch(IllegalStateException e)` com `verifyException("com.google.common.base.Preconditions", e)`. Isso é o comportamento da corrigida: `!bodyNode.isBlock()` seguido de `Preconditions.checkState(config.isIdeMode)` com `isIdeMode = false` lança `IllegalStateException`. Na defeituosa o bloco não existe, nenhuma exceção é lançada e o teste falha com `Expecting exception: IllegalStateException`, coerente com o código sem a checagem. |
| F3 | Sim | O teste usa só objetos em memória do Rhino (`AstRoot`, `Name`, `FunctionNode`), um `Config` com `LinkedHashSet` vazio e `ToolErrorReporter`, em chamada única e determinística; sem data/hora, fuso, locale, ordem de `HashMap`/`HashSet` (o `LinkedHashSet` está vazio e mantém ordem), rede, arquivo ou memória. |
| F4 | Sim | `fix_test_suite.run.log` e `fix_test_suite.summary.log` listam como removidos só 4 testes de `NodeTraversal_ESTest` (`test10`, `test00`, `test25`, `test09`, todos `Expecting exception`), e `Number of failing tests: 4`. `IRFactory_ESTest::test33` não aparece como removido e consta na suíte filtrada. `37f.1.trigger.log` está vazio (0 bytes): nenhum teste falha na corrigida. |
| F5 | Sim | A falha é `AssertionFailedError: Expecting exception: IllegalStateException`, uma divergência de comportamento do código sob teste; não há timeout, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória no trigger log. `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version". |

Observações:
- O trigger log tem um único teste (`test33`), então a análise cobre 100% dos reveladores.
- Os 4 testes de `NodeTraversal_ESTest` removidos na filtragem falham na corrigida e não são reveladores. Isso coincide com o hunk de `NodeTraversal.java` (mensagem em `checkState`), mas não influencia a decisão.
- Ponto para o humano: a asserção de `test33` é apenas "lança `IllegalStateException`" (sem mensagem), e o patch é uma remoção de checagem; confirme a leitura do sentido do patch.

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente: 
