# Checklist do ambiente: Guilherme Celente

| Item | Teste 1: Lang-50 | Teste 2: Math-101 | Teste 3: Closure-42 | Teste 4: Chart-26 | Teste 5: Time-5 |
|---|---|---|---|---|---|
| Data/hora | 12/11/2026 11:43 | 12/11/2026 12:30 |  |  |  |
| A1 Docker em execução | ok | ok (docker info sem erro) |  |  |  |
| A2 ID da imagem (8 primeiros caracteres) | ok (45031972) | ok (45031972) |  |  |  |
| A3 Recursos do Docker | ok (10 CPUs, 7,75 GiB) | ok (10 CPUs, 7,75 GiB) |  |  |  |
| A4 CPUS/MEMORIA inalterados | ok (CPUS=2, MEMORIA=6g) | ok (CPUS=2, MEMORIA=6g) |  |  |  |
| A5 Repositório limpo e atualizado | ok (árvore local limpa; branch sem upstream remoto, pull não aplicável) | ok (árvore sem alterações em ambiente/, scripts/ e dados/sorteio/; sem pull, branch sem upstream remoto) |  |  |  |
| A6 Versões no contêiner | ok (Java 1.8.0_452; Defects4J a83e479; SHAs e TZ conferidos; cgroup 2 CPUs, 6 GiB) | ok (Java 1.8.0_452; Defects4J a83e479; SHAs e TZ conferidos; cgroup 2 CPUs, 6 GiB; JVM 2 CPUs efetivas; nproc 10 esperado) |  |  |  |
| A7 Ordem correta | ok (ordem 1) | ok (ordem 2; ordem 1 Lang-50 com commit cb5dc3c) |  |  |  |
| A8 Pasta inexistente | ok | ok |  |  |  |
| A9 Disco livre | ok (759 GiB livres) | ok (759 GiB livres) |  |  |  |
| A10 Sem concorrência | ok (AC Power, docker ps vazio) | ok (AC Power, docker ps vazio, modo economia de energia desligado) |  |  |  |
| D1–D5 Manifesto e log conferidos | ok (D1 manifesto; D2 semente 1768226709; D3 orçamento 360 = 360×1 classe; D4 por evidência indireta: suites/logs/Lang.50f.log com -b 360 e -s 1768226709, config sha OK; D5 todas as etapas código 0) | NÃO OK: D1 manifesto bate com a seção 1; D2 semente 29410720 ok; D3 orçamento 360 = 360×1 classe ok; D4 não conferível (suites/logs vazio, gerar falhou antes de gerar suíte; sem linha de search_budget/assertion_strategy); D5 falhou: etapa gerar código 1 (javac 'unmappable character for encoding ASCII', erro técnico alheio à ferramenta; execução parada para decisão do grupo) |  |  |  |
| Máquina (modelo / arquitetura) | Apple M5 (Mac17,4) / arm64 | Apple M5 (Mac17,4) / arm64 |  |  |  |
| Observações | executado por agente de IA (execução centralizada) | executado por agente de IA (execução centralizada) |  |  |  |
