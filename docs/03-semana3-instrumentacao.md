# Semana 3: Instrumentação do experimento

**Entrega:** qua, 11/11/2026 18:15 (horário da reunião do grupo).
**Base:** enunciado em [`00-enunciados.md`](00-enunciados.md) + o que foi prometido em [`02-entrega-semana2.md`](02-entrega-semana2.md) (seções "Proposta de instrumentação", "Objetos experimentais" e "Instrumentos de coleta").

## 1. O que o professor exige

| # | Exigência | Obrigatório? |
|---|---|---|
| E1 | Manual do pesquisador: procedimento experimental detalhado, incluindo preparação do ambiente, seleção e preparação de objetos e descrição detalhada do tratamento | Sim |
| E2 | Checklist do ambiente experimental: ferramentas, configurações necessárias e evidências conferidas **antes de cada teste** | Sim |
| E3 | Demais questionários, formulários, scripts, sistemas, roteiros ou checklists usados no teste e na medição | Conforme o escopo |

O foco da avaliação é: todos os instrumentos existem e o contexto/ambiente está controlado.

## 2. Instrumentos que a semana 2 prometeu (mapa para E3)

Cada item abaixo foi citado na entrega 2 e, portanto, precisa existir (ou ter justificativa) na semana 3.

| Instrumento prometido | Tipo | Atende | Status |
|---|---|---|---|
| Imagem de contêiner (JDK + Defects4J + EvoSuite + scripts, versões fixas, CPU/memória fixas) | Ambiente | E1, E2 | feito: `ambiente/Dockerfile`, `ambiente/rodar.sh` (build ainda não testado) |
| Script de sorteio (semente, 10 por projeto, 7 + 3 reservas, permutação pesquisador, ordem) | Script | E1, E3 | feito: `scripts/listar_falhas.sh`, `scripts/sorteio.py` (testado) |
| Pipeline de execução (checkout → geração → filtragem 5× → detecção → cobertura → CSV/logs) | Script | E1, E3 | feito: `scripts/executar_teste.sh` + `scripts/registrar.py` (falta rodar no contêiner) |
| Script de cobertura da falha (patch × relatório por linha → total/parcial/nenhuma; regra para correções que só removem código) | Script | E3 | feito: `scripts/cobertura_falha.py` (testado com patches reais e XML sintético) |
| Planilha de registro por teste (CSV, campos definidos na entrega 2) | Formulário | E3 | feito: `dados/registro.csv`, gerada pelo `registrar.py` |
| Tabela de caracterização das falhas (forma de revelação, tamanho da correção) | Formulário | E3 | feito: `scripts/caracterizar.py` → `dados/caracterizacao.csv` (testado) |
| Checklist de falso positivo (executor + segundo integrante) | Checklist | E3 | feito: `docs/checklist-falso-positivo.md` |
| Manifesto de versões (gravado pelo pipeline no início de cada teste) | Registro | E2, E3 | feito: `manifesto.txt` gravado pelo `executar_teste.sh` |
| Cronometragem por etapa (automática no pipeline) | Registro | E3 | feito: `tempos.csv` por teste |
| Logs EvoSuite/JUnit arquivados sem edição | Registro | E3 | feito: `resultados/<Falha>/logs/` + logs do Defects4J |
| Script de análise (p̂, IC Clopper-Pearson, binomial exato, Mann-Whitney + efeito, por bloco, tabelas de contingência) | Script | E3 | feito: `scripts/analise.py` (testado com dados sintéticos) |
| Roteiro de conferência cruzada por rodízio | Roteiro | E3 | feito: `docs/roteiro-conferencia.md` |
| Piloto com 2 falhas fora da amostra (validar pipeline, tempo, script de cobertura da falha) | Procedimento | E1 | procedimento descrito (manual, seção 6); **execução pendente** |

## 3. Pontos em aberto herdados da semana 2

Itens que a entrega 2 deixou explicitamente para depois, ou que precisam ser verificados antes de virar instrumento. **Não decidir sozinho: levantar e confirmar com o grupo.**

1. **Versões exatas** de JDK, Defects4J e EvoSuite ("serão definidas e confirmadas no piloto"). Verificar compatibilidade entre elas.
2. **Cobertura "de instruções"**: a entrega 2 diz medir cobertura de instruções com `defects4j coverage`. Verificar qual ferramenta/métrica o `defects4j coverage` realmente reporta (linha, ramo, instrução) e se isso bate com a medida do artigo. Se não bater, registrar o ajuste.
3. **Scripts nativos do Defects4J** para geração, filtragem de instáveis, detecção e cobertura: confirmar quais existem na versão escolhida e se suportam as opções exigidas (180 s por classe, filtragem por mutação desativada, semente, 5 execuções).
4. **Falhas depreciadas e lista atual**: a versão atual do Defects4J pode ter número de falhas ativas diferente das 357 do artigo. Registrar a contagem por projeto.
5. **Semente do sorteio**: confirmar 20261030 e registrar antes de rodar.
6. **Quais 2 falhas** serão usadas no piloto (e excluídas do sorteio).
7. **CPU e memória** fixadas no contêiner (valores).
8. **Estrutura do repositório** do grupo (onde ficam listas, CSV, logs, um commit por teste).
9. **Rodízio** da conferência cruzada (quem confere quem).
10. **Formato de entrega** ao professor (documento único com anexos? repositório?).

