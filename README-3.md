# 💧 Santa Rita River Observatory — Fernandópolis, SP

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?logo=streamlit&logoColor=white)](https://santa-rita-river-observatory.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: Academic](https://img.shields.io/badge/License-Academic-blue.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

🌐 **Languages:** English | [Português](README.pt-BR.md) | [Español](README.es.md)

**Undergraduate Research (Iniciação Científica) — Agronomy**
Universidade Camilo Castelo Branco (UNICASTELO) · Fernandópolis, SP · 2015–2017
**Author:** Amauri Almeida de Souza Junior · **Advisor:** Prof. Dr. Luiz Sergio Vanzela

---

## ❓ Research Question

> "Does land use and management (pasture vs. sugarcane) have a statistically significant influence on sediment transport and specific discharge in the Santa Rita River sub-basins, in Fernandópolis, SP?"

**Answer:** Yes. The sugarcane-dominated basin (Basin 2, 1.309 km²) consistently showed higher specific sediment production than the pasture basin (Basin 1, 0.710 km²), especially during the rainy months — confirming that land management significantly affects the quality and availability of surface water resources.

---

## 📊 Data Summary

| Indicator | Value |
|---|---|
| Basin 1 — Pasture | 0.710 km² |
| Basin 2 — Sugarcane | 1.309 km² |
| Monitoring period | Aug/2016 – Jul/2017 (12 months) |
| Collection points | 4 stakes (B1 start/end · B2 start/end) |
| Variables analyzed | 5 (specific discharge, total solids, electrical conductivity, sediment production, runoff coefficient) |
| Presentation | XI Scientific Initiation Meeting — Universidade Brasil, Oct/2017 |

---

## 🔵 Key Findings

- **Sugarcane produces more sediment than pasture** — Basin 2 shows consistently higher specific sediment production than Basin 1 throughout the monitoring period, especially during harvest and replanting, when soil cover is reduced.
- **Distinct runoff coefficients between basins** — pasture's more continuous year-round cover yields a lower runoff coefficient (C), retaining more water in the basin and reducing peak discharge after rain events.
- **Marked seasonality** — the highest sediment values were recorded in the rainy months (October–March), coinciding with sugarcane's growth cycle and greater soil exposure in Basin 2; the dry season showed similar values between basins.
- **Electrical conductivity as a water-quality indicator** — Basin 2 (sugarcane) showed higher conductivity, indicating greater ion loading from agricultural inputs (fertilizers and herbicides).
- **Direct impact on water resource sustainability** — confirms that land management directly influences surface water quality and availability; the monitoring model is replicable in similar basins across the São Paulo interior.

---

## 🗺️ Study Area

```
Basin 1 (Pasture)        → 0.710 km²  · 20°17'22.44" S / 50°16'45.41" W
Basin 2 (Sugarcane)      → 1.309 km²  · 20°17'27.36" S / 50°16'26.42" W
Santa Rita River          → Main tributary · Fernandópolis, SP
Köppen Climate            → Aw (tropical, wet summer / dry winter)
Avg. Temperature          → 23.5 °C · Avg. Precipitation: 1,321 mm/year
Soil                       → Red and Red-Yellow Argisols (PVA10)
```

The dashboard's interactive map (Folium) plots both basins with clickable markers detailing collection points, basin type, and coordinates.

---

## 🔬 Methodology

```
Field           →  Monthly discharge measurement via the integrating-float method
                    3 cross-sectional profiles (S1, S2, S3), measured every 10 cm
                    5 velocity repetitions per section
                    Q = v · Sm   |   v = 0.85 × (d / tm)

Laboratory      →  Total solids: gravimetric method (oven-dried 105°C / 24h)
                    Ohaus Adventurer analytical balance (0.0001 g precision)
                    Electrical conductivity: Digimed DM-31

Geoprocessing   →  Land-use mapping via LANDSAT 8 imagery (2015)
                    Slope from ASTER/NASA Digital Elevation Model (30 m)
                    Runoff coefficient (C) weighted by land-use class and area

Statistics      →  Gravetter & Wallnau (1995) criterion for comparing basin means
                    Excel for statistical analysis · ArcGIS 10 for mapping
                    Coby (1954) method for total sediment discharge
```

---

## 🖥️ Dashboard Overview

The Streamlit app is organized into five tabs:

1. **🗺️ Map & Analysis** — interactive Folium map of both basins, plus Plotly charts comparing specific discharge and sediment production across basins.
2. **🔬 Methodology & Pipeline** — the full six-step research pipeline, from basin demarcation to statistical analysis, and a land-use distribution chart.
3. **💡 What We Found** — the five key findings above, plus the final scientific conclusion.
4. **📷 In the Field** — real field photos: collection points, stake fabrication and installation, lab instruments (analytical balance, conductivity meter, drying oven), and the IC certificate.
5. **📚 Sources & Credits** — academic references, advisor's Lattes/CNPq record, and Escavador researcher profile.

The full interface — including all data labels, chart titles, and narrative text — is natively trilingual (PT/EN/ES), switchable from the sidebar.

---

## 🛠️ Tech Stack

| Technology | Use |
|---|---|
| Python 3.11 | Core language |
| Streamlit | Dashboard framework |
| Folium + streamlit-folium | Interactive geospatial mapping |
| Plotly (Express & Graph Objects) | Comparative bar, pie, and line charts |
| Pandas / NumPy | Data processing |

---

## 📁 Repository Structure

```
santa-rita-river-observatory/
├── streamlit_app.py         # Main dashboard (5 tabs, PT/EN/ES)
├── setup_folders.py         # One-time script to create the field-photos folder
├── requirements.txt         # Python dependencies
├── README.md                  # This file (English)
├── README.pt-BR.md            # Portuguese version
├── README.es.md               # Spanish version
└── assets/
    └── campo/                # Field photos (see LEIA_ME_FOTOS.md for filenames)
        ├── 01_ponto_b1_foz.jpg
        ├── 02_ponto_b2_foz.jpg
        ├── ...
        └── certificado_ic_2017.pdf
```

💡 Missing photos automatically render as labeled placeholders. Drop files into `assets/campo/` using the exact filenames and the app detects them on next run.

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/amaurialmeida/santa-rita-river-observatory.git
cd santa-rita-river-observatory

# Install dependencies
pip install -r requirements.txt

# Create the field-photos folder structure
python setup_folders.py

# Run
streamlit run streamlit_app.py
```

---

## 🌐 Live App

🔗 **[santa-rita-river-observatory.streamlit.app](https://santa-rita-river-observatory.streamlit.app/)**

Available in 🇧🇷 Portuguese, 🇺🇸 English, and 🇪🇸 Spanish.

---

## 🏆 Academic Recognition

Certificate of presentation at the **XI Scientific Initiation Meeting** of Universidade Brasil.
📅 São Paulo, October 20, 2017
✍️ Signed by: Prof. Dr. Daniel S. F. Magalhães · Prof. Dr. Marcello Magri Amaral · Prof. Dr. Ricardo Scarparo Navarro

---

## 📚 References

- Vanzela, L.S.; Hernandez, F.B.T.; Franco, R.A.M. (2010) — Influence of land use and occupation on the water resources of Córrego Três Barras. *Rev. Bras. Eng. Agrícola e Ambiental*, v.14, n.1, pp.55–64.
- Porto, R. de M. (1999) — *Hidráulica Básica*. 2nd ed. São Carlos: EESC-USP. 519p.
- Bertoni, J.; Lombardi Neto, F. (1999) — *Conservação do Solo*. 4th ed. São Paulo: Ícone. 355p.
- Silva, D.D.; Pruski, F.F. et al. (2005) — Effect of cover on soil loss. *Eng. Agrícola*, v.25, n.2, pp.409–419.
- NASA/ASTER (2010) — Digital Elevation Model, 30 m resolution.

---

## 🔗 Academic / Professional Links

| Platform | Link |
|---|---|
| Lattes — Amauri A. de Souza Junior | http://lattes.cnpq.br/9545242042800090 |
| Lattes — Prof. Dr. Luiz Sergio Vanzela (Advisor) | http://lattes.cnpq.br/0284046584743018 |
| Escavador | https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior |

---

## 🌿 Environmental Portfolio

This project is part of the author's environmental research and data science portfolio.
🔗 [amaurialmeida.github.io/environmental-portfolio](https://amaurialmeida.github.io/environmental-portfolio)

---

© 2015–2026 · Amauri Almeida de Souza Junior · Academic Research · UNICASTELO Fernandópolis
