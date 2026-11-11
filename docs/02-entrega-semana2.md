# Entrega 2: Planejamento do experimento

> Transcrição de `segunda_entrega_revisada.docx`. Entregue em 04/11/2026. **Documento vigente**: prevalece sobre a entrega 1.

## Escopo e contexto do experimento

Queremos verificar se a efetividade do EvoSuite na detecção de falhas reais é compatível com a evidência publicada por Shamshiri et al. (2015). Medimos essa efetividade pela proporção de falhas detectadas por execução e pela cobertura que as suítes geradas alcançam, do ponto de vista dos próprios pesquisadores, estudantes do sexto período de Engenharia de Software da PUCPR. No modelo de Wohlin et al. (2012), o objetivo fica assim: analisar suítes de testes unitários geradas pelo EvoSuite, com o propósito de avaliá-las frente a um benchmark da literatura, com respeito à efetividade na detecção de falhas reais, do ponto de vista dos pesquisadores, no contexto de um experimento in-vitro sobre falhas do Defects4J.

Só repetir o número do artigo, porém, deixaria de fora a questão que mais nos interessa: a validade de construto do próprio benchmark. Os autores reconhecem que o Defects4J não distingue o tipo nem a gravidade das falhas e que cada falha é a diferença minimizada entre a versão defeituosa e a corrigida, e não a mudança que de fato introduziu o bug (Shamshiri et al., 2015, seção II.D). Nem toda falha do conjunto se comporta, portanto, como uma regressão real, e a taxa publicada pode subestimar ou superestimar a efetividade da ferramenta. Como usamos a mesma base e o mesmo cenário, herdamos essa ameaça. Em vez de deixá-la implícita, decidimos assumi-la e examiná-la: caracterizamos cada falha sorteada e medimos, além da cobertura da classe, a cobertura das linhas alteradas pela correção, como fez o artigo original. Com isso, conseguimos discutir não só se a nossa taxa bate com a publicada, mas também o quanto a nossa amostra se parece com o conjunto de falhas que produziu aquele valor.

O experimento é orientado a artefatos. Os sujeitos são os 7 integrantes do grupo (Lucas Reali, Guilherme Fadel, Guilherme Celente, Leonardo Ceccon, Gabriel Moribe, Gabriel Conti e Thiago Akimoto), que operam o EvoSuite sobre os objetos, que são falhas reais do Defects4J. A população de acesso são as falhas ativas (não depreciadas) dos cinco projetos Java originais do benchmark: JFreeChart (Chart), Closure, Commons Lang, Commons Math e Joda-Time (Time), que somavam 357 falhas na versão usada pelo artigo. Vamos realizar 35 testes, 5 por integrante, cada um sobre uma falha diferente. Um teste consiste em gerar a suíte, executá-la nas versões corrigida e defeituosa e medir as coberturas, tudo por script. Estimamos de 10 a 15 minutos por teste (3 deles só para a busca por classe), o que dá cerca de 1 hora por integrante. Esse tempo será confirmado no piloto, descrito na seção de instrumentação.

## Variáveis

### Variável independente: uso da técnica de geração de testes EvoSuite

- **Definição constitutiva:** técnica de geração automática de testes unitários baseada em busca. O EvoSuite evolui suítes inteiras com um algoritmo genético guiado por critérios de cobertura e só no final acrescenta asserções de regressão (Fraser; Arcuri, 2013). A variável tem um único nível: no lugar de um segundo tratamento, comparamos o resultado com o valor de referência de Shamshiri et al. (2015).
- **Definição operacional:** executar o EvoSuite (versão fixada no protocolo) com as opções padrão, 180 s de busca por classe e a filtragem de asserções por mutação desativada, como em Shamshiri et al. (2015). A geração é feita sobre cada classe modificada pela correção da falha, na versão corrigida (propriedade `classes.modified` do Defects4J). Fazemos uma execução por falha e registramos a semente do EvoSuite.

### Variável dependente: detecção da falha

