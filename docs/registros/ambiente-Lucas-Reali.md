# Checklist do ambiente: Lucas Reali

| Item | Teste 1: Lang-31 | Teste 2: Chart-2 | Teste 3: Closure-75 | Teste 4: Time-18 | Teste 5: Math-63 |
|---|---|---|---|---|---|
| Data/hora | 12/11/2026 11:29 | 12/11/2026 07:11 (America/Los_Angeles) |  |  |  |
| A1 Docker em execução | ok | ok |  |  |  |
| A2 ID da imagem (8 primeiros caracteres) | ok (45031972) | ok (45031972) |  |  |  |
| A3 Recursos do Docker | ok (10 CPUs, 8,3 GB) | ok (10 CPUs, 8,3 GB) |  |  |  |
| A4 CPUS/MEMORIA inalterados | ok (CPUS=2, MEMORIA=6g) | ok (CPUS=2, MEMORIA=6g) |  |  |  |
| A5 Repositório limpo e atualizado | ok | ok (status limpo em ambiente/, scripts/ e dados/sorteio/; branch sem remoto, sem pull) |  |  |  |
| A6 Versões no contêiner | ok (Java 1.8.0_452; Defects4J a83e479; SHAs e TZ conferidos; cgroup 2 CPUs) | ok (Java 1.8.0_452; Defects4J a83e479; SHAs e TZ conferidos; cgroup 200000/100000 = 2 CPUs) |  |  |  |
| A7 Ordem correta | ok (ordem 1) | ok (ordem 2; Lang-31 com commit 889cdb2) |  |  |  |
| A8 Pasta inexistente | ok | ok |  |  |  |
| A9 Disco livre | ok (759 GiB livres) | ok (759 GiB livres) |  |  |  |
| A10 Sem concorrência | ok (AC Power, modo economia desligado, docker ps vazio) | ok (AC Power, docker ps vazio) |  |  |  |
| D1–D5 Manifesto e log conferidos | ok (D1 manifesto; D2 semente 432222207; D3 orçamento 360 = 360×1 classe; D4 por evidência indireta: suites/logs/Lang.31f.log com -b 360 e -s 432222207, config sha OK; D5 todas as etapas código 0) | ok (D1 manifesto; D2 semente 1123060191; D3 orçamento 360 = 360×1 classe; D4 por evidência indireta: suites/logs/Chart.2f.log com -b 360 e -s 1123060191, config sha OK; D5 todas as etapas código 0) |  |  |  |  |
| Máquina (modelo / arquitetura) | Apple M5 (Mac17,4) / arm64 | Apple M5 (Mac17,4) / arm64 |  |  |  |
| Observações | executado por agente de IA (execução centralizada) | executado por agente de IA (execução centralizada) |  |  |  |
