# Conferência cruzada: testes de Gabriel Conti

Conferente designado: Thiago Akimoto — pré-conferência feita por agente de IA, pendente de validação humana

- Data: 12/11/2026
- Método: só arquivos versionados e `git`; nada foi reexecutado. O Docker foi usado apenas para ler os patches (`cat $D4J_HOME/framework/projects/<P>/patches/<id>.src.patch`).
- Todos os testes foram executados por agente de IA; esta conferência também é de agente. Nada aqui substitui a validação humana.
- `dados/registro.csv` e demais arquivos não foram alterados. A coluna `conferencia` fica para o conferente humano preencher.

## Resumo

| Teste | Falha | Resultado sugerido |
|---|---|---|
| 1 | Math-45 | ok:Thiago Akimoto |
| 2 | Closure-22 (substituta de Closure-88) | ok:Thiago Akimoto |
| 3 | Time-23 | divergente:Thiago Akimoto:C4 (menor, só a contagem `testes_finais`) |
| 4 | Lang-25 | ok:Thiago Akimoto |
| 5 | Chart-8 | ok:Thiago Akimoto |

Verificações comuns a todos os testes:

- C2: `id_imagem` = `sha256:45031972…` em todos; Java 1.8.0_452; Defects4J `a83e4792…` (v2.0.1); EvoSuite SHA-256 `939c0c76…` e config SHA-256 `7349236d…` (iguais ao manual, seção 1, e ao `docs/checklist-ambiente.md`); `tz` = America/Los_Angeles; `cpus_limite` = 2; `memoria_limite` = 6g; `memoria_cgroup` = 6442450944; `nproc_visto` = 10 (esperado, conforme nota do usuário). `orcamento_total_s` = 360 e uma única classe modificada em cada manifesto, de acordo com `n_classes = 1`. Sementes iguais às de `dados/sorteio/atribuicao.csv` (para Closure-22, a de Closure-88, herdada via `substituicoes.csv`).
- C3: datas dos manifestos (UTC): Math-45 15:02:51, Closure-88 16:50:02, Closure-22 16:52:30, Time-23 17:49:01, Lang-25 18:48:17, Chart-8 19:24:56. Os commits (-0300) também crescem: `eebedca` 12:06, `7c89ffb` 13:51, `31cd6c3` 14:02, `1d7da59` 14:55, `57732d3` 15:50, `ad836fa` 16:30. Cada commit vem depois do início do respectivo manifesto (12:02 -0300 etc.). Cada teste foi iniciado depois do commit do anterior. As ordens 1 de todos os colegas vêm antes das ordens 2, e assim por diante.
- C8: `git log --format=%h -- resultados/<Falha>` retorna um único commit por pasta (`eebedca`, `7c89ffb` para Closure-88, `31cd6c3`, `1d7da59`, `57732d3`, `ad836fa`). Os commits só adicionam arquivos em `resultados/` (status `A`); os arquivos modificados (`M`) são apenas os compartilhados esperados (`dados/registro.csv`, `docs/registros/ambiente-Gabriel-Conti.md`, e, no commit de Closure-88, `substituicoes.csv`, `registro-substituidas.csv` e os registros de decisões). `git status` não mostra alteração em arquivo rastreado. Os tempos dos logs de geração, detecção e cobertura (por exemplo `Start test generation 07:03:01`, `Start executing test suites 07:04:28`) coincidem com as linhas de `tempos.csv`. Limite desta checagem: `git log` só prova que não houve edição depois do commit.
- C1: a coluna de cada teste em `docs/registros/ambiente-Gabriel-Conti.md` está preenchida, com A1-A10 e D1-D5 `ok` e a evidência indireta de D4 (`-b 360`, `-s <semente>` em `suites/logs/<P>.<id>f.log`, SHA da config), conforme a decisão do usuário. Conferi `-b 360` e a semente nos cinco `suites/logs/*.log`.
- C7: não se aplica a nenhum teste (nenhum `indeterminado` e nenhuma classificação à mão). Mesmo assim fiz verificação independente de `cobertura_falha` cruzando o patch com `coverage.xml` (detalhes em cada teste).

## Teste 1: Math-45 (ordem 1)