- **Definição constitutiva:** capacidade de a suíte gerada revelar uma falha real, ou seja, de produzir um comportamento observável diferente entre a versão defeituosa e a corrigida (Shamshiri et al., 2015).
- **Definição operacional:** variável binária por falha. Vale 1 quando pelo menos um teste da suíte passa na versão corrigida e falha na defeituosa, e 0 caso contrário. Antes disso, descartamos os testes instáveis, que são os que não repetem o mesmo resultado em 5 execuções seguidas na versão corrigida. Toda detecção é confirmada manualmente, para excluir falsos positivos. A medida agregada é p̂ = falhas detectadas / 35.

### Variável dependente: cobertura de instruções da classe

- **Definição constitutiva:** grau em que o código relevante à falha é exercitado pela suíte gerada. A cobertura é condição necessária, mas não suficiente, para a detecção, já que o estado incorreto ainda precisa chegar a uma asserção (Shamshiri et al., 2015).
- **Definição operacional:** percentual de instruções executadas nas classes modificadas pela correção, medido com a ferramenta de cobertura do Defects4J (`defects4j coverage`) sobre a suíte filtrada, na versão corrigida. É a mesma medida que o artigo usa para as classes relevantes à falha, o que mantém direta a comparação de H0₂. Registramos um valor por falha e a mediana por projeto.

### Variável dependente: cobertura da falha

- **Definição constitutiva:** grau em que a suíte executa exatamente o trecho de código alterado pela correção. O artigo usa essa medida para separar as falhas que nem chegaram a ser executadas daquelas que foram executadas sem ser reveladas (Shamshiri et al., 2015). Ela também cobre uma fraqueza da medida anterior: em classes grandes, a cobertura da classe pode ser alta sem que a linha defeituosa seja tocada.
- **Definição operacional:** variável ordinal por falha, com os três níveis do artigo: **total** (todas as instruções modificadas pela correção foram executadas), **parcial** (parte delas) e **nenhuma**. As linhas modificadas vêm do patch da falha no Defects4J (linhas da versão corrigida que foram adicionadas ou alteradas) e são cruzadas com o relatório por linha do `defects4j coverage`. Quando a correção só remove código, consideramos a linha logo depois do trecho removido. Essa regra é uma decisão nossa e fica registrada no protocolo.

### Variáveis de caracterização das falhas (observadas, não manipuladas)

Estas variáveis não são tratamentos e não entram como variáveis independentes. Elas só descrevem a amostra, para que possamos compará-la com o conjunto usado no artigo e discutir a ameaça de construto herdada.

- **Forma de revelação pelo teste do desenvolvedor:** asserção, exceção ou ambas, conforme a causa que o Defects4J registra para os testes que revelam a falha (`defects4j info`). É a mesma classificação usada na Tabela II de Shamshiri et al. (2015).
- **Tamanho da correção:** número de linhas alteradas no patch da falha.

## Seleção de sujeitos

Como o experimento é orientado a artefatos e a medição é automática, duas seleções afetam a validade: a dos sujeitos que operam o experimento e a dos objetos (falhas) sobre os quais ele opera. O cenário de recrutar 60 voluntários entre 150 estudantes não se aplica aqui, porque não há participantes externos nem tarefa humana sendo avaliada.

**Sujeitos.** Participam todos os 7 integrantes do grupo (censo), com o mesmo perfil: estudantes do mesmo período e da mesma disciplina. Não há voluntariado nem recusa, e por isso não existe autosseleção de sujeitos. Todos seguem o mesmo protocolo, na mesma imagem de ambiente e por script, o que deixa a influência do operador restrita aos passos manuais (preparação do ambiente e confirmação de falsos positivos).

**Objetos.** Nesse desenho, a autosseleção apareceria se escolhêssemos falhas "convenientes". Para evitar isso, seguimos o procedimento abaixo:

