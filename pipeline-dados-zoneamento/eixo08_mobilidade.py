# -*- coding: utf-8 -*-
"""
Eixo 8 — Mobilidade/transporte (Parte B). Fonte: PDAD-DF 2021.

  - % que usa ônibus como principal meio de transporte   Tabela A.62
  - Tempo médio de deslocamento até o trabalho (minutos) Tabela A.63

A PDAD só publica a distribuição percentual do tempo de deslocamento em
faixas, não uma média direta em minutos por RA. Pra ter um indicador único
e comparável, calculamos uma média ponderada pelo ponto médio de cada
faixa (mesmo método descrito no zoneamento original): faixas suprimidas
pela fonte ("(***)") e a opção "Não sabe" são excluídas do cálculo.
"""
import pdad_xlsx as pdad
from common import RAS_OFICIAIS, salvar

# ponto médio (minutos) de cada faixa de tempo da Tabela A.63
PONTOS_MEDIOS = {
    "Até 15 minutos": 7.5,
    "Mais de 15 até 30 minutos": 22.5,
    "Mais de 30 até 45 minutos": 37.5,
    "Mais de 45 minutos até 1 hora": 52.5,
    "Mais de 1 hora até 1 hora e 15 minutos": 67.5,
    "Mais de 1 hora e 15 minutos até 1 hora e meia": 82.5,
    "Mais de 1 hora e meia até 1 hora e 45 minutos": 97.5,
    "Mais de 1 hora e 45 minutos até 2 horas": 112.5,
    "Mais de 2 horas": 140.0,  # ponto médio assumido, faixa aberta
}


def _media_ponderada(valores_por_faixa):
    soma_pct = 0.0
    soma_pct_x_min = 0.0
    for faixa, minutos in PONTOS_MEDIOS.items():
        v = valores_por_faixa.get(faixa)
        if isinstance(v, (int, float)):
            soma_pct += v
            soma_pct_x_min += v * minutos
    if soma_pct == 0:
        return None, 0.0
    return round(soma_pct_x_min / soma_pct, 1), round(soma_pct, 1)


def extrair():
    onibus = pdad.ler_coluna("A62", "Ônibus")
    _, linhas_a63 = pdad.ler_tabela("A63")
    colunas_a63, _ = pdad._monta_colunas(pdad._wb("Relatorio_DF_percentual-2021.xlsx")["A63"],
                                          pdad._acha_linha_local(pdad._wb("Relatorio_DF_percentual-2021.xlsx")["A63"]))

    from common import normaliza_ra
    dataset = {}
    for nome_bruto, vals in linhas_a63.items():
        if nome_bruto.upper() == "DF":
            continue
        ra = normaliza_ra(nome_bruto)
        if ra is None:
            continue
        por_faixa = dict(zip(colunas_a63, vals))
        tempo_medio, cobertura_pct = _media_ponderada(por_faixa)
        dataset[ra] = {
            "onibus_pct": onibus.get(ra),
            "tempo_medio_min": tempo_medio,
            "tempo_cobertura_pct": cobertura_pct,
        }
    for ra in RAS_OFICIAIS:
        dataset.setdefault(ra, {"onibus_pct": None, "tempo_medio_min": None, "tempo_cobertura_pct": None})
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo08_mobilidade", d,
           campos_extra_ordem=["onibus_pct", "tempo_medio_min", "tempo_cobertura_pct"])
    for ra in ["Plano Piloto", "Gama", "Fercal"]:
        print(ra, d[ra])
