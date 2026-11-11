# Manual do pesquisador

**Experimento:** efetividade do EvoSuite na detecção de falhas reais do Defects4J, comparada a Shamshiri et al. (2015).
**Para quem:** os 7 integrantes do grupo, que fazem os testes, e quem confere o trabalho de outro integrante.
**Regra geral:** tudo roda por script, dentro da mesma imagem de contêiner. Nenhum passo do tratamento é feito à mão, e ninguém escolhe, troca, repete ou descarta falhas fora das regras deste manual.

## 1. Visão geral

Cada **teste** do experimento corresponde a uma falha do Defects4J. São 35 testes: 5 projetos × 7 falhas, e cada pesquisador faz 5, um de cada projeto, na ordem sorteada. Um teste segue este fluxo:

```
checklist do ambiente → executar_teste.sh
   ├─ manifesto (versões e recursos)
   ├─ gerar      EvoSuite na versão CORRIGIDA, sobre as classes modificadas
   ├─ filtrar    remove testes que não compilam e testes instáveis (5 execuções seguidas)
   ├─ detectar   roda a suíte filtrada na versão DEFEITUOSA
   ├─ cobrir     cobertura de linhas e ramos (Cobertura), na versão corrigida
   ├─ cobertura da falha (total / parcial / nenhuma)
   └─ registro   uma linha em dados/registro.csv
→ se houve detecção: checklist de falso positivo
→ commit
→ conferência por outro integrante (rodízio)
```

## 2. Papéis

| Papel | Quem | Responsabilidade |
|---|---|---|
| Responsável pela imagem | 1 integrante (a definir) | Constrói a imagem uma vez, exporta e distribui o arquivo; divulga o ID da imagem de referência |
| Responsável pelo sorteio | 1 integrante (a definir), na reunião | Roda `listar_falhas.sh`, `sorteio.py` e `caracterizar.py` na frente do grupo e faz o commit antes de qualquer teste |
| Executor | Cada um dos 7 | Faz os seus 5 testes na ordem sorteada, preenche os checklists e faz um commit por teste |
| Conferente | O próximo da lista (rodízio cíclico, coluna `conferente` em `atribuicao.csv`) | Confere os 5 testes do colega pelos logs (ver `roteiro-conferencia.md`) |

## 3. Preparação do ambiente (uma vez)

### 3.1 Requisitos da máquina de cada integrante

- Docker instalado e em execução (Docker Desktop no macOS/Windows).
- Nas configurações do Docker Desktop, reservar **pelo menos** os recursos do contêiner (`CPUS` e `MEMORIA` em `ambiente/rodar.sh`), com folga para o sistema.
- Espaço em disco para a imagem e para os resultados (o tamanho exato será medido no piloto).
- Git e acesso ao repositório do grupo.

### 3.2 Construção da imagem (só o responsável)

A imagem está definida em `ambiente/Dockerfile` e fixa:

| Componente | Versão |
|---|---|
| Sistema base | Ubuntu 20.04 (`linux/amd64`) |
| Java | OpenJDK 8, exigido pelo Defects4J 2.x |
| Defects4J | v2.0.1, commit `a83e47921152721569cb95d6d7b91c4be277d940` |
| EvoSuite | 1.1.0, SHA-256 `939c0c762d20872b410ecfd79fc2ac77e13e984031dca3f45f78fa44ba627ef7` (conferido no build) |
| Configuração do EvoSuite | `ambiente/evosuite.config` (seção 5) |
| Fuso horário | `America/Los_Angeles`, exigido pelo Defects4J |

```bash
ambiente/rodar.sh construir     # demora: baixa os repositórios dos projetos do Defects4J
ambiente/rodar.sh exportar      # gera experimento-evosuite-d4j.tar.gz e imprime o ID da imagem
```

O responsável publica o arquivo `.tar.gz` (em um drive do grupo, não no Git) e registra o **ID da imagem de referência** na seção "Decisões tomadas" do `03-semana3-instrumentacao.md`.

> Por que construir uma vez só: o `apt` do Ubuntu pode instalar atualizações diferentes em dias diferentes. Construindo uma única vez e distribuindo o mesmo arquivo, garantimos que os 7 usam o mesmo binário, e o manifesto de cada teste prova isso (campo `id_imagem`).

### 3.3 Instalação nos demais integrantes

```bash
git clone <repositório do grupo> && cd experimentacao
ambiente/rodar.sh importar experimento-evosuite-d4j.tar.gz
```