1. Listar, para cada projeto, as falhas ativas do Defects4J (`defects4j query`), sem as depreciadas, e registrar a lista no repositório do grupo.
2. Fixar e registrar a semente do sorteio antes de ver o resultado (por exemplo, 20261030, a data deste planejamento). Antes do sorteio, tirar da lista as 2 falhas usadas no piloto.
3. Sortear por script (`random.Random(semente).sample`) 10 falhas por projeto, sem reposição. As 7 primeiras entram no experimento e as 3 seguintes ficam de reserva. Ninguém escolhe, troca ou descarta falhas manualmente.
4. Distribuir as 7 falhas de cada projeto entre os 7 pesquisadores por uma permutação sorteada, de modo que cada pesquisador receba exatamente uma falha de cada projeto (5 testes por integrante).
5. Sortear a ordem de execução dos 5 testes de cada pesquisador.
6. Caracterizar as 35 falhas sorteadas (forma de revelação e tamanho da correção) e versionar essa tabela antes de qualquer execução. Esse passo não altera a amostra, apenas documenta como ela é.
7. **Regra de substituição**, definida antes da execução: uma falha só é trocada por uma reserva do mesmo projeto se houver um impedimento técnico que não dependa da ferramenta (por exemplo, o projeto não compila no ambiente), e o motivo é registrado. Se o EvoSuite não gerar testes ou não detectar a falha, o resultado vale 0 e a falha não é substituída, para não favorecer a ferramenta.

É importante deixar claro o limite desse procedimento. O sorteio controla o viés de quem escolhe as falhas, mas não torna as falhas do Defects4J mais representativas de regressões reais. Essa questão é tratada como ameaça de construto herdada (ver "Análise de ameaças à validade") e discutida a partir da caracterização feita no passo 6.

## Desenho experimental

O desenho tem um fator (a técnica de geração) com um único nível, o EvoSuite, comparado ao valor de referência da literatura. Três recursos aumentam a confiabilidade (Wohlin et al., 2012):

- **Bloqueamento por projeto** (5 blocos de 7 falhas). A taxa de detecção muda bastante de um projeto para outro (de 8,9% em Closure a 40,5% em Math, segundo Shamshiri et al., 2015), e Almasi et al. (2017) mostram que a efetividade depende do software testado. O bloqueio evita que o sorteio produza uma amostra desequilibrada e permite comparar cada bloco com a taxa publicada para o mesmo projeto.
- **Pareamento.** Cada falha é um par de versões, defeituosa e corrigida (Just; Jalali; Ernst, 2014). A mesma suíte roda nas duas, então a comparação acontece dentro do próprio objeto. Além disso, cada pesquisador executa uma falha de cada projeto, o que cruza pesquisador e projeto de forma balanceada.
- **Aleatoriedade** na seleção das falhas, na atribuição aos pesquisadores e na ordem de execução, sempre por script e com semente registrada.

A tabela abaixo mostra como sujeitos, objetos e tratamento se combinam. Cada célula é um teste (7 × 5 = 35). Os identificadores das falhas serão preenchidos depois do sorteio, e a última linha traz o valor de referência de cada bloco.

| Pesquisador | Bloco Chart | Bloco Closure | Bloco Lang | Bloco Math | Bloco Time | Ordem de execução |
|---|---|---|---|---|---|---|
| Lucas Reali | Chart-__ / EvoSuite | Closure-__ / EvoSuite | Lang-__ / EvoSuite | Math-__ / EvoSuite | Time-__ / EvoSuite | sorteada (registrar) |
| Guilherme Fadel | Chart-__ / EvoSuite | Closure-__ / EvoSuite | Lang-__ / EvoSuite | Math-__ / EvoSuite | Time-__ / EvoSuite | sorteada (registrar) |
| Guilherme Celente | Chart-__ / EvoSuite | Closure-__ / EvoSuite | Lang-__ / EvoSuite | Math-__ / EvoSuite | Time-__ / EvoSuite | sorteada (registrar) |
| Leonardo Ceccon | Chart-__ / EvoSuite | Closure-__ / EvoSuite | Lang-__ / EvoSuite | Math-__ / EvoSuite | Time-__ / EvoSuite | sorteada (registrar) |
| Gabriel Moribe | Chart-__ / EvoSuite | Closure-__ / EvoSuite | Lang-__ / EvoSuite | Math-__ / EvoSuite | Time-__ / EvoSuite | sorteada (registrar) |
| Gabriel Conti | Chart-__ / EvoSuite | Closure-__ / EvoSuite | Lang-__ / EvoSuite | Math-__ / EvoSuite | Time-__ / EvoSuite | sorteada (registrar) |
| Thiago Akimoto | Chart-__ / EvoSuite | Closure-__ / EvoSuite | Lang-__ / EvoSuite | Math-__ / EvoSuite | Time-__ / EvoSuite | sorteada (registrar) |
| **Referência (Shamshiri et al., 2015)** | 37,3% | 8,9% | 14,2% | 40,5% | 31,5% | 26,5% (média) · 23,0% (geral) |

