# Conferência cruzada: testes de Lucas Reali

Conferente designado: Guilherme Fadel — pré-conferência feita por agente de IA, pendente de validação humana

- Data da conferência: 12/11/2026
- Base: só arquivos versionados e `git` (nada foi reexecutado). O docker foi usado apenas para ler os patches do Defects4J (`cat $D4J_HOME/framework/projects/<P>/patches/<id>.src.patch`), para C5/C7.
- Todos os 5 testes foram executados por um agente de IA; esta conferência também é de agente. A leitura foi cética: números do registro foram recalculados a partir de `deteccao/`, `cobertura/`, `tempos.csv` e `cobertura_falha.txt`.
- Resultado sugerido por teste (a gravar em `conferencia` somente após validação humana; `dados/registro.csv` NÃO foi alterado):

| Teste | Resultado sugerido |
|---|---|
| Lang-31 (ordem 1) | ok:Guilherme Fadel |
| Chart-2 (ordem 2) | ok:Guilherme Fadel |
| Closure-75 (ordem 3) | divergente:Guilherme Fadel:C5 |
| Time-18 (ordem 4) | ok:Guilherme Fadel |
| Math-63 (ordem 5) | ok:Guilherme Fadel (com ressalvas C1 e C4 abaixo, sem divergência) |

## Verificações comuns a todos os testes

- Os 5 manifestos têm o mesmo `id_imagem` (`sha256:45031972...446e`), `cpus_limite=2`, `memoria_limite=6g`, `memoria_cgroup=6442450944`, Java 1.8.0_452, Defects4J `a83e479...`, `evosuite_sha256=939c0c76...`, `evosuite_config_sha256=7349236d...` (o valor combinado) e `tz=America/Los_Angeles`. `nproc_visto=10` é esperado (decisão do usuário: o limite é por cota de cgroup).
- Semente: a do manifesto, a de `suites/logs/<P>.<id>f.log` (`-s`) e a de `dados/sorteio/atribuicao.csv` são idênticas nos 5 testes. Orçamento `-b 360` (360 × 1 classe) nos 5 logs, o que cobre o D4 por evidência indireta.
- Todos os `tempos.csv` têm código de saída 0 em todas as etapas, `etapas_com_erro` vazio no registro, e `tempo_total_s` do registro = soma dos segundos (286, 291, 417, 322, 376).
- Cada `resultados/<Falha>` aparece em um único commit (só adição de arquivos). `dados/registro.csv` tem 28 campos em todas as linhas.
- Cronologia (C3): ver tabela abaixo; a ordem sorteada é respeitada e os horários do manifesto (UTC-8) batem com os commits (UTC-3, diferença de 5 h).

| Ordem | Falha | `data_hora` do manifesto | Commit | Data do commit |
|---|---|---|---|---|
| 1 | Lang-31 | 06:29:09 -08:00 (= 11:29 -03:00) | 889cdb2 | 11:34:37 -0300 |
| 2 | Chart-2 | 07:11:48 -08:00 (= 12:11 -03:00) | 34bc6ef | 12:17:12 -0300 |
| 3 | Closure-75 | 09:10:27 -08:00 (= 14:10 -03:00) | 95324cb | 14:18:08 -0300 |
| 4 | Time-18 | 10:04:47 -08:00 (= 15:04 -03:00) | e3be2e2 | 15:10:35 -0300 |
| 5 | Math-63 | 10:57:36 -08:00 (= 15:57 -03:00) | dd85dbc | 16:05:44 -0300 |

## Teste 1: Lang-31 (ordem 1) — sugerido: ok

| Item | Resultado | Evidência / observação |
|---|---|---|
| C1 | ok | `ambiente-Lucas-Reali.md`, coluna Lang-31: A1-A10 e D1-D5 `ok`. Observação: a data/hora desta coluna (11:29) está em horário de Brasília, enquanto as demais colunas usam America/Los_Angeles; o instante é o mesmo do manifesto (06:29 -08:00). Só formato, sem efeito |
| C2 | ok | Manifesto completo; semente 432222207 = `atribuicao.csv`; `classes_modificadas: StringUtils` |
| C3 | ok | Primeiro teste; commit 889cdb2 anterior a todos os demais do Lucas |
| C4 | ok | `bug_detection`: Lang,31f,Pass,0 → `Pass`/0/0. `coverage`: 1170/1131/1055/1023 = registro (96,67%). `cobertura_falha.txt`: parcial (4 de 6) = registro. 427 testes gerados e finais, 0 removidos (`fix_test_suite.summary.log`) |
| C5 | n/a | Não detectou (`nao_se_aplica`) |
| C6 | ok | `Pass`; `fix_test_suite.run.log` vazio (0 bytes), resumo: 0 não compilam, 0 falham; nenhuma remoção em massa |
| C7 | n/a | Classificação automática (`parcial`), não indeterminada. Verificação extra: no patch, as linhas-alvo 1446, 1447, 1452, 1454, 1455 e o trecho final cabem no hunk `@@ -1443,21`; as linhas 1454 e 1455 (ramo de caractere suplementar) têm hits=0, o que sustenta `parcial` |
| C8 | ok | `git log` da pasta: só 889cdb2, apenas adições |

