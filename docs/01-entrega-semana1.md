# Entrega 1: Hipótese de pesquisa e escopo do experimento

> Transcrição de `Entrega1_Hipotese_e_Escopo_EvoSuite_Defects4J.docx`. Entregue em 29/10/2026.
> Onde houver divergência, vale a entrega 2 (o grupo passou de 6 para 7 integrantes: 30 → 35 testes, 6 → 7 falhas por projeto).

**Título:** Hipótese de pesquisa e escopo do experimento: geração automática de testes unitários e detecção de falhas reais

## 1 Tema e questão de pesquisa

O experimento verifica se a taxa com que o EvoSuite detecta falhas reais é compatível com a relatada na literatura. A referência central é Shamshiri et al. (2015), que aplicaram a ferramenta às 357 falhas reais do Defects4J: cada execução do EvoSuite detectou, em média, 82,1 falhas (23,0%), e 145 falhas (40,6%) foram detectadas em pelo menos uma de 10 execuções.

**Questão de pesquisa:** a taxa de detecção de falhas reais por execução do EvoSuite, replicada em 35 falhas sorteadas do Defects4J, é compatível com o valor publicado, e a detecção está associada à cobertura de código obtida? Como questão secundária, descritiva, examinamos até que ponto o resultado depende das falhas que entram na amostra e da forma como a cobertura é medida (validade de construto do benchmark).

## 2 Hipótese de pesquisa (teórica)

**Hipótese:** a probabilidade de uma suíte gerada automaticamente detectar uma falha real cresce com a cobertura do código defeituoso. A cobertura, porém, é condição necessária e não suficiente, pois o estado incorreto precisa se propagar até uma asserção (oráculo). Por isso, espera-se uma taxa de detecção limitada, em torno de um quarto das falhas por execução.

A relação esperada é A → B, em que A é a técnica de geração baseada em busca (variável independente) e B é a efetividade em detectar falhas (variáveis dependentes). A hipótese se apoia em quatro referências:

- **Mecanismo da ferramenta (Fraser; Arcuri, 2013):** o EvoSuite evolui suítes inteiras com um algoritmo genético guiado por critérios de cobertura e só depois acrescenta asserções de regressão. Ele otimiza cobertura, não detecção de falhas.
- **Evidência sobre cobertura e oráculo (Shamshiri et al., 2015):** 16,2% das falhas nunca foram executadas pelos testes gerados, enquanto 63,3% das não detectadas foram cobertas ao menos uma vez sem serem reveladas. As suítes que detectaram falhas tiveram cobertura significativamente maior (Mann-Whitney, p < 0,001; correlação média de Pearson de 0,40).
- **Variação por contexto (Almasi et al., 2017):** em um sistema financeiro industrial, o EvoSuite detectou 56,40% de 25 falhas reais. A efetividade depende do software sob teste, o que justifica bloquear por projeto.
- **Base de objetos (Just; Jalali; Ernst, 2014):** o Defects4J isola cada falha real em um par de versões defeituosa/corrigida com diferença mínima, o que permite medir a detecção de forma objetiva e pareada.

Desdobramento operacional (p = proporção de falhas detectadas por execução):

- **H0₁:** p = 26,5% · **H1₁:** p ≠ 26,5%. O valor é a média das taxas por projeto de Shamshiri et al. (2015) (Chart 37,3%; Closure 8,9%; Lang 14,2%; Math 40,5%; Time 31,5%), equivalente a uma amostra balanceada entre os projetos (7 falhas por projeto). Teste binomial exato bicaudal, α = 0,05; a taxa geral de 23,0% serve de referência secundária.
- **H0₂:** a cobertura de instruções das suítes que detectam a falha é igual à das que não detectam · **H1₂:** é maior nas que detectam. Teste de Mann-Whitney unilateral, α = 0,05, comparado ao resultado significativo de Shamshiri et al. (2015).

Com 35 testes, a margem de erro de uma proporção próxima de 26% é de cerca de ±15 pontos percentuais (IC 95%). O resultado será lido como compatibilidade com a literatura, e não como estimativa precisa nem prova de equivalência.

## 3 Escopo (modelo de Wohlin et al., 2012)