**Hipóteses** (desdobramento operacional da primeira entrega; p = proporção de falhas detectadas por execução):

- **H0₁:** p = 26,5% · **H1₁:** p ≠ 26,5%. O valor de referência é a média das taxas por projeto de Shamshiri et al. (2015) (Chart 37,3%; Closure 8,9%; Lang 14,2%; Math 40,5%; Time 31,5%). A taxa geral de 23,0% fica como referência secundária. Teste binomial exato bicaudal, α = 0,05.
- **H0₂:** a cobertura de instruções das suítes que detectam a falha é igual à das que não detectam · **H1₂:** é maior nas que detectam. Teste de Mann-Whitney unilateral, α = 0,05, comparado ao resultado significativo de Shamshiri et al. (2015).

**Questão secundária: validade de construto.** Além das duas hipóteses, queremos olhar para a pergunta que motivou a escolha do tema: até que ponto o resultado depende das falhas que entram na amostra e da forma como medimos a cobertura? Como cada categoria terá poucos casos, essa parte é descritiva, sem teste de hipótese, e se divide em duas frentes:

- **Representatividade das falhas.** Comparamos a composição da nossa amostra (forma de revelação e tamanho da correção) com a do conjunto original e a proporção de detecção em cada forma de revelação com a Tabela II do artigo. Se a taxa variar muito entre categorias, isso indica que o valor agregado depende da mistura de falhas do benchmark, que é justamente a ameaça que os autores apontam.
- **Validade da medida de cobertura.** Cruzamos a detecção com a cobertura da falha (total, parcial ou nenhuma) e comparamos a cobertura da classe com a cobertura da falha. Pela hipótese da primeira entrega, as falhas detectadas devem ter cobertura total ou parcial, e parte das não detectadas deve ter sido executada sem ser revelada, como o artigo observou. Casos com cobertura alta da classe e cobertura nenhuma da falha mostram o quanto a medida da classe pode enganar.

**Ajustes em relação à primeira entrega.** O primeiro ajuste é o tamanho do grupo, que passou a ter 7 integrantes. Mantida a regra de 5 testes por integrante, o experimento sobe de 30 para 35 testes, com 7 falhas por projeto (antes, 6). O valor de referência de 26,5% continua o mesmo, porque é a média simples das taxas dos cinco projetos e equivale a uma amostra balanceada entre eles. O segundo ajuste é a inclusão da cobertura da falha e da caracterização das falhas, para tratar de forma explícita a ameaça de construto que o artigo declara e que a primeira entrega ainda não discutia.

**Plano de análise.** Para H0₁, calculamos p̂ com intervalo de confiança de 95% (Clopper-Pearson) e aplicamos o teste binomial exato contra 26,5%. Como análise complementar, comparamos a taxa de cada bloco com a do projeto na literatura, de forma descritiva, já que cada bloco tem só 7 falhas. Para H0₂, aplicamos Mann-Whitney unilateral à cobertura de instruções agrupada por detecção e reportamos o tamanho de efeito. Na questão secundária, apresentamos tabelas de contingência (detecção × forma de revelação e detecção × cobertura da falha) e a comparação com os números do artigo, lembrando que lá cada falha recebeu 10 execuções e aqui recebe uma. Com 35 testes, a margem de erro de uma proporção perto de 26% é de cerca de ±15 pontos percentuais, e o poder do teste binomial é baixo para desvios moderados: aproximadamente 53% se a taxa verdadeira for 10% e 66% se for 45%. Por isso, vamos ler o resultado como compatibilidade com a literatura, e não como estimativa precisa nem prova de equivalência.

