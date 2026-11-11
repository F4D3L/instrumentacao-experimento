# Ambiente do experimento: o que deve ser feito

Todos os comandos são executados a partir da **raiz do projeto** (`experimentacao/`).
O procedimento completo está em [`docs/manual-do-pesquisador.md`](../docs/manual-do-pesquisador.md); este arquivo é o roteiro prático.

## Conteúdo desta pasta

| Arquivo | Para que serve |
|---|---|
| `Dockerfile` | Imagem única: Ubuntu 20.04 (amd64), OpenJDK 8, Defects4J v2.0.1 e EvoSuite 1.1.0, com as versões fixadas |
| `evosuite.config` | Configuração do tratamento (substitui a padrão do Defects4J) |
| `rodar.sh` | Constrói, exporta e importa a imagem e roda comandos no contêiner, sempre com os mesmos recursos (`CPUS=2`, `MEMORIA=6g`) |

O build baixa automaticamente os repositórios dos projetos (`defects4j-repos.zip`, via `init.sh`). **Não é preciso clonar nada do GitHub**: as versões defeituosa e corrigida de cada falha são obtidas pelo próprio Defects4J, dentro do contêiner.

## 1. Preparar o Docker (todos os integrantes, uma vez)

1. Instalar e abrir o **Docker Desktop**.
2. Em *Settings → Resources*, reservar **pelo menos 2 CPUs e 6 GB de memória**, com folga para o sistema.
3. Mac com Apple Silicon: em *Settings → General*, ativar **"Use Rosetta for x86_64/amd64 emulation"**. A imagem é amd64 e roda bem mais rápido assim.

## 2. Construir a imagem (só o responsável pela imagem, uma vez)

```bash
ambiente/rodar.sh construir      # demora: baixa o Defects4J, o EvoSuite e os repositórios dos projetos
ambiente/rodar.sh exportar       # gera experimento-evosuite-d4j.tar.gz e imprime o ID da imagem
```

- Publique o `experimento-evosuite-d4j.tar.gz` no drive do grupo (**não** no Git).
- Registre o **ID da imagem de referência** em "Decisões tomadas" do `docs/03-semana3-instrumentacao.md`.

## 3. Importar a imagem (demais integrantes)

```bash
ambiente/rodar.sh importar experimento-evosuite-d4j.tar.gz
```

O ID impresso tem de ser **idêntico** ao de referência. Se não for, não execute nada e avise o grupo.

## 4. Conferir as versões dentro do contêiner

```bash
ambiente/rodar.sh bash -c 'java -version 2>&1 | head -1; git -C $D4J_HOME rev-parse HEAD; \
  sha256sum $D4J_HOME/framework/lib/test_generation/generation/evosuite-current.jar \
            $D4J_HOME/framework/lib/test_generation/bin/evosuite.config; echo "TZ=$TZ"; nproc'
```

Resultado esperado:

| Item | Valor |
|---|---|
| Java | `openjdk version "1.8.0_…"` |
| Defects4J | `a83e47921152721569cb95d6d7b91c4be277d940` |
| EvoSuite (jar) | `939c0c762d20872b410ecfd79fc2ac77e13e984031dca3f45f78fa44ba627ef7` |
| `evosuite.config` | `7349236dc06a8861d1dd05231d10180141ab4da41c2184cd624b7ac586cd3d92` |
| Fuso | `TZ=America/Los_Angeles` |
| CPUs | `2` |

## 5. Piloto (valida o pipeline; antes do sorteio)

Escolha as 2 falhas do piloto **antes do sorteio** e registre a escolha em "Decisões tomadas". Para cada uma:

```bash
ambiente/rodar.sh scripts/executar_teste.sh --piloto <Projeto-ID> <semente_evosuite>
# exemplo: ambiente/rodar.sh scripts/executar_teste.sh --piloto Lang-1 42
```

Validações:

```bash
cat dados/registro-piloto.csv                                   # resumo; etapas_com_erro tem de estar vazio
cat resultados/piloto/<Falha>/tempos.csv                        # tempo por etapa; código de saída 0 em todas
grep -E 'search_budget|assertion_strategy' resultados/piloto/<Falha>/logs/gerar.log   # tem de mostrar 180 e all
cat resultados/piloto/<Falha>/cobertura_falha.txt               # conferir à mão (abaixo)
```

- Se alguma etapa tiver código diferente de 0, abra o log correspondente em `resultados/piloto/<Falha>/logs/`.
- **Conferência manual da cobertura da falha:** compare as linhas listadas em `cobertura_falha.txt` com o patch e com o XML de cobertura:
  ```bash
  ambiente/rodar.sh bash -c 'cat $D4J_HOME/framework/projects/<Projeto>/patches/<id>.src.patch'
  # XML: resultados/piloto/<Falha>/cobertura/coverage_log/<Projeto>/evosuite/<id>f.1.xml
  ```
- Anote o tempo total por teste e o espaço em disco usado. Esses valores substituem as estimativas do manual.

Os resultados do piloto **não entram** na análise.

## 6. Sorteio e caracterização (uma vez, na reunião, depois do piloto)

> A pasta ainda não é um repositório Git. Crie o repositório do grupo (`git init` + remoto) antes deste passo.

```bash
ambiente/rodar.sh scripts/listar_falhas.sh
ambiente/rodar.sh python3 scripts/sorteio.py --semente 20261030 --piloto <Falha-1> <Falha-2>
ambiente/rodar.sh python3 scripts/caracterizar.py
git add dados/ && git commit -m "sorteio e caracterização"
```

A partir daqui, `dados/falhas-ativas/`, `dados/sorteio/` e `dados/caracterizacao.csv` não mudam mais.

## 7. Execução dos testes (cada pesquisador, 5 testes na ordem sorteada)

Para cada linha sua em `dados/sorteio/atribuicao.csv`, na ordem da coluna `ordem`:

1. Preencher o [`docs/checklist-ambiente.md`](../docs/checklist-ambiente.md) (itens A1 a A10).
2. Executar:
   ```bash
   ambiente/rodar.sh scripts/executar_teste.sh "<Seu Nome>" <Projeto-ID>
   ```
3. Conferir o manifesto (itens D1 a D5 do checklist).
4. Se `deteccao_automatica = 1`: preencher o [`docs/checklist-falso-positivo.md`](../docs/checklist-falso-positivo.md) e atualizar `falso_positivo` e `deteccao_confirmada` em `dados/registro.csv`.
5. Fazer o commit e o push:
   ```bash
   git add resultados/<Falha> dados/registro.csv docs/registros/
   git commit -m "teste <Falha> (<Seu Nome>, ordem <n>)" && git push
   ```

## 8. Conferência e análise

1. Cada conferente segue o [`docs/roteiro-conferencia.md`](../docs/roteiro-conferencia.md) e preenche a coluna `conferencia`.
2. Com os 35 testes confirmados:
   ```bash
   ambiente/rodar.sh python3 scripts/analise.py
   ```

## Regras que não podem ser quebradas

- Não alterar `evosuite.config`, `rodar.sh` (CPU e memória) nem os scripts durante a execução.
- Não rodar nada fora do contêiner.
- Não repetir um teste: o pipeline se recusa a rodar se `resultados/<Falha>` já existir.
- Não trocar falhas, exceto pela regra de substituição do manual (seção 8).
