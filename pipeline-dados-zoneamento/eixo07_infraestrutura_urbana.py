# -*- coding: utf-8 -*-
"""
Eixo 7 — Infraestrutura urbana (Parte B). Fonte: PDAD-DF 2021, Tabela A.79.

  - Pavimentação (%, rua asfaltada/pavimentada)
  - Iluminação pública (%, rua iluminada)
  - Drenagem pluvial (%, rua com drenagem de água da chuva)
"""
import pdad_xlsx as pdad
from common import RAS_OFICIAIS, salvar


def extrair():
    pavimentacao = pdad.ler_coluna("A79", "Rua asfaltada /pavimentada_Sim")
    iluminacao = pdad.ler_coluna("A79", "Rua com iluminação_Sim")
    drenagem = pdad.ler_coluna("A79", "Drenagem de água da chuva_Sim")

    dataset = {}
    for ra in RAS_OFICIAIS:
        dataset[ra] = {
            "pavimentacao_pct": pavimentacao.get(ra),
            "iluminacao_publica_pct": iluminacao.get(ra),
            "drenagem_pct": drenagem.get(ra),
        }
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo07_infraestrutura_urbana", d,
           campos_extra_ordem=["pavimentacao_pct", "iluminacao_publica_pct", "drenagem_pct"])
    for ra in ["Plano Piloto", "São Sebastião", "SCIA/Estrutural"]:
        print(ra, d[ra])