## Teste 2: Chart-2 (ordem 2) — sugerido: ok

| Item | Resultado | Evidência / observação |
|---|---|---|
| C1 | ok | Coluna Chart-2: tudo `ok`; A7 cita o commit 889cdb2 do Lang-31 (existe) |
| C2 | ok | Semente 1123060191 = `atribuicao.csv`; classe `DatasetUtilities` |
| C3 | ok | Commit 34bc6ef posterior ao de Lang-31 e anterior ao de Closure-75; manifesto 07:11 posterior a 06:29 |
| C4 | ok | `bug_detection`: Chart,2f,Pass,0; `coverage`: 808/790/548/512 = registro (97,77%); `cobertura_falha`: total 12/12 = registro; 149 gerados, 0 removidos |
| C5 | n/a | Não detectou |
| C6 | ok | `Pass`; `fix_test_suite.run.log` vazio; 0 removidos |
| C7 | n/a | Automática (`total`). Verificação extra: as linhas-alvo 755, 758-760, 764, 767 e 1249, 1252-1254, 1258, 1261 coincidem com as linhas `-` dos dois hunks do patch; todas com hits maiores que 0 |
| C8 | ok | Só o commit 34bc6ef |

## Teste 3: Closure-75 (ordem 3) — sugerido: divergente:Guilherme Fadel:C5

| Item | Resultado | Evidência / observação |
|---|---|---|
| C1 | ok | Coluna Closure-75: tudo `ok` |
| C2 | ok | Semente 1156291063 = `atribuicao.csv`; classe `NodeUtil` |
| C3 | ok | Commit 95324cb entre Chart-2 e Time-18 |
| C4 | ok | `bug_detection`: Closure,75f,Fail,1 → `Fail`/1/1. `coverage`: 827/656/893/626 = registro (79,32%). `cobertura_falha`: total 3/3 = registro; 783 testes, 0 removidos |
| C5 | PROBLEMA | Detectou (`deteccao_automatica=1`), mas **não existe `docs/registros/falso-positivo-Closure-75.md`** (nem no commit 95324cb nem depois). O registro está com `falso_positivo=pendente`, `deteccao_confirmada=pendente` e `observacoes` vazio, enquanto Lang-12, Time-13, Chart-17 e Math-63 já têm o checklist e a anotação de FP pré-avaliado. É preciso criar o checklist (executor) antes de poder concordar com a decisão. Avaliação independente preliminar, só para ajudar o executor (não substitui o checklist): `75b.1.trigger.log` mostra `NodeUtil_ESTest::test069`, `AssertionFailedError: expected null, but was:<0.0>` em `assertNull`; o teste é `NodeUtil.getStringNumberValue("\u000B")` + `assertNull`. O patch remove, da versão corrigida para a defeituosa, o `if (rawJsString.contains("\u000b")) return null;`, então a corrigida devolve `null` e a defeituosa `0.0`; isso é coerente com F1 e F2. `75f.1.trigger.log` tem 0 bytes e `fix_test_suite.run.log` está vazio (F4); não há dependência de data, locale, rede ou arquivo (F3); a mensagem é de asserção de valor (F5). Tudo indica detecção verdadeira, mas a decisão formal é do executor |
| C6 | n/a | Detectou |
| C7 | n/a | Automática (`total`). Verificação extra: linhas-alvo 313, 315 e 378 = linhas `-` do patch; hits 11, 1 e 1 |
| C8 | ok | Só o commit 95324cb |

## Teste 4: Time-18 (ordem 4) — sugerido: ok

