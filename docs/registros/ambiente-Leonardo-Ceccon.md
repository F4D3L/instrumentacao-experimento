# Checklist do ambiente: Leonardo Ceccon

| Item | Teste 1: Lang-46 | Teste 2: Time-22 | Teste 3: Math-52 | Teste 4: Closure-38 | Teste 5: Chart-11 |
|---|---|---|---|---|---|
| Data/hora | 12/11/2026 11:50 | 12/11/2026 13:36 |  |  |  |
| A1 Docker em execução | ok | ok |  |  |  |
| A2 ID da imagem (8 primeiros caracteres) | ok (45031972) | ok (45031972) |  |  |  |
| A3 Recursos do Docker | ok (10 CPUs, 7,75 GiB) | ok (10 CPUs, 7,75 GiB) |  |  |  |
| A4 CPUS/MEMORIA inalterados | ok (CPUS=2, MEMORIA=6g) | ok (CPUS=2, MEMORIA=6g) |  |  |  |
| A5 Repositório limpo e atualizado | ok (sem modificações em ambiente/, scripts/ e dados/sorteio/; branch sem upstream remoto, pull não aplicável) | ok (sem modificações em ambiente/, scripts/ e dados/sorteio/; branch sem upstream remoto, pull não aplicável) |  |  |  |
| A6 Versões no contêiner | ok (Java 1.8.0_452; Defects4J a83e479; SHAs e TZ conferidos; cgroup 2 CPUs, 6 GiB) | ok (Java 1.8.0_452; Defects4J a83e479; SHAs e TZ conferidos; cgroup 2 CPUs, 6 GiB; availableProcessors=2) |  |  |  |
| A7 Ordem correta | ok (ordem 1) | ok (ordem 2; Lang-46 com commit de6d728) |  |  |  |
| A8 Pasta inexistente | ok | ok |  |  |  |
| A9 Disco livre | ok (759 GiB livres) | ok (759 GiB livres) |  |  |  |
| A10 Sem concorrência | ok (AC Power, docker ps vazio) | ok (AC Power, docker ps vazio) |  |  |  |
| D1–D5 Manifesto e log conferidos | ok (D1 manifesto bate com a seção 1; D2 semente 1936996271; D3 orçamento 360 = 360×1 classe; D4 por evidência indireta: suites/logs/Lang.46f.log com -b 360 e -s 1936996271, evosuite_config_sha256 OK; D5 todas as etapas código 0) | ok (D1 manifesto bate com a seção 1; D2 semente 1945184215; D3 orçamento 360 = 360×1 classe; D4 por evidência indireta: suites/logs/Time.22f.log com -b 360 e -s 1945184215, evosuite_config_sha256 OK; D5 todas as etapas código 0) | | | |
| Máquina (modelo / arquitetura) | Apple M5 (Mac17,4) / arm64 | MacBook Air (Mac17,4) / Apple M5 / arm64 |  |  |  |
| Observações | executado por agente de IA (execução centralizada) | executado por agente de IA (execução centralizada) |  |  |  |
