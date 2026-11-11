#!/usr/bin/env python3
"""Caracterização das falhas sorteadas (variáveis observadas, não manipuladas).

Rodar UMA vez, no contêiner, logo depois do sorteio e antes de qualquer teste:
    ambiente/rodar.sh python3 scripts/caracterizar.py

Para cada falha de dados/sorteio/amostra.csv (experimento e reservas):
 - Forma de revelação pelo teste do desenvolvedor: lê os mesmos dados que o
   `defects4j info` mostra em "Root cause in triggering tests"
   (framework/projects/<P>/trigger_tests/<id>). Cada teste revelador é classificado
   como asserção (AssertionFailedError, AssertionError, ComparisonFailure) ou exceção
   (qualquer outro tipo). A falha é "assercao" se todos forem asserção, "excecao" se
   todos forem exceção e "ambas" caso contrário.
 - Tamanho da correção: linhas alteradas no patch (framework/projects/<P>/patches/<id>.src.patch),
   somando linhas adicionadas e removidas, sem contar cabeçalhos.

Saída: dados/caracterizacao.csv
"""

import csv
import os
import re
import sys

D4J = os.environ.get("D4J_HOME", "/defects4j")

TIPOS_ASSERCAO = {
    "junit.framework.AssertionFailedError",
    "junit.framework.ComparisonFailure",
    "java.lang.AssertionError",
    "org.junit.ComparisonFailure",
    "org.junit.internal.ArrayComparisonFailure",
}


def tipos_reveladores(projeto, bid):
    caminho = os.path.join(D4J, "framework/projects", projeto, "trigger_tests", str(bid))
    with open(caminho, errors="replace") as f:
        linhas = f.read().splitlines()
    tipos = []
    for i, linha in enumerate(linhas):
        if linha.startswith("--- ") and i + 1 < len(linhas):
            tipos.append(re.split(r"[:\s]", linhas[i + 1].strip(), maxsplit=1)[0])
    return tipos


def forma_revelacao(tipos):
    assercao = [t in TIPOS_ASSERCAO for t in tipos]
    if all(assercao):
        return "assercao"
    if not any(assercao):
        return "excecao"
    return "ambas"


def tamanho_patch(projeto, bid):
    caminho = os.path.join(D4J, "framework/projects", projeto, "patches", "%d.src.patch" % bid)
    adic = remov = 0
    with open(caminho, errors="replace") as f:
        for linha in f:
            if linha.startswith("+++") or linha.startswith("---"):
                continue
            if linha.startswith("+"):
                adic += 1
            elif linha.startswith("-"):
                remov += 1
    return adic, remov


def classes_modificadas(projeto, bid):
    caminho = os.path.join(D4J, "framework/projects", projeto, "modified_classes", "%d.src" % bid)
    with open(caminho) as f:
        return [l.strip() for l in f if l.strip()]


def main():
    amostra = sys.argv[1] if len(sys.argv) > 1 else "dados/sorteio/amostra.csv"
    saida = sys.argv[2] if len(sys.argv) > 2 else "dados/caracterizacao.csv"
    if os.path.exists(saida):
        sys.exit("%s já existe; não sobrescrevo." % saida)

    linhas = []
    with open(amostra) as f:
        for r in csv.DictReader(f):
            projeto, bid = r["falha"].split("-")
            bid = int(bid)
            tipos = tipos_reveladores(projeto, bid)
            adic, remov = tamanho_patch(projeto, bid)
            classes = classes_modificadas(projeto, bid)
            linhas.append([
                r["falha"], projeto, r["papel"], len(tipos), forma_revelacao(tipos),
                ";".join(sorted(set(tipos))), adic + remov, adic, remov, len(classes), ";".join(classes),
            ])

    with open(saida, "w", newline="") as f:
        w = csv.writer(f)
        # O patch do Defects4J vai da versão corrigida para a defeituosa:
        # "+" = linhas que só existem na defeituosa; "-" = linhas que só existem na corrigida.
        w.writerow([
            "falha", "projeto", "papel", "n_testes_reveladores", "forma_revelacao", "tipos_excecao",
            "linhas_alteradas", "linhas_so_defeituosa", "linhas_so_corrigida",
            "n_classes_modificadas", "classes_modificadas",
        ])
        w.writerows(linhas)
    print("Caracterização gravada em", saida, "(%d falhas)" % len(linhas))


if __name__ == "__main__":
    main()
