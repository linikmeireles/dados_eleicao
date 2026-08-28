# -*- coding: utf-8 -*-
"""
Eixo 2 — Segurança pública (Parte A). Fonte: Anuário de Segurança Pública
do DF 2026, 2ª edição (SSP-DF) — anuario2026.txt.

  - Indicador 1: Taxa de homicídio por 100 mil habitantes, por RA (2025) — Mapa 1
  - Indicador 2: Taxa de feminicídio por 100 mil mulheres, por RA (2025) — Mapa 2
  - Indicador 3: Roubo a pedestre, ocorrências por RA, 2016-2025 — Tabela 54

Este módulo faz o parsing direto do texto extraído do PDF do Anuário (os
Mapas 1/2 e a Tabela 54 têm layout tabular reconhecível linha a linha).
Pra conferir/atualizar os dados brutos por RA (contagens mensais 2025),
ver também ssp_por_ra.py, que baixa e lê o balanço criminal por RA
publicado à parte em ssp.df.gov.br/dados-por-regiao-administrativa —
IMPORTANTE: como já documentado no projeto (ver Bloco de notas -
progresso.txt), esse balanço bruto por RA às vezes diverge do número que
o Anuário usa internamente pra Mapa 1/2 (ex.: Cruzeiro, Núcleo Bandeirante
e Park Way aparecem como 0,00 no Mapa 1 mas têm 1-2 homicídios no balanço
bruto atualizado em 05/01/2026) — os dois têm que ser tratados como fontes
distintas, não intercambiáveis.
"""
import re
from common import RAS_OFICIAIS, normaliza_ra, salvar, fonte

_NOMES_ORDENADOS = sorted(RAS_OFICIAIS, key=len, reverse=True)


def _texto():
    return open(fonte("anuario2026.txt"), encoding="utf-8").read()


def _extrai_mapa_taxa(texto, titulo_mapa):
    """Extrai a lista 'Região Administrativa <espaços> Taxa' que aparece ao
    lado dos Mapas 1 e 2 (o texto extraído do PDF mistura, na mesma linha
    física, o rótulo solto do mapa e a linha da tabela de ranking — por
    isso a busca é feita com regex 'nome + só espaço + número' em vez de
    por linha inteira, senão o rótulo do mapa atrapalha)."""
    idx = texto.find(titulo_mapa)
    if idx < 0:
        raise ValueError(f"não achei o mapa {titulo_mapa!r} no Anuário")
    trecho = texto[idx: idx + 12000]
    out = {}
    for nome in _NOMES_ORDENADOS:
        variantes = [nome]
        if nome == "Plano Piloto":
            variantes.append("Brasília (Plano Piloto)")
        if nome == "Sol Nascente/Pôr do Sol":
            variantes.append("Sol Nascente e Pôr do Sol")
        if nome == "Sudoeste/Octogonal":
            variantes.append("Sudoeste e Octogonal")
        for variante in variantes:
            m = re.search(rf"{re.escape(variante)}[ \t]+(\d+,\d+)", trecho)
            if m:
                out[nome] = float(m.group(1).replace(",", "."))
                break
    return out


def _extrai_tabela54(texto):
    idx = texto.find("TABELA 54")
    if idx < 0:
        raise ValueError("não achei a TABELA 54 (roubo a pedestre) no Anuário")
    trecho = texto[idx: idx + 4500]
    anos = list(range(2016, 2026))
    out = {}
    for linha in trecho.splitlines():
        stripped = linha.strip()
        for nome in _NOMES_ORDENADOS + ["Distrito Federal"]:
            if stripped.startswith(nome):
                resto = stripped[len(nome):].strip()
                # valores podem ser número (2.771), "-" (não existia a RA) ou "*"/"%"
                tokens = re.findall(r"[\d.]+|-|\*", resto)
                if len(tokens) < 12:
                    break
                serie = {}
                for ano, tok in zip(anos, tokens[:10]):
                    if tok in ("-", "*"):
                        serie[str(ano)] = None
                    else:
                        serie[str(ano)] = int(tok.replace(".", ""))
                var_2016_2025_txt = re.search(r"(-?\d+%|\*)\s+(-?\d+%|\*)", resto)
                serie["variacao_2016_2025"] = var_2016_2025_txt.group(1) if var_2016_2025_txt else None
                serie["variacao_2024_2025"] = var_2016_2025_txt.group(2) if var_2016_2025_txt else None
                key = "Distrito Federal" if nome == "Distrito Federal" else nome
                out[key] = serie
                break
    return out


def extrair():
    texto = _texto()
    homicidio = _extrai_mapa_taxa(texto, "MAPA 1")
    feminicidio = _extrai_mapa_taxa(texto, "MAPA 2")
    roubo = _extrai_tabela54(texto)

    dataset = {}
    for ra in RAS_OFICIAIS:
        serie_roubo = roubo.get(ra, {})
        dataset[ra] = {
            "taxa_homicidio_100mil_hab_2025": homicidio.get(ra),
            "taxa_feminicidio_100mil_mulheres_2025": feminicidio.get(ra),
            "roubo_pedestre_2016": serie_roubo.get("2016"),
            "roubo_pedestre_2024": serie_roubo.get("2024"),
            "roubo_pedestre_2025": serie_roubo.get("2025"),
            "roubo_pedestre_var_2016_2025": serie_roubo.get("variacao_2016_2025"),
            "roubo_pedestre_var_2024_2025": serie_roubo.get("variacao_2024_2025"),
        }
    dataset["_Distrito Federal (total)"] = {
        "roubo_pedestre_2025": roubo.get("Distrito Federal", {}).get("2025"),
    }
    return dataset


if __name__ == "__main__":
    d = extrair()
    salvar("eixo02_seguranca", {k: v for k, v in d.items() if k in RAS_OFICIAIS},
           campos_extra_ordem=["taxa_homicidio_100mil_hab_2025", "taxa_feminicidio_100mil_mulheres_2025",
                                "roubo_pedestre_2016", "roubo_pedestre_2024", "roubo_pedestre_2025",
                                "roubo_pedestre_var_2016_2025", "roubo_pedestre_var_2024_2025"])
    for ra in ["Fercal", "Águas Claras", "Cruzeiro"]:
        print(ra, d[ra])
    print("DF total roubo 2025:", d["_Distrito Federal (total)"])