## Proposta de instrumentação

O experimento é automatizado, então o que precisa ser preparado é o ambiente, o sorteio e o registro dos dados. Os scripts nativos do Defects4J (geração, filtragem de testes, detecção e cobertura) serão encadeados em um único pipeline, para que os 7 integrantes executem exatamente os mesmos passos. A única peça nova é um script curto que cruza o patch de cada falha com o relatório de cobertura para classificar a cobertura da falha.

### Procedimento experimental

**Preparação (feita uma vez, em conjunto)**

1. Montar uma imagem de contêiner única com o JDK, o Defects4J, o EvoSuite e os scripts, com versões fixadas e registradas. As versões exatas serão definidas e confirmadas no piloto, já que EvoSuite e Defects4J exigem versões compatíveis de Java. Fixar também CPU e memória do contêiner.
2. Rodar um piloto com 2 falhas fora da amostra, para validar o pipeline, medir o tempo por teste e conferir manualmente o script de cobertura da falha.
3. Executar o sorteio (seção "Seleção de sujeitos") e versionar no repositório a semente, as listas, as 35 falhas, as reservas, a atribuição e a ordem de execução, antes de qualquer teste.
4. Extrair a caracterização das 35 falhas (forma de revelação com `defects4j info` e tamanho da correção a partir do patch) e versionar a tabela.

**Execução (por pesquisador, para cada falha, na ordem sorteada)**

1. Fazer o checkout da versão corrigida da falha (`defects4j checkout`), compilar e obter as classes modificadas.
2. Gerar a suíte com o EvoSuite para cada classe modificada, com 180 s de busca por classe e semente registrada.
3. Compilar a suíte, remover os testes que não compilam e executá-la 5 vezes na versão corrigida, descartando os testes instáveis.
4. Fazer o checkout da versão defeituosa e executar a suíte filtrada; registrar os testes que falham (detecção = 1 ou 0).
5. Medir, na versão corrigida e com a suíte filtrada, a cobertura de instruções das classes modificadas e a cobertura da falha (total, parcial ou nenhuma).
6. Se houve detecção, inspecionar as mensagens de falha e confirmar que elas se relacionam à falha corrigida (e não, por exemplo, a dependência de ambiente ou de ordem); registrar a conclusão.
7. Registrar o teste na planilha e arquivar logs e relatórios no repositório, com um commit por teste.

**Consolidação**

1. Cada detecção e cada resultado "não detectado com testes gerados" é conferido por um segundo integrante, escolhido por rodízio, a partir dos logs arquivados.
2. Executar o script de análise (Python ou R) sobre a planilha consolidada: p̂, intervalo de confiança, teste binomial, Mann-Whitney, comparação por bloco e as tabelas da questão secundária.

### Objetos experimentais

Os objetos são as 35 falhas sorteadas do Defects4J (cada uma com as versões defeituosa e corrigida, as classes modificadas, o patch da correção e os testes do projeto), mais o ambiente de execução descrito abaixo. A imagem de contêiner substitui máquinas virtuais separadas e garante que todos usem as mesmas versões.

| Instrumento | Objetivo | Momento de utilização | Características fundamentais |
|---|---|---|---|
| Defects4J | Fornecer as falhas reais, as versões defeituosa/corrigida, o patch de cada correção e os comandos de checkout, teste e cobertura | Sorteio, caracterização e todos os testes | Cinco projetos Java originais (357 falhas); lista de falhas ativas obtida por `defects4j query`; versão fixada |
| EvoSuite | Gerar as suítes JUnit (tratamento) | Passo de geração de cada teste | Opções padrão; 180 s por classe; filtragem de asserções por mutação desativada; semente registrada; versão fixada |
| Imagem de contêiner | Garantir o mesmo ambiente para os 7 integrantes | Preparação e todos os testes | JDK, Defects4J, EvoSuite e scripts com versões fixas; CPU e memória limitadas e iguais |
| Script de sorteio | Selecionar as falhas, atribuí-las aos pesquisadores e definir a ordem | Preparação (uma vez) | Semente registrada antes do sorteio; saída versionada; reproduzível |
| Pipeline de execução | Executar geração, filtragem, detecção e cobertura sem passos manuais | Cada teste | Um script único; saída padronizada (CSV e logs); mesmo comando para todos |
| Script de cobertura da falha | Classificar a cobertura das linhas alteradas pela correção | Cada teste, após a medição de cobertura | Lê o patch e o relatório por linha; aplica a regra para correções que só removem código; validado no piloto |

