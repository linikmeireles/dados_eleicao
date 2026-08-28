# -*- coding: utf-8 -*-
"""
Utilidades comuns ao pipeline de dados do zoneamento-11-eixos.

Cada módulo eixoNN_*.py deste pacote:
  1) lê as fontes brutas já baixadas em ../fontes-pesquisa-2026-08-27/
  2) devolve os indicadores daquele eixo, por Região Administrativa (RA),
     numa lista de dicts (uma linha por RA) pronta pra virar CSV/JSON.

Este arquivo só cuida de coisas usadas por vários eixos: a lista oficial
das 33 RAs, normalização de nome de RA (cada fonte escreve diferente:
"Ceilândia" vs "Ceilandia", "SCIA/Estrutural" vs "Estrutural" etc.), e
helpers pra abrir PDF/XLSX/HTML.
"""
import os
import re
import unicodedata

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTES_DIR = os.path.join(os.path.dirname(BASE_DIR), "fontes-pesquisa-2026-08-27")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# As 33 Regiões Administrativas oficiais usadas no projeto (mesma lista do
# zoneamento e do mapa de calor eleitoral), na grafia canônica que os
# scripts deste pacote devem usar na saída.
RAS_OFICIAIS = [
    "Plano Piloto", "Gama", "Taguatinga", "Brazlândia", "Sobradinho",
    "Planaltina", "Paranoá", "Núcleo Bandeirante", "Ceilândia", "Guará",
    "Cruzeiro", "Samambaia", "Santa Maria", "São Sebastião",
    "Recanto das Emas", "Lago Sul", "Riacho Fundo", "Lago Norte",
    "Candangolândia", "Águas Claras", "Riacho Fundo II",
    "Sudoeste/Octogonal", "Varjão", "Park Way", "SCIA/Estrutural",
    "Sobradinho II", "Jardim Botânico", "Itapoã", "SIA", "Vicente Pires",
    "Fercal", "Sol Nascente/Pôr do Sol", "Arniqueira",
]

# RAs criadas em 2022/2026 que várias fontes ainda não segmentam à parte
# (ficam agregadas em Recanto das Emas e Planaltina, respectivamente) —
# ver Anuário 2026, "Dados das novas Regiões Administrativas".
RAS_NOVAS_NAO_SEGMENTADAS = {"Água Quente": "Recanto das Emas", "Arapoanga": "Planaltina"}


def _strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def _norm_key(s):
    s = _strip_accents(s).upper()
    s = re.sub(r"[^A-Z0-9]+", "", s)
    return s


# mapeia toda variação de grafia já vista nas fontes para o nome canônico
_ALIASES = {
    "PLANOPILOTO": "Plano Piloto", "BRASILIA": "Plano Piloto",
    "BRASILIAPLANOPILOTO": "Plano Piloto",
    "GAMA": "Gama",
    "TAGUATINGA": "Taguatinga",
    "BRAZLANDIA": "Brazlândia",
    "SOBRADINHO": "Sobradinho", "SOBRADINHOI": "Sobradinho",
    "PLANALTINA": "Planaltina",
    "PARANOA": "Paranoá",
    "NUCLEOBANDEIRANTE": "Núcleo Bandeirante",
    "CEILANDIA": "Ceilândia", "CEILANDIA9": "Ceilândia",
    "GUARA": "Guará",
    "CRUZEIRO": "Cruzeiro",
    "SAMAMBAIA": "Samambaia",
    "SANTAMARIA": "Santa Maria",
    "SAOSEBASTIAO": "São Sebastião",
    "RECANTODASEMAS": "Recanto das Emas",
    "LAGOSUL": "Lago Sul",
    "RIACHOFUNDO": "Riacho Fundo", "RIACHOFUNDOI": "Riacho Fundo",
    "LAGONORTE": "Lago Norte",
    "CANDANGOLANDIA": "Candangolândia",
    "AGUASCLARAS": "Águas Claras",
    "RIACHOFUNDOII": "Riacho Fundo II",
    "SUDOESTEOCTOGONAL": "Sudoeste/Octogonal", "SUDOESTE": "Sudoeste/Octogonal",
    "SUDOESTEEOCTOGONAL": "Sudoeste/Octogonal",
    "VARJAO": "Varjão",
    "PARKWAY": "Park Way",
    "SCIAESTRUTURAL": "SCIA/Estrutural", "ESTRUTURAL": "SCIA/Estrutural",
    "SCIA": "SCIA/Estrutural",
    "ESTRUTURALSETORCOMPLEMENTARDEINDUSTRIAEABASTECIMENTOSCIA": "SCIA/Estrutural",
    "SOBRADINHOII": "Sobradinho II",
    "JARDIMBOTANICO": "Jardim Botânico",
    "ITAPOA": "Itapoã",
    "SIA": "SIA",
    "VICENTEPIRES": "Vicente Pires",
    "FERCAL": "Fercal",
    "SOLNASCENTEPORDOSOL": "Sol Nascente/Pôr do Sol", "SOLNASCENTE": "Sol Nascente/Pôr do Sol",
    "PORDOSOL": "Sol Nascente/Pôr do Sol", "SOLNASCENTEEPORDOSOL": "Sol Nascente/Pôr do Sol",
    "ARNIQUEIRA": "Arniqueira",
    # variações extras vistas em páginas de site (não em tabela da PDAD)
    "VILAPLANALTO": "Plano Piloto", "BRASILIA9": "Plano Piloto",
    "SUDOESTEXVIII": "Sudoeste/Octogonal",
}


def normaliza_ra(nome_bruto):
    """Recebe o nome de RA como aparece numa fonte qualquer e devolve o
    nome canônico usado em RAS_OFICIAIS, ou None se não reconhecer
    (ex.: linha de total do DF, região nova ainda não segmentada)."""
    key = _norm_key(nome_bruto)
    return _ALIASES.get(key)


def novo_dataset():
    """dict RA canônica -> {} vazio, pronto pra cada extrator preencher."""
    return {ra: {} for ra in RAS_OFICIAIS}


def salvar(eixo_slug, dataset, campos_extra_ordem=None):
    """Salva o dataset (dict RA->indicadores) em CSV e JSON dentro de output/."""
    import csv
    import json as _json

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_path = os.path.join(OUTPUT_DIR, f"{eixo_slug}.json")
    csv_path = os.path.join(OUTPUT_DIR, f"{eixo_slug}.csv")

    _json.dump(dataset, open(json_path, "w", encoding="utf-8"),
               ensure_ascii=False, indent=1)

    campos = list(campos_extra_ordem) if campos_extra_ordem else sorted(
        {k for v in dataset.values() for k in v.keys()})
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["RA"] + campos)
        for ra in RAS_OFICIAIS:
            row = dataset.get(ra, {})
            w.writerow([ra] + [row.get(c, "") for c in campos])
    print(f"[{eixo_slug}] salvo: {json_path} e {csv_path}")
    return json_path, csv_path


def fonte(*rel_path):
    return os.path.join(FONTES_DIR, *rel_path)
