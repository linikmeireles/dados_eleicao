# -*- coding: utf-8 -*-
"""
Eixo 9 — Educação (Parte C).

Diferente dos outros eixos, a rede pública de ensino é organizada pela
SEEDF em 14 Coordenações Regionais de Ensino (CRE) — a unidade real de
gestão —, não diretamente por RA. Este módulo devolve:

  1) `CRES_SEDE`: a lista oficial das 14 CREs (cre_seedf.html), pelo
     nome da RA-sede de cada uma.
  2) `mapa_cre_para_ra()`: LACUNA — a página só lista o NOME das 14 CREs,
     não a tabela completa "CRE → todas as RAs que ela cobre" (ex.: a CRE
     Plano Piloto também cobre Cruzeiro, Lago Sul, Lago Norte,
     Sudoeste/Octogonal, Varjão e Jardim Botânico no zoneamento original)
     — essa tabela detalhada não estava em nenhuma página/PDF salvo,
     precisaria ser conferida direto no site da SEEDF ou por contato.
  3) Indicadores DF-wide extraídos das duas matérias de jornal já salvas
     (não são por RA nem por CRE — ficam registrados como estão nas
     fontes, sem inventar recorte territorial que a fonte não tem):
     - IDEB ensino médio 2023 e posições no ranking nacional
       (correiobraziliense_ideb_2026.html)
     - Fila de espera em creche, nível DF (bsbemdia/Panorama de vagas —
       o valor por CRE só existe num painel Power BI vivo, não capturável)

  Indicador 1.3 (rede física, Censo Escolar SEEDF 2025) e Indicador 1.1/1.2
  (CEPIs de creche e fila por CRE): LACUNA — precisam do dataset bruto por
  escola do INEP/SEEDF (data.se.df.gov.br), nunca baixado nem processado
  (mesma lacuna já registrada no zoneamento original).
"""
import re
from bs4 import BeautifulSoup
from common import fonte

CRES_SEDE = ["Brazlândia", "Ceilândia", "Gama", "Guará", "Núcleo Bandeirante",
             "Paranoá", "Planaltina", "Plano Piloto", "Recanto das Emas",
             "Samambaia", "Santa Maria", "São Sebastião", "Sobradinho", "Taguatinga"]


def mapa_cre_para_ra():
    """LACUNA: devolve só a lista de sedes; a cobertura completa de RAs por
    CRE precisa ser conferida na SEEDF (ver docstring do módulo)."""
    return {sede: None for sede in CRES_SEDE}


def indicadores_df_wide():
    """Fatos de nível Distrito Federal (não por RA/CRE) extraídos das
    matérias já salvas — ver docstring do módulo pra limitação."""
    html = open(fonte("correiobraziliense_ideb_2026.html"), encoding="utf-8", errors="ignore").read()
    text = BeautifulSoup(html, "lxml").get_text(" ", strip=True)
    m1 = re.search(r"ensino médio.{0,60}caiu de ([\d,]+) para ([\d,]+)", text)
    m2 = re.search(r"(\d+)ª colocada nos anos iniciais.{0,10}(\d+)ª nos anos finais.{0,10}(\d+)ª no ensino médio", text)
    m3 = re.search(r"Está em (\d+)ª, (\d+)ª e (\d+)ª", text)
    return {
        "ideb_ensino_medio_2023": float(m1.group(2).replace(",", ".")) if m1 else None,
        "ideb_ensino_medio_2019": float(m1.group(1).replace(",", ".")) if m1 else None,
        "ranking_2019_iniciais_finais_medio": [int(g) for g in m2.groups()] if m2 else None,
        "ranking_2023_iniciais_finais_medio": [int(g) for g in m3.groups()] if m3 else None,
        "fila_creche_df_nivel": "lacuna: só existe em painel Power BI dinâmico (SEEDF), não capturável",
    }


if __name__ == "__main__":
    print("CREs (sede):", CRES_SEDE)
    print("cobertura CRE->RA completa:", "LACUNA (ver docstring)")
    print("indicadores DF-wide:", indicadores_df_wide())
