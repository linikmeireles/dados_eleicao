# -*- coding: utf-8 -*-
"""
Eixo 6 — Saneamento básico (Parte B). Fonte: PDAD-DF 2021.

  - Água tratada (%, rede geral CAESB)      Tabela A.75
  - Esgotamento sanitário (%, rede geral)   Tabela A.76
  - Coleta de lixo direta (%)               Tabela A.78
"""
import pdad_xlsx as pdad
from common import RAS_OFICIAIS, salvar


def extrair():
    agua = pdad.ler_coluna("A75", "Rede Geral (CAESB)_Sim")
    esgoto = pdad.ler_coluna("A76", "Rede Geral (CAESB)_Sim")
    lixo = pdad.ler_coluna("A78", "Coleta convencional direta (não\nseletiva)_Sim")

    dataset = {}
    for ra in RAS_OFICIAIS:
        dataset[ra] = {
            "agua_rede_geral_pct": agua.get(ra),
            "esgoto_rede_geral_pct": esgoto.get(ra),
            "lixo_coleta_direta_pct": lixo.get(ra),
        }
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo06_saneamento", d,
           campos_extra_ordem=["agua_rede_geral_pct", "esgoto_rede_geral_pct", "lixo_coleta_direta_pct"])
    for ra in ["Plano Piloto", "São Sebastião", "Fercal"]:
        print(ra, d[ra])
