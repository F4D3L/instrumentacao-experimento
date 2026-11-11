# Checklist de falso positivo

Aplicar a **toda detecção automática** (`deteccao_automatica = 1`). O objetivo é confirmar que o teste falha na versão defeituosa **por causa da falha corrigida**, e não por ambiente, ordem de execução ou não determinismo.
O executor preenche; o conferente revisa (ver `roteiro-conferencia.md`).
Registro: copie o modelo da seção 3 para `docs/registros/falso-positivo-<Falha>.md` e faça o commit junto com o teste.

## 1. Onde olhar

| Evidência | Arquivo |
|---|---|
| Testes que falharam na defeituosa, com stack trace | `resultados/<Falha>/deteccao/bug_detection_log/<Projeto>/evosuite/<id>b.1.trigger.log` |
| Suíte filtrada | `resultados/<Falha>/suites/<Projeto>/evosuite/1/<Projeto>-<id>f-evosuite.1.tar.bz2` |
| Patch da correção | `framework/projects/<Projeto>/patches/<id>.src.patch`, no contêiner (`$D4J_HOME`) |
| Testes removidos na filtragem | `resultados/<Falha>/suites/<Projeto>/evosuite/1/fix_test_suite.run.log` |

Para ver o patch:

```bash
ambiente/rodar.sh bash -c 'cat $D4J_HOME/framework/projects/<Projeto>/patches/<id>.src.patch'
```

## 2. Perguntas (fixas)

Para cada teste revelador (ou para uma amostra de até 3, se houver muitos):

| # | Pergunta | Resposta esperada para confirmar |
|---|---|---|
| F1 | O stack trace ou a asserção que falhou passa por um método ou classe alterado no patch? | Sim |
| F2 | O valor esperado na asserção (ou a exceção lançada) é coerente com o comportamento da versão **corrigida**, e o valor obtido, com o da **defeituosa**? | Sim |
| F3 | A falha **não** depende de data/hora, fuso, locale, ordem de `HashMap`/`HashSet`, rede, sistema de arquivos ou memória? | Sim (não depende) |
| F4 | O teste passou nas 5 execuções da filtragem na versão corrigida, ou seja, não aparece como removido no `fix_test_suite.run.log`? | Sim |
| F5 | A mensagem não é de erro de infraestrutura (timeout do EvoSuite, `ClassNotFoundException`, `NoClassDefFoundError`, falta de memória)? | Sim |

**Decisão:**

- Todas as respostas conforme o esperado → `falso_positivo = nao`, `deteccao_confirmada = 1`.
- F3 ou F5 falham em **todos** os testes reveladores → `falso_positivo = sim`, `deteccao_confirmada = 0`.
- Dúvida (por exemplo, F1 ou F2 sem resposta clara) → `falso_positivo = duvida`. Deixe `deteccao_confirmada = pendente` e leve o caso à reunião; a decisão do grupo é registrada em "Decisões tomadas".

## 3. Modelo de registro (copiar para `docs/registros/falso-positivo-<Falha>.md`)

```markdown
# Falso positivo: <Falha>

- Executor: <nome> · Data: <data>
- Testes reveladores (`testes_reveladores`): <n>
- Testes analisados: <Classe::método>, ...

| # | Resposta | Justificativa (trecho do log/patch) |
|---|---|---|
| F1 |  |  |
| F2 |  |  |
| F3 |  |  |
| F4 |  |  |
| F5 |  |  |

- Decisão do executor: falso_positivo = <nao|sim|duvida>; deteccao_confirmada = <1|0|pendente>
- Conferente: <nome> · Data: <data> · Concorda? <sim|não, motivo>
```