### Instrumentos de coleta

| Instrumento | Objetivo | Momento de utilização | Características fundamentais |
|---|---|---|---|
| Planilha de registro por teste (CSV) | Guardar os dados brutos para análise | Ao final de cada teste | Campos: ID da falha, projeto, pesquisador, ordem, semente, nº de testes gerados/descartados, detecção (0/1), cobertura da classe (%), cobertura da falha (total/parcial/nenhuma), tempo, observações. Uma linha por teste. |
| Tabela de caracterização das falhas | Descrever a amostra e compará-la ao conjunto do artigo | Preparação, logo após o sorteio | Uma linha por falha: forma de revelação (asserção/exceção/ambas) e linhas alteradas na correção; versionada antes da execução |
| Logs do EvoSuite e do JUnit | Permitir auditoria e a conferência por outro integrante | Gerados durante cada teste | Arquivados no repositório sem edição manual; incluem as 5 execuções de verificação de instabilidade |
| Relatório de cobertura | Medir as variáveis dependentes de cobertura | Após a execução na versão corrigida | Gerado por `defects4j coverage`; cobertura de instruções das classes modificadas e cobertura por linha, usada para classificar a cobertura da falha |
| Cronometragem | Registrar o tempo por etapa, para o piloto e para detectar sobrecarga da máquina | Início e fim de cada etapa | Registro automático de data/hora pelo pipeline; não é variável de análise |
| Checklist de falso positivo | Confirmar que a detecção se deve à falha, e não ao ambiente ou à ordem | Após cada detecção | Perguntas fixas (a falha ocorre na área corrigida? o teste é determinístico?), respondidas pelo executor e conferidas por um segundo integrante |
| Manifesto de versões | Documentar o ambiente de cada execução | Início de cada teste | Versões de JDK, Defects4J, EvoSuite e do contêiner, e recursos usados; gravado pelo pipeline |

## Análise de ameaças à validade

Mesmo com o planejamento acima, algumas ameaças continuam. Para cada uma, descrevemos o impacto no experimento e o que fazemos para reduzi-la. Na primeira, a mais importante para nós, o honesto é reconhecer que o desenho não a elimina.

