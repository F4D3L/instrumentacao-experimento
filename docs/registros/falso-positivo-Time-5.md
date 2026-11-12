# Falso positivo: Time-5

- Executor: Guilherme Celente (pré-preenchido por agente de IA; pendente de confirmação humana) · Data: 12/11/2026
- Testes reveladores (`testes_reveladores`): 2
- Testes analisados: org.joda.time.Period_ESTest::test74, org.joda.time.Period_ESTest::test33

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 | Sim (ambos) | O patch (`5.src.patch`) altera `Period.normalizedStandard(PeriodType)` (hunk `@@ -1625,19 +1625,13 @@`). Em test33 o trace é `PeriodType.setIndexedField(PeriodType.java:690)` <- `Period.withYears(Period.java:896)` <- `Period.normalizedStandard(Period.java:1631)`. Em test74 a asserção falha porque a exceção veio de `org.joda.time.PeriodType.setIndexedField(PeriodType.java:690)` chamado no mesmo fluxo de `normalizedStandard`. O patch está no sentido corrigida->defeituosa: as linhas removidas (`-`) são o código corrigido com `type.isSupported(DurationFieldType.YEARS_TYPE)`; as linhas adicionadas (`+`) são o código defeituoso, que chama `result.withYears(years)` sem checar o suporte. |
| F2 | Sim (ambos) | test74 (gerado sobre a versão corrigida) espera `UnsupportedOperationException` com a mensagem "Unable to normalize as PeriodType is missing either years or months but period has a month/year amount: P117Y29M117W29DT29H0.117S", que é o `throw` presente só no código corrigido (linhas `-` do patch). Na defeituosa o log mostra `java.lang.UnsupportedOperationException: Field is not supported` vinda de `setIndexedField`, em outra classe (`PeriodType`), e `EvoAssertions.assertThrownBy` reporta "Exception was not thrown in org.joda.time.Period but in org.joda.time.PeriodType.setIndexedField(PeriodType.java:690)". test33 (`Period.months(-2150).normalizedStandard(PeriodType.months())`) espera retorno normal (versão corrigida pula `YEARS` não suportado); na defeituosa lança exceção em `withYears`. |
| F3 | Sim (não depende) | Os dois testes usam apenas construtores/métodos puros de `Period` e `PeriodType` com valores fixos (`new Period(117, 29, 117, 29, 29, 0, 0, 117)`, `Period.months(-2150)`, `PeriodType.weeks()`/`months()`). Não há data/hora corrente, fuso, locale, `HashMap`/`HashSet`, rede, arquivos nem dependência de memória; o trace não passa por nenhum desses itens. |
| F4 | Sim | `fix_test_suite.summary.log`: "Number of uncompilable tests: 0" e "Number of failing tests: 0"; `fix_test_suite.run.log` e `fix_test_suite.compile.log` vazios. Nenhum teste removido, e `5f.1.trigger.log` (versão corrigida) está vazio, ou seja, test74 e test33 passam na corrigida. `run_bug_detection.pl.log`: "Found 2 failing tests on buggy version". |
| F5 | Sim | As mensagens são `UnsupportedOperationException: Field is not supported` e `AssertionFailedError: Exception was not thrown in org.joda.time.Period but in ...PeriodType.setIndexedField`. Nenhuma é timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError` ou falta de memória. |

- Decisão do executor: falso_positivo = nao; deteccao_confirmada = pendente (aguarda validação humana)
- Conferente:  · Data:  · Concorda? 
