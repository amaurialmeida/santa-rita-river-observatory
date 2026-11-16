import os
import base64

import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from translations import TRANSLATIONS

st.set_page_config(
    page_title="Rio Santa Rita · River Observatory",
    page_icon="💧",
    layout="wide",
)

# ============================================================
# IDIOMAS (mesmos 10 do portfólio)
# ============================================================

LANGS = [
    ("pt", "🇧🇷", "PT"), ("en", "🇺🇸", "EN"), ("es", "🇪🇸", "ES"),
    ("it", "🇮🇹", "IT"), ("fr", "🇫🇷", "FR"), ("de", "🇩🇪", "DE"),
    ("zh", "🇨🇳", "ZH"), ("ar", "🇸🇦", "AR"), ("el", "🇬🇷", "EL"),
    ("af", "🇿🇦", "AF"),
]
CODES = [c for c, _, _ in LANGS]
FLAGS = {c: f"{flag} {label}" for c, flag, label in LANGS}

# separador decimal / de milhar usado no texto e nos gráficos (Plotly: "decimal+milhar")
DECIMAL = {"pt": ",", "en": ".", "es": ",", "it": ",", "fr": ",", "de": ",",
           "zh": ".", "ar": ".", "el": ",", "af": ","}
PLOTLY_SEP = {"pt": ",.", "en": ".,", "es": ",.", "it": ",.", "fr": ", ",
              "de": ",.", "zh": ".,", "ar": ".,", "el": ",.", "af": ", "}


def _initial_lang():
    q = st.query_params.get("lang")
    if isinstance(q, list):
        q = q[0] if q else None
    return q if q in CODES else "pt"


if "lang" not in st.session_state:
    st.session_state.lang = _initial_lang()


def render_lang_selector():
    """Seletor com os 10 idiomas; guarda a escolha também na URL (?lang=xx)."""
    try:
        escolha = st.pills(
            "Language", CODES, selection_mode="single",
            default=st.session_state.lang, format_func=lambda c: FLAGS[c],
            key="lang_pick", label_visibility="collapsed",
        )
    except AttributeError:  # versões antigas do Streamlit sem st.pills
        escolha = st.radio(
            "Language", CODES, index=CODES.index(st.session_state.lang),
            format_func=lambda c: FLAGS[c], horizontal=True,
            key="lang_pick", label_visibility="collapsed",
        )
    if escolha and escolha != st.session_state.lang:
        st.session_state.lang = escolha
        st.query_params["lang"] = escolha
        st.rerun()


render_lang_selector()
LANG = st.session_state.lang
T = TRANSLATIONS[LANG]
RTL = LANG == "ar"


def fmt(x, nd=1):
    """Número com o separador decimal do idioma."""
    return f"{x:.{nd}f}".replace(".", DECIMAL[LANG])


def plot(fig):
    """st.plotly_chart compatível com versões novas e antigas do Streamlit."""
    fig.update_layout(separators=PLOTLY_SEP[LANG])
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


def show_image(path):
    try:
        st.image(path, width="stretch")
    except TypeError:
        st.image(path, use_container_width=True)


def br(text):
    return text.replace("\n", "<br>")


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&family=Noto+Serif:wght@700&family=Noto+Sans:wght@400;500&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Naskh+Arabic:wght@400;700&display=swap');

:root{
  --water:#1A6B9A;--water-dark:#0D4E72;--water-mid:#2580B3;--water-light:#3FA0D0;
  --earth:#5C3D1E;--earth-mid:#7A5230;--earth-light:#A06A3A;
  --cream:#F5F8FA;--warm-gray:#7A8A96;--success:#2D7A3A;--success-soft:#D4EDDA;
  --alert:#C0520B;--alert-soft:#FDE8D8;--black:#0D1117;
}
html,body,[class*="css"]{font-family:'DM Sans','Noto Sans','Noto Sans SC','Noto Naskh Arabic',sans-serif;background-color:var(--cream);color:var(--black);}