O ID que o comando imprime tem de ser **idêntico** ao de referência. Se não for, pare e avise o grupo.

### 3.4 Plataforma

A imagem é `linux/amd64`. Em Macs com Apple Silicon ela roda emulada, que é mais lento. Como o orçamento do EvoSuite é medido em tempo, uma máquina mais lenta explora menos na mesma busca. Isso é uma ameaça interna já declarada (diferenças de ambiente). O piloto mede o tempo em cada tipo de máquina do grupo, e o manifesto registra o `kernel`/arquitetura de cada teste.

## 4. Seleção e preparação dos objetos (uma vez, antes de qualquer teste)

Feito na reunião, por script, com o resultado versionado antes do primeiro teste.

1. **Confirmar e registrar** a semente do sorteio (proposta: `20261030`) e as 2 falhas do piloto na seção "Decisões tomadas", **antes** de rodar o sorteio.
2. **Listar as falhas ativas** com o próprio Defects4J:
   ```bash
   ambiente/rodar.sh scripts/listar_falhas.sh        # grava dados/falhas-ativas/<Projeto>.txt
   ```
3. **Sortear**:
   ```bash
   ambiente/rodar.sh python3 scripts/sorteio.py --semente <semente> --piloto <Falha-1> <Falha-2>
   ```
   O script:
   - mantém só os IDs ativos que já estavam nas 357 falhas usadas por Shamshiri et al. (2015): Chart ≤ 26, Closure ≤ 133, Lang ≤ 65, Math ≤ 106 e Time ≤ 27. Com as depreciações do Defects4J 2.0 (Closure-63, Closure-93, Lang-2 e Time-21), isso dá 353 falhas elegíveis antes de retirar as do piloto;
   - retira as 2 falhas do piloto;
   - sorteia 10 falhas por projeto com um único `random.Random(semente)`, percorrendo os projetos em ordem alfabética: as 7 primeiras entram e as 3 seguintes ficam de reserva;
   - sorteia, para cada projeto, a permutação que distribui as 7 falhas entre os pesquisadores, depois a ordem dos 5 testes de cada pesquisador e, por fim, uma semente do EvoSuite para cada teste;
   - define o conferente de cada pesquisador como o seguinte na lista (rodízio cíclico);
   - grava `dados/sorteio/amostra.csv`, `atribuicao.csv` e `parametros.txt`, e se recusa a sobrescrever um sorteio já feito.
4. **Caracterizar** as falhas sorteadas (experimento e reservas):
   ```bash
   ambiente/rodar.sh python3 scripts/caracterizar.py   # grava dados/caracterizacao.csv
   ```
   - *Forma de revelação*: tipo da exceção de cada teste revelador do desenvolvedor, a mesma informação que o `defects4j info` mostra em "Root cause in triggering tests". `AssertionFailedError`, `AssertionError` e `ComparisonFailure` contam como asserção; qualquer outro tipo, como exceção. A falha é classificada como `assercao`, `excecao` ou `ambas`.
   - *Tamanho da correção*: linhas adicionadas + linhas removidas no patch da falha.
5. **Commit** de `dados/falhas-ativas/`, `dados/sorteio/` e `dados/caracterizacao.csv`, com a mensagem `sorteio e caracterização`. Daqui em diante, esses arquivos não mudam.

## 5. Descrição detalhada do tratamento

**Variável independente:** uso da técnica de geração de testes EvoSuite, em nível único, comparada ao valor de referência da literatura.

| Aspecto | Como é aplicado | Onde está fixado |
|---|---|---|
| Ferramenta | EvoSuite 1.1.0, chamado pelo `gen_tests.pl -g evosuite` do Defects4J | Imagem (SHA-256 conferido) |
| Versão alvo | Versão **corrigida** da falha (`<id>f`) | `executar_teste.sh` |
| Classes alvo | Classes modificadas pela correção (`classes.modified`, arquivo `modified_classes/<id>.src` do Defects4J) | Padrão do `gen_tests.pl` |
| Modo | Testes de regressão (o padrão do Defects4J) | `gen_tests.pl` sem `-E` |
| Orçamento | **180 s de busca por classe**. O wrapper do Defects4J divide o `-b` total por 2 e pelo número de classes (metade para a busca, metade para a geração de asserções), então o pipeline passa `-b = 360 × nº de classes` | `executar_teste.sh` |
| Critério e opções | Os da configuração padrão do Defects4J 2.0.1: `-criterion branch`, `stopping_condition=MaxTime`, `filter_assertions=false`, `-mem 1500` etc. | `ambiente/evosuite.config` |
| Asserções | **Filtragem de asserções por mutação desativada**: `-Dassertion_strategy=all` (o padrão do EvoSuite 1.1.0 é `MUTATION`). Atenção: `filter_assertions=false` não é essa opção, porque ela controla a filtragem de asserções *instáveis* | `ambiente/evosuite.config` |
| Repetições | 1 execução por falha (`-n 1`) | `executar_teste.sh` |
| Semente | Sorteada por teste (`semente_evosuite` em `atribuicao.csv`) e passada com `-s` | `sorteio.py` |

