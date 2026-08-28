# -*- coding: utf-8 -*-
"""
Leitor da Tabela 1 do boletim do IPEA (deficit_ipea.txt — Boletim Regional,
Urbano e Ambiental nº 25, jan-jun/2021, base PDAD-DF 2018), que traz déficit
habitacional e renda domiciliar média por "estrato" de RA.

Plano Piloto e Jardim Botânico são publicados pela fonte já subdivididos em
estratos menores (Asa Norte/Asa Sul/Noroeste/Demais áreas e Jardim Botânico-
Tradicional/Jardim Mangueiral). Este módulo agrega esses estratos de volta
pra RA, ponderando pelo número de domicílios de cada um (estimado como
deficit_est / pct_deficit_est, já que a fonte não publica o total de
domicílios diretamente) — é a mesma lógica descrita no zoneamento original
("agregação ponderada pelo número estimado de domicílios de cada substrato").
"""
import re
from common import fonte

# ordem das colunas numéricas em cada linha da Tabela 1 (12 números):
#   déficit habitacional: estimativa, limite inferior, limite superior, CV
#   renda domiciliar:      estimativa, limite inferior, limite superior, CV
#   % domicílios em déficit no estrato: estimativa, limite inferior, limite superior, CV
COLS = [
    "deficit_est", "deficit_liminf", "deficit_limsup", "deficit_cv",
    "renda_est", "renda_liminf", "renda_limsup", "renda_cv",
    "pct_deficit_est", "pct_deficit_liminf", "pct_deficit_limsup", "pct_deficit_cv",
]

# rótulo exato como aparece no PDF -> (RA canônica, é sub-estrato?)
LINHAS = [
    ("Asa Norte", "Plano Piloto"), ("Asa Sul", "Plano Piloto"),
    ("Noroeste", "Plano Piloto"), ("Demais áreas", "Plano Piloto"),
    ("Gama", "Gama"), ("Taguatinga", "Taguatinga"), ("Brazlândia", "Brazlândia"),
    ("Sobradinho", "Sobradinho"), ("Planaltina", "Planaltina"), ("Paranoá", "Paranoá"),
    ("Núcleo Bandeirante", "Núcleo Bandeirante"), ("Ceilândia", "Ceilândia"),
    ("Guará", "Guará"), ("Cruzeiro", "Cruzeiro"), ("Samambaia", "Samambaia"),
    ("Santa Maria", "Santa Maria"), ("São Sebastião", "São Sebastião"),
    ("Recanto das Emas", "Recanto das Emas"), ("Lago Sul", "Lago Sul"),
    ("Riacho Fundo", "Riacho Fundo"), ("Lago Norte", "Lago Norte"),
    ("Candangolândia", "Candangolândia"), ("Águas Claras", "Águas Claras"),
    ("Riacho Fundo II", "Riacho Fundo II"), ("Sudoeste/Octogonal", "Sudoeste/Octogonal"),
    ("Varjão", "Varjão"), ("Park Way", "Park Way"),
    ("SCIA-Estrutural", "SCIA/Estrutural"), ("Sobradinho II", "Sobradinho II"),
    ("Jardim Botânico - Tradicional", "Jardim Botânico"),
    ("Jardim Mangueiral", "Jardim Botânico"),
    ("Itapoã", "Itapoã"), ("SIA", "SIA"), ("Vicente Pires", "Vicente Pires"),
    ("Fercal", "Fercal"), ("Sol Nascente/Pôr do Sol", "Sol Nascente/Pôr do Sol"),
    ("Arniqueira", "Arniqueira"),
]

_NUM = re.compile(r"-?\d{1,3}(?:\.\d{3})*,\d+")


def _to_float(s):
    return float(s.replace(".", "").replace(",", "."))


def _carrega_texto():
    return open(fonte("deficit_ipea.txt"), encoding="utf-8").read().splitlines()


def ler_estratos():
    """Devolve {rótulo_da_fonte: {coluna: valor_float}} — um dict por linha
    (estrato), antes de agregar Plano Piloto/Jardim Botânico."""
    linhas_txt = _carrega_texto()
    out = {}
    rotulos = [r for r, _ in LINHAS]
    for line in linhas_txt:
        stripped = line.strip()
        for rotulo in rotulos:
            if stripped.startswith(rotulo) and rotulo not in out:
                resto = stripped[len(rotulo):]
                nums = _NUM.findall(resto)
                if len(nums) >= 12:
                    out[rotulo] = dict(zip(COLS, (_to_float(n) for n in nums[:12])))
                break
    faltando = [r for r in rotulos if r not in out]
    if faltando:
        raise ValueError(f"não achei linha de dados pra: {faltando}")
    return out


def por_ra():
    """Devolve {RA canônica: {coluna: valor}}, já com Plano Piloto e Jardim
    Botânico agregados (ponderado pelos domicílios implícitos de cada
    substrato: deficit_est / pct_deficit_est)."""
    estratos = ler_estratos()
    ra_de = dict(LINHAS)

    # domicílios implícitos por estrato (denominador da ponderação)
    for rotulo, vals in estratos.items():
        vals["_domicilios"] = vals["deficit_est"] / (vals["pct_deficit_est"] or float("nan"))

    agregados = {}
    grupos = {}
    for rotulo, ra in ra_de.items():
        grupos.setdefault(ra, []).append(estratos[rotulo])

    for ra, lista in grupos.items():
        if len(lista) == 1:
            v = lista[0]
            agregados[ra] = {
                "deficit_habitacional_pct": round(v["pct_deficit_est"] * 100, 1),
                "renda_domiciliar_media_2018": round(v["renda_est"], 2),
            }
        else:
            peso_total = sum(v["_domicilios"] for v in lista)
            pct = sum(v["pct_deficit_est"] * v["_domicilios"] for v in lista) / peso_total
            renda = sum(v["renda_est"] * v["_domicilios"] for v in lista) / peso_total
            agregados[ra] = {
                "deficit_habitacional_pct": round(pct * 100, 1),
                "renda_domiciliar_media_2018": round(renda, 2),
            }
    return agregados


if __name__ == "__main__":
    d = por_ra()
    for ra in ["Plano Piloto", "Jardim Botânico", "Guará", "Fercal"]:
        print(ra, d[ra])