| Tipo | Ameaça | Descrição e impacto | Mitigação |
|---|---|---|---|
| Construto | Representatividade das falhas do Defects4J (herdada do artigo) | Shamshiri et al. (2015, seção II.D) apontam que o Defects4J não distingue tipo nem gravidade das falhas, que cada falha é um diff minimizado até a correção, e não a mudança que introduziu o bug, e que só entram falhas que chegaram ao repositório público. Como usamos a mesma base e o mesmo cenário, herdamos a ameaça: p̂ pode subestimar ou superestimar a efetividade em regressões reais. O sorteio com bloqueamento resolve o viés de seleção, não este. | Não é mitigada pelo desenho; é declarada como herdada. Caracterizamos as 35 falhas, comparamos a amostra e a detecção por categoria com a Tabela II do artigo e limitamos a conclusão a falhas do tipo presente no Defects4J. |
| Construto | Detecção binária como medida de efetividade | Um teste pode falhar na versão defeituosa por diferenças que nada têm a ver com a falha (falso positivo), e testes úteis podem ser descartados como instáveis (falso negativo). Os dois casos distorcem p̂ e a comparação com o valor publicado. | Mesma regra de filtragem do artigo; checklist de falso positivo e dupla conferência; relatar os casos descartados. |
| Construto | Cobertura da classe inteira como substituta da cobertura da falha | Em classes grandes, a cobertura da classe pode ser alta sem que as linhas da falha sejam executadas. Isso dilui a medida e pode enfraquecer a associação com a detecção, levando a não rejeitar H0₂ sem motivo. | Medimos também a cobertura da falha (total, parcial ou nenhuma), como no artigo, e comparamos as duas medidas na questão secundária. |
| Conclusão | Baixo poder e baixa precisão | Com 35 testes, a margem de erro é de cerca de ±15 p.p. e o poder é baixo para desvios moderados. Não rejeitar H0₁ não prova que a taxa é igual à publicada. | Reportar o intervalo de confiança; interpretar como compatibilidade; não afirmar equivalência. |
| Conclusão | Grupos pequenos no Mann-Whitney e nas categorias | Se houver poucas detecções (por exemplo, menos de 5), o grupo "detectou" fica pequeno e o teste perde validade e poder. As categorias da questão secundária também terão poucos casos. Há ainda duas hipóteses testadas sem correção para múltiplas comparações. | Verificar o tamanho dos grupos antes do teste; se necessário, reportar só descrição e tamanho de efeito; tratar H0₂ e a questão secundária como complementares. |
| Interna | Diferenças de ambiente e de versões | Hardware diferente altera o resultado da busca com orçamento de tempo fixo, e versões do EvoSuite, do Defects4J ou do JDK diferentes das do artigo de 2015 podem alterar a taxa de detecção. Nesse caso, a diferença observada não seria atribuível à técnica. | Imagem de contêiner única com recursos fixos; manifesto de versões; discutir a diferença de versões ao comparar com a literatura. |
| Interna | Variabilidade da busca e instabilidade de testes | Há uma única execução por falha, e o EvoSuite é estocástico: cada resultado é uma realização aleatória, e a variação entre execuções não é medida. Testes instáveis também podem afetar a detecção. O ruído aumenta a variância, sem tendência conhecida. | Semente registrada; 5 execuções para identificar instabilidade; 35 falhas diferentes em vez de repetir a mesma. |
| Interna | Erro do operador | Sete pessoas executam passos manuais (preparação, checklist), o que pode introduzir desvios entre pesquisadores. | Pipeline único; piloto; conferência cruzada por rodízio. |
| Externa | Objetos restritos ao Defects4J | São cinco projetos Java de código aberto, antigos e muito usados em pesquisa, que não representam outras linguagens nem sistemas industriais. Almasi et al. (2017) obtiveram 56,40% em um sistema financeiro, bem acima da taxa do benchmark. Os resultados não se generalizam. | Delimitar a conclusão ao benchmark; citar a variação entre contextos como limite da generalização. |
| Externa | Uma ferramenta, uma configuração e estudantes como operadores | Só o EvoSuite é avaliado, com orçamento de 3 minutos por classe. Outros orçamentos ou ferramentas podem dar resultados diferentes. Como a execução é automática, a experiência dos operadores pesa pouco, mas a conclusão vale só para essa configuração. | Restringir a conclusão à configuração replicada do artigo. |

## Referências

- ALMASI, M. M. et al. An industrial evaluation of unit test generation: finding real faults in a financial application. In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING: SOFTWARE ENGINEERING IN PRACTICE TRACK, 39., 2017, Buenos Aires. Proceedings […]. IEEE, 2017. p. 263–272.
- FRASER, G.; ARCURI, A. Whole test suite generation. IEEE Transactions on Software Engineering, v. 39, n. 2, p. 276–291, 2013.
- JUST, R.; JALALI, D.; ERNST, M. D. Defects4J: a database of existing faults to enable controlled testing studies for Java programs. In: INTERNATIONAL SYMPOSIUM ON SOFTWARE TESTING AND ANALYSIS, 2014, San Jose. Proceedings […]. ACM, 2014. p. 437–440.
- SHAMSHIRI, S. et al. Do automatically generated unit tests find real faults? An empirical study of effectiveness and challenges. In: INTERNATIONAL CONFERENCE ON AUTOMATED SOFTWARE ENGINEERING, 30., 2015, Lincoln. Proceedings […]. IEEE/ACM, 2015. p. 201–211.
- WOHLIN, C. et al. Experimentation in software engineering. Berlin: Springer, 2012.