| Item | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna "Teste 1" completa, todos `ok`; D4 por evidência indireta (`Math.45f.log`: `-b 360`, `-s 2061223299`). |
| C2 | ok | Manifesto conforme os valores comuns; semente 2061223299 = `atribuicao.csv`; classe `OpenMapRealMatrix` (1 classe). |
| C3 | ok | Manifesto 15:02:51Z; commit `eebedca` 12:06:37 -0300; primeiro da lista do pesquisador. |
| C4 | ok | `bug_detection`: Fail, `num_trigger` 1 = `resultado_d4j` Fail / `testes_reveladores` 1 / `deteccao_automatica` 1. `coverage`: 100/97/24/24 = `linhas_*` 100/97, `ramos` 24/24, 97,00 %. Testes: 10 gerados e 10 finais conferem com a contagem de `@Test` nos dois `.tar.bz2`. `tempo_total_s` 147 = 64+33+30+20+0. `cobertura_falha` = total = `cobertura_falha.txt`. |
| C5 | ok, concordo | Revisão independente abaixo. |
| C6 | não se aplica | Detectou. |
| C7 | não se aplica | `total` automático; verificado à mão: o patch remove as linhas 50-53 da corrigida (`long lRow...` até o `throw`), e `45f.1.xml` tem linhas 50, 51 e 52 com 29 hits e a 53 com 1 hit. |
| C8 | ok | Um único commit na pasta. |

Revisão de C5 (falso positivo):

- Teste revelador: `OpenMapRealMatrix_ESTest::test3`. O `45b.1.trigger.log` tem 1 teste (`AssertionFailedError: Expecting exception: IllegalArgumentException`, linha 77). O `45f.1.trigger.log` tem 0 bytes.
- F1: o teste chama `new OpenMapRealMatrix(2145707400, 492)`, construtor alterado pelo patch (o patch remove, da corrigida para a defeituosa, a checagem `lRow * lCol >= Integer.MAX_VALUE` com `NumberIsTooLargeException`). Confirmado no patch.
- F2: o comentário do teste ("1,055,688,040,800 is larger than... 2,147,483,647") corresponde à checagem que só existe na corrigida; 2145707400 × 492 = 1.055.688.040.800. Coerente.
- F3: só aritmética com literais inteiros; sem data, fuso, locale, hash, rede, arquivo. Na defeituosa o construtor não aloca memória proporcional às dimensões (o teste chegou ao `fail` sem erro de memória). Confirmado.
- F4: `fix_test_suite.summary.log` com 0 não compilam e 0 falham; `run.log` e `compile.log` vazios.
- F5: falha de asserção do próprio teste, sem timeout nem erro de classe ou memória.
- Concordo: `falso_positivo = nao`, `deteccao_confirmada = 1`. Falta só a confirmação humana.

## Teste 2: Closure-22, substituta de Closure-88 (ordem 2)

| Item | Resultado | Evidência |
|---|---|---|
| C1 | ok | Colunas "Closure-88" e "Closure-22" preenchidas. Na coluna de Closure-88, D4 é "não aplicável" e D5 é `falha` (etapa `gerar` com código 1), exceção justificada pela substituição. Closure-22: tudo `ok` com D4 indireto (`Closure.22f.log`: `-b 360`, `-s 1061168894`). |
| C2 | ok | Manifesto conforme os valores comuns; classe `CheckSideEffects` (1 classe); semente 1061168894 = a de Closure-88 em `atribuicao.csv` e a de `substituicoes.csv`. |
| C3 | ok | Closure-88 16:50:02Z (commit `7c89ffb` 13:51:52 -0300) e Closure-22 16:52:30Z (commit `31cd6c3` 14:02:46 -0300). Ocupa a ordem 2, entre Math-45 e Time-23. |
| C4 | ok | `bug_detection`: Fail, `num_trigger` 1 = registro (Fail/1/1). `coverage`: 67/50/38/33 = registro, 74,63 %. 10 gerados e 10 finais conferem. `tempo_total_s` 323 = 203+52+40+28+0. `cobertura_falha` total = `cobertura_falha.txt`. |
| C5 | ok, concordo | Revisão independente abaixo. |
| C6 | não se aplica | Detectou. |
| C7 | não se aplica | `total` automático; verificado: `22f.1.xml` tem hits > 0 nas linhas 101, 107, 111 e 115 (17, 10, 10, 6). Observação cosmética: `cobertura_falha.txt` lista a linha 107 duas vezes (dois blocos do patch resolvem para a mesma linha pela regra da seção 5.2, item 3), por isso `linhas_consideradas=5` para 4 linhas distintas. Não altera a classificação nem nenhuma coluna do registro. |
| C8 | ok | Um único commit em `resultados/Closure-22` e outro em `resultados/Closure-88`. |

