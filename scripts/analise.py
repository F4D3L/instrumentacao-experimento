#!/usr/bin/env python3
"""Análise do experimento (plano de análise da entrega 2). Só biblioteca padrão.

Uso:
    python3 scripts/analise.py [--registro dados/registro.csv] [--caracterizacao dados/caracterizacao.csv]
                               [--permitir-pendentes]

 - H0₁: p̂ com IC 95% de Clopper-Pearson e teste binomial exato bicaudal contra 26,5%
   (e contra 23,0%, referência secundária). Mesmo método do binom.test do R.
 - Comparação descritiva por bloco (projeto) com a taxa publicada.
 - H0₂: Mann-Whitney unilateral (cobertura maior nas suítes que detectam), p-valor exato
   condicional aos postos (trata empates), mais tamanho de efeito A12 de Vargha-Delaney
   e correlação rank-biserial.
 - Questão secundária: tabelas detecção × forma de revelação e detecção × cobertura da falha,
   e casos de cobertura da classe alta com cobertura da falha nenhuma.

A detecção usada é a coluna deteccao_confirmada (após o checklist de falso positivo).
"""

import argparse
import csv
import sys
from collections import Counter, defaultdict
from math import comb

ALFA = 0.05
P0 = 0.265
P0_SECUNDARIA = 0.230
REFERENCIA = {"Chart": 0.373, "Closure": 0.089, "Lang": 0.142, "Math": 0.405, "Time": 0.315}
PROJETOS = ["Chart", "Closure", "Lang", "Math", "Time"]


# ---------- Binomial ----------

def pmf(k, n, p):
    return comb(n, k) * p**k * (1 - p) ** (n - k)


def binomial_bicaudal(k, n, p):
    """p-valor exato bicaudal: soma das probabilidades <= P(X = k)."""
    pk = pmf(k, n, p)
    return min(1.0, sum(pmf(i, n, p) for i in range(n + 1) if pmf(i, n, p) <= pk * (1 + 1e-7)))


def _bissecao(f, alvo, crescente):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        meio = (lo + hi) / 2
        if (f(meio) < alvo) == crescente:
            lo = meio
        else:
            hi = meio
    return (lo + hi) / 2


def clopper_pearson(k, n, alfa=ALFA):
    inf = 0.0 if k == 0 else _bissecao(lambda p: sum(pmf(i, n, p) for i in range(k, n + 1)), alfa / 2, True)
    sup = 1.0 if k == n else _bissecao(lambda p: sum(pmf(i, n, p) for i in range(0, k + 1)), alfa / 2, False)
    return inf, sup


# ---------- Mann-Whitney ----------

def postos(valores):
    ordem = sorted(range(len(valores)), key=lambda i: valores[i])
    r = [0.0] * len(valores)
    i = 0
    while i < len(ordem):
        j = i
        while j + 1 < len(ordem) and valores[ordem[j + 1]] == valores[ordem[i]]:
            j += 1
        for t in range(i, j + 1):
            r[ordem[t]] = (i + j) / 2 + 1
        i = j + 1
    return r


def mann_whitney_maior(x, y):
    """H1: x tende a ser maior que y. Retorna U_x, p exato (condicional aos postos), A12, r."""
    n1, n2 = len(x), len(y)
    r = postos(list(x) + list(y))
    r2 = [int(round(2 * v)) for v in r]  # postos dobrados (inteiros, mesmo com empates)
    soma_obs = sum(r2[:n1])
    # dp[j][s] = nº de subconjuntos de tamanho j com soma de postos dobrados s
    dp = [defaultdict(int) for _ in range(n1 + 1)]
    dp[0][0] = 1
    for v in r2:
        for j in range(n1, 0, -1):
            for s, c in list(dp[j - 1].items()):
                dp[j][s + v] += c
    total = comb(n1 + n2, n1)
    p = sum(c for s, c in dp[n1].items() if s >= soma_obs) / total
    u = sum(r[:n1]) - n1 * (n1 + 1) / 2
    a12 = u / (n1 * n2)
    return u, p, a12, 2 * a12 - 1


def mediana(v):
    v = sorted(v)
    if not v:
        return float("nan")
    m = len(v) // 2
    return v[m] if len(v) % 2 else (v[m - 1] + v[m]) / 2


