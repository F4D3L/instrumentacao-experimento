# Semana 4: Resultados e conclusões

## Decisões tomadas

| Data | Decisão | Motivo |
|---|---|---|
| 12/11/2026 | CPU/memória do contêiner = 2 CPUs e 6g (valores de `ambiente/rodar.sh`) | Pendência 7 da semana 3 |
| 12/11/2026 | Semente do sorteio = 20261030 | Pendência 5 da semana 3 |
| 12/11/2026 | Falhas do piloto = Lang-1 (semente EvoSuite 1) e Math-5 (semente EvoSuite 2), excluídas do sorteio | Pendência 6 da semana 3 |
| 12/11/2026 | Responsável pela imagem e pelo sorteio = execução centralizada por agente de IA (Claude Code), a pedido do grupo, na máquina de Lucas Reali (ver desvio abaixo) | Decisão do grupo |
| 12/11/2026 | ID da imagem de referência = `sha256:45031972753e1f1906530e802b0714d06bbd13e2ec516bb455dc30b3499d446e` | Conferido em todo teste contra o `manifesto.txt` |
| 12/11/2026 | Paralelismo = 1 teste por vez, em série | O orçamento do EvoSuite é medido em tempo; testes simultâneos disputariam CPU e alterariam o tratamento |
| 12/11/2026 | Ordem global = rodízio por ordem (todos os ordem 1 na ordem da lista de pesquisadores, depois os ordem 2, e assim por diante) | Preserva a ordem sorteada de cada pesquisador |
| 12/11/2026 | Docker Desktop com Rosetta; host: `{"A1_docker_info":"ok (exit 0)","A2_id_imagem":"sha256:45031972753e1f1906530e802b0714d06bbd13e2ec516bb455dc30b3499d446e (igual ao ID de referência)","A3_docker_recursos":"10 CPUs, 8319504384 bytes (>= 2 CPUs e >= 6g)","A4_rodar_sh":"CPUS=\"2\", MEMORIA=\"6g\"","A5_git_status_ambiente_scripts_dados_sorteio":"vazio (sem modificações); git pull não executado","A6_java":"openjdk version \"1.8.0_452\"","A6_defects4j_commit":"a83e47921152721569cb95d6d7b91c4be277d940","A6_evosuite_sha256":"939c0c762d20872b410ecfd79fc2ac77e13e984031dca3f45f78fa44ba627ef7 (/defects4j/framework/lib/test_generation/generation/evosuite-current.jar)","A6_evosuite_config_sha256":"7349236dc06a8861d1dd05231d10180141ab4da41c2184cd624b7ac586cd3d92 (/defects4j/framework/lib/test_generation/bin/evosuite.config)","A6_TZ":"America/Los_Angeles","A6_nproc":"10 (esperado pela nota do usuário: limite por cgroup)","A6_cgroup_cpu_max":"200000 100000 (2 CPUs)","A6_jvm_effective_cpu_count":"2","A6_cgroup_memory_max":"6442450944 (6g)","A9_disco_livre":"759Gi disponíveis (926Gi total, 17% usado)","A10_docker_ps":"vazio (nenhum contêiner rodando)","A10_energia":"Conectado à tomada (AC Power), bateria 47% carregando","maquina_modelo":"Apple M5","maquina_arquitetura":"arm64","host_nucleos_fisicos":"10"}`; branch git `experimento/execucao`, só commits locais; imagem não exportada porque só há uma máquina | Registro do ambiente de execução (checklist A1 a A10) |

## Piloto

Fontes lidas por mim: `dados/registro-piloto.csv`; `resultados/piloto/{Lang-1,Math-5}/` (`tempos.csv`, `manifesto.txt`, `cobertura_falha.txt`, `logs/{gerar,filtrar,detectar,cobrir,cobertura_falha}.log`, `suites/logs/*.log`, `fix_test_suite.summary.log`, `deteccao/bug_detection`, `cobertura/coverage`, `coverage.xml` para as linhas-alvo); `scripts/cobertura_falha.py`; `ambiente/evosuite.config`; seções 5 e 6 do manual do pesquisador.