Verificação da substituição:

- `resultados/Closure-88`: `tempos.csv` mostra `gerar` com código 1 em 7 s e nenhuma etapa seguinte além de `cobertura_falha` (0 s, `nenhuma`, sem relatório). Não há `deteccao/`, `cobertura/` nem `suite-gerada.tar.bz2`: o EvoSuite não foi executado. `logs/gerar.log` termina em `45 errors`, `BUILD FAILED`, `Compile failed` e `Cannot compile! at /defects4j/framework/bin/gen_tests.pl line 230`. `grep -c unmappable` = 45, ou seja, todos os 45 erros são "unmappable character for encoding ASCII". A causa declarada ("o projeto não compila no ambiente") confere e é igual à de Math-101, que o manual (seção 8) prevê como motivo técnico alheio à ferramenta.
- `dados/sorteio/substituicoes.csv`: linha `Gabriel Conti,2,Closure-88,Closure-22,8,1061168894,Thiago Akimoto,...`. Em `amostra.csv`, Closure-22 é a `posicao_sorteio` 8, a primeira reserva de Closure (as demais: 9 = Closure-7, 10 = Closure-74). Semente e conferente herdados corretamente.
- `dados/registro-substituidas.csv` tem a linha de Closure-88 (`sem_suite`, `etapas_com_erro = gerar`, 7 s), e `dados/registro.csv` não tem Closure-88, mantendo n = 35. Os números batem com `resultados/Closure-88`. `registro.csv` tem 28 campos em todas as linhas.
- Decisão registrada em `docs/03-semana3-instrumentacao.md` e `docs/04-semana4-resultados.md` (commit `7c89ffb`), antes da execução da substituta.
- Ressalva: a substituição foi decidida pela falha da etapa `gerar` no primeiro e único teste de Closure-88, e o manual manda "avisar o grupo". As notas do usuário de 12/11/2026 registram a decisão. Peço à validação humana que confirme que o grupo foi avisado.

Revisão de C5 (falso positivo):

- Teste revelador: `CheckSideEffects_ESTest::test5`. O `22b.1.trigger.log` tem 1 teste (`NullPointerException` em `NodeUtil.isExpressionResultUsed(NodeUtil.java:3113)`, chamado de `CheckSideEffects.visit(CheckSideEffects.java:130)`). O `22f.1.trigger.log` tem 0 bytes.
- F1: `CheckSideEffects.visit` é o método alterado pelo patch (que, da corrigida para a defeituosa, troca `if (n.isExprResult() || n.isBlock()) return;` por checagens sobre `parent`). Confirmado.
- F2: o teste chama `checkSideEffects0.visit(nodeTraversal0, node0, node0)` (mesmo nó como `n` e `parent`). Na corrigida, o retorno antecipado `n.isBlock()`/`isExprResult()` evita o caminho; na defeituosa o fluxo chega a `isExpressionResultUsed` com nó sem pai e lança NPE. É coerente, mas é uma inferência do patch e dos logs (o executor admite não ter confirmado o tipo do nó). O cenário é artificial (visit chamado com o nó raiz como pai dele mesmo), porém a diferença de comportamento vem exatamente do trecho corrigido.
- F3: o teste cria `Compiler`, `CompilerOptions`, lista vazia e `NodeTraversal`; sem dependência de data, fuso, locale, hash, rede, arquivo ou memória.
- F4: `fix_test_suite.summary.log` com 0 não compilam e 0 falham; `run.log` vazio.
- F5: NPE em código do Closure; sem timeout nem erro de infraestrutura.
- Concordo: `falso_positivo = nao`, `deteccao_confirmada = 1`, com a ressalva de F2 acima. Falta só a confirmação humana.

## Teste 3: Time-23 (ordem 3)

