#!/usr/bin/env python3
"""Sorteio dos objetos do experimento (seção "Seleção de sujeitos" da entrega 2).

Rodar UMA vez, no contêiner, depois de listar_falhas.sh e antes de qualquer teste:
    ambiente/rodar.sh python3 scripts/sorteio.py --semente 20261030 --piloto Lang-1 Math-5

Procedimento (determinístico dada a semente):
 1. Lê as falhas ativas de dados/falhas-ativas/<Projeto>.txt.
 2. Mantém só os IDs que existiam no conjunto de 357 falhas usado por Shamshiri et al.
    (2015) e retira as 2 falhas do piloto.
 3. Com um único random.Random(semente), percorre os projetos em ordem alfabética e
    sorteia 10 falhas por projeto (sample, sem reposição): 7 entram, 3 são reservas.
 4. Para cada projeto, sorteia uma permutação dos 7 pesquisadores (falha i -> pesquisador i).
 5. Para cada pesquisador, sorteia a ordem de execução dos seus 5 testes.
 6. Para cada teste, sorteia a semente do EvoSuite.
O conferente de cada teste é o pesquisador seguinte na lista abaixo (rodízio cíclico).

Saídas em dados/sorteio/ (o script se recusa a sobrescrever um sorteio já feito).
"""

import argparse
import csv
import os
import platform
import random
import sys
from datetime import datetime

PROJETOS = ["Chart", "Closure", "Lang", "Math", "Time"]

# Maior ID de cada projeto no Defects4J 1.0 (357 falhas), usado por Shamshiri et al. (2015)
MAX_ID_ARTIGO = {"Chart": 26, "Closure": 133, "Lang": 65, "Math": 106, "Time": 27}

# Ordem fixa (a mesma da tabela de desenho da entrega 2)
PESQUISADORES = [
    "Lucas Reali",
    "Guilherme Fadel",
    "Guilherme Celente",
    "Leonardo Ceccon",
    "Gabriel Moribe",
    "Gabriel Conti",
    "Thiago Akimoto",
]

POR_PROJETO = 7
RESERVAS = 3


def ler_ativas(pasta, projeto):
    with open(os.path.join(pasta, projeto + ".txt")) as f:
        return sorted(int(linha) for linha in f if linha.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--semente", type=int, required=True)
    ap.add_argument("--piloto", nargs=2, required=True, metavar="FALHA", help="ex.: Lang-1 Math-5")
    ap.add_argument("--listas", default="dados/falhas-ativas")
    ap.add_argument("--saida", default="dados/sorteio")
    args = ap.parse_args()

    if os.path.exists(os.path.join(args.saida, "atribuicao.csv")):
        sys.exit("Sorteio já realizado em %s; não sobrescrevo." % args.saida)

    piloto = set()
    for f in args.piloto:
        projeto, bid = f.split("-")
        if projeto not in PROJETOS:
            sys.exit("Projeto inválido no piloto: " + f)
        piloto.add((projeto, int(bid)))

    rng = random.Random(args.semente)

    elegiveis = {}
    amostra = []  # (projeto, posicao, falha, papel)
    for projeto in PROJETOS:
        ativas = ler_ativas(args.listas, projeto)
        elegiveis[projeto] = [b for b in ativas if b <= MAX_ID_ARTIGO[projeto] and (projeto, b) not in piloto]
        sorteadas = rng.sample(elegiveis[projeto], POR_PROJETO + RESERVAS)
        for i, b in enumerate(sorteadas, 1):
            papel = "experimento" if i <= POR_PROJETO else "reserva"
            amostra.append((projeto, i, "%s-%d" % (projeto, b), papel))

    falhas_de = {p: [a[2] for a in amostra if a[0] == p and a[3] == "experimento"] for p in PROJETOS}
    testes = {pesq: [] for pesq in PESQUISADORES}
    for projeto in PROJETOS:
        permutacao = rng.sample(PESQUISADORES, len(PESQUISADORES))
        for falha, pesq in zip(falhas_de[projeto], permutacao):
            testes[pesq].append((projeto, falha))

    atribuicao = []
    for k, pesq in enumerate(PESQUISADORES):
        ordem = rng.sample(testes[pesq], len(testes[pesq]))
        conferente = PESQUISADORES[(k + 1) % len(PESQUISADORES)]
        for n, (projeto, falha) in enumerate(ordem, 1):
            semente_evo = rng.randint(1, 2**31 - 1)
            atribuicao.append((pesq, n, falha, projeto, semente_evo, conferente))

    os.makedirs(args.saida, exist_ok=True)
    with open(os.path.join(args.saida, "amostra.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["projeto", "posicao_sorteio", "falha", "papel"])
        w.writerows(amostra)
    with open(os.path.join(args.saida, "atribuicao.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pesquisador", "ordem", "falha", "projeto", "semente_evosuite", "conferente"])
        w.writerows(atribuicao)
    with open(os.path.join(args.saida, "parametros.txt"), "w") as f:
        f.write("data_hora: %s\n" % datetime.now().isoformat(timespec="seconds"))
        f.write("semente: %d\n" % args.semente)
        f.write("piloto (excluídas): %s\n" % " ".join(sorted(args.piloto)))
        f.write("python: %s\n" % platform.python_version())
        f.write("criterio: IDs ativos <= %s\n" % MAX_ID_ARTIGO)
        for p in PROJETOS:
            f.write("elegiveis %s: %d\n" % (p, len(elegiveis[p])))

    print("Sorteio gravado em", args.saida)
    for linha in atribuicao:
        print("%-18s %d  %-12s semente_evo=%d  conferente=%s" % (linha[0], linha[1], linha[2], linha[4], linha[5]))


if __name__ == "__main__":
    main()
