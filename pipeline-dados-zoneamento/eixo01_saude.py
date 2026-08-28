# -*- coding: utf-8 -*-
"""
Eixo 1 — Saúde (Parte A).

  - Indicador 1: % de dependência do SUS por RA (2021)
    Fonte: PDAD-DF 2021, Tabela A.19 ("Pessoas com plano de saúde
    privado" — dependência do SUS = "Não" tem plano privado). O PDS
    2024-2027 (SES-DF) reproduz o mesmo número no Gráfico 5, p.42 —
    são a mesma fonte primária (PDAD), duas publicações.

  - Indicador 2: Leitos de internação hospitalar por Região de Saúde (2022)
    Fonte: Plano Distrital de Saúde 2024-2027 (SES-DF), Tabela 48
    (CNES, coluna 2022).
  - Indicador 3: Produção ambulatorial da APS por Região de Saúde
    (total 2018-2022, procedimentos)
    Fonte: PDS 2024-2027, Tabela 43 (SISAB, coluna Total).

Indicadores 2 e 3 são por "Região de Saúde" (7 regiões), não por RA — o
mapeamento RA→Região de Saúde abaixo (Decreto nº 37.515/2016) é o mesmo
usado pelo zoneamento original pra distribuir o valor da região a cada RA
que ela cobre.
"""
import re
import pdad_xlsx as pdad
from common import RAS_OFICIAIS, salvar, fonte

# Mapeamento RA → Região de Saúde (SES-DF, Decreto nº 37.515/2016), usado
# pra agregar os indicadores 2 e 3 quando essa parte for implementada.
REGIAO_DE_SAUDE = {
    "Plano Piloto": "Central", "Lago Norte": "Central", "Varjão": "Central",
    "Cruzeiro": "Central", "Sudoeste/Octogonal": "Central", "Lago Sul": "Central",
    "Núcleo Bandeirante": "Centro-Sul", "Riacho Fundo": "Centro-Sul",
    "Riacho Fundo II": "Centro-Sul", "Park Way": "Centro-Sul",
    "Candangolândia": "Centro-Sul", "Guará": "Centro-Sul", "SIA": "Centro-Sul",
    "SCIA/Estrutural": "Centro-Sul",
    "Taguatinga": "Sudoeste", "Vicente Pires": "Sudoeste", "Águas Claras": "Sudoeste",
    "Arniqueira": "Sudoeste", "Recanto das Emas": "Sudoeste", "Samambaia": "Sudoeste",
    "Gama": "Sul", "Santa Maria": "Sul",
    "Fercal": "Norte", "Planaltina": "Norte", "Sobradinho": "Norte", "Sobradinho II": "Norte",
    "Itapoã": "Leste", "Jardim Botânico": "Leste", "Paranoá": "Leste", "São Sebastião": "Leste",
    "Brazlândia": "Oeste", "Sol Nascente/Pôr do Sol": "Oeste", "Ceilândia": "Oeste",
}


_REGIOES = ["Central", "Centro-Sul", "Leste", "Norte", "Oeste", "Sudoeste", "Sul"]
_NUM = re.compile(r"\d{1,3}(?:\.\d{3})*")


def _tabela_por_regiao(nome_tabela, indice_valor):
    """Lê uma tabela do PDS com uma linha por Região de Saúde e vários anos
    em colunas; devolve {região: valor} pegando a coluna de índice
    `indice_valor` (0 = primeiro número da linha, -1 = último)."""
    texto = open(fonte("pds2024.txt"), encoding="utf-8").read()
    # a 1ª ocorrência do título é sempre o Sumário (índice) do PDS — a
    # tabela com os dados de verdade é a 2ª ocorrência.
    idx = texto.find(nome_tabela)
    if idx < 0:
        raise ValueError(f"não achei {nome_tabela!r} no PDS")
    idx = texto.find(nome_tabela, idx + 1)
    if idx < 0:
        raise ValueError(f"só achei {nome_tabela!r} uma vez (no Sumário) — a tabela de dados não apareceu")
    trecho = texto[idx: idx + 2500]
    out = {}
    for linha in trecho.splitlines():
        s = linha.strip()
        for regiao in _REGIOES:
            if s.startswith(regiao) and regiao not in out:
                nums = _NUM.findall(s[len(regiao):])
                if nums:
                    out[regiao] = int(nums[indice_valor].replace(".", ""))
    return out


def extrair():
    dependencia_sus = pdad.ler_coluna("A19", "Não")
    leitos_2022 = _tabela_por_regiao("Tabela 48. Leitos de internação hospitalar", indice_valor=4)  # coluna 2022
    producao_total = _tabela_por_regiao("Tabela 43. Produção Ambulatorial", indice_valor=-1)  # coluna Total 2018-2022

    dataset = {}
    for ra in RAS_OFICIAIS:
        regiao = REGIAO_DE_SAUDE.get(ra)
        dataset[ra] = {
            "dependencia_sus_pct": dependencia_sus.get(ra),
            "regiao_de_saude": regiao,
            "leitos_internacao_regiao_saude_2022": leitos_2022.get(regiao),
            "producao_ambulatorial_aps_regiao_saude_total_18_22": producao_total.get(regiao),
        }
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo01_saude", d,
           campos_extra_ordem=["dependencia_sus_pct", "regiao_de_saude",
                                "leitos_internacao_regiao_saude_2022",
                                "producao_ambulatorial_aps_regiao_saude_total_18_22"])
    for ra in ["Cruzeiro", "Varjão", "SCIA/Estrutural"]:
        print(ra, d[ra])