| Item | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna "Time-23" completa, todos `ok`; D4 indireto (`Time.23f.log`: `-b 360`, `-s 1592096377`). |
| C2 | ok | Manifesto conforme os valores comuns; semente 1592096377 = `atribuicao.csv`; classe `DateTimeZone` (1 classe). |
| C3 | ok | Manifesto 17:49:01Z; commit `1d7da59` 14:55:51 -0300; depois de Closure-22. |
| C4 | problema (menor) | Conferem: `bug_detection` Pass / `num_trigger` 0 (registro Pass/0/0); `coverage` 338/289/162/130, 85,50 %; `cobertura_falha` total (12/12) = `cobertura_falha.txt`; `tempo_total_s` 342 = 200+71+42+29+0; gerados 51 = `@Test` do `suite-gerada.tar.bz2`. **Não confere:** `testes_finais = 52`. O `fix_test_suite.summary.log` removeu 1 teste (`DateTimeZone_ESTest::test11`), o que deixa 50 testes ativos. O 52 vem do `registrar.py` (`contar_testes`), que conta a ocorrência de `@Test` por texto: no `.java` filtrado ela aparece 52 vezes porque o Defects4J substitui o teste removido por um stub vazio `@Test public void test11() {}` e deixa o original comentado (`//   @Test(timeout = 4000)`), e os dois entram na conta. O valor correto é 50 (ou 51, se o stub for contado). O executor já registrou a inconsistência em `observacoes`. Não afeta `resultado_d4j`, `testes_reveladores` nem cobertura, mas a coluna `testes_finais` está superestimada, e o mesmo efeito vale para qualquer teste com remoção na filtragem (Lang-37, Closure-37, Time-20 e Math-63 foram citados). Decisão do grupo pendente (corrigir `testes_finais` ou ajustar a contagem antes da análise). |
| C5 | não se aplica | Não detectou (`falso_positivo = nao_se_aplica`). |
| C6 | ok | `bug_detection` = Pass (não é Broken); `23b.1.trigger.log` e `23f.1.trigger.log` com 0 bytes; `run_bug_detection.pl.log` sem falha. Remoção na filtragem: 1 teste em 51 (`test11`, `AssertionFailedError` em `assertTrue(dateTimeZone0.isFixed())` após `DateTimeZone.setProvider(new UTCProvider())`, classificado pelo Defects4J como "flaky method"). Não é remoção em massa nem erro de infraestrutura (0 não compilam). |
| C7 | não se aplica | `total` automático; verificado: o patch remove 5 `map.put` (WET, CET, MET, ECT, EET) e altera `IET`, `AGT`, `IST`, `VST`; `23f.1.xml` mostra linhas 564-568, 577, 580, 582, 584, 585, 587 e 589 com 5 hits. As 12 linhas de `cobertura_falha.txt` conferem. |
| C8 | ok | Um único commit na pasta. O `.bak` do tar é produto normal de `fix_test_suite.pl`. |

## Teste 4: Lang-25 (ordem 4)

| Item | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna "Lang-25" completa, todos `ok`; D4 indireto (`Lang.25f.log`: `-b 360`, `-s 2130647482`). A observação "pull não executado" em A5 é aceitável (repositório local sem alterações em `ambiente/`, `scripts/`, `dados/sorteio/`). |
| C2 | ok | Manifesto conforme os valores comuns; semente 2130647482 = `atribuicao.csv`; classe `EntityArrays` (1 classe). |
| C3 | ok | Manifesto 18:48:17Z; commit `57732d3` 15:50:12 -0300; depois de Time-23. |
| C4 | ok | `bug_detection` Pass / `num_trigger` 0 = registro; `coverage` 26/26/2/2, 100,00 %; 11 gerados e 11 finais; `tempo_total_s` 80 = 16+25+23+16+0; `cobertura_falha` total = `cobertura_falha.txt`. |
| C5 | não se aplica | Não detectou. |
| C6 | ok | `bug_detection` = Pass; os dois `trigger.log` com 0 bytes; filtragem sem remoção (0/0, `run.log` e `compile.log` vazios). A geração terminou em cerca de 6 s (`Start 10:48:27`, `End 10:48:33`), bem abaixo do orçamento de 360 s, o que é esperado: o EvoSuite para quando cobre todos os objetivos de uma classe com 26 linhas e 2 ramos (100 % de cobertura). |
| C7 | não se aplica | `total` automático; verificado: o patch altera a tabela `ISO8859_1_ESCAPE` (hunk `@@ -71,33 +71,33 @@`, só linhas de elementos do inicializador, não executáveis individualmente no Cobertura). Pela regra 3 da seção 5.2 usa-se a próxima linha executável do arquivo, a 130 (`hits=1`, execução do inicializador estático). Classificação correta pelas regras, embora baseada em 1 única linha. |
| C8 | ok | Um único commit na pasta. |