**Síntese:** analisar suítes de testes unitários geradas pelo EvoSuite, com o propósito de avaliá-las frente a um benchmark da literatura, com respeito à efetividade na detecção de falhas reais, do ponto de vista dos pesquisadores, no contexto de um experimento in-vitro sobre falhas do Defects4J conduzido por estudantes de Engenharia de Software da PUCPR.

| Elemento | Definição neste experimento |
|---|---|
| **Objeto** (o que é estudado) | Suítes de testes unitários JUnit geradas pelo EvoSuite para as classes modificadas na correção de falhas reais do Defects4J. A configuração replica Shamshiri et al. (2015): opções padrão, orçamento de busca de 3 min por classe e filtragem de asserções por mutação desativada. A suíte é gerada na versão corrigida, com uma execução por falha e semente registrada. |
| **Propósito** (para que) | Avaliar a efetividade da geração automática de testes na detecção de falhas reais e verificar se os resultados são compatíveis com a evidência publicada (replicação com benchmark da literatura). |
| **Foco de qualidade** (o que é medido) | Efetividade, medida por três variáveis dependentes: (1) **Detecção da falha** (sim/não): ao menos um teste passa na versão corrigida e falha na versão defeituosa, após remover testes instáveis (5 execuções na versão corrigida). (2) **Cobertura de instruções da classe** (%) das classes modificadas pela correção, medida com `defects4j coverage` na versão corrigida. (3) **Cobertura da falha** (total/parcial/nenhuma): execução das linhas alteradas pela correção, obtidas do patch da falha no Defects4J. Caracterização das falhas (observada, não manipulada): forma de revelação pelo teste do desenvolvedor (asserção/exceção/ambas) e tamanho da correção, usadas só para descrever a amostra. |
| **Perspectiva** (quem avalia) | Pesquisadores, representando desenvolvedores que adotariam a geração automática de testes como rede de proteção em testes de regressão. |
| **Contexto** (ambiente e população) | Experimento in-vitro, offline e orientado a artefatos: 7 pesquisadores do 6º período de Engenharia de Software da PUCPR operam as ferramentas sobre artefatos. População: falhas reais ativas (não depreciadas) dos 5 projetos Java originais do Defects4J (JFreeChart, Closure, Commons Lang, Commons Math e Joda-Time). **Bloqueamento:** por projeto, com 7 falhas por bloco (5 × 7 = 35 testes; 5 por pesquisador, uma de cada projeto). **Aleatoriedade:** sorteio das falhas ativas de cada projeto com semente registrada (7 falhas e 3 reservas por projeto); atribuição aos pesquisadores e ordem de execução também sorteadas. **Pareamento:** cada falha é um par versão defeituosa/corrigida; a suíte é gerada na corrigida e executada nas duas versões. **Controle:** execução por pipeline único em uma imagem de contêiner, com versões do EvoSuite, do Defects4J e do JDK fixadas e CPU e memória iguais para todos. |

A única variável independente é a técnica de geração de testes (EvoSuite, em nível único, comparado ao benchmark). Como a medição é automática e cada um dos 7 pesquisadores executa uma falha de cada projeto, a influência do operador fica restrita aos passos manuais (preparação do ambiente e confirmação de falsos positivos, conferida por um segundo integrante).

## Referências

- ALMASI, M. M. et al. An industrial evaluation of unit test generation: finding real faults in a financial application. In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING: SOFTWARE ENGINEERING IN PRACTICE TRACK, 39., 2017, Buenos Aires. Proceedings [...]. IEEE, 2017. p. 263–272.
- FRASER, G.; ARCURI, A. Whole test suite generation. IEEE Transactions on Software Engineering, v. 39, n. 2, p. 276–291, 2013.
- JUST, R.; JALALI, D.; ERNST, M. D. Defects4J: a database of existing faults to enable controlled testing studies for Java programs. In: INTERNATIONAL SYMPOSIUM ON SOFTWARE TESTING AND ANALYSIS, 2014, San Jose. Proceedings [...]. ACM, 2014. p. 437–440.
- SHAMSHIRI, S. et al. Do automatically generated unit tests find real faults? An empirical study of effectiveness and challenges. In: INTERNATIONAL CONFERENCE ON AUTOMATED SOFTWARE ENGINEERING, 30., 2015, Lincoln. Proceedings [...]. IEEE/ACM, 2015. p. 201–211.
- WOHLIN, C. et al. Experimentation in software engineering. Berlin: Springer, 2012.
