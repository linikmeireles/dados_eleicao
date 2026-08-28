# -*- coding: utf-8 -*-
"""
Eixo 3 — Assistência Social (Parte A).

  - Indicador 4: IVS-DF (Índice de Vulnerabilidade Social) por RA, 2018 e 2021
    Fonte: Plano Distrital de Assistência Social 2024-2027 (SEDES-DF),
    Quadro 7 (pas2024.txt).

  - Indicador 1 e 2 (CRAS e CREAS por RA) e Indicador 3 (CadÚnico/Bolsa
    Família/IVCAD por área de abrangência de CRAS): LACUNA NESTE SCRIPT.
    O pas2024.txt tem os TOTAIS de CRAS/CREAS do DF (Quadros 27/28,
    déficit conforme o Pacto SUAS) mas não achei ainda, dentro deste PDF,
    a lista unidade-a-unidade de qual RA tem qual CRAS/CREAS (a que
    aparece no zoneamento original, ex. "Itapoã: 2 CRAS, 0 CREAS") — essa
    lista provavelmente está num anexo/mapa que não extraiu como texto
    corrido. Precisaria localizar manualmente ou reconstruir a partir da
    página oficial de CRAS (sedes_cras.html, já baixada).
"""
from common import RAS_OFICIAIS, normaliza_ra, salvar, fonte


def _ivs_df():
    texto = open(fonte("pas2024.txt"), encoding="utf-8").read()
    idx = texto.find("Quadro 7: Índice de Vulnerabilidade Social")
    if idx < 0:
        raise ValueError("não achei o Quadro 7 (IVS-DF) no PAS")
    trecho = texto[idx: idx + 3000]
    linhas = [l.strip() for l in trecho.splitlines() if l.strip()]
    # formato: Território / 2018 / 2021 (cabeçalho), depois grupos de
    # 4 linhas por território: Nome, valor2018, valor2021, seta (↑/↓/=)
    out = {}
    i = linhas.index("Território") if "Território" in linhas else 1
    i += 3  # pula "Território", "2018", "2021"
    while i + 3 <= len(linhas):
        nome, v2018, v2021, seta = linhas[i:i + 4]
        if not re.match(r"^0,\d+$|^\d,\d+$", v2018) or seta not in ("↑", "↓", "="):
            break
        out[nome] = (float(v2018.replace(",", ".")), float(v2021.replace(",", ".")))
        i += 4
    return out


import re  # (usado em _ivs_df acima)


def extrair():
    ivs = _ivs_df()
    dataset = {}
    for ra in RAS_OFICIAIS:
        v = ivs.get(ra) or ivs.get(ra.replace("SCIA/Estrutural", "SCIA/Estrutural"))
        dataset[ra] = {
            "ivs_df_2018": v[0] if v else None,
            "ivs_df_2021": v[1] if v else None,
            "cras_qtd": None,  # LACUNA — ver docstring
            "creas_qtd": None,  # LACUNA — ver docstring
        }
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo03_assistencia_social", d,
           campos_extra_ordem=["ivs_df_2018", "ivs_df_2021", "cras_qtd", "creas_qtd"])
    for ra in ["Fercal", "SCIA/Estrutural", "Lago Sul"]:
        print(ra, d[ra])
