# -*- coding: utf-8 -*-
"""
Eixo 4 — Emprego e Renda (Parte B do zoneamento).

Indicadores e fonte:
  - Taxa de desocupação (%)              PDAD-DF 2021, Tabela A.51
  - Informalidade (% sem carteira)       PDAD-DF 2021, Tabela A.64
  - Renda domiciliar média (R$, base 2018) IPEA, Boletim Regional nº 25,
                                          Tabela 1 (base PDAD-DF 2018)
  - % domicílios até 2 SM (2021)         PDAD-DF 2021, Tabela A.67
"""
import pdad_xlsx as pdad
import deficit_ipea
from common import RAS_OFICIAIS, salvar


def extrair():
    desocupacao = pdad.ler_coluna("A51", "Desocupada")
    sem_carteira = pdad.ler_coluna("A64", "Não")
    renda_ate1 = pdad.ler_coluna("A67", "Até 1")
    renda_1a2 = pdad.ler_coluna("A67", "Mais de 1 até 2")
    ipea = deficit_ipea.por_ra()

    dataset = {}
    for ra in RAS_OFICIAIS:
        renda_ate2sm = None
        if ra in renda_ate1 and ra in renda_1a2:
            v1, v2 = renda_ate1[ra], renda_1a2[ra]
            if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
                renda_ate2sm = round(v1 + v2, 1)
        dataset[ra] = {
            "desocupacao_pct": desocupacao.get(ra),
            "sem_carteira_pct": sem_carteira.get(ra),
            "renda_domiciliar_media_2018": ipea.get(ra, {}).get("renda_domiciliar_media_2018"),
            "renda_ate2sm_pct": renda_ate2sm,
        }
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo04_emprego_renda", d,
           campos_extra_ordem=["desocupacao_pct", "sem_carteira_pct",
                                "renda_domiciliar_media_2018", "renda_ate2sm_pct"])
    for ra in ["Plano Piloto", "Gama", "Fercal"]:
        print(ra, d[ra])