def pct(x):
    return ("%.1f%%" % (100 * x)).replace(".", ",")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registro", default="dados/registro.csv")
    ap.add_argument("--caracterizacao", default="dados/caracterizacao.csv")
    ap.add_argument("--permitir-pendentes", action="store_true",
                    help="usa deteccao_automatica onde a confirmação ainda está pendente (só para ensaio)")
    args = ap.parse_args()

    testes = list(csv.DictReader(open(args.registro)))
    pendentes = [t["falha"] for t in testes if t["deteccao_confirmada"] not in ("0", "1")]
    if pendentes and not args.permitir_pendentes:
        sys.exit("Detecções sem confirmação: %s. Preencha o checklist ou use --permitir-pendentes." % ", ".join(pendentes))
    for t in testes:
        t["det"] = int(t["deteccao_confirmada"]) if t["deteccao_confirmada"] in ("0", "1") else int(t["deteccao_automatica"])
        t["cob"] = float(t["cobertura_linhas_pct"])
    carac = {}
    try:
        carac = {r["falha"]: r for r in csv.DictReader(open(args.caracterizacao))}
    except FileNotFoundError:
        pass

    n = len(testes)
    k = sum(t["det"] for t in testes)
    if n != 35:
        print("AVISO: o registro tem %d testes (o desenho prevê 35)." % n)
    if pendentes:
        print("AVISO: ensaio com %d detecções ainda não confirmadas." % len(pendentes))

    print("\n== H0₁: taxa de detecção ==")
    inf, sup = clopper_pearson(k, n)
    print("Detectadas: %d de %d  ->  p̂ = %s  (IC 95%% Clopper-Pearson: %s a %s)" % (k, n, pct(k / n), pct(inf), pct(sup)))
    for p0, nome in ((P0, "principal"), (P0_SECUNDARIA, "secundária")):
        pv = binomial_bicaudal(k, n, p0)
        decisao = "rejeita H0" if pv < ALFA else "não rejeita H0"
        print("Binomial exato bicaudal vs %s (%s): p = %.4f  ->  %s" % (pct(p0), nome, pv, decisao))

    print("\n== Por bloco (descritivo; 7 falhas por bloco) ==")
    print("%-8s %10s %10s %12s" % ("Projeto", "Detect.", "Taxa", "Referência"))
    for proj in PROJETOS:
        bloco = [t for t in testes if t["projeto"] == proj]
        kb = sum(t["det"] for t in bloco)
        taxa = pct(kb / len(bloco)) if bloco else "-"
        print("%-8s %6d/%-3d %10s %12s" % (proj, kb, len(bloco), taxa, pct(REFERENCIA[proj])))

    print("\n== H0₂: cobertura de linhas × detecção ==")
    det = [t["cob"] for t in testes if t["det"] == 1]
    nao = [t["cob"] for t in testes if t["det"] == 0]
    print("Detectaram: n = %d, mediana = %.1f%%  |  Não detectaram: n = %d, mediana = %.1f%%"
          % (len(det), mediana(det), len(nao), mediana(nao)))
    if not det or not nao:
        print("Um dos grupos está vazio; o teste não se aplica.")
    else:
        u, pv, a12, rb = mann_whitney_maior(det, nao)
        decisao = "rejeita H0" if pv < ALFA else "não rejeita H0"
        print("Mann-Whitney unilateral (maior nas que detectam): U = %.1f, p exato = %.4f  ->  %s" % (u, pv, decisao))
        print("Tamanho de efeito: A12 = %.3f, rank-biserial r = %.3f" % (a12, rb))
        if min(len(det), len(nao)) < 5:
            print("AVISO: grupo com menos de 5 casos; reportar como descritivo (ver ameaças à validade).")

    print("\n== Questão secundária ==")
    if carac:
        tab = Counter((carac[t["falha"]]["forma_revelacao"], t["det"]) for t in testes if t["falha"] in carac)
        print("Detecção × forma de revelação:")
        for forma in ("assercao", "excecao", "ambas"):
            d, nd = tab[(forma, 1)], tab[(forma, 0)]
            print("  %-9s detectou %2d | não detectou %2d | taxa %s" % (forma, d, nd, pct(d / (d + nd)) if d + nd else "-"))
        tam_det = [int(carac[t["falha"]]["linhas_alteradas"]) for t in testes if t["falha"] in carac and t["det"]]
        tam_nao = [int(carac[t["falha"]]["linhas_alteradas"]) for t in testes if t["falha"] in carac and not t["det"]]
        print("Tamanho da correção (mediana de linhas): detectadas %.1f | não detectadas %.1f"
              % (mediana(tam_det), mediana(tam_nao)))
    else:
        print("(sem dados/caracterizacao.csv)")
    tab = Counter((t["cobertura_falha"], t["det"]) for t in testes)
    print("Detecção × cobertura da falha:")
    for nivel in ("total", "parcial", "nenhuma", "indeterminado"):
        d, nd = tab[(nivel, 1)], tab[(nivel, 0)]
        if d + nd:
            print("  %-13s detectou %2d | não detectou %2d" % (nivel, d, nd))
    med = mediana([t["cob"] for t in testes])
    enganosos = [t for t in testes if t["cobertura_falha"] == "nenhuma" and t["cob"] >= med]
    print("Cobertura da classe >= mediana (%.1f%%) mas cobertura da falha nenhuma: %d caso(s) %s"
          % (med, len(enganosos), ", ".join(t["falha"] for t in enganosos)))


if __name__ == "__main__":
    main()
