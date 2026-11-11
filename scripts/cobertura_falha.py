#!/usr/bin/env python3
"""Classifica a cobertura da falha: total, parcial ou nenhuma.

Uso:
    python3 scripts/cobertura_falha.py <patch .src.patch> <coverage.xml | ->

Regras (entrega 2 + decisões da semana 3):
 - O patch do Defects4J vai da versão CORRIGIDA para a DEFEITUOSA. As linhas "-" são,
   portanto, as linhas da versão corrigida que a correção adicionou ou alterou; os
   números delas são os do lado "-" do cabeçalho @@ (numeração da versão corrigida).
 - Um bloco de mudança é uma sequência contínua de linhas "+"/"-". Se o bloco tem
   linhas "-", elas são as linhas-alvo. Se só tem "+" (a correção apenas removeu
   código), a linha-alvo é a linha da versão corrigida logo depois do trecho removido.
 - O Cobertura só registra linhas executáveis. Linhas-alvo que não aparecem no relatório
   (comentário, chave, declaração) são ignoradas; se nenhuma linha-alvo do bloco for
   executável, usa-se a próxima linha executável do mesmo arquivo.
 - total: todas as linhas consideradas foram executadas (hits > 0); parcial: parte
   delas; nenhuma: nenhuma delas. Sem relatório de cobertura ("-"): nenhuma.
 - indeterminado: nenhuma linha executável pôde ser associada ao patch (conferir à mão).

Saída: linhas chave=valor, a primeira sendo cobertura_falha=<classe>.
"""

import re
import sys
import xml.etree.ElementTree as ET


def blocos_do_patch(caminho):
    """Retorna [(arquivo, [linhas-alvo na versão corrigida], so_remocao)]."""
    blocos = []
    arquivo = None
    linha_antiga = 0
    menos, mais = [], 0

    def fechar():
        nonlocal menos, mais
        if menos:
            blocos.append((arquivo, menos, False))
        elif mais:
            blocos.append((arquivo, [linha_antiga], True))
        menos, mais = [], 0

    with open(caminho, errors="replace") as f:
        for linha in f:
            linha = linha.rstrip("\n")
            if linha.startswith("diff "):
                fechar()
                continue
            if linha.startswith("--- "):
                fechar()
                arquivo = re.sub(r"^--- (a/)?", "", linha).split("\t")[0]
                continue
            if linha.startswith("+++ "):
                continue
            m = re.match(r"^@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@", linha)
            if m:
                fechar()
                linha_antiga = int(m.group(1))
                continue
            if linha.startswith("\\"):
                continue
            if linha.startswith("-"):
                menos.append(linha_antiga)
                linha_antiga += 1
            elif linha.startswith("+"):
                mais += 1
            else:
                fechar()
                linha_antiga += 1
        fechar()
    return blocos


def linhas_executaveis(caminho_xml):
    """Retorna {arquivo relativo: {linha: hits}} a partir do coverage.xml do Cobertura."""
    cobertura = {}
    raiz = ET.parse(caminho_xml).getroot()
    for classe in raiz.iter("class"):
        arq = classe.get("filename")
        linhas = cobertura.setdefault(arq, {})
        for l in classe.iter("line"):
            n, hits = int(l.get("number")), int(l.get("hits"))
            linhas[n] = max(hits, linhas.get(n, 0))
    return cobertura


def classificar(blocos, cobertura):
    consideradas = []  # (arquivo, linha, hits)
    avisos = []
    for arquivo, alvos, _ in blocos:
        chave = next((k for k in cobertura if arquivo.endswith(k)), None)
        if chave is None:
            avisos.append("arquivo sem cobertura no relatório: %s" % arquivo)
            continue
        linhas = cobertura[chave]
        exec_alvos = [l for l in alvos if l in linhas]
        if not exec_alvos:
            seguintes = sorted(l for l in linhas if l > max(alvos))
            if not seguintes:
                avisos.append("bloco sem linha executável: %s:%s" % (arquivo, alvos))
                continue
            exec_alvos = [seguintes[0]]
        consideradas += [(arquivo, l, linhas[l]) for l in exec_alvos]

    if not consideradas:
        return "indeterminado", consideradas, avisos
    cobertas = sum(1 for _, _, h in consideradas if h > 0)
    if cobertas == len(consideradas):
        return "total", consideradas, avisos
    if cobertas == 0:
        return "nenhuma", consideradas, avisos
    return "parcial", consideradas, avisos


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    blocos = blocos_do_patch(sys.argv[1])
    if sys.argv[2] == "-":
        print("cobertura_falha=nenhuma")
        print("observacao=sem relatório de cobertura (suíte vazia ou não executada)")
        return
    classe, consideradas, avisos = classificar(blocos, linhas_executaveis(sys.argv[2]))
    print("cobertura_falha=%s" % classe)
    print("linhas_consideradas=%d" % len(consideradas))
    print("linhas_cobertas=%d" % sum(1 for _, _, h in consideradas if h > 0))
    for arquivo, l, h in consideradas:
        print("linha=%s:%d hits=%d" % (arquivo, l, h))
    for a in avisos:
        print("aviso=%s" % a)


if __name__ == "__main__":
    main()
