# Fonte da verdade do experimento

Projeto da disciplina **Experimentação em Engenharia de Software** (BES · PUCPR · 2026, prof. Rafael Carvalho Machado).
Grupo de 7: Lucas Reali, Guilherme Fadel, Guilherme Celente, Leonardo Ceccon, Gabriel Moribe, Gabriel Conti, Thiago Akimoto.

## Para o agente: leia nesta ordem

1. [`00-enunciados.md`](00-enunciados.md): o que o professor pediu em cada semana (texto do enunciado).
2. [`01-entrega-semana1.md`](01-entrega-semana1.md): hipótese e escopo (entregue em 29/10/2026).
3. [`02-entrega-semana2.md`](02-entrega-semana2.md): planejamento do experimento (entregue em 04/11/2026). **É o documento mais recente e prevalece sobre a semana 1.**
4. [`03-semana3-instrumentacao.md`](03-semana3-instrumentacao.md): o que precisa ser produzido agora, o que a semana 2 já prometeu e o que ainda está em aberto.

Regras:

- Hierarquia: enunciado do professor > entrega da semana 2 > entrega da semana 1. Os `.docx` na raiz do projeto são os originais; os `.md` aqui são transcrições fiéis deles.
- Não invente números, referências ou decisões. Se algo não estiver nestes arquivos, trate como **em aberto** e pergunte.
- Toda decisão nova tomada na semana 3 deve ser registrada em `03-semana3-instrumentacao.md` (seção "Decisões tomadas").
- Idioma de todo o material: português (Brasil), normas ABNT nas referências.

## Fatos fixados (resumo rápido)

| Item | Valor |
|---|---|
| Ferramenta (tratamento, nível único) | EvoSuite, opções padrão, 180 s de busca por classe, filtragem de asserções por mutação desativada, 1 execução por falha, semente registrada |
| Geração | Sobre as classes modificadas (`classes.modified`), na versão **corrigida** |
| Objetos | Falhas reais ativas do Defects4J, 5 projetos originais: Chart, Closure, Lang, Math, Time |
| Amostra | 35 falhas = 5 blocos (projetos) × 7; 5 testes por pesquisador (1 de cada projeto); 3 reservas por projeto |
| Sorteio | `random.Random(semente).sample`, semente proposta 20261030, 10 por projeto (7 + 3 reservas), 2 falhas do piloto excluídas antes |
| Variáveis dependentes | Detecção (0/1); cobertura de instruções da classe (%); cobertura da falha (total/parcial/nenhuma) |
| Caracterização (não manipulada) | Forma de revelação (asserção/exceção/ambas); tamanho da correção (linhas no patch) |
| H0₁ | p = 26,5% (média por projeto de Shamshiri et al., 2015). Binomial exato bicaudal, α = 0,05. Referência secundária 23,0% |
| H0₂ | Cobertura igual entre suítes que detectam e não detectam. Mann-Whitney unilateral, α = 0,05 |
| Referências por projeto | Chart 37,3% · Closure 8,9% · Lang 14,2% · Math 40,5% · Time 31,5% |
| Filtro de instáveis | 5 execuções na versão corrigida |
| Ambiente | Imagem de contêiner única, versões fixadas, CPU/memória iguais |
| Artigo base | Shamshiri et al. (2015), ASE: 357 falhas, 23,0% por execução, 40,6% em ao menos 1 de 10 |
