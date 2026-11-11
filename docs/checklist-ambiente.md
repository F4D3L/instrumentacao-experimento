# Checklist do ambiente experimental

Preencher **antes de cada teste**. Se qualquer item não for atendido, **não execute**: corrija o problema ou avise o grupo.
Registro: copie a tabela da seção 4 para `docs/registros/ambiente-<Seu-Nome>.md`, preencha uma coluna por teste e faça o commit junto com o teste.

## 1. Ferramentas e versões de referência

| Ferramenta | Versão / valor esperado | Onde aparece |
|---|---|---|
| Imagem do experimento | `experimento-evosuite-d4j:1`, ID = **valor de referência** registrado em "Decisões tomadas" | `docker image inspect`, `manifesto.txt` (`id_imagem`) |
| Java | `openjdk version "1.8.0_…"` | `manifesto.txt` (`java`) |
| Defects4J | commit `a83e47921152721569cb95d6d7b91c4be277d940` (v2.0.1) | `manifesto.txt` (`defects4j_commit`) |
| EvoSuite | 1.1.0, SHA-256 `939c0c762d20872b410ecfd79fc2ac77e13e984031dca3f45f78fa44ba627ef7` | `manifesto.txt` (`evosuite_sha256`) |
| Configuração do EvoSuite | SHA-256 `7349236dc06a8861d1dd05231d10180141ab4da41c2184cd624b7ac586cd3d92` | `manifesto.txt` (`evosuite_config_sha256`) |
| Fuso horário | `America/Los_Angeles` | `manifesto.txt` (`tz`) |
| Recursos do contêiner | `CPUS` e `MEMORIA` acordados (proposta: 2 CPUs, 6 GB) | `ambiente/rodar.sh`, `manifesto.txt` |

## 2. Antes de executar (evidências)

| # | Item | Como verificar (evidência) |
|---|---|---|
| A1 | Docker em execução | `docker info` responde sem erro |
| A2 | Imagem correta | `docker image inspect --format '{{.Id}}' experimento-evosuite-d4j:1` é igual ao ID de referência |
| A3 | Docker com recursos suficientes | `docker info --format '{{.NCPU}} CPUs, {{.MemTotal}} bytes'` ≥ `CPUS` e `MEMORIA` de `rodar.sh` |
| A4 | Recursos do contêiner não foram alterados | `grep -E '^(CPUS\|MEMORIA)=' ambiente/rodar.sh` mostra os valores acordados |
| A5 | Repositório atualizado e sem alterações locais | `git pull` sem conflito; `git status` sem modificações em `ambiente/`, `scripts/` e `dados/sorteio/` |
| A6 | Versões dentro do contêiner | o comando da seção 3 mostra Java 1.8, o commit do Defects4J, os dois SHA-256 e o fuso esperados |
| A7 | Teste certo, na ordem certa | a falha é a próxima da sua `ordem` em `dados/sorteio/atribuicao.csv`, e as anteriores já têm commit |
| A8 | Teste ainda não executado | a pasta `resultados/<Falha>` **não** existe |
| A9 | Espaço em disco | `df -h .` com espaço livre acima do mínimo medido no piloto |
| A10 | Máquina sem concorrência | computador ligado na tomada, sem modo de economia de energia, sem outras tarefas pesadas (builds, jogos, vídeo) e sem outro contêiner rodando (`docker ps` vazio) |

## 3. Comando de verificação das versões (A6)

```bash
ambiente/rodar.sh bash -c 'java -version 2>&1 | head -1; git -C $D4J_HOME rev-parse HEAD; \
  sha256sum $D4J_HOME/framework/lib/test_generation/generation/evosuite-current.jar \
            $D4J_HOME/framework/lib/test_generation/bin/evosuite.config; echo "TZ=$TZ"; nproc'
```

## 4. Depois de executar (conferir o manifesto)

| # | Item | Evidência |
|---|---|---|
| D1 | O manifesto bate com a seção 1 | `resultados/<Falha>/manifesto.txt` |
| D2 | `semente_evosuite` igual à de `atribuicao.csv` | `manifesto.txt` |
| D3 | `orcamento_total_s` = 360 × nº de classes modificadas | `manifesto.txt` |
| D4 | O log da geração mostra o orçamento e as asserções corretos | `grep -E 'search_budget\|assertion_strategy' resultados/<Falha>/logs/gerar.log` |
| D5 | Todas as etapas com código 0, ou exceção tratada conforme o manual (seção 8) | `tempos.csv` / coluna `etapas_com_erro` |

## 5. Modelo de registro (copiar para `docs/registros/ambiente-<Seu-Nome>.md`)

```markdown
# Checklist do ambiente: <Seu Nome>

| Item | Teste 1: <Falha> | Teste 2: <Falha> | Teste 3: <Falha> | Teste 4: <Falha> | Teste 5: <Falha> |
|---|---|---|---|---|---|
| Data/hora |  |  |  |  |  |
| A1 Docker em execução |  |  |  |  |  |
| A2 ID da imagem (8 primeiros caracteres) |  |  |  |  |  |
| A3 Recursos do Docker |  |  |  |  |  |
| A4 CPUS/MEMORIA inalterados |  |  |  |  |  |
| A5 Repositório limpo e atualizado |  |  |  |  |  |
| A6 Versões no contêiner |  |  |  |  |  |
| A7 Ordem correta |  |  |  |  |  |
| A8 Pasta inexistente |  |  |  |  |  |
| A9 Disco livre |  |  |  |  |  |
| A10 Sem concorrência |  |  |  |  |  |
| D1–D5 Manifesto e log conferidos |  |  |  |  |  |
| Máquina (modelo / arquitetura) |  |  |  |  |  |
| Observações |  |  |  |  |  |
```

Preencha cada célula com `ok` ou com a descrição do problema.