.hero-wrap{
  background:linear-gradient(135deg,var(--water-dark) 0%,var(--water) 60%,#1A85C0 100%);
  border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;position:relative;overflow:hidden;
}
.hero-wrap::before{content:"💧";font-size:180px;position:absolute;right:-20px;top:-20px;opacity:0.06;}
.hero-tag{background:#7ECBF5;color:var(--water-dark);font-family:'DM Mono',monospace;font-size:0.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:0.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,0.78);max-width:660px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.85);font-size:0.72rem;font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;padding:5px 12px;border-radius:20px;letter-spacing:0.5px;}
.badge-water{background:rgba(126,203,245,0.22);border-color:#7ECBF5;color:#7ECBF5;}

.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--water);box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;}
.metric-box.earth{border-top-color:var(--earth-light);}
.metric-box.success{border-top-color:var(--success);}
.metric-val{font-family:'Playfair Display','Noto Serif',serif;font-size:2.1rem;font-weight:900;color:var(--water-dark);line-height:1;margin-bottom:0.3rem;direction:ltr;}
.metric-label{font-size:0.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}

.section-label{font-family:'DM Mono','Noto Sans','Noto Sans SC','Noto Naskh Arabic',monospace;font-size:0.65rem;color:var(--water-dark);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.3rem;}
.section-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.9rem;font-weight:700;color:var(--water-dark);margin-bottom:1.2rem;line-height:1.2;}

