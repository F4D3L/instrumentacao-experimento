# Checklist do ambiente: Gabriel Conti

| Item | Teste 1: Math-45 | Teste 2: Closure-88 | Teste 3: Time-23 | Teste 4: Lang-25 | Teste 5: Chart-8 |
|---|---|---|---|---|---|
| Data/hora | 12/11/2026 12:03 | 12/11/2026 13:50 |  |  |  |
| A1 Docker em execução | ok | ok |  |  |  |
| A2 ID da imagem (8 primeiros caracteres) | ok (45031972) | ok (45031972) |  |  |  |
| A3 Recursos do Docker | ok (10 CPUs, 8,3 GB) | ok (10 CPUs, 8,3 GB) |  |  |  |
| A4 CPUS/MEMORIA inalterados | ok (CPUS=2, MEMORIA=6g) | ok (CPUS=2, MEMORIA=6g) |  |  |  |
| A5 Repositório limpo e atualizado | ok (sem alterações em ambiente/, scripts/, dados/sorteio/) | ok (sem alterações em ambiente/, scripts/, dados/sorteio/) |  |  |  |
| A6 Versões no contêiner | ok (Java 1.8.0_452; Defects4J a83e479; SHAs e TZ conferidos; cgroup 2 CPUs, 6 GB; nproc=10 esperado) | ok (Java 1.8.0_452; Defects4J a83e479; SHAs e TZ conferidos; cgroup 2 CPUs, 6 GB; nproc=10 esperado) |  |  |  |
| A7 Ordem correta | ok (ordem 1) | ok (ordem 2; Math-45 com commit eebedca) |  |  |  |
| A8 Pasta inexistente | ok | ok |  |  |  |
| A9 Disco livre | ok (759 GiB livres) | ok (759 GiB livres) |  |  |  |
| A10 Sem concorrência | ok (AC Power, docker ps vazio) | ok (AC Power, docker ps vazio) |  |  |  |
| D1–D5 Manifesto e log conferidos | ok (D1 manifesto bate com a seção 1; D2 semente 2061223299; D3 orçamento 360 = 360×1 classe; D4 por evidência indireta: suites/logs/Math.45f.log com -b 360 e -s 2061223299, config sha OK; D5 todas as etapas código 0) | ok para D1-D3 (manifesto bate com a seção 1; semente 1061168894; orçamento 360 = 360×1 classe); D4 não aplicável: EvoSuite não foi executado (o projeto não compila, falha na etapa gerar antes do EvoSuite); D5 falha: etapa gerar terminou com código 1 (javac: unmappable character for encoding ASCII)  |  |  |  |
| Máquina (modelo / arquitetura) | Mac17,4 (Apple M5) / arm64 | Mac17,4 (Apple M5) / arm64 |  |  |  |
| Observações | executado por agente de IA (execução centralizada) | executado por agente de IA (execução centralizada) |  |  |  |
