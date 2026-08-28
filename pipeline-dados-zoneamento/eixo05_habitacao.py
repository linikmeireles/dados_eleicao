# -*- coding: utf-8 -*-
"""
Eixo 5 — Habitação (Parte B).

  - Déficit habitacional (%, base 2018)   IPEA, Boletim Regional nº 25, Tabela 1
  - Sem regularização fundiária do lote (%, 2021) PDAD-DF 2021, Tabela A.71
"""
import pdad_xlsx as pdad
import deficit_ipea
from common import RAS_OFICIAIS, salvar


def extrair():
    sem_regularizacao = pdad.ler_coluna("A71", "Não")
    ipea = deficit_ipea.por_ra()

    dataset = {}
    for ra in RAS_OFICIAIS:
        dataset[ra] = {
            "deficit_habitacional_pct": ipea.get(ra, {}).get("deficit_habitacional_pct"),
            "sem_regularizacao_pct": sem_regularizacao.get(ra),
        }
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo05_habitacao", d,
           campos_extra_ordem=["deficit_habitacional_pct", "sem_regularizacao_pct"])
    for ra in ["Plano Piloto", "Gama", "Brazlândia"]:
        print(ra, d[ra])