## 4. Entregáveis da semana 3 (proposta, a confirmar)

- [x] Manual do pesquisador (E1): `docs/manual-do-pesquisador.md`
- [x] Checklist do ambiente experimental, preenchido antes de cada teste (E2): `docs/checklist-ambiente.md`
- [x] Scripts: sorteio, pipeline, cobertura da falha, análise (E3): `scripts/`
- [x] Formulários: CSV de registro, tabela de caracterização, checklist de falso positivo, roteiro de conferência (E3)
- [x] Definição do contêiner + manifesto de versões (E1/E2): `ambiente/` (build pendente)
- [ ] Resultado do piloto (tempo por teste, validação do script de cobertura da falha)

## 5. Decisões tomadas

> Registrar aqui toda decisão nova (data, decisão, motivo). Esta seção passa a ser fonte da verdade junto com a entrega 2.

| Data | Decisão | Motivo |
|---|---|---|
| 10/11/2026 | Defects4J **v2.0.1** (Java 8, EvoSuite 1.1.0 incluso) | Versão estável compatível com o EvoSuite; o 3.x exige Java 11 |
| 10/11/2026 | População: falhas ativas com IDs que já estavam nas 357 do artigo (Chart ≤ 26, Closure ≤ 133, Lang ≤ 65, Math ≤ 106, Time ≤ 27) = 353 falhas elegíveis | O 2.0 acrescentou as Closure-134 a 176, que não estavam no artigo; restringir mantém a comparação limpa. As depreciadas no 2.0 são Closure-63, Closure-93, Lang-2 e Time-21 |
| 10/11/2026 | Cobertura medida é **de linhas** (Cobertura), não "de instruções"; ramos também registrados | O `defects4j coverage` usa Cobertura, que reporta linhas (statements) e ramos. Ajusta o termo da entrega 2 |
| 10/11/2026 | Orçamento passado ao `gen_tests.pl`: `-b = 360 × nº de classes` | O wrapper do Defects4J divide o `-b` por 2 (busca/asserções) e pelo nº de classes; assim, a busca fica em 180 s por classe |
| 10/11/2026 | Filtragem de asserções por mutação desativada com `-Dassertion_strategy=all` | No EvoSuite 1.1.0, `filter_assertions` (já `false`) filtra asserções instáveis; a minimização por mutação é `assertion_strategy` (padrão `MUTATION`) |
| 10/11/2026 | Demais opções do EvoSuite = configuração padrão do Defects4J 2.0.1 (inclui `-criterion branch`) | "Opções padrão" interpretado como o padrão da integração Defects4J; **conferir no artigo** |
| 10/11/2026 | Filtragem de instáveis com o `fix_test_suite.pl` nativo | Já remove testes até a suíte passar 5 vezes seguidas na corrigida, exatamente como no planejamento |
| 10/11/2026 | Detecção com o `run_bug_detection.pl` nativo; `Broken` (a suíte não roda na defeituosa) = 0, marcado para conferência | Ferramenta nativa; o caso `Broken` não estava previsto na entrega 2 |
| 10/11/2026 | Cobertura da falha: linhas-alvo = linhas `-` do patch (o patch do D4J vai da corrigida para a defeituosa); linhas não executáveis são ignoradas e, se o trecho não tiver nenhuma executável, usa-se a próxima executável | Complementa a regra da entrega 2 para o caso de linhas que o Cobertura não registra |
| 10/11/2026 | Semente do EvoSuite sorteada por teste pelo `sorteio.py`; conferente = próximo pesquisador da lista (cíclico) | Semente registrada antes da execução; rodízio simples e balanceado |
| 10/11/2026 | Imagem `linux/amd64`, construída uma vez e distribuída (`docker save/load`); ID conferido em todo teste | Mesmo binário para os 7, inclusive em Apple Silicon (emulado) |
| 12/11/2026 | Permissão de execução (`chmod +x`) em `ambiente/rodar.sh`, `scripts/executar_teste.sh` e `scripts/listar_falhas.sh`; conteúdo inalterado | Os arquivos estavam versionados sem o bit de execução (modo 100644), e os comandos do manual falhavam com `Permission denied`. Correção de instrumentação, antes do piloto e do sorteio, sem efeito no tratamento |
| a confirmar | CPU/memória do contêiner (proposta: 2 CPUs, 6 GB); semente do sorteio (proposta: 20261030); falhas do piloto; responsável pela imagem e pelo sorteio; ID da imagem de referência | Pendências do grupo |
