# 💧 Observatório do Ribeirão Santa Rita — Fernandópolis, SP

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://santa-rita-river-observatory.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: Academic](https://img.shields.io/badge/License-Academic-green.svg)]()
[![UNICASTELO](https://img.shields.io/badge/IC-UNICASTELO_Fernand%C3%B3polis-1A6B9A)]()

> **Iniciação Científica** — Curso de Agronomia  
> Universidade Camilo Castelo Branco (UNICASTELO) · Fernandópolis – SP · 2015–2017  
> Discente: **Amauri Almeida de Souza Junior** · Orientador: **Prof. Dr. Luiz Sergio Vanzela**

---

## ❓ Pergunta Científica

> *"O manejo do uso e ocupação do solo (pastagem vs. cana-de-açúcar) influencia de forma estatisticamente significativa o transporte de sedimentos e a vazão específica nas sub-bacias do Ribeirão Santa Rita, em Fernandópolis – SP?"*

**Resposta:** Sim. A bacia com predominância de cana-de-açúcar (Bacia 2, 1,309 km²) apresentou produção específica de sedimentos consistentemente superior à bacia de pastagem (Bacia 1, 0,710 km²), especialmente nos meses chuvosos, confirmando a influência do manejo do solo sobre a qualidade e disponibilidade dos recursos hídricos superficiais.

---

## 📊 Resumo dos Dados

| Indicador | Valor |
|---|---|
| Bacia 1 — Pastagem | **0,710 km²** |
| Bacia 2 — Cana-de-açúcar | **1,309 km²** |
| Período monitorado | **Ago/2016 a Jul/2017 (12 meses)** |
| Pontos de coleta | **4 estacas** (B1 início/final · B2 início/final) |
| Variáveis analisadas | **4** (vazão, sólidos totais, condutividade, produção de sedimentos) |
| Apresentação | **XI Encontro de IC — Universidade Brasil, Out/2017** |

### 🔵 Descobertas Principais

1. **Cana-de-açúcar produz mais sedimentos** — Bacia 2 com produção específica ~2× maior nos meses chuvosos (out–mar)
2. **Sazonalidade marcante** — maiores valores nos meses chuvosos; estação seca com valores próximos entre bacias
3. **Condutividade elétrica diferenciada** — Bacia 2 apresentou maiores valores, indicando carreamento de íons de insumos agrícolas
4. **Coeficiente de escoamento** — pastagem retém mais água, reduzindo pico de escoamento pós-eventos chuvosos
5. **Modelo replicável** — metodologia aplicável a bacias similares do interior paulista

---

## 🗺️ Área de Estudo

```
Bacia 1 (Pastagem)      → 0,710 km²  · 20°17'22,44" S / 50°16'45,41" O
Bacia 2 (Cana-de-açúcar) → 1,309 km²  · 20°17'27,36" S / 50°16'26,42" O
Ribeirão Santa Rita      → Afluente principal · Fernandópolis – SP
Clima Köppen             → Aw (tropical úmido) · T média: 23,5 °C · P: 1.321 mm/ano
Solo                     → Argissolos Vermelhos e Vermelhos-Amarelos (PVA10)
```

---

## 🔬 Metodologia

```
Campo          →   Medição mensal de vazão pelo método do flutuador integrador
                   3 seções batimétricas (S1, S2, S3) · 5 repetições de velocidade
                   Q = v · Sm   |   v = 0,85 · (d / tm)

Laboratório    →   Sólidos totais: método gravimétrico (estufa 105°C / 24h)
                   Balança analítica Ohaus Adventurer (0,0001 g)
                   Condutividade: Digimed DM-31

Geoprocessamento → Mapeamento LANDSAT 8 (2015) · Declividade ASTER/NASA (30 m)
                   Coef. de escoamento (C) ponderado por classe de uso e área

Análise        →   Critério Gravetter & Wallnau (1995)
                   Excel · ArcGIS 10 · Método de Coby (1954) para descarga sólida
```

---

## 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|---|---|
| `Python 3.11` | Linguagem principal |
| `Streamlit` | Dashboard interativo |
| `Plotly` | Gráficos dinâmicos modernos |
| `Folium` | Mapeamento geoespacial interativo |
| `Pandas / NumPy` | Processamento de dados |

---

## 📁 Estrutura do Repositório

```
santa-rita-river-observatory/
├── app.py                          # Dashboard principal
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
└── assets/
    └── campo/                      # ← COLOQUE SUAS FOTOS AQUI
        ├── 01_ponto_b1_foz.jpg
        ├── 02_ponto_b2_foz.jpg
        ├── 03_estacas_confeccao.jpg
        ├── 04_estacas_prontas_tamanho.jpg
        ├── 05_estacas_instaladas.jpg
        ├── 06_balanca_ohaus_adventurer.jpg
        ├── 07_condutivimetro_digimed_dm31.jpg
        ├── 08_estufa_solab.jpg
        ├── 09_capsulas_porcelana.jpg
        ├── 10_bancada_notebook_amostras.jpg     ← foto destaque (largura total)
        ├── 11_certificado_ic_2017.jpg           ← ou .pdf
        └── certificado_ic_2017.pdf              ← PDF do certificado (opcional)
```

> 💡 **Fotos ausentes** exibem placeholders automáticos com nome e legenda. Adicione as fotos na pasta correta e o sistema detecta na próxima execução.

---

## 🚀 Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/amaurialmeida/santa-rita-river-observatory.git
cd santa-rita-river-observatory

# Instale as dependências
pip install -r requirements.txt

# Crie a pasta de fotos
mkdir -p assets/campo

# Execute
streamlit run app.py
```

---

## 🏆 Reconhecimento Científico

**Certificado de apresentação** no XI Encontro de Iniciação Científica da Universidade Brasil  
📅 São Paulo, 20 de outubro de 2017  
✍️ Assinado por: Prof. Dr. Daniel S. F. Magalhães · Prof. Dr. Marcello Magri Amaral · Prof. Dr. Ricardo Scarparo Navarro

---

## 📚 Referências Principais

- **Vanzela, L.S.; Hernandez, F.B.T.; Franco, R.A.M.** (2010) — Influência do uso e ocupação do solo nos recursos hídricos do Córrego Três Barras. *Rev. Bras. Eng. Agrícola e Ambiental*, v.14, n.1, pp.55–64.
- **Porto, R. de M.** (1999) — *Hidráulica Básica*. 2ª ed. São Carlos: EESC-USP. 519p.
- **Bertoni, J.; Lombardi Neto, F.** (1999) — *Conservação do Solo*. 4ª ed. São Paulo: Ícone. 355p.
- **Silva, D.D.; Pruski, F.F. et al.** (2005) — Efeito da cobertura nas perdas de solo. *Eng. Agrícola*, v.25, n.2, p.409–419.
- **NASA/ASTER** (2010) — Digital Elevation Model, 30 m resolution.

---

## 🔗 Vínculos Acadêmicos

| Plataforma | Link |
|---|---|
| Lattes — Amauri A. de Souza Junior | http://lattes.cnpq.br/9545242042800090 |
| Lattes — Prof. Dr. Luiz Sergio Vanzela | http://lattes.cnpq.br/0284046584743018 |
| Escavador | https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior |

---

## 🌿 Portfólio Ambiental

Este projeto é parte do portfólio de pesquisa ambiental do autor.  
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio/)

---

*© 2015–2026 · Amauri Almeida de Souza Junior · Pesquisa Acadêmica · UNICASTELO Fernandópolis*
