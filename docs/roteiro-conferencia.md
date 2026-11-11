# Roteiro de conferência cruzada

Cada teste é conferido por um segundo integrante, a partir **só dos arquivos versionados**, sem reexecutar nada.
**Rodízio:** o conferente é o pesquisador seguinte na lista, de forma cíclica (coluna `conferente` em `dados/sorteio/atribuicao.csv`):

Lucas Reali → Guilherme Fadel → Guilherme Celente → Leonardo Ceccon → Gabriel Moribe → Gabriel Conti → Thiago Akimoto → Lucas Reali

## Para cada teste do colega

| # | Verificação | Onde |
|---|---|---|
| C1 | O checklist do ambiente do teste está preenchido e todos os itens estão `ok` (ou com a exceção justificada) | `docs/registros/ambiente-<Nome>.md` |
| C2 | O manifesto mostra a imagem, as versões, os SHA-256 e os recursos de referência; a semente é a de `atribuicao.csv` | `resultados/<Falha>/manifesto.txt` |
| C3 | Os testes foram feitos na ordem sorteada (datas dos manifestos e dos commits em ordem crescente) | `manifesto.txt` e `git log` |
| C4 | A linha do registro bate com as saídas: `resultado_d4j`/`testes_reveladores` com `deteccao/bug_detection`; `linhas_*` com `cobertura/coverage`; `cobertura_falha` com `cobertura_falha.txt` | `dados/registro.csv` e `resultados/<Falha>/` |
| C5 | **Se detectou:** o checklist de falso positivo está preenchido e você concorda com a decisão | `docs/registros/falso-positivo-<Falha>.md` |
| C6 | **Se não detectou e havia testes gerados:** o `bug_detection` é `Pass` (ou `Broken` com o motivo anotado); nenhum teste foi removido por erro de infraestrutura em massa (ler o `fix_test_suite.run.log`) | `deteccao/`, `suites/.../fix_test_suite.*.log` |
| C7 | **Se `cobertura_falha` é `indeterminado` ou foi classificada à mão:** a classificação segue as regras da seção 5.2 do manual | `cobertura_falha.txt`, patch e `coverage.xml` |
| C8 | Nenhum log foi editado à mão (`git log -p` da pasta mostra só o commit do teste) | `git log -p resultados/<Falha>` |

## Resultado

Na linha do teste em `dados/registro.csv`, coluna `conferencia`:

- `ok:<seu nome>`, se todos os itens passaram;
- `divergente:<seu nome>:<itens>`, se algum falhou. Nesse caso, avise o executor; a divergência é resolvida pelos dois e, se persistir, na reunião do grupo, com a decisão registrada em "Decisões tomadas" do `03-semana3-instrumentacao.md`.

A análise (`scripts/analise.py`) só é rodada quando os 35 testes estiverem com a conferência `ok`.
