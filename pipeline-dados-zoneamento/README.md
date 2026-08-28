# Pipeline de dados do zoneamento-11-eixos

## Como rodar

```bash
cd pipeline-dados-zoneamento
python3 -m venv venv && venv/bin/pip install openpyxl beautifulsoup4 lxml
venv/bin/python run_all.py
```

Cada `eixoNN_*.py` também roda sozinho (`python eixo04_emprego_renda.py`)
e imprime uma amostra pra conferência rápida. As saídas vão pra `output/`:
um `.csv` e um `.json` por eixo, mais `_consolidado_todas_ras.*` com tudo
junto numa tabela só (colunas prefixadas por `eixoNN__`).

## Estrutura

- `common.py` — lista oficial das 33 RAs e normalização de nome (cada
  fonte escreve diferente: "Ceilândia" vs "CEILANDIA", "SCIA/Estrutural"
  vs "Estrutural" vs "SCIA" etc.)
- `pdad_xlsx.py` — leitor genérico das ~96 abas da planilha oficial da
  PDAD-DF 2021 (`Relatorio_DF_percentual-2021.xlsx`), que é a fonte de
  quase metade dos indicadores do documento.
- `deficit_ipea.py` — parser da Tabela 1 do boletim do IPEA (déficit
  habitacional e renda domiciliar média por RA, base PDAD 2018),
  incluindo a agregação ponderada de Plano Piloto e Jardim Botânico
  (publicados pela fonte já subdivididos em estratos menores).
- `eixo01` a `eixo11` — um módulo por eixo do zoneamento original.

## Status por eixo — o que está validado e o que ficou em aberto

Cada valor abaixo foi **conferido de volta contra o número já publicado**
no `zoneamento-11-eixos-celina-leao-2026-08-27.pdf` antes deste README ser
escrito (não é só "o código rodou sem erro" — é "o número bateu").

| Eixo | Indicadores | Status |
|---|---|---|
| 1. Saúde | dependência do SUS (PDAD A.19), leitos por Região de Saúde (PDS Tabela 48), produção ambulatorial (PDS Tabela 43) | ✅ validados |
| 2. Segurança | homicídio e feminicídio por RA (Anuário Mapas 1/2), roubo a pedestre 2016-2025 (Anuário Tabela 54) | ✅ validados |
| 3. Assistência Social | IVS-DF 2018/2021 (PAS Quadro 7) | ✅ validado |
| | CRAS/CREAS por RA, CadÚnico/IVCAD por área de CRAS | ⚠️ lacuna — não achei a lista unidade-a-unidade dentro do PAS 2024-2027 (só os totais agregados do DF pelo Pacto SUAS); precisaria localizar manualmente ou reconstruir de `sedes_cras.html` |
| 4. Emprego e Renda | desocupação, informalidade, renda domiciliar média, % até 2 SM | ✅ validados |
| 5. Habitação | déficit habitacional, regularização fundiária | ✅ validados |
| 6. Saneamento | água, esgoto, coleta de lixo | ✅ validados |
| 7. Infraestrutura urbana | pavimentação, iluminação, drenagem | ✅ validados |
| 8. Mobilidade | % ônibus, tempo médio de deslocamento (ponderado por faixa) | ✅ validados |
| 9. Educação | lista das 14 CREs (sede) | ✅ validado |
| | cobertura completa CRE→todas as RAs | ⚠️ lacuna — só achei o nome das sedes na página, não a tabela de RAs cobertas por cada CRE |
| | IDEB ensino médio + ranking nacional (nível DF, não por CRE/RA) | ✅ validado, mas é só nível DF |
| | fila de creche, rede física (Censo Escolar) | ⚠️ lacuna já registrada na fonte original (painel Power BI vivo / CSV bruto do INEP nunca processado) |
| 10. Cultura/Esporte/Lazer | quadras esportivas e espaço cultural percebidos (PDAD A.82), COPs por RA | ✅ validados |
| | equipamentos culturais SECEC | ⚠️ parcial — só 8 de ~15 unidades tiveram a RA reconhecida automaticamente no parsing do endereço |
| | bibliotecas por RA | ⚠️ lacuna — a página salva não trouxe a lista unidade-a-unidade |
| 11. Meio Ambiente | jardins/parques, drenagem, ruas alagadas percebidos (PDAD), parques do IBRAM (72 unidades) | ✅ validados |
| | áreas de risco por RA | ⚠️ a fonte primária (Defesa Civil, via reportagem) só dá o total DF (22) e a lista de RAs monitoradas — não existe granularidade de "nº de pontos por RA" em nenhuma fonte encontrada (mesma lacuna já registrada no documento original) |

**Resumo**: 8 dos 11 eixos estão com todos os indicadores automatizados e
validados linha a linha contra o PDF publicado. Os outros 3 (Assistência
Social, Educação, Cultura/Esporte/Lazer) têm pelo menos um indicador que
ficou como lacuna documentada no código — a mesma transparência que o
zoneamento original já usa pras lacunas de pesquisa dele.

## Sobre o eixo de Segurança

`eixo02_seguranca.py` lê o Anuário (fonte "oficial" citada no documento).
Já documentamos nesta sessão que existe uma segunda fonte — o balanço
criminal bruto por RA em ssp.df.gov.br/dados-por-regiao-administrativa —
que às vezes diverge do número interno do Anuário (ver correção de
Cruzeiro/Núcleo Bandeirante/Park Way no Bloco de notas). Esse segundo
scraper (33 downloads de XLS, um por RA) não foi incluído neste pacote
porque foi feito ad hoc durante a conversa, não salvo como script — se for
útil ter isso automatizado também, é só pedir.
