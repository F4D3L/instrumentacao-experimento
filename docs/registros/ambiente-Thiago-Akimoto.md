# Checklist do ambiente: Thiago Akimoto

| Item | Teste 1: Lang-12 | Teste 2: Time-13 | Teste 3: Chart-17 | Teste 4: Math-65 | Teste 5: Closure-108 |
|---|---|---|---|---|---|
| Data/hora | 12/11/2026 12:07 (America/Sao_Paulo) |  |  |  |  |
| A1 Docker em execução | ok (docker info responde, servidor 29.9.1) |  |  |  |  |
| A2 ID da imagem (8 primeiros caracteres) | ok (45031972) |  |  |  |  |
| A3 Recursos do Docker | ok (10 CPUs, 8,3 GB; exigido 2 CPUs e 6g) |  |  |  |  |
| A4 CPUS/MEMORIA inalterados | ok (CPUS="2", MEMORIA="6g") |  |  |  |  |
| A5 Repositório limpo e atualizado | ok (sem alterações em ambiente/, scripts/, dados/sorteio/; sem upstream configurado para a branch, fetch sem erro) |  |  |  |  |
| A6 Versões no contêiner | ok (openjdk 1.8.0_452; Defects4J a83e479; EvoSuite 939c0c76...; config 7349236d...; TZ America/Los_Angeles; nproc=10 esperado por cota de cgroup; cpu.max 200000 100000 = 2 CPUs; memory.max 6442450944) |  |  |  |  |
| A7 Ordem correta | ok (ordem 1 de Thiago Akimoto: Lang-12; sem falhas anteriores) |  |  |  |  |
| A8 Pasta inexistente | ok (resultados/Lang-12 não existe) |  |  |  |  |
| A9 Disco livre | ok (759 GiB livres) |  |  |  |  |
| A10 Sem concorrência | ok (AC Power; docker ps vazio) |  |  |  |  |
| D1–D5 Manifesto e log conferidos | ok (D1 manifesto bate com a seção 1; D2 semente 728680798; D3 orçamento 360 = 360 × 1 classe; D4 por evidência indireta: Lang.12f.log com -b 360 e -s 728680798, evosuite_config_sha256 7349236d...; D5 todas as etapas com código 0) |  |  |  |  |
| Máquina (modelo / arquitetura) | Mac17,4 / Apple M5, arm64 |  |  |  |  |
| Observações | executado por agente de IA (execução centralizada) |  |  |  |  |
