# -*- coding: utf-8 -*-
"""
Eixo 10 — Cultura, Esporte e Lazer (Parte C).

  - Indicador 2.1 (percepção): % quadra esportiva e % espaço cultural
    público percebidos nas cercanias — PDAD-DF 2021, Tabela A.82.
  - Indicador 2.2: Centros Olímpicos e Paralímpicos (COP) por RA — lista
    oficial da SEL-DF (cops.html), 12 unidades em 11 RAs. Lista estável,
    reproduzida aqui diretamente (não muda com frequência).
  - Equipamentos culturais geridos pela SECEC: contagem PARCIAL — o
    parsing por endereço (secec_equipamentos_culturais.html, 15 "cartas
    de serviço") só reconheceu a localidade de 8 das ~15 unidades de
    forma automática; o resto tem o endereço num formato que o regex
    atual não pega. Ver saída "equipamentos_culturais_qtd" com essa
    ressalva, e conferir contra o zoneamento original se precisão total
    for necessária.
  - Bibliotecas da Rede SECEC/BNB por RA: LACUNA. A página
    (secec_bibliotecas.html) descreve a rede em prosa, mas não trouxe,
    no HTML salvo, a lista unidade-a-unidade por RA (19 das 33 RAs no
    zoneamento original) — provavelmente estava num mapa/tabela
    interativa que não virou texto na hora de salvar a página.
"""
import re
from bs4 import BeautifulSoup
import pdad_xlsx as pdad
from common import RAS_OFICIAIS, normaliza_ra, salvar, fonte

# Lista oficial de Centros Olímpicos e Paralímpicos (SEL-DF) por RA —
# 12 unidades, Ceilândia com 2 (Setor O e Parque da Vaquejada/Sol Nascente).
COPS_POR_RA = {
    "Brazlândia": 1, "Recanto das Emas": 1, "Ceilândia": 2, "Santa Maria": 1,
    "Sobradinho": 1, "SCIA/Estrutural": 1, "São Sebastião": 1, "Gama": 1,
    "Riacho Fundo": 1, "Planaltina": 1, "Samambaia": 1,
}


def _equipamentos_culturais_parcial():
    html = open(fonte("secec_equipamentos_culturais.html"), encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ", strip=True)
    contagem = {}
    nao_reconhecidos = 0
    for m in re.finditer(r"ENDERE[ÇC]O(?:.{5,150}?)CEP[:\s]*[\d.-]+\s*([A-Za-zÀ-ÿ/ ]{2,30})\s*[–-]\s*DF", text):
        ra = normaliza_ra(m.group(1))
        if ra:
            contagem[ra] = contagem.get(ra, 0) + 1
        else:
            nao_reconhecidos += 1
    return contagem, nao_reconhecidos


def extrair():
    quadras = pdad.ler_coluna("A82", "Quadras esportivas_Sim")
    espaco_cultural = pdad.ler_coluna("A82", "Espaço cultural_Sim")
    equipamentos, nao_reconhecidos = _equipamentos_culturais_parcial()
    if nao_reconhecidos:
        print(f"[eixo10] aviso: {nao_reconhecidos} equipamento(s) culturais não "
              f"tiveram a RA reconhecida automaticamente (ver docstring do módulo).")

    dataset = {}
    for ra in RAS_OFICIAIS:
        dataset[ra] = {
            "quadras_esportivas_percebido_pct": quadras.get(ra),
            "espaco_cultural_percebido_pct": espaco_cultural.get(ra),
            "cops_qtd": COPS_POR_RA.get(ra, 0),
            "equipamentos_culturais_secec_qtd_parcial": equipamentos.get(ra, 0),
            "bibliotecas_qtd": None,  # LACUNA — ver docstring
        }
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo10_cultura_esporte_lazer", d,
           campos_extra_ordem=["quadras_esportivas_percebido_pct", "espaco_cultural_percebido_pct",
                                "cops_qtd", "equipamentos_culturais_secec_qtd_parcial", "bibliotecas_qtd"])
    print("total COPs:", sum(v["cops_qtd"] for v in d.values()), "(esperado 12)")
    for ra in ["Plano Piloto", "Ceilândia", "Fercal"]:
        print(ra, d[ra])
