#!/usr/bin/env python3
"""Consolida os resultados de um teste numa linha da planilha de registro (CSV).

Chamado pelo executar_teste.sh ao final de cada teste; não é para uso manual.
Lê as saídas do Defects4J em <resultado>/ e acrescenta uma linha em <registro>.
As colunas falso_positivo, deteccao_confirmada, conferencia e observacoes são
preenchidas depois, à mão, pelo executor e pelo conferente (ver docs/).
"""

import argparse
import csv
import os
import re
import tarfile

COLUNAS = [
    "falha", "projeto", "pesquisador", "ordem", "semente_evosuite", "n_classes",
    "testes_gerados", "testes_removidos_nao_compilam", "testes_removidos_falham_ou_instaveis", "testes_finais",
    "resultado_d4j", "testes_reveladores", "deteccao_automatica",
    "linhas_total", "linhas_cobertas", "cobertura_linhas_pct", "ramos_total", "ramos_cobertos",
    "cobertura_falha", "tempo_total_s", "etapas_com_erro", "id_imagem", "data_hora",
    "conferente", "falso_positivo", "deteccao_confirmada", "conferencia", "observacoes",
]


def contar_testes(arquivo):
    if not os.path.isfile(arquivo):
        return 0
    total = 0
    with tarfile.open(arquivo, "r:bz2") as tar:
        for m in tar.getmembers():
            if m.isfile() and m.name.endswith(".java"):
                total += tar.extractfile(m).read().decode("utf-8", "replace").count("@Test")
    return total


def ler_tabela_d4j(pasta, nome):
    """Tabelas do Defects4J (DBD::CSV): arquivo <nome> com cabeçalho."""
    for caminho in (os.path.join(pasta, nome), os.path.join(pasta, nome + ".csv")):
        if os.path.isfile(caminho):
            with open(caminho) as f:
                linhas = list(csv.DictReader(f))
            return linhas[-1] if linhas else None
    return None


def ler_chave_valor(caminho):
    dados = {}
    if os.path.isfile(caminho):
        for linha in open(caminho):
            if "=" in linha:
                k, v = linha.rstrip("\n").split("=", 1)
                dados.setdefault(k, v)
    return dados


def main():
    ap = argparse.ArgumentParser()
    for a in ("resultado", "registro", "pesquisador", "falha", "ordem", "semente", "conferente", "n-classes"):
        ap.add_argument("--" + a, required=True)
    args = ap.parse_args()
    out = args.resultado
    projeto, bid = args.falha.split("-")

    # Geração e filtragem
    gerados = contar_testes(os.path.join(out, "suite-gerada.tar.bz2"))
    suite_final = os.path.join(out, "suites", projeto, "evosuite", "1", "%s-%sf-evosuite.1.tar.bz2" % (projeto, bid))
    finais = contar_testes(suite_final)
    resumo_fix = os.path.join(out, "suites", projeto, "evosuite", "1", "fix_test_suite.summary.log")
    nao_compilam = falham = ""
    if os.path.isfile(resumo_fix):
        texto = open(resumo_fix, errors="replace").read()
        m = re.search(r"Number of uncompilable tests: (\d+)", texto)
        nao_compilam = m.group(1) if m else ""
        m = re.search(r"Number of failing tests: (\d+)", texto)
        falham = m.group(1) if m else ""

    # Detecção (Pass = não detectou; Fail = detectou; Broken = suíte não roda)
    det = ler_tabela_d4j(os.path.join(out, "deteccao"), "bug_detection")
    if det is None:
        resultado, reveladores = ("sem_suite" if gerados == 0 else "sem_resultado"), "0"
    else:
        resultado, reveladores = det.get("test_classification", ""), det.get("num_trigger", "0") or "0"
    deteccao = "1" if resultado == "Fail" else "0"

    # Cobertura da classe (Cobertura: linhas e ramos das classes modificadas, versão corrigida)
    cob = ler_tabela_d4j(os.path.join(out, "cobertura"), "coverage")
    lt = int(cob["lines_total"]) if cob else 0
    lc = int(cob["lines_covered"]) if cob else 0
    bt = cob["branches_total"] if cob else "0"
    bc = cob["branches_covered"] if cob else "0"
    pct = "%.2f" % (100.0 * lc / lt) if lt else "0.00"

    cf = ler_chave_valor(os.path.join(out, "cobertura_falha.txt")).get("cobertura_falha", "")

    # Tempos e erros
    tempo, erros = 0, []
    with open(os.path.join(out, "tempos.csv")) as f:
        for r in csv.DictReader(f):
            tempo += int(r["segundos"])
            if r["codigo_saida"] != "0":
                erros.append(r["etapa"])
    manifesto = {}
    for linha in open(os.path.join(out, "manifesto.txt")):
        k, _, v = linha.partition(": ")
        manifesto[k] = v.strip()

    linha = {
        "falha": args.falha, "projeto": projeto, "pesquisador": args.pesquisador, "ordem": args.ordem,
        "semente_evosuite": args.semente, "n_classes": args.n_classes,
        "testes_gerados": gerados, "testes_removidos_nao_compilam": nao_compilam,
        "testes_removidos_falham_ou_instaveis": falham, "testes_finais": finais,
        "resultado_d4j": resultado, "testes_reveladores": reveladores, "deteccao_automatica": deteccao,
        "linhas_total": lt, "linhas_cobertas": lc, "cobertura_linhas_pct": pct,
        "ramos_total": bt, "ramos_cobertos": bc, "cobertura_falha": cf,
        "tempo_total_s": tempo, "etapas_com_erro": ";".join(erros),
        "id_imagem": manifesto.get("id_imagem", ""), "data_hora": manifesto.get("data_hora", ""),
        "conferente": args.conferente,
        # Só detecções precisam do checklist de falso positivo
        "falso_positivo": "pendente" if deteccao == "1" else "nao_se_aplica",
        "deteccao_confirmada": "pendente" if deteccao == "1" else "0",
        "conferencia": "pendente", "observacoes": "",
    }

    novo = not os.path.isfile(args.registro)
    os.makedirs(os.path.dirname(args.registro) or ".", exist_ok=True)
    with open(args.registro, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        if novo:
            w.writeheader()
        w.writerow(linha)

    print("\nResumo de %s:" % args.falha)
    for k in ("testes_gerados", "testes_finais", "resultado_d4j", "deteccao_automatica",
              "cobertura_linhas_pct", "cobertura_falha", "tempo_total_s", "etapas_com_erro"):
        print("  %-24s %s" % (k, linha[k]))
    if deteccao == "1":
        print("  -> Preencher o checklist de falso positivo (docs/checklist-falso-positivo.md).")


if __name__ == "__main__":
    main()
