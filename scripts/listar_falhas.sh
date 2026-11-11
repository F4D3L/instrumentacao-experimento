#!/usr/bin/env bash
# Lista as falhas ativas (não depreciadas) de cada projeto, com o próprio Defects4J,
# e grava uma lista por projeto em dados/falhas-ativas/. Rodar UMA vez, no contêiner:
#   ambiente/rodar.sh scripts/listar_falhas.sh

set -euo pipefail

SAIDA=dados/falhas-ativas
mkdir -p "$SAIDA"

for p in Chart Closure Lang Math Time; do
  defects4j bids -p "$p" > "$SAIDA/$p.txt"
  echo "$p: $(wc -l < "$SAIDA/$p.txt") falhas ativas"
done