**1. Pipeline.** Completa todas as etapas sem erro nos dois pilotos. `etapas_com_erro` está vazio nas duas linhas do `registro-piloto.csv`, e `tempos.csv` tem código de saída 0 em `gerar`, `filtrar`, `detectar`, `cobrir` e `cobertura_falha`. Todos os passos dos logs do Defects4J terminam em "OK". Os dois manifestos têm o mesmo `id_imagem` (a imagem da Fase 1) e conferem `cpus_limite=2`, `memoria_limite=6g`, `memoria_cgroup=6442450944`, `nproc_visto=10` (esperado, conforme a decisão do grupo), `java 1.8.0_452`, `defects4j_commit a83e479…`, `evosuite_sha256 939c0c76…` e `evosuite_config_sha256 7349236d…`.

**2. Orçamento e asserções (item D4).** Conferido por evidência indireta, conforme o critério decidido: (a) `resultados/piloto/Lang-1/suites/logs/Lang.1f.log` tem `-b 360` e `-s 1`; `resultados/piloto/Math-5/suites/logs/Math.5f.log` tem `-b 360` e `-s 2`. Cada falha tem 1 classe modificada (NumberUtils e Complex), então 360 × 1 = 360, o que pelo wrapper dá 180 s de busca por classe. `orcamento_total_s=360` nos dois manifestos. (b) SHA-256 de `ambiente/evosuite.config` recalculado: `7349236dc06a8861d1dd05231d10180141ab4da41c2184cd624b7ac586cd3d92`, igual ao dos manifestos; o arquivo contém `-Dassertion_strategy=all`. **D4 = ok nos dois.** A geração durou 199 s nos dois (Lang: 06:09:38 a 06:12:46; Math: 06:15:03 a 06:18:12, horário de Los Angeles), compatível com 180 s de busca mais a fase de asserções e o overhead.

**3. Script de cobertura da falha.** A lógica de `scripts/cobertura_falha.py` segue as regras 1 a 4 da seção 5.2. Conferido no `coverage.xml`:
- Lang-1: linhas 467 (6 hits), 468 (7), 469 (6), 470 (6), 471 (1), 477 (6) e 480 (4), todas com hits > 0, então **total**, 7/7, igual ao `cobertura_falha.txt`. As linhas 472 a 475 não constam no relatório.
- Math-5: linha 305 com hits = 0 (as linhas 304 e 308 têm hits = 1), então **nenhuma**, 0/1, igual ao `cobertura_falha.txt`.

As duas conferências manuais batem com a do script. O piloto exercitou os casos **total** e **nenhuma**. Os casos **parcial**, **só remoção** e **indeterminado** não foram exercitados.

**4. Tempos.**

| Falha | gerar | filtrar | detectar | cobrir | cobertura_falha | total |
|---|---|---|---|---|---|---|
| Lang-1 | 199 s | 28 s | 24 s | 18 s | 0 s | 269 s |
| Math-5 | 199 s | 35 s | 30 s | 21 s | 0 s | 285 s |

Média de 277 s por teste (cerca de 4,6 min). Estimativa para 35 testes em série: 35 × 277 s = 9695 s, cerca de 2,69 h, sem contar intervalos entre testes. **Ressalva:** os dois pilotos têm 1 classe modificada. Falhas com k classes recebem `-b = 360 × k`, então a geração cresce cerca de 180 s de busca mais o tempo de asserções por classe extra. A estimativa é um piso. Os pilotos rodaram numa única máquina, Apple Silicon com emulação amd64 (kernel linuxkit x86_64); o manual pede o tempo de cada tipo de máquina do grupo.

**5. Espaço.** `resultados/piloto/Lang-1` ocupa 192 KB e `Math-5` ocupa 144 KB (média de cerca de 168 KB por teste). Para 35 testes são cerca de 6 MB em `resultados/`, desprezível. A imagem tem 1.81 GB. A queda de espaço observada no disco durante os pilotos (cerca de 37 MB no Lang-1 e 2,6 MB no Math-5) é do Docker, não da pasta de resultados.

