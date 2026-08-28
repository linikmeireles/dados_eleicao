# -*- coding: utf-8 -*-
"""
Eixo 11 — Meio Ambiente (Parte C).

  - Indicador 3.1 (percepção): % jardins/parques nas cercanias (PDAD A.82),
    % drenagem de água de chuva na rua (PDAD A.79, mesma coluna do eixo 7),
    % ruas alagadas em ocasião de chuva (PDAD A.81)
  - Parques do IBRAM: contagem por RA (ibram_parques.html, tabela oficial
    "Nome / Recategorização / Localização" — 72 unidades no total)
  - Áreas de risco de alagamento/erosão/deslizamento: a fonte (Defesa
    Civil/SSP-DF, via reportagem — não há tabela oficial por RA, só a
    lista de RAs afetadas) não dá o número de pontos por RA individual,
    só o total DF (22) e a lista de RAs monitoradas — reproduzido aqui
    como está nas duas matérias já salvas.
"""
from bs4 import BeautifulSoup
import pdad_xlsx as pdad
from common import RAS_OFICIAIS, normaliza_ra, salvar, fonte

# RAs oficialmente monitoradas por risco de alagamento/erosão/deslizamento
# (Defesa Civil/Sudec-SSP-DF, citada em duas matérias — não há tabela
# oficial com o nº de pontos por RA individual, só o total DF = 22).
AREAS_RISCO_TOTAL_DF = 22
RAS_COM_RISCO = ["Arniqueira", "Fercal", "Núcleo Bandeirante", "Vicente Pires",
                  "Planaltina", "Riacho Fundo", "Sobradinho II", "Sol Nascente/Pôr do Sol"]
RAS_RISCO_MAIOR_ATENCAO = ["Sol Nascente/Pôr do Sol", "Fercal", "Vicente Pires",
                            "Sobradinho II", "Arniqueira"]


def _parques_ibram():
    html = open(fonte("ibram_parques.html"), encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table")
    contagem = {}
    for row in table.find_all("tr")[2:]:
        cells = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
        if len(cells) >= 3 and cells[2]:
            ra = normaliza_ra(cells[2])
            if ra:
                contagem[ra] = contagem.get(ra, 0) + 1
    return contagem


def extrair():
    jardins = pdad.ler_coluna("A82", "Jardins ou parques_Sim")
    drenagem = pdad.ler_coluna("A79", "Drenagem de água da chuva_Sim")
    ruas_alagadas = pdad.ler_coluna("A81", "Ruas Alagadas_Sim")
    parques = _parques_ibram()

    dataset = {}
    for ra in RAS_OFICIAIS:
        dataset[ra] = {
            "jardins_parques_percebido_pct": jardins.get(ra),
            "drenagem_percebido_pct": drenagem.get(ra),
            "ruas_alagadas_percebido_pct": ruas_alagadas.get(ra),
            "parques_ibram_qtd": parques.get(ra, 0),
            "area_de_risco_monitorada": ra in RAS_COM_RISCO,
            "area_de_risco_maior_atencao": ra in RAS_RISCO_MAIOR_ATENCAO,
        }
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo11_meio_ambiente", d,
           campos_extra_ordem=["jardins_parques_percebido_pct", "drenagem_percebido_pct",
                                "ruas_alagadas_percebido_pct", "parques_ibram_qtd",
                                "area_de_risco_monitorada", "area_de_risco_maior_atencao"])
    total_parques = sum(v["parques_ibram_qtd"] for v in d.values())
    print("total parques IBRAM (esperado 72):", total_parques)
    for ra in ["Plano Piloto", "Fercal", "Planaltina"]:
        print(ra, d[ra])
