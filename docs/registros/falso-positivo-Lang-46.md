# Falso positivo: Lang-46

- Executor: Leonardo Ceccon (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 1
- Testes analisados: org.apache.commons.lang.StringEscapeUtils_ESTest::test06

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim | `46b.1.trigger.log`: `AssertionFailedError: expected:<h.[]/&\"re\f x!T(B#J> but was:<h.[\]/&\"re\f x!T(B#J>` em `StringEscapeUtils_ESTest.test06(StringEscapeUtils_ESTest.java:83)`. O teste chama `StringEscapeUtils.escapeJava(String)`, método alterado em `46.src.patch` (hunk `@@ -83,7 +83,7 @@`, além de `escapeJavaStyleString`). O patch está no sentido corrigida -> defeituosa: as linhas `-` (`escapeJavaStyleString(str, false, false)`, `if (escapeForwardSlash) { out.write('\\'); }` no `case '/'`) são da corrigida; na defeituosa o `case '/'` sempre escreve `\` antes de `/`. |
| F2 | Sim | Na suíte filtrada (gerada sobre a corrigida), `test06` faz `escapeJava("h./&\"re\f x!T(B#J")` e espera `"h./&\\\"re\\f x!T(B#J"`, isto é, `/` sem barra invertida, como na corrigida (`escapeJava` passa `escapeForwardSlash=false`). Valor obtido na defeituosa: `h.\/&...`, com a barra invertida extra, coerente com o `case '/'` sem condição do código defeituoso. |
| F3 | Sim | O teste só transforma uma string literal em memória (uma chamada determinística a `escapeJava`); não usa data/hora, fuso, locale, `HashMap`/`HashSet`, rede, arquivos nem memória. |
| F4 | Sim | `fix_test_suite.summary.log`: "Number of uncompilable tests: 0" e "Number of failing tests: 0"; `fix_test_suite.run.log` e `fix_test_suite.compile.log` estão vazios (0 bytes), logo `test06` não foi removido. `46f.1.trigger.log` vazio (0 bytes): nenhum teste falha na corrigida. |
| F5 | Sim | A falha é `AssertionFailedError` de valor de string, sem timeout, `ClassNotFoundException`, `NoClassDefFoundError` nem falta de memória. `run_bug_detection.pl.log`: "Found 1 failing tests on buggy version". |

Observação: o trigger log tem um único teste (`test06`), então a análise cobre 100% dos reveladores.

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente:
