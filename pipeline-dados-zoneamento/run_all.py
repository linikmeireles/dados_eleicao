# -*- coding: utf-8 -*-
"""
Roda os 11 módulos de eixo e salva a saída de cada um em output/
(CSV + JSON, um par de arquivo por eixo). Eixos 9 (parcial) não tem uma
tabela por RA (a rede de ensino é organizada por CRE) — ver
eixo09_educacao.py e o README pra detalhes.

Uso:
    python run_all.py
"""
import eixo01_saude
import eixo02_seguranca
import eixo03_assistencia_social
import eixo04_emprego_renda
import eixo05_habitacao
import eixo06_saneamento
import eixo07_infraestrutura_urbana
import eixo08_mobilidade
import eixo09_educacao
import eixo10_cultura_esporte_lazer
import eixo11_meio_ambiente
from common import RAS_OFICIAIS, salvar

MODULOS = [
    ("eixo01_saude", eixo01_saude,
     ["dependencia_sus_pct", "regiao_de_saude", "leitos_internacao_regiao_saude_2022",
      "producao_ambulatorial_aps_regiao_saude_total_18_22"]),
    ("eixo02_seguranca", eixo02_seguranca,
     ["taxa_homicidio_100mil_hab_2025", "taxa_feminicidio_100mil_mulheres_2025",
      "roubo_pedestre_2016", "roubo_pedestre_2024", "roubo_pedestre_2025",
      "roubo_pedestre_var_2016_2025", "roubo_pedestre_var_2024_2025"]),
    ("eixo03_assistencia_social", eixo03_assistencia_social,
     ["ivs_df_2018", "ivs_df_2021", "cras_qtd", "creas_qtd"]),
    ("eixo04_emprego_renda", eixo04_emprego_renda,
     ["desocupacao_pct", "sem_carteira_pct", "renda_domiciliar_media_2018", "renda_ate2sm_pct"]),
    ("eixo05_habitacao", eixo05_habitacao,
     ["deficit_habitacional_pct", "sem_regularizacao_pct"]),
    ("eixo06_saneamento", eixo06_saneamento,
     ["agua_rede_geral_pct", "esgoto_rede_geral_pct", "lixo_coleta_direta_pct"]),
    ("eixo07_infraestrutura_urbana", eixo07_infraestrutura_urbana,
     ["pavimentacao_pct", "iluminacao_publica_pct", "drenagem_pct"]),
    ("eixo08_mobilidade", eixo08_mobilidade,
     ["onibus_pct", "tempo_medio_min", "tempo_cobertura_pct"]),
    ("eixo10_cultura_esporte_lazer", eixo10_cultura_esporte_lazer,
     ["quadras_esportivas_percebido_pct", "espaco_cultural_percebido_pct", "cops_qtd",
      "equipamentos_culturais_secec_qtd_parcial", "bibliotecas_qtd"]),
    ("eixo11_meio_ambiente", eixo11_meio_ambiente,
     ["jardins_parques_percebido_pct", "drenagem_percebido_pct", "ruas_alagadas_percebido_pct",
      "parques_ibram_qtd", "area_de_risco_monitorada", "area_de_risco_maior_atencao"]),
]


def main():
    consolidado = {ra: {} for ra in RAS_OFICIAIS}
    for slug, modulo, campos in MODULOS:
        print(f"\n=== {slug} ===")
        dataset = modulo.extrair()
        salvar(slug, {k: v for k, v in dataset.items() if k in RAS_OFICIAIS}, campos_extra_ordem=campos)
        for ra in RAS_OFICIAIS:
            consolidado[ra].update({f"{slug}__{k}": v for k, v in dataset.get(ra, {}).items()})

    salvar("_consolidado_todas_ras", consolidado)
    print("\n=== eixo09_educacao (não é por RA — ver saída própria) ===")
    print("CREs (sede):", eixo09_educacao.CRES_SEDE)
    print("indicadores DF-wide:", eixo09_educacao.indicadores_df_wide())

    print("\nPronto. Saídas em output/ — um .csv e um .json por eixo, mais "
          "_consolidado_todas_ras.(csv|json) com tudo junto por RA.")


if __name__ == "__main__":
    main()