**É proibido** alterar `evosuite.config`, o orçamento, a semente ou qualquer script durante a execução, repetir um teste para "tentar de novo" ou rodar fora do contêiner. O pipeline recusa rodar duas vezes a mesma falha (`resultados/<falha>` já existe).

### 5.1 Medição (automática)

| Variável | Como é obtida |
|---|---|
| Testes gerados / removidos / finais | Contagem de `@Test` na suíte gerada e na filtrada. Os removidos vêm do `fix_test_suite.summary.log` |
| Filtragem de instáveis | `fix_test_suite.pl` remove testes que não compilam e testes que falham na versão corrigida até a suíte inteira **passar 5 vezes seguidas** |
| Detecção automática | `run_bug_detection.pl`: a suíte filtrada é executada na versão defeituosa. `Fail` = ao menos um teste falha (detecção 1); `Pass` = nenhum falha (0); `Broken` = a suíte não compila ou não roda na defeituosa (0, marcada para conferência) |
| Cobertura da classe | `run_coverage.pl` (Cobertura) na versão corrigida, só nas classes modificadas: **cobertura de linhas** (%), com os ramos também registrados |
| Cobertura da falha | `cobertura_falha.py` cruza o patch com o `coverage.xml` (regras na seção 5.2) |
| Tempo por etapa | `tempos.csv` (início, fim, segundos e código de saída de cada etapa) |
| Ambiente | `manifesto.txt` (ID da imagem, CPU/memória, Java, commit do Defects4J, SHA-256 do EvoSuite e da configuração) |

### 5.2 Regras da cobertura da falha

1. O patch do Defects4J vai da versão **corrigida para a defeituosa**. As linhas marcadas com `-` no patch são, portanto, as linhas da versão corrigida que a correção adicionou ou alterou, e são essas as **linhas-alvo**.
2. Se um trecho do patch tem só linhas `+` (a correção apenas removeu código), a linha-alvo é a linha da versão corrigida logo depois do trecho removido (regra da entrega 2).
3. O Cobertura só registra linhas executáveis. Linhas-alvo que não aparecem no relatório (comentário, chave, declaração) são ignoradas. Se nenhuma linha-alvo de um trecho for executável, usa-se a próxima linha executável do arquivo.
4. **total** = todas as linhas consideradas foram executadas; **parcial** = parte delas; **nenhuma** = nenhuma delas, ou não há relatório (suíte vazia). **indeterminado** = nenhuma linha pôde ser associada, o que exige conferência manual.

## 6. Piloto (antes do sorteio)

Duas falhas **fora da amostra**, escolhidas e registradas antes do sorteio, que as exclui.

```bash
ambiente/rodar.sh scripts/executar_teste.sh --piloto <Falha> <semente_evosuite>
```

Os resultados vão para `resultados/piloto/` e `dados/registro-piloto.csv`. No piloto, conferir e registrar:

- [ ] o pipeline completa todas as etapas sem erro (`etapas_com_erro` vazio);
- [ ] o tempo por teste (`tempo_total_s`) em cada tipo de máquina do grupo;
- [ ] o `cobertura_falha.txt` bate com uma conferência manual: abrir o patch e o `coverage.xml` e checar linha a linha;
- [ ] o log do EvoSuite (`logs/gerar.log`) mostra `search_budget` de 180 e `assertion_strategy` igual a `all`;
- [ ] o tamanho da imagem e o espaço usado por teste.

Os resultados do piloto **não entram** na análise.

## 7. Execução de um teste (passo a passo)

Faça os seus 5 testes **na ordem** da coluna `ordem` de `dados/sorteio/atribuicao.csv`.