.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);border-left:4px solid var(--water-light);margin-bottom:1rem;}
.info-card.earth{border-left-color:var(--earth-light);}
.info-card.alert{border-left-color:var(--alert);}
.sim-notice{background:#FFF8E8;border:1px solid #C09020;border-left:5px solid #C09020;border-radius:12px;padding:0.9rem 1.2rem;margin:0.6rem 0 1rem;font-size:0.88rem;color:#5C3D1E;line-height:1.55;}
.sim-notice strong{color:#8A6010;}

.timeline-item{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #e8f0f5;}
.timeline-year{font-family:'Playfair Display','Noto Serif',serif;font-size:1.1rem;font-weight:700;color:var(--water);min-width:80px;}
.timeline-content{flex:1;}
.timeline-title{font-weight:500;color:var(--water-dark);margin-bottom:0.2rem;}
.timeline-desc{font-size:0.85rem;color:var(--warm-gray);}

.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;}
.source-badge{background:var(--water-dark);color:white;font-family:'DM Mono',monospace;font-size:0.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}

.method-step{display:flex;align-items:flex-start;gap:1rem;padding:1rem;background:white;border-radius:12px;margin-bottom:0.8rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);}
.step-num{background:var(--water);color:white;font-family:'Playfair Display','Noto Serif',serif;font-size:1.1rem;font-weight:700;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-content{flex:1;}
.step-title{font-weight:500;color:var(--water-dark);font-size:0.95rem;}
.step-desc{font-size:0.82rem;color:var(--warm-gray);margin-top:0.2rem;}

.discovery-box{background:linear-gradient(135deg,#EFF7FF 0%,#DCF0FF 100%);border:2px solid var(--water-light);border-radius:16px;padding:1.8rem;margin:1rem 0;}
.discovery-title{font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.1rem;font-weight:700;color:var(--water-dark);margin-bottom:0.5rem;}

.footer-wrap{background:var(--water-dark);border-radius:20px;padding:2rem;color:rgba(255,255,255,0.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display','Noto Serif',serif;color:#7ECBF5;font-size:1.2rem;margin-bottom:0.5rem;}

.photo-placeholder{background:#EFF7FF;border:2px dashed var(--water-mid);border-radius:12px;padding:2rem;text-align:center;min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.photo-emoji{font-size:2.5rem;}
.photo-title{font-weight:600;color:var(--water-dark);margin:0.5rem 0 0.2rem;font-size:0.9rem;}
.photo-desc{font-size:0.78rem;color:var(--warm-gray);line-height:1.5;}
.photo-path{font-size:0.65rem;color:var(--water-mid);font-family:'DM Mono',monospace;margin-top:0.5rem;background:#DCF0FF;padding:3px 8px;border-radius:4px;direction:ltr;}
.photo-legenda{font-size:0.72rem;color:var(--warm-gray);font-style:italic;padding:0.5rem 0.8rem;background:#f5f8fa;text-align:center;border-top:1px solid #e0ecf5;}

.photo-destaque{border:3px solid var(--water);border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(26,107,154,0.15);}
.photo-cert{border:3px solid #C09020;border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(192,144,32,0.15);}

.escavador-card{background:linear-gradient(135deg,#FFF8E8,#FFF0C8);border:2px solid #C09020;border-radius:16px;padding:1.5rem;margin-top:1rem;}
.eq-box{direction:ltr;text-align:left;}
</style>
""", unsafe_allow_html=True)

if RTL:
    # Árabe: texto da direita para a esquerda; mapa, gráficos e fórmulas continuam LTR
    st.markdown("""
<style>
[data-testid="stMain"], [data-testid="stAppViewContainer"] .main { direction: rtl; text-align: right; }
.hero-wrap, .info-card, .method-step, .discovery-box, .timeline-item, .escavador-card, .sim-notice { direction: rtl; text-align: right; }
.hero-wrap::before { right: auto; left: -20px; }
.info-card, .info-card.earth, .info-card.alert { border-left: none; border-right: 4px solid var(--water-light); }
.sim-notice { border-left: 1px solid #C09020; border-right: 5px solid #C09020; }
.js-plotly-plot, iframe { direction: ltr; }
body, html, [class*="css"] { font-family: 'Noto Naskh Arabic','DM Sans',sans-serif; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS HIDROLÓGICOS — SIMULADOS (apenas ilustrativos)
# Os valores medidos em campo estão no relatório da Iniciação Científica.
# Substitua estas listas pelos dados reais quando estiverem digitalizados.
# ============================================================

meses = T["months"]

# Produção específica de sedimentos simulada (t km⁻² mês⁻¹)
sed_b1 = [0.8, 1.2, 3.4, 4.1, 3.8, 4.5, 3.9, 3.2, 1.1, 0.6, 0.4, 0.3]
sed_b2 = [1.5, 2.1, 6.2, 7.8, 7.1, 8.3, 7.2, 6.0, 2.0, 1.1, 0.7, 0.5]

# Vazão específica simulada (L s⁻¹ km⁻²)
vazao_b1 = [3.2, 4.1, 8.5, 10.2, 9.8, 11.3, 10.1, 8.7, 3.8, 2.1, 1.5, 1.1]
vazao_b2 = [4.8, 6.2, 12.1, 14.5, 13.8, 15.9, 14.2, 12.0, 5.4, 3.0, 2.1, 1.6]

COR_B1, COR_B2 = "#E67E22", "#1A6B9A"


def sim_notice():
    st.markdown(
        f'<div class="sim-notice">⚠️ <strong>{T["sim_title"]}.</strong> {T["sim_text"]}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-tag">{T['hero_tag']}</div>
  <div class="hero-title">{T['hero_title']}</div>
  <div class="hero-subtitle">{T['hero_subtitle']}</div>
  <div class="hero-badges">
    <span class="badge badge-water">{T['badge1']}</span>
    <span class="badge badge-water">{T['badge2']}</span>
    <span class="badge">{T['badge3']}</span>
    <span class="badge">{T['badge4']}</span>
    <span class="badge">{T['badge5']}</span>
  </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown(f'<div class="metric-box"><div class="metric-val">{fmt(0.71, 2)} km²</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-box earth"><div class="metric-val">{fmt(1.31, 2)} km²</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="metric-box success"><div class="metric-val">12</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="metric-box"><div class="metric-val">4</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ABAS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([T['tab1'], T['tab2'], T['tab3'], T['tab4'], T['tab5']])


def dms(deg, minutes, seconds, negative=True):
    v = deg + minutes / 60 + seconds / 3600
    return -v if negative else v


# Pontos de coleta (coordenadas registradas em campo, convertidas de graus-minutos-segundos)
BACIAS = [
    {"nome": T["map_basin1"], "manejo": T["mgmt1"], "area": 0.710, "cor": COR_B1, "icone": "orange",
     "lat": dms(20, 17, 22.44), "lon": dms(50, 16, 45.41)},
    {"nome": T["map_basin2"], "manejo": T["mgmt2"], "area": 1.309, "cor": COR_B2, "icone": "blue",
     "lat": dms(20, 17, 27.36), "lon": dms(50, 16, 26.42)},
]

# ── TAB 1: MAPA ──────────────────────────────────────────────
with tab1:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card">{T["map_hint"]}</div>', unsafe_allow_html=True)

    # A chave fica no Streamlit Secrets, nunca no código público.
    try:
        carto_key = st.secrets.get("CARTO_API_KEY", "")
    except Exception:
        carto_key = ""

    centro = [sum(b["lat"] for b in BACIAS) / 2, sum(b["lon"] for b in BACIAS) / 2]

    # tiles=None impede o Folium de adicionar uma camada base automaticamente.
    mapa = folium.Map(location=centro, zoom_start=15, tiles=None, control_scale=True)

    if carto_key:
        folium.TileLayer(
            tiles=("https://{s}.basemaps.cartocdn.com/rastertiles/voyager/"
                   "{z}/{x}/{y}{r}.png?key=" + carto_key),
            attr=('&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                  'contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'),
            name="CARTO Voyager", subdomains="abcd", max_zoom=20, overlay=False, control=True,
        ).add_to(mapa)
    else:
        # Fallback: o app continua funcional sem o Secret configurado.
        folium.TileLayer(
            "OpenStreetMap", name="OpenStreetMap",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            control=True,
        ).add_to(mapa)

    for b in BACIAS:
        popup_html = f"""<div style='font-family:sans-serif;min-width:220px;padding:10px'>
            <h4 style='color:#0D4E72;margin:0 0 8px'>{b['nome']}</h4>
            <p style='margin:3px 0;font-size:13px'>🗺️ {T['popup_area']}: <b>{fmt(b['area'], 3)} km²</b></p>
            <p style='margin:3px 0;font-size:13px'>🌱 {T['popup_mgmt']}: <b>{b['manejo']}</b></p>
            <p style='margin:3px 0;font-size:13px'>📍 {T['popup_tributary']}</p>
            <p style='margin:3px 0;font-size:11px;color:#888'>{T['popup_city']}</p>
            <p style='margin:3px 0;font-size:11px;color:#888'>{T['outlet']} · {T['lat']}: {fmt(b['lat'], 5)} | {T['lon']}: {fmt(b['lon'], 5)}</p>
        </div>"""
        folium.Marker(
            location=[b["lat"], b["lon"]],
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=f"💧 {T['outlet_tt']} · {b['nome']} · {fmt(b['area'], 3)} km²",
            icon=folium.Icon(color=b["icone"], icon="tint", prefix="fa"),
        ).add_to(mapa)

    folium_static(mapa, width=1100, height=500)
    st.caption(T["map_note"])

    # ── Gráficos
    st.markdown(f"<br><div class='section-label'>{T['temporal_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['temporal_title']}</div>", unsafe_allow_html=True)
    sim_notice()

    # Sedimentos lado a lado
    fig_sed = go.Figure()
    fig_sed.add_trace(go.Bar(
        name=T["basin_short1"], x=meses, y=sed_b1, marker_color=COR_B1, opacity=0.85,
        hovertemplate='<b>%{x}</b><br>B1: %{y:.1f} t km⁻²<extra></extra>'))
    fig_sed.add_trace(go.Bar(
        name=T["basin_short2"], x=meses, y=sed_b2, marker_color=COR_B2, opacity=0.85,
        hovertemplate='<b>%{x}</b><br>B2: %{y:.1f} t km⁻²<extra></extra>'))
    fig_sed.update_layout(
        barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic'), height=380,
        xaxis=dict(showgrid=False, tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor='#e0ecf5', title=T['bar_y']),
        title=dict(text=T['bar_title'], font=dict(size=14)),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
        margin=dict(t=60, b=20))
    plot(fig_sed)

    col_a, col_b = st.columns(2)
    with col_a:
        nomes_curtos = [br(T["basin_short1"].replace(" · ", "\n")), br(T["basin_short2"].replace(" · ", "\n"))]
        df_vazao_media = pd.DataFrame({
            "Bacia": nomes_curtos,
            "Vazao": [float(np.mean(vazao_b1)), float(np.mean(vazao_b2))],
        })
        fig_vaz = px.bar(df_vazao_media, x="Bacia", y="Vazao", title=T['prod_title'],
                         color="Bacia",
                         color_discrete_map={nomes_curtos[0]: COR_B1, nomes_curtos[1]: COR_B2},
                         text="Vazao")
        fig_vaz.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_vaz.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False, height=340,
            font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic'),
            title=dict(font=dict(size=13)),
            xaxis_title=None, yaxis_title=T["prod_y"], margin=dict(t=50, b=20))
        plot(fig_vaz)

    with col_b:
        uso_data = pd.DataFrame({"Uso": T["pie_cats"], "Area": [45, 38, 12, 5]})
        fig_pie = px.pie(uso_data, values='Area', names='Uso', title=T['pie_title'],
                         color_discrete_sequence=[COR_B1, COR_B2, '#2D7A3A', '#A0A0A0'])
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=340,
            font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic'),
            title=dict(font=dict(size=13)), margin=dict(t=50, b=20))
        plot(fig_pie)

    # Série mensal por bacia
    st.markdown(f"<div class='section-label'>{T['timeline_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['timeline_title']}</div>", unsafe_allow_html=True)

    bacia_idx = st.selectbox(T['select_basin'], [0, 1], format_func=lambda i: T["basin_opts"][i])
    y_data = vazao_b1 if bacia_idx == 0 else vazao_b2
    cor_sel = COR_B1 if bacia_idx == 0 else COR_B2

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=meses, y=y_data, mode='lines+markers',
        line=dict(color=cor_sel, width=3),
        marker=dict(size=9, color=cor_sel, line=dict(width=2, color='white')),
        fill='tozeroy',
        fillcolor=f'rgba({int(cor_sel[1:3], 16)},{int(cor_sel[3:5], 16)},{int(cor_sel[5:7], 16)},0.10)',
        hovertemplate='<b>%{x}</b><br>%{y:.1f} L s⁻¹ km⁻²<extra></extra>'))
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280,
        font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic'),
        xaxis=dict(showgrid=False, tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor='#e0ecf5', title=T["flow_axis"]),
        title=dict(text=T["basin_opts"][bacia_idx], font=dict(size=13)),
        margin=dict(t=50, b=20))
    plot(fig_line)

# ── TAB 2: METODOLOGIA ────────────────────────────────────────
with tab2:
    st.markdown(f'<div class="section-label">{T["method_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["method_title"]}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="discovery-box">
      <div class="discovery-title">{T['sci_question_title']}</div>
      <p style="font-size:1.05rem;color:#0D4E72;line-height:1.7"><em>{T['sci_question']}</em></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["pipeline_label"]}</div>', unsafe_allow_html=True)

    for i, step in enumerate(T['steps'], start=1):
        st.markdown(f"""
        <div class="method-step">
          <div class="step-num">{i}</div>
          <div class="step-content">
            <div class="step-title">{step['title']}</div>
            <div class="step-desc">{step['desc']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
        <div class="info-card">
          <strong>{T['basin_chars_title']}</strong><br><br>
          <div style="font-size:0.88rem;line-height:2">{T['basin_chars']}</div>
          <div style="font-size:0.78rem;color:#7A8A96;margin-top:0.5rem">{T['basin_source']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="info-card earth">
          <strong>{T['method_vars_title']}</strong><br><br>
          <div style="font-size:0.88rem;line-height:2">{T['method_vars']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Fórmulas (notação matemática igual em todos os idiomas)
    L = T["eq_labels"]
    st.markdown(f"""
    <div class="info-card" style="margin-top:1rem;background:linear-gradient(135deg,#EFF7FF,#DCF0FF)">
      <strong style="color:#0D4E72">{T['eq_title']}</strong><br><br>
      <div class="eq-box" style="font-family:'DM Mono',monospace;font-size:0.85rem;line-height:2.2;color:#1A6B9A">
        <b>{L[0]}:</b> F = L / [2 · (A/π)<sup>0{DECIMAL[LANG]}5</sup>]<br>
        <b>{L[1]}:</b> C1 = 2 / (1 + F)<br>
        <b>{L[2]}:</b> C2 = Σ(Ai · Ci) / A<br>
        <b>{L[3]}:</b> C = [2/(1+F)] · (C2/C1)<br>
        <b>{L[4]}:</b> v = {fmt(0.85, 2)} · (d / t<sub>m</sub>)<br>
        <b>{L[5]}:</b> Q = v · S<sub>m</sub><br>
        <b>{L[6]}:</b> S<sub>m</sub> = (S1 + S2 + S3) / 3
      </div>
      <div style="font-size:0.75rem;color:#7A8A96;margin-top:0.5rem">{T['eq_source']}</div>
    </div>
    """, unsafe_allow_html=True)

# ── TAB 3: DESCOBERTAS ────────────────────────────────────────
with tab3:
    st.markdown(f'<div class="section-label">{T["discovery_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["discovery_title"]}</div>', unsafe_allow_html=True)

    for emoji, item in zip(["🔵", "🟠", "🟡", "🟢", "🔴"], T['discoveries']):
        st.markdown(f"""
        <div class="discovery-box" style="margin-bottom:0.8rem">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <span style="font-size:1.5rem">{emoji}</span>
            <div>
              <div class="discovery-title">{item['title']}</div>
              <p style="color:#1A3A5A;line-height:1.65;font-size:0.93rem;margin:0">{item['text']}</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{T["conclusion_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card" style="border-left-color:#0D4E72;background:linear-gradient(135deg,#EFF7FF,#D8EEFA)">
      <strong style="color:#0D4E72;font-size:1rem">{T['conclusion_title']}</strong><br><br>
      <p style="color:#1A6B9A;line-height:1.7;font-size:0.93rem">{T['conclusion_text']}</p>
      <p style="color:#2580B3;font-size:0.82rem;margin-bottom:0"><em>{T['conclusion_author']}</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Impacto comparativo (valores ilustrativos)
    sim_notice()
    categorias = [br(c) for c in T["impact_cats"]]
    vals_b1 = [3.8, 0.5, 6.5, 72]
    vals_b2 = [7.1, 0.9, 9.4, 118]

    fig_impact = go.Figure()
    fig_impact.add_trace(go.Bar(name=T["basin_short1"], x=categorias, y=vals_b1,
                                marker_color=COR_B1, opacity=0.85))
    fig_impact.add_trace(go.Bar(name=T["basin_short2"], x=categorias, y=vals_b2,
                                marker_color=COR_B2, opacity=0.85))
    fig_impact.update_layout(
        barmode='group', title=dict(text=T['impact_title'], font=dict(size=13)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=360,
        font=dict(family='DM Sans, Noto Sans, Noto Sans SC, Noto Naskh Arabic'),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#e0ecf5'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02), margin=dict(t=60, b=20))
    plot(fig_impact)

# ── TAB 4: EM CAMPO ───────────────────────────────────────────
# (emoji, caminho da imagem) na mesma ordem da lista T["photos"]
PHOTO_FILES = [
    ("💧", "assets/campo/01_ponto_b1_foz.jpg"),
    ("🌾", "assets/campo/02_ponto_b2_foz.jpg"),
    ("🪵", "assets/campo/03_estacas_confeccao.jpg"),
    ("📏", "assets/campo/04_estacas_prontas_tamanho.jpg"),
    ("✅", "assets/campo/05_estacas_instaladas.jpg"),
    ("⚖️", "assets/campo/06_balanca_ohaus_adventurer.jpg"),
    ("⚡", "assets/campo/07_condutivimetro_digimed_dm31.jpg"),
    ("🔥", "assets/campo/08_estufa_solab.jpg"),
    ("🫙", "assets/campo/09_capsulas_porcelana.jpg"),
    ("🔬", "assets/campo/10_bancada_notebook_amostras.jpg"),   # destaque
    ("🏆", "assets/campo/11_certificado_ic_2017.jpg"),          # certificado
]
IDX_DESTAQUE, IDX_CERT = 9, 10


def _photo(i):
    emoji, path = PHOTO_FILES[i]
    return {"emoji": emoji, "path": path, **T["photos"][i]}


with tab4:
    st.markdown(f'<div class="section-label">{T["field_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["field_title"]}</div>', unsafe_allow_html=True)

    fotos_normais = [_photo(i) for i in range(len(PHOTO_FILES)) if i not in (IDX_DESTAQUE, IDX_CERT)]
    foto_destaque = _photo(IDX_DESTAQUE)
    foto_cert = _photo(IDX_CERT)

    # Grade de 3 colunas
    for row_start in range(0, len(fotos_normais), 3):
        row_photos = fotos_normais[row_start:row_start + 3]
        cols = st.columns(len(row_photos))
        for col, foto in zip(cols, row_photos):
            with col:
                if os.path.exists(foto['path']):
                    show_image(foto['path'])
                else:
                    st.markdown(f"""
                    <div class="photo-placeholder">
                      <div class="photo-emoji">{foto['emoji']}</div>
                      <div class="photo-title">{foto['titulo']}</div>
                      <div class="photo-desc">{foto['desc']}</div>
                      <div class="photo-path">{foto['path']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(f'<div class="photo-legenda">{foto["legenda"]}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Foto destaque — largura total
    st.markdown("---")
    st.markdown(f"<div class='section-label'>{T['destaque_label']}</div>", unsafe_allow_html=True)
    if os.path.exists(foto_destaque['path']):
        show_image(foto_destaque['path'])
    else:
        st.markdown(f"""
        <div class="photo-placeholder" style="min-height:280px">
          <div class="photo-emoji">{foto_destaque['emoji']}</div>
          <div class="photo-title" style="font-size:1.1rem">{foto_destaque['titulo']}</div>
          <div class="photo-desc" style="max-width:600px">{foto_destaque['desc']}</div>
          <div class="photo-path">{foto_destaque['path']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f'<div class="photo-legenda" style="font-size:0.82rem;padding:0.7rem 1.2rem">{foto_destaque["legenda"]}</div>', unsafe_allow_html=True)

    # Certificado
    st.markdown("---")
    st.markdown(f"<div class='section-label' style='color:#C09020'>{T['cert_label']}</div>", unsafe_allow_html=True)
    col_cert, col_cert_text = st.columns([1, 1])
    with col_cert:
        if os.path.exists(foto_cert['path']):
            show_image(foto_cert['path'])
        else:
            pdf_path = "assets/campo/certificado_ic_2017.pdf"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    pdf_b64 = base64.b64encode(f.read()).decode()
                st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_b64}" width="100%" height="400px" style="border-radius:8px;border:1px solid #ddd"></iframe>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="photo-placeholder" style="border-color:#C09020;background:#FFF8E8">
                  <div class="photo-emoji">🏆</div>
                  <div class="photo-title">{foto_cert['titulo']}</div>
                  <div class="photo-desc">{foto_cert['desc']}</div>
                  <div class="photo-path">{foto_cert['path']}</div>
                </div>
                """, unsafe_allow_html=True)
    with col_cert_text:
        st.markdown(f"""
        <div style="padding:1rem">
          <div style="font-family:'Playfair Display','Noto Serif','Noto Sans SC','Noto Naskh Arabic',serif;font-size:1.3rem;font-weight:700;color:#8A6010;margin-bottom:1rem">
            {T['cert_heading']}
          </div>
          <div style="font-size:0.9rem;line-height:1.8;color:#5C3D1E">{T['cert_html']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Linha do tempo
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-label'>{T['timeline_field_label']}</div>", unsafe_allow_html=True)
    for item in T['timeline_field_items']:
        st.markdown(f"""
        <div class="timeline-item">
          <div class="timeline-year">{item['date']}</div>
          <div class="timeline-content">
            <div class="timeline-title">{item['title']}</div>
            <div class="timeline-desc">{item['desc']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── TAB 5: FONTES ─────────────────────────────────────────────
ESCAVADOR_URL = "https://www.escavador.com/sobre/403010308/amauri-almeida-de-souza-junior"
FONTES_SIGLAS = [
    ("UNICASTELO", "#0D4E72"), ("CNPQ/LATTES", "#1A6B9A"), ("ESCAVADOR", "#2580B3"),
    ("VANZELA et al.", "#3FA0D0"), ("PORTO (1999)", "#0D4E72"), ("BERTONI & LOMBARDI", "#1A6B9A"),
    ("NASA/ASTER", "#2580B3"), ("IBGE", "#3FA0D0"), ("SILVA et al. (2005)", "#0D4E72"),
]

with tab5:
    st.markdown(f'<div class="section-label">{T["sources_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["sources_title"]}</div>', unsafe_allow_html=True)

    for (sigla, cor), fonte in zip(FONTES_SIGLAS, T["sources"]):
        st.markdown(f"""
        <div class="info-card" style="border-left-color:{cor}">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <div style="background:{cor};color:white;font-family:'DM Mono',monospace;font-size:0.6rem;
                 padding:4px 7px;border-radius:4px;white-space:nowrap;flex-shrink:0;margin-top:2px;
                 letter-spacing:0.5px;font-weight:bold;max-width:120px;text-align:center;direction:ltr">{sigla}</div>
            <div>
              <div style="font-weight:500;font-size:0.9rem;color:#0D4E72">{fonte['nome']}</div>
              <div style="font-size:0.82rem;color:#7A8A96;margin-top:0.2rem">{fonte['desc']}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="escavador-card">
      <strong style="color:#8A6010">{T['escavador_label']}</strong><br>
      <p style="font-size:0.88rem;color:#5C3D1E;margin-top:0.5rem">{T['escavador_text']}</p>
      <a href="{ESCAVADOR_URL}" target="_blank"
         style="background:#C09020;color:white;padding:6px 16px;border-radius:6px;
                text-decoration:none;font-size:0.82rem;font-family:'DM Mono','Noto Sans','Noto Naskh Arabic',monospace">
        {T['escavador_btn']}
      </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<br><div class='section-label'>{T['tech_label']}</div>", unsafe_allow_html=True)
    techs = ["Python 3.11", "Streamlit", "Plotly", "Folium", "Pandas", "NumPy", "ArcGIS 10", "LANDSAT 8", "ASTER/NASA"]
    badges_html = "".join([f'<span class="source-badge">{t}</span>' for t in techs])
    st.markdown(f'<div class="source-badges">{badges_html}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="footer-wrap" style="margin-top:2rem">
      <div class="footer-title">{T['footer_title']}</div>
      <p style="margin:0.5rem 0;font-size:0.9rem">{T['footer_desc']}</p>
      <p style="margin:1rem 0 0.5rem;font-size:0.85rem;opacity:0.7">
        {T['footer_links']} &nbsp;|&nbsp;
        🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:#7ECBF5">{T['footer_portfolio']}</a> &nbsp;|&nbsp;
        🐙 <a href="https://github.com/amaurialmeida" style="color:#7ECBF5">GitHub</a> &nbsp;|&nbsp;
        🔗 <a href="{ESCAVADOR_URL}" style="color:#7ECBF5">Escavador</a>
      </p>
      <p style="font-size:0.75rem;opacity:0.5;margin:0">{T['footer_copy']}</p>
    </div>
    """, unsafe_allow_html=True)