| Item | Resultado | Evidência / observação |
|---|---|---|
| C1 | ok | Coluna Time-18: tudo `ok` (nproc 10 anotado como esperado) |
| C2 | ok | Semente 96211347 = `atribuicao.csv`; classe `GJChronology` |
| C3 | ok | Commit e3be2e2 entre Closure-75 e Math-63 |
| C4 | ok | `bug_detection`: Time,18f,Pass,0; `coverage`: 323/257/158/112 = registro (79,57%); `cobertura_falha`: parcial 7/8 = registro; 35 testes, 0 removidos |
| C5 | n/a | Não detectou |
| C6 | ok | `Pass`; `fix_test_suite.run.log` vazio; 0 removidos |
| C7 | n/a | Automática (`parcial`). A única linha com hits=0 é a 376 (`throw ex` do ramo de 29/02 após a mudança de calendário), o que sustenta `parcial`. Ressalva menor: a linha 378 (chave de fechamento do `catch`) consta como executável no relatório do Cobertura; não afeta a classificação e não pôde ser checada sem o código-fonte |
| C8 | ok | Só o commit e3be2e2 |

## Teste 5: Math-63 (ordem 5) — sugerido: ok (com ressalvas, sem divergência)

| Item | Resultado | Evidência / observação |
|---|---|---|
| C1 | ok (ressalva) | Coluna Math-63: tudo `ok`. Ressalva: o campo Data/hora diz `12/11/2026 11:57`, mas o manifesto é 10:57:36 -08:00 e o commit é de 16:05 -03:00 (= 11:05 -08:00); 11:57 -08:00 seria posterior ao commit. Parece erro de digitação (11:57 em vez de 10:57). Sugestão: o executor corrigir o campo |
| C2 | ok | Semente 570411696 = `atribuicao.csv`; classe `MathUtils` |
| C3 | ok | Último teste; commit dd85dbc é o mais recente do Lucas |
| C4 | ok (ressalva) | `bug_detection`: Math,63f,Fail,1 → `Fail`/1/1. `coverage`: 487/479/435/424 = registro (98,36%). `cobertura_falha`: total 1/1 (linha 417) = registro e = linha `-` do patch. Ressalva de contagem: `testes_gerados=187`, `removidos_falham=1`, `testes_finais=188` (o final é maior que o gerado). Causa verificada: o `fix_test_suite.pl` deixa um método vazio `@Test public void test078() {}` e o comentário `// @Test(timeout = 4000)` do método removido, e o `contar_testes` conta `@Test` por texto (188 ocorrências no arquivo final; 187 no gerado). É artefato sistemático do script (o mesmo padrão aparece em Lang-37, Closure-37 e Time-23), não erro de digitação do executor; `testes_finais` deve ser lido como contagem de anotações, não de testes executáveis (186 reais + 1 stub vazio) |
| C5 | ok (concordo) | Revisão independente de `falso-positivo-Math-63.md`. `63b.1.trigger.log`: `MathUtils_ESTest::test057`, `assertFalse` na linha 473; `63f.1.trigger.log` com 0 bytes. O teste é `doubleArray0[0] = (double) Float.NaN; MathUtils.equals(doubleArray0, doubleArray0); assertFalse(...)`. O patch (corrigida para defeituosa) troca `return equals(x, y, 1);` por `return (Double.isNaN(x) && Double.isNaN(y)) \|\| x == y;`, de modo que NaN com NaN é `false` na corrigida e `true` na defeituosa: coerente com F2. F1: o topo da pilha é a asserção, e a ligação com o método alterado vem da leitura do código (a versão `double[]` delega ao `equals(double,double)`); a justificativa "Sim (indireto)" está honesta e adequada. F3: teste determinístico, sem tempo, locale ou rede. F4: `test057` não está no `fix_test_suite.run.log` (só `test078`, de `mulAndCheck`, removido, sem relação). F5: `AssertionFailedError` de valor. Concordo: `falso_positivo=nao`, `deteccao_confirmada=1`. O campo "Conferente" do arquivo está em branco e deve ser preenchido após a validação humana |
| C6 | n/a | Detectou |
| C7 | n/a | Automática (`total`); linha 417 = única linha `-` do hunk `@@ -414,7` |
| C8 | ok | Só o commit dd85dbc |

## Pendências para o executor e para a validação humana

1. Closure-75: criar `docs/registros/falso-positivo-Closure-75.md`, atualizar `falso_positivo`/`deteccao_confirmada` e `observacoes` na linha do registro. Depois disso o C5 pode ser reavaliado.
2. Math-63: corrigir a data/hora do `ambiente-Lucas-Reali.md` (11:57 para 10:57) e preencher o campo "Conferente" do checklist de FP após a validação humana.
3. Registrar para o grupo a nota sobre `testes_finais` (stub vazio e `@Test` comentado contados), para a análise não tratá-lo como erro de dado.
4. Esta pré-conferência foi feita por agente de IA; nenhuma coluna `conferencia` foi preenchida.
