#!/usr/bin/env bash
# Executa comandos dentro da imagem do experimento, sempre com os mesmos recursos.
#
# Uso (a partir da raiz do repositório):
#   ambiente/rodar.sh construir                 # só quem constrói a imagem (uma vez)
#   ambiente/rodar.sh exportar                  # gera experimento-evosuite-d4j.tar.gz para distribuir
#   ambiente/rodar.sh importar <arquivo.tar.gz> # demais integrantes
#   ambiente/rodar.sh <comando> [args...]       # roda o comando no contêiner
#
# Exemplo:
#   ambiente/rodar.sh scripts/executar_teste.sh "Lucas Reali" Lang-12

set -euo pipefail

IMAGEM="experimento-evosuite-d4j:1"
# Recursos fixos do contêiner (iguais para os 7 integrantes)
CPUS="2"
MEMORIA="6g"

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"

case "${1:-}" in
  construir)
    docker build --platform linux/amd64 -t "$IMAGEM" "$RAIZ/ambiente"
    ;;
  exportar)
    docker save "$IMAGEM" | gzip > "$RAIZ/experimento-evosuite-d4j.tar.gz"
    echo "ID da imagem: $(docker image inspect --format '{{.Id}}' "$IMAGEM")"
    ;;
  importar)
    gunzip -c "$2" | docker load
    echo "ID da imagem: $(docker image inspect --format '{{.Id}}' "$IMAGEM")"
    ;;
  "")
    echo "uso: $0 construir | exportar | importar <arquivo> | <comando> [args...]" >&2
    exit 1
    ;;
  *)
    ID_IMAGEM="$(docker image inspect --format '{{.Id}}' "$IMAGEM")"
    TTY=""; [ -t 0 ] && TTY="-t"
    docker run --rm -i $TTY \
      --platform linux/amd64 \
      --cpus "$CPUS" --memory "$MEMORIA" --memory-swap "$MEMORIA" \
      -e ID_IMAGEM="$ID_IMAGEM" -e CPUS="$CPUS" -e MEMORIA="$MEMORIA" \
      -v "$RAIZ":/experimento \
      "$IMAGEM" "$@"
    ;;
esac