1. `git pull`.
2. Preencher o **checklist do ambiente** (`checklist-ambiente.md`) para este teste. Se algum item falhar, não execute.
3. Executar:
   ```bash
   ambiente/rodar.sh scripts/executar_teste.sh "<Seu Nome>" <Projeto-ID>
   ```
   O nome tem de ser exatamente o de `atribuicao.csv`. Não use o computador para tarefas pesadas enquanto o teste roda.
4. Ler o resumo impresso no final. Se `etapas_com_erro` não estiver vazio, veja a seção 8.
5. Se `deteccao_automatica = 1`, preencher o **checklist de falso positivo** (`checklist-falso-positivo.md`) e atualizar as colunas `falso_positivo` e `deteccao_confirmada` da sua linha em `dados/registro.csv`.
6. Anotar em `observacoes` qualquer coisa fora do normal.
7. Commit de tudo o que o teste produziu, com a mensagem `teste <Falha> (<Seu Nome>, ordem <n>)`:
   ```bash
   git add resultados/<Falha> dados/registro.csv docs/registros/ && git commit -m "teste <Falha> (<Seu Nome>, ordem <n>)"
   git push
   ```
   Os logs são arquivados **sem edição manual**.

## 8. Situações de exceção

| Situação | O que fazer |
|---|---|
| O EvoSuite não gera nenhum teste, ou a suíte fica vazia depois da filtragem | O resultado vale (detecção 0). **Não substituir** a falha. Registrar em `observacoes` |
| `resultado_d4j = Broken` (a suíte não compila ou não roda na versão defeituosa) | Detecção 0. Registrar e deixar para o conferente analisar o log em `deteccao/` |
| `cobertura_falha = indeterminado` | Classificar à mão, seguindo a seção 5.2, e registrar o raciocínio em `observacoes` |
| Uma etapa falha por motivo **técnico alheio à ferramenta** (o projeto não compila no ambiente, o checkout falha) | Avisar o grupo. Se confirmado, aplicar a **regra de substituição**: usar a próxima reserva do mesmo projeto (`amostra.csv`, na ordem de `posicao_sorteio`), registrar o motivo em "Decisões tomadas" e manter a pasta da falha original como evidência |
| Falta de memória, queda de energia ou execução interrompida | Não apagar nada. Avisar o grupo; a decisão de reexecutar é tomada em conjunto e registrada, com o motivo e a pasta original preservada |

## 9. Consolidação

1. Cada conferente revisa os 5 testes do colega pelo `roteiro-conferencia.md` e preenche a coluna `conferencia` (`ok` ou `divergente`, com a nota).
2. Com as 35 linhas confirmadas (nenhuma `pendente` em `deteccao_confirmada`):
   ```bash
   ambiente/rodar.sh python3 scripts/analise.py
   ```
   O script calcula p̂, o IC de 95% (Clopper-Pearson), o binomial exato bicaudal contra 26,5% e 23,0%, a comparação por bloco, o Mann-Whitney unilateral exato com tamanho de efeito (A12 e rank-biserial) e as tabelas da questão secundária.

## 10. Estrutura do repositório

```
ambiente/            Dockerfile, evosuite.config, rodar.sh
scripts/             listar_falhas.sh, sorteio.py, caracterizar.py, executar_teste.sh,
                     cobertura_falha.py, registrar.py, analise.py
dados/
  falhas-ativas/     listas do Defects4J (uma por projeto)
  sorteio/           amostra.csv, atribuicao.csv, parametros.txt
  caracterizacao.csv
  registro.csv       planilha de registro (uma linha por teste)
  registro-piloto.csv
resultados/<Falha>/  manifesto.txt, tempos.csv, logs/, suites/, deteccao/, cobertura/,
                     cobertura_falha.txt, suite-gerada.tar.bz2
resultados/piloto/   o mesmo, para o piloto
docs/                manual, checklists, roteiro e registros preenchidos (docs/registros/)
```

## 11. Itens a confirmar antes da execução

Estes valores estão nos scripts, mas são **propostas**. Precisam ser confirmados pelo grupo e registrados em "Decisões tomadas":

- recursos do contêiner: `CPUS=2` e `MEMORIA=6g` (`ambiente/rodar.sh`);
- semente do sorteio (proposta: 20261030);
- as 2 falhas do piloto;
- quem é o responsável pela imagem e quem conduz o sorteio;
- critério de busca do EvoSuite: mantivemos o `-criterion branch` da configuração padrão do Defects4J. Conferir no artigo se é o mesmo usado por Shamshiri et al. (2015).
