#!/usr/bin/env bash
# Pipeline de um teste do experimento (uma falha), sempre dentro do contêiner:
#   ambiente/rodar.sh scripts/executar_teste.sh "<Pesquisador>" <Projeto-ID>
#   ambiente/rodar.sh scripts/executar_teste.sh --piloto <Projeto-ID> <semente_evosuite>
#
# Etapas (cada uma cronometrada em tempos.csv, com log próprio em logs/):
#   manifesto -> gerar (EvoSuite na versão corrigida) -> filtrar (remove testes que não
#   compilam e instáveis até a suíte passar 5x seguidas na corrigida) -> detectar (roda a
#   suíte filtrada na defeituosa) -> cobrir (Cobertura na corrigida) -> cobertura da falha
#   -> registro no CSV.
# Nenhuma etapa é repetida ou pulada à mão: se algo falhar, o registro mostra onde.

set -uo pipefail

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ"

if [ "${1:-}" = "--piloto" ]; then
  [ $# -eq 3 ] || { echo "uso: $0 --piloto <Projeto-ID> <semente_evosuite>" >&2; exit 1; }
  PESQ="piloto"; FALHA="$2"; SEMENTE="$3"; ORDEM="0"; CONFERENTE=""
  OUT="$RAIZ/resultados/piloto/$FALHA"
  REGISTRO="$RAIZ/dados/registro-piloto.csv"
else
  [ $# -eq 2 ] || { echo "uso: $0 \"<Pesquisador>\" <Projeto-ID>" >&2; exit 1; }
  PESQ="$1"; FALHA="$2"
  LINHA="$(python3 - "$PESQ" "$FALHA" <<'EOF'
import csv, sys
for r in csv.DictReader(open("dados/sorteio/atribuicao.csv")):
    if r["pesquisador"] == sys.argv[1] and r["falha"] == sys.argv[2]:
        print(r["ordem"], r["semente_evosuite"], r["conferente"], sep="|")
EOF
)"
  [ -n "$LINHA" ] || { echo "ERRO: $FALHA não está atribuída a '$PESQ' em dados/sorteio/atribuicao.csv" >&2; exit 1; }
  IFS="|" read -r ORDEM SEMENTE CONFERENTE <<< "$LINHA"
  OUT="$RAIZ/resultados/$FALHA"
  REGISTRO="$RAIZ/dados/registro.csv"
fi

PROJ="${FALHA%-*}"
BID="${FALHA#*-}"
PATCH="$D4J_HOME/framework/projects/$PROJ/patches/$BID.src.patch"
CLASSES="$D4J_HOME/framework/projects/$PROJ/modified_classes/$BID.src"
[ -f "$PATCH" ] || { echo "ERRO: falha $FALHA não existe no Defects4J" >&2; exit 1; }
[ -e "$OUT" ] && { echo "ERRO: $OUT já existe; cada teste roda uma única vez." >&2; exit 1; }

mkdir -p "$OUT/logs"
TMP="$(mktemp -d /tmp/d4j-XXXXXX)"
TEMPOS="$OUT/tempos.csv"
echo "etapa,inicio,fim,segundos,codigo_saida" > "$TEMPOS"

etapa() {
  local nome="$1"; shift
  local ini fim rc
  ini=$(date +%s)
  echo "[$(date '+%H:%M:%S')] $nome..."
  "$@" > "$OUT/logs/$nome.log" 2>&1
  rc=$?
  fim=$(date +%s)
  echo "$nome,$ini,$fim,$((fim - ini)),$rc" >> "$TEMPOS"
  [ $rc -eq 0 ] || echo "  ATENÇÃO: etapa $nome terminou com código $rc (ver $OUT/logs/$nome.log)"
  return $rc
}

manifesto() {
  echo "data_hora: $(date -Iseconds)"
  echo "pesquisador: $PESQ"
  echo "falha: $FALHA"
  echo "ordem: $ORDEM"
  echo "semente_evosuite: $SEMENTE"
  echo "id_imagem: ${ID_IMAGEM:-desconhecido}"
  echo "cpus_limite: ${CPUS:-desconhecido}"
  echo "memoria_limite: ${MEMORIA:-desconhecido}"
  echo "nproc_visto: $(nproc)"
  echo "memoria_cgroup: $(cat /sys/fs/cgroup/memory.max 2>/dev/null || cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null)"
  echo "kernel: $(uname -srm)"
  echo "tz: $TZ"
  echo "java: $(java -version 2>&1 | head -1)"
  echo "defects4j_commit: $(git -C "$D4J_HOME" rev-parse HEAD)"
  echo "evosuite_sha256: $(sha256sum "$D4J_HOME/framework/lib/test_generation/generation/evosuite-current.jar" | cut -d' ' -f1)"
  echo "evosuite_config_sha256: $(sha256sum "$D4J_HOME/framework/lib/test_generation/bin/evosuite.config" | cut -d' ' -f1)"
  echo "python: $(python3 --version 2>&1)"
  echo "classes_modificadas: $(tr '\n' ' ' < "$CLASSES")"
  echo "orcamento_total_s: $ORCAMENTO"
}

N_CLASSES=$(grep -c . "$CLASSES")
ORCAMENTO=$((360 * N_CLASSES))   # 180 s de busca + 180 s de asserções por classe
SUITE_DIR="$OUT/suites/$PROJ/evosuite/1"
SUITE="$SUITE_DIR/$PROJ-${BID}f-evosuite.1.tar.bz2"

manifesto > "$OUT/manifesto.txt"
cat "$OUT/manifesto.txt"

etapa gerar gen_tests.pl -g evosuite -p "$PROJ" -v "${BID}f" -n 1 -o "$OUT/suites" \
  -b "$ORCAMENTO" -s "$SEMENTE" -t "$TMP"

if [ -f "$SUITE" ]; then
  cp "$SUITE" "$OUT/suite-gerada.tar.bz2"
  etapa filtrar fix_test_suite.pl -p "$PROJ" -d "$SUITE_DIR" -v "${BID}f" -t "$TMP"
  etapa detectar run_bug_detection.pl -p "$PROJ" -d "$SUITE_DIR" -o "$OUT/deteccao" -v "${BID}f" -t "$TMP"
  etapa cobrir run_coverage.pl -p "$PROJ" -d "$SUITE_DIR" -o "$OUT/cobertura" -v "${BID}f" -t "$TMP"
else
  echo "  ATENÇÃO: o EvoSuite não produziu suíte; detecção = 0 e cobertura = 0 (regra de substituição: a falha NÃO é trocada)."
fi

XML="$OUT/cobertura/coverage_log/$PROJ/evosuite/${BID}f.1.xml"
[ -f "$XML" ] || XML="-"
etapa cobertura_falha python3 scripts/cobertura_falha.py "$PATCH" "$XML"
cp "$OUT/logs/cobertura_falha.log" "$OUT/cobertura_falha.txt"

python3 scripts/registrar.py --resultado "$OUT" --registro "$REGISTRO" \
  --pesquisador "$PESQ" --falha "$FALHA" --ordem "$ORDEM" --semente "$SEMENTE" \
  --conferente "$CONFERENTE" --n-classes "$N_CLASSES"

rm -rf "$TMP"