**6. Sinais de problema.** Nenhum. Não há `OutOfMemory`, timeout, `killed`, `exception` ou `error` nos logs. As únicas ocorrências de "broken" são as linhas padrão "Excluding broken/flaky tests ... OK" do checkout. `fix_test_suite.summary.log` mostra 0 classes não compiláveis, 0 testes não compiláveis e 0 testes falhando nos dois. Testes gerados = finais (120/120 e 77/77), então não houve remoção em massa. `bug_detection` deu `Pass` com `num_trigger` 0 nos dois (não `Broken`), e os `trigger.log` estão vazios. Cobertura: Lang 99,21% de linhas (376/379) e 337/350 ramos; Math 95,10% de linhas (194/204) e 160/170 ramos. `evosuite-report/statistics.csv` (não rastreado, conforme a decisão) tem as duas classes.

**7. Git.** `ambiente/Dockerfile` não foi modificado (git status limpo em `ambiente/`), então não houve commit do Dockerfile. Commit `bb2546dc344c45493d9447a220e6e890fb6973e7` com a mensagem "piloto Lang-1 e Math-5", sem linha de atribuição, com 45 arquivos (`resultados/piloto/` e `dados/registro-piloto.csv`). `docs/prompt-agente-execucao.md` e `evosuite-report/` continuam não rastreados. Nada foi executado no contêiner após o piloto e não houve push.

## Desvios e decisões

| Data | Desvio/decisão | Motivo | Impacto |
|---|---|---|---|
| 12/11/2026 | **Execução centralizada:** os 35 testes foram executados por um agente de IA em uma única máquina, e não por cada um dos 7 integrantes; a coluna `pesquisador` mantém o integrante sorteado | Decisão do grupo | Elimina a variação entre operadores e máquinas, mas descaracteriza o papel de sujeito do pesquisador e a independência da conferência cruzada. Ameaça à validade interna/de construto a discutir no relatório |
| 12/11/2026 | Build da imagem: `build-1` falhou (código 126, `Permission denied`: `ambiente/rodar.sh` estava versionado como 100644); relançado como `bash ambiente/rodar.sh construir` (`build-2`), sem alterar nenhum arquivo | Bit de execução ausente no versionamento | Nenhum no tratamento. O Dockerfile não foi alterado |
| 12/11/2026 | Permissão de execução (`chmod +x`) dada aos `.sh` (commit `9cccda6`) | Os comandos do manual falhavam com `Permission denied` | Nenhum no tratamento; conteúdo dos scripts inalterado |
| 12/11/2026 | Build feito com `bash ambiente/rodar.sh construir`, antes da correção de permissão | Mesmo motivo do item anterior | Nenhum no tratamento |
| 12/11/2026 | Evidência de CPU do checklist (A6) corrigida: `nproc` mostra 10 porque `--cpus` limita por cota de cgroup; a evidência passa a ser `cpu.max` = `200000 100000` e `availableProcessors` = 2 na JVM (o valor "CPUs 2" esperado em `ambiente/README.md` e no checklist estava errado) | Nota do usuário (12/11/2026) | Nenhum no tratamento |
| 12/11/2026 | Item D4 do checklist conferido por evidência indireta: (a) `suites/logs/<P>.<id>f.log` com `-b` = 360 × nº de classes e `-s` = semente; (b) o wrapper `evosuite.sh` calcula `search_budget` = 180; (c) `evosuite_config_sha256` do manifesto | `gen_tests.pl` grava a saída do EvoSuite só em modo debug (`Utils::exec_cmd`), então `grep search_budget` em `logs/gerar.log` nunca encontra nada | Correção do checklist, sem mudança de script nem de tratamento |
| 12/11/2026 | `evosuite-report/statistics.csv`, gerado pelo EvoSuite na raiz do repositório, fica fora dos commits por teste e é commitado uma única vez no fim, como evidência complementar | Decisão do usuário | Nenhum no tratamento |
| 12/11/2026 | Lang-37: `testes_finais` (365) > `testes_gerados` (364) com 1 removido. Causa: o contador de `registrar.py` conta a substring `@Test`, e o `fix_test_suite.pl` deixa um stub vazio (`test345`) com `@Test` mais o código original comentado (também com `@Test`); a suíte final tem 363 testes ativos. Valores mantidos como gerados; explicação em `observacoes` | Artefato de contagem do script, sem falha de execução | Nenhum no tratamento (detecção, cobertura e resultado inalterados); a contagem de testes finais fica inflada em +2 por teste removido em outras falhas |

## Tempos

_(a preencher ao final da execução)_