## Teste 5: Chart-8 (ordem 5)

| Item | Resultado | Evidência |
|---|---|---|
| C1 | ok | Coluna "Chart-8" completa, todos `ok`; D4 indireto (`Chart.8f.log`: `-b 360`, `-s 606828139`). |
| C2 | ok | Manifesto conforme os valores comuns; semente 606828139 = `atribuicao.csv`; classe `Week` (1 classe). |
| C3 | ok | Manifesto 19:24:56Z; commit `ad836fa` 16:30:52 -0300; depois de Lang-25. |
| C4 | ok | `bug_detection` Fail / `num_trigger` 1 = registro (Fail/1/1); `coverage` 160/156/68/64, 97,50 %; 31 gerados e 31 finais; `tempo_total_s` 275 = 195+34+28+18+0; `cobertura_falha` total = `cobertura_falha.txt` (linha 175, 3 hits). O commit também reescreveu a linha de Lang-61 em `registro.csv` só para acrescentar o `\n` final que faltava no arquivo (conteúdo idêntico). |
| C5 | ok, concordo | Revisão independente abaixo. |
| C6 | não se aplica | Detectou. |
| C7 | não se aplica | `total` automático; verificado: o patch altera só a linha 175 da corrigida (`this(time, zone, Locale.getDefault());`); `8f.1.xml` tem a linha 175 com 3 hits. Classificação baseada em 1 linha. |
| C8 | ok | Um único commit na pasta. |

Revisão de C5 (falso positivo):

- Teste revelador: `Week_ESTest::test12`. O `8b.1.trigger.log` tem 1 teste (`AssertionFailedError: Expecting exception: IllegalArgumentException`, linha 357). O `8f.1.trigger.log` tem 0 bytes.
- F1: o stack trace não passa por `Week` (a falha é o `fail(...)` do teste), mas a linha anterior é `new Week(mockDate0, (TimeZone) null)`, o construtor alterado pelo patch (da corrigida para a defeituosa, `zone` é trocado por `RegularTimePeriod.DEFAULT_TIME_ZONE`). Resposta "Sim" aceitável, pois o patch inteiro é esse construtor.
- F2: o teste espera `IllegalArgumentException` ("Null 'zone' argument.") para zona `null`: comportamento da corrigida, que repassa a zona ao construtor de 3 argumentos que a valida. Na defeituosa a zona é ignorada, não há exceção e o teste cai no `fail`. Coerente.
- F3: usa `MockDate` (data simulada pelo EvoSuite) e zona `null` fixa; o desfecho independe de relógio, fuso real, locale ou ordem de hash. Confirmado.
- F4: `fix_test_suite.summary.log` com 0 não compilam e 0 falham; `run.log` vazio.
- F5: falha de asserção do próprio teste, sem erro de infraestrutura.
- Concordo: `falso_positivo = nao`, `deteccao_confirmada = 1`. Falta só a confirmação humana.

## Pontos para a validação humana

1. Time-23, C4: `testes_finais = 52` está superestimado (correto: 50). Decidir se corrige o valor no registro (e como tratar os demais testes com remoção na filtragem) ou se ajusta a contagem do `registrar.py` antes da análise. Por isso a sugestão para Time-23 é `divergente:C4`; se o grupo considerar que `testes_finais` não entra na conferência, o resultado passa a `ok`.
2. Closure-22/Closure-88: substituição bem documentada e a causa confere; confirmar que o grupo foi avisado (manual, seção 8).
3. Closure-22, F2: a coerência do falso positivo depende de inferência do patch e dos logs (o teste não foi reexecutado nem inspecionado em depuração).
4. As conclusões de F1-F5 vêm da leitura dos logs e dos patches por agente; a confirmação humana de `deteccao_confirmada` segue pendente nos três testes com detecção (Math-45, Closure-22 e Chart-8).
5. Lang-25 e Chart-8 têm `cobertura_falha` total baseada em 1 linha; está de acordo com as regras, mas é uma classificação frágil para a análise.
