# Imagem única do experimento (EvoSuite × Defects4J).
# Construída UMA vez por um integrante e distribuída aos demais (docker save/load),
# para que os 7 pesquisadores usem exatamente a mesma imagem (mesmo ID no manifesto).
#
# Versões fixadas:
#   - Ubuntu 20.04 (mesma base do Dockerfile oficial do Defects4J)
#   - OpenJDK 8 (exigido pelo Defects4J 2.x)
#   - Defects4J v2.0.1 (commit a83e47921152721569cb95d6d7b91c4be277d940)
#   - EvoSuite 1.1.0 (baixado pelo init.sh do Defects4J; SHA-256 conferido abaixo)
#
# Plataforma fixada em linux/amd64: em Macs com Apple Silicon a imagem roda emulada,
# o que é mais lento, mas garante o mesmo binário para todos.

FROM --platform=linux/amd64 ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        openjdk-8-jdk \
        git \
        subversion \
        perl \
        cpanminus \
        build-essential \
        make \
        curl \
        wget \
        unzip \
        bc \
        python3 \
        ca-certificates \
        tzdata && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# O Defects4J gera e executa testes no fuso America/Los_Angeles
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Defects4J fixado na tag v2.0.1
ARG D4J_COMMIT=a83e47921152721569cb95d6d7b91c4be277d940
RUN git clone https://github.com/rjust/defects4j.git /defects4j && \
    cd /defects4j && git checkout -q $D4J_COMMIT

WORKDIR /defects4j
RUN cpanm --installdeps . && ./init.sh

# EvoSuite: confere que é o binário esperado
RUN echo "939c0c762d20872b410ecfd79fc2ac77e13e984031dca3f45f78fa44ba627ef7  /defects4j/framework/lib/test_generation/generation/evosuite-1.1.0.jar" | sha256sum -c -

# Configuração do tratamento (substitui a padrão do Defects4J; ver comentários no arquivo)
COPY evosuite.config /defects4j/framework/lib/test_generation/bin/evosuite.config

ENV PATH="/defects4j/framework/bin:/defects4j/framework/util:${PATH}"
ENV D4J_HOME=/defects4j

# O repositório do grupo é montado em /experimento (ver ambiente/rodar.sh)
WORKDIR /experimento
