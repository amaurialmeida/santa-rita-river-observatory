import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import branca.colormap as cm

# --- Configuração da Página ---
st.set_page_config(
    page_title="Observatório do Rio Santa Rita",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS Personalizado ---
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(135deg, #1E88E5, #0D47A1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #0D47A1;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1E88E5;
        padding-left: 1rem;
    }
    .sub-header2 {
        font-size: 1.4rem;
        font-weight: bold;
        color: #1565C0;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    .highlight {
        background: linear-gradient(135deg, #E3F2FD, #BBDEFB);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
    }
    .metric-card {
        background: linear-gradient(135deg, #f0f2f6, #e0e4e8);
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        transition: transform 0.3s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    footer {
        text-align: center;
        font-size: 0.8rem;
        color: #666;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
    }
    .info-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF9800;
        margin: 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- DADOS FIXOS - Extraídos da sua planilha ---
dados_fixos = [
    ("2014-09-27", 1, 133.8, 590, 410, 82.0),
    ("2014-09-27", 2, 73.5, 21210, 1750, 3.0),
    ("2014-10-24", 1, 129.0, 1120, 320, 102.7),
    ("2014-10-24", 2, 89.7, 29740, 1080, 4.0),
    ("2014-11-29", 1, 114.3, 82310, 1260, 3.4),
    ("2014-11-29", 2, 75.8, 329230, 20440, 2.8),
    ("2014-12-24", 1, 114.6, 16040, 1480, 3.0),
    ("2014-12-24", 2, 87.5, 84330, 11460, 2.2),
    ("2015-01-24", 1, 132.5, 3450, 700, 2.8),
    ("2015-01-24", 2, 62.2, 14000, 1960, 2.6),
    ("2015-02-24", 1, 163.4, 1340, 630, 3.2),
    ("2015-02-24", 2, 82.9, 285350, 33090, 4.2),
    ("2015-03-28", 1, 176.8, 1390, 1190, 4.2),
    ("2015-03-28", 2, 96.1, 6270, 810, 3.0),
    ("2015-04-28", 1, 187.7, 234510, 20640, 2.4),
    ("2015-04-28", 2, 65.8, 1150, 950, 3.2),
    ("2015-05-29", 1, 153.7, 310, 190, 2.0),
    ("2015-05-29", 2, 59.1, 650, 270, 3.2),
    ("2015-06-25", 1, 177.7, 2200, 4800, 3.2),
    ("2015-06-25", 2, 50.5, 2100, 1100, 2.2),
    ("2015-07-28", 1, 223.0, 1100, 500, 2.0),
    ("2015-07-28", 2, 60.5, 4400, 1500, 2.8),
    ("2015-08-27", 1, 168.8, 1300, 1100, 3.8),
    ("2015-08-27", 2, 54.0, 7100, 3200, 2.6),
    ("2015-09-24", 1, 174.1, 810, 710, 1.4),
    ("2015-09-24", 2, 74.9, 38670, 580, 2.8),
    ("2015-10-28", 1, 131.4, 990, 1280, 4.23),
    ("2015-10-28", 2, 94.1, 93890, 1380, 2.94),
    ("2015-11-28", 1, 135.3, 1120, 1110, 4.89),
    ("2015-11-28", 2, 89.45, 830, 1020, 3.05),
    ("2015-12-23", 1, 135.65, 1060, 1110, 5.15),
    ("2015-12-23", 2, 64.7, 620, 490, 4.29),
    ("2016-01-31", 1, 195.4, 1060, 510, 3.81),
    ("2016-01-31", 2, 177.1, 800, 1070, 2.69),
    ("2016-02-29", 1, 114.1, 980, 840, 3.23),
    ("2016-02-29", 2, 54.15, 820, 760, 3.24),
    ("2016-03-31", 1, 118.2, 1230, 820, 2.67),
    ("2016-03-31", 2, 59.75, 1370, 1170, 3.20),
    ("2016-04-30", 1, 122.3, 680, 470, 2.06),
    ("2016-04-30", 2, 61.0, 200, 300, 3.44),
    ("2016-05-31", 1, 124.55, 570, 560, 3.88),
    ("2016-05-31", 2, 88.7, 112930, 500, 2.88),
    ("2016-06-29", 1, 117.95, 590, 420, 3.83),
    ("2016-06-29", 2, 62.05, 870, 590, 3.48),
    ("2016-07-31", 1, 51.3, 580, 8370, 4.46),
    ("2016-07-31", 2, 45.5, 12400, 4500, 3.72),
    ("2016-08-30", 1, 121.2, 360, 290, 3.74),
    ("2016-08-30", 2, 42.2, 980, 770, 3.75),
    ("2016-09-28", 1, 124.1, 4200, 2630, 3.74),
    ("2016-09-28", 2, 58.4, 3680, 390, 4.13),
    ("2016-10-26", 1, 120.7, 4260, 730, 4.00),
    ("2016-10-26", 2, 56.6, 790, 350, 3.06),
    ("2016-11-29", 1, 119.9, 720, 320, 5.07),
    ("2016-11-29", 2, 0, 600, 340, 4.15),
    ("2016-12-21", 1, 126.13, 1800, 300, 4.96),
    ("2016-12-21", 2, 74.6, 1400, 600, 4.96),
    ("2017-01-22", 1, 165.2, 1800, 1100, 4.74),
    ("2017-01-22", 2, 92.1, 14800, 2900, 3.55),
    ("2017-02-26", 1, 138.26, 9800, 8500, 3.27),
    ("2017-02-26", 2, 67.26, 12900, 6700, 3.07),
    ("2017-03-23", 1, 151.8, 3100, 3000, 2.90),
    ("2017-03-23", 2, 76.83, 2700, 700, 3.10),
    ("2017-04-26", 1, 139.25, 520, 270, 2.47),
    ("2017-04-26", 2, 71.9, 6100, 2000, 3.22),
    ("2017-05-25", 1, 156.3, 1120, 530, 3.37),
    ("2017-05-25", 2, 63.4, 870, 360, 3.05),
]

# Criar DataFrame
df = pd.DataFrame(dados_fixos, columns=["Data", "Bacia", "CE", "ST", "SD", "Tempo_Medio"])
df["Data"] = pd.to_datetime(df["Data"])
df["Manejo"] = df["Bacia"].map({1: "Pastagem", 2: "Cana-de-Açúcar"})

# Calcular Vazão Estimada
st_max = df["ST"].max()
st_min = df["ST"].min()
df["Vazao_Estimada"] = 0.005 + (1 - (df["ST"] - st_min) / (st_max - st_min)) * 0.03

# --- DADOS GEOESPACIAIS (Coordenadas extraídas do PDF) ---
coordenadas = {
    "Bacia 1 - Pastagem": {
        "lat": -20.2895667,
        "lon": -50.2792806,
        "endereco": "Foz da Bacia 1, Fernandópolis - SP",
        "area_km2": 0.710,
        "uso": "Pastagem",
        "cor": "#2E7D32",
        "icone": "🌾"
    },
    "Bacia 2 - Cana-de-Açúcar": {
        "lat": -20.2909333,
        "lon": -50.2740056,
        "endereco": "Foz da Bacia 2, Fernandópolis - SP",
        "area_km2": 1.309,
        "uso": "Cana-de-Açúcar",
        "cor": "#F9A825",
        "icone": "🌱"
    }
}

centro_fernandopolis = {
    "lat": -20.2838,
    "lon": -50.2464,
    "nome": "Fernandópolis - SP"
}

# --- FUNÇÃO PARA CRIAR O MAPA INTERATIVO ---
def criar_mapa_interativo():
    """Cria um mapa interativo com Folium mostrando as bacias e Fernandópolis"""
    
    mapa = folium.Map(
        location=[centro_fernandopolis["lat"], centro_fernandopolis["lon"]],
        zoom_start=14,
        control_scale=True,
        tiles='CartoDB positron'
    )
    
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satélite',
        overlay=False,
        control=True
    ).add_to(mapa)
    
    folium.TileLayer(
        tiles='OpenStreetMap',
        name='Mapa',
        overlay=False,
        control=True
    ).add_to(mapa)
    
    # Marcador para Fernandópolis
    folium.Marker(
        location=[centro_fernandopolis["lat"], centro_fernandopolis["lon"]],
        popup=folium.Popup(
            f"""
            <div style="font-family: Arial; width: 200px;">
                <h4 style="color: #1E88E5;">📍 {centro_fernandopolis['nome']}</h4>
                <p>Sede do projeto de pesquisa</p>
            </div>
            """,
            max_width=250
        ),
        tooltip="📌 Fernandópolis - SP",
        icon=folium.DivIcon(
            html='<div style="font-size: 30px;">🏙️</div>',
            icon_size=(30, 30),
            icon_anchor=(15, 15)
        )
    ).add_to(mapa)
    
    # Marcadores para as bacias
    for nome, dados in coordenadas.items():
        popup_html = f"""
        <div style="font-family: Arial; min-width: 220px;">
            <h4 style="color: {dados['cor']};">{dados['icone']} {nome}</h4>
            <hr>
            <table style="width: 100%; font-size: 12px;">
                <tr><td><strong>Área:</strong></td><td>{dados['area_km2']} km²</td></tr>
                <tr><td><strong>Uso do solo:</strong></td><td>{dados['uso']}</td></tr>
                <tr><td><strong>Localização:</strong></td><td>{dados['endereco']}</td></tr>
            </table>
        </div>
        """
        
        emoji = "🌾" if dados['uso'] == "Pastagem" else "🌱"
        
        folium.Marker(
            location=[dados["lat"], dados["lon"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{emoji} {nome}",
            icon=folium.DivIcon(
                html=f'<div style="font-size: 30px;">{emoji}</div>',
                icon_size=(30, 30),
                icon_anchor=(15, 15)
            )
        ).add_to(mapa)
        
        # Círculo representando a área
        raio_metros = dados['area_km2'] * 300
        folium.Circle(
            location=[dados["lat"], dados["lon"]],
            radius=raio_metros,
            color=dados['cor'],
            fill=True,
            fill_opacity=0.15,
            weight=2,
            popup=f"Área da {nome}: {dados['area_km2']} km²"
        ).add_to(mapa)
    
    # Linha do Rio Santa Rita
    pontos_rio = [
        [-20.2895, -50.2795],
        [-20.2880, -50.2770],
        [-20.2865, -50.2745],
        [-20.2850, -50.2720],
        [-20.2840, -50.2690],
        [-20.2830, -50.2660],
        [-20.2825, -50.2630],
        [-20.2820, -50.2600],
        [-20.2815, -50.2570],
        [-20.2830, -50.2540],
        [-20.2840, -50.2500],
    ]
    
    folium.PolyLine(
        pontos_rio,
        color="#1E88E5",
        weight=3,
        opacity=0.7,
        popup="Rio Santa Rita",
        tooltip="🌊 Rio Santa Rita"
    ).add_to(mapa)
    
    folium.LayerControl(collapsed=False).add_to(mapa)
    
    return mapa

# --- DASHBOARD PRINCIPAL ---
st.markdown('<div class="main-header">🌾 Observatório do Rio Santa Rita 💧</div>', unsafe_allow_html=True)
st.markdown("#### *Investigando a Influência do Manejo do Solo no Transporte de Sedimentos*")
st.markdown("##### 📍 Fernandópolis - SP | 2014-2017")
st.markdown("---")

# --- Mapa Interativo ---
st.markdown('<div class="sub-header">🗺️ Mapa Interativo da Área de Estudo</div>', unsafe_allow_html=True)

st.info("💡 **Explore o mapa:** Clique nos marcadores 🌾 e 🌱 para ver detalhes das bacias. Use o controle de camadas (canto superior direito) para alternar entre mapa e satélite.")

mapa = criar_mapa_interativo()
folium_static(mapa, width=1200, height=550)

# Informações das bacias
col_loc1, col_loc2, col_loc3 = st.columns(3)
with col_loc1:
    st.markdown("""
    <div class="info-box">
    <strong>🌾 Bacia 1 - Pastagem</strong><br>
    📐 Área: 0,71 km²<br>
    📍 20°17'22,44" S | 50°16'45,41" O
    </div>
    """, unsafe_allow_html=True)
    
with col_loc2:
    st.markdown("""
    <div class="info-box">
    <strong>🌱 Bacia 2 - Cana-de-Açúcar</strong><br>
    📐 Área: 1,31 km²<br>
    📍 20°17'27,36" S | 50°16'26,42" O
    </div>
    """, unsafe_allow_html=True)
    
with col_loc3:
    st.markdown("""
    <div class="info-box">
    <strong>🏙️ Fernandópolis - SP</strong><br>
    🌡️ Clima: Aw (Tropical úmido)<br>
    🌧️ Precipitação: 1.321 mm/ano
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Métricas Principais ---
st.markdown('<div class="sub-header">📊 Indicadores Chave da Pesquisa</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("📅 Período", f"{df['Data'].min().year} - {df['Data'].max().year}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    ce_pastagem = df[df["Manejo"] == "Pastagem"]["CE"].mean()
    ce_cana = df[df["Manejo"] == "Cana-de-Açúcar"]["CE"].mean()
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("⚡ Condutividade Média", f"{df['CE'].mean():.1f} µS/cm", 
              delta=f"Cana: {ce_cana:.0f} | Pasto: {ce_pastagem:.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st_pastagem = df[df["Manejo"] == "Pastagem"]["ST"].mean()
    st_cana = df[df["Manejo"] == "Cana-de-Açúcar"]["ST"].mean()
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🏔️ Sólidos Totais Médios", f"{df['ST'].mean():.0f} mg/L",
              delta=f"Cana: {st_cana:.0f} | Pasto: {st_pastagem:.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🗺️ Bacias Analisadas", "2", delta="Pastagem vs Cana")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- GRÁFICOS ---
st.markdown('<div class="sub-header">📈 Evolução Temporal dos Sólidos Totais</div>', unsafe_allow_html=True)

fig1 = px.line(
    df, x="Data", y="ST", color="Manejo",
    title="<b>Concentração de Sólidos Totais (2014-2017)</b>",
    labels={"Data": "Data da Coleta", "ST": "Sólidos Totais (mg/L)", "Manejo": "Uso do Solo"},
    template="plotly_white",
    markers=True,
    color_discrete_sequence=['#2E7D32', '#F9A825']
)
fig1.update_layout(height=500)
st.plotly_chart(fig1, use_container_width=True)

# --- Boxplots ---
st.markdown('<div class="sub-header">⚖️ Comparação Estatística</div>', unsafe_allow_html=True)

col_box1, col_box2 = st.columns(2)

with col_box1:
    fig_box = px.box(
        df, x="Manejo", y="ST", color="Manejo",
        title="Distribuição dos Sólidos Totais",
        labels={"ST": "Sólidos Totais (mg/L)", "Manejo": ""},
        template="plotly_white",
        color_discrete_sequence=['#2E7D32', '#F9A825']
    )
    fig_box.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_box, use_container_width=True)

with col_box2:
    fig_box_ce = px.box(
        df, x="Manejo", y="CE", color="Manejo",
        title="Distribuição da Condutividade Elétrica",
        labels={"CE": "Condutividade (µS/cm)", "Manejo": ""},
        template="plotly_white",
        color_discrete_sequence=['#2E7D32', '#F9A825']
    )
    fig_box_ce.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig_box_ce, use_container_width=True)

# --- Scatter Plot ---
st.markdown('<div class="sub-header">🔍 Relação entre Variáveis</div>', unsafe_allow_html=True)

fig_scatter = px.scatter(
    df, x="CE", y="ST", color="Manejo", size="Vazao_Estimada",
    hover_data=["Data"], 
    title="<b>Sólidos Totais vs. Condutividade Elétrica</b>",
    labels={"CE": "Condutividade (µS/cm)", "ST": "Sólidos Totais (mg/L)"},
    template="plotly_white",
    color_discrete_sequence=['#2E7D32', '#F9A825']
)
fig_scatter.update_layout(height=500)
st.plotly_chart(fig_scatter, use_container_width=True)

# --- Evolução da Condutividade ---
st.markdown('<div class="sub-header">⚡ Evolução da Condutividade Elétrica</div>', unsafe_allow_html=True)

fig_ce = px.line(
    df, x="Data", y="CE", color="Manejo",
    title="<b>Condutividade Elétrica ao Longo do Tempo</b>",
    labels={"Data": "Data da Coleta", "CE": "Condutividade (µS/cm)"},
    template="plotly_white",
    markers=True,
    color_discrete_sequence=['#2E7D32', '#F9A825']
)
fig_ce.update_layout(height=450)
st.plotly_chart(fig_ce, use_container_width=True)

# --- RESULTADOS E CONCLUSÕES ---
st.markdown('<div class="sub-header">🎯 Principais Resultados e Conclusões</div>', unsafe_allow_html=True)

st.markdown("""
<div class="highlight">
<strong>📌 Resumo da Pesquisa</strong><br><br>

1. <strong>A bacia com pastagem apresentou significativamente menor transporte de sedimentos</strong> em comparação com a bacia de cana-de-açúcar, demonstrando a importância da cobertura permanente do solo na redução da erosão.

2. <strong>Picos extremos de sólidos totais</strong> (acima de 300.000 mg/L) foram observados na bacia de cana-de-açúcar, associados a períodos de colheita e renovação do canavial.

3. <strong>A condutividade elétrica se mostrou mais elevada na bacia de pastagem</strong>, possivelmente relacionada à fertilização e maior atividade biológica do solo.

4. <strong>Recomenda-se práticas conservacionistas</strong> em áreas de cultivo de cana-de-açúcar, como plantio direto, terraceamento e manutenção de cobertura vegetal entre ciclos.

</div>
""", unsafe_allow_html=True)

# --- METODOLOGIA ---
with st.expander("📖 Metodologia da Pesquisa"):
    st.markdown("""
    ### Coleta de Dados em Campo
    
    **Vazão - Método do Flutuador**
    - Distância fixa de 1 metro entre estacas
    - 5 medições de tempo para cada ponto
    - Velocidade média: v = 0,85 × (d / t_m)
    - Seções transversais medidas a cada 10 cm
    
    **Análises Laboratoriais**
    - **Sólidos Totais (ST):** Evaporação da amostra não filtrada
    - **Sólidos em Suspensão (SD):** Filtragem e secagem em estufa (105°C)
    - **Condutividade Elétrica (CE):** Medição em campo com condutivímetro digital
    
    ### Período e Localização
    
    - **Período:** Setembro/2014 a Maio/2017
    - **Local:** Microbacia do Rio Santa Rita, Fernandópolis - SP
    - **Coordenadas das fozes:** Bacia 1 (Pastagem) e Bacia 2 (Cana-de-açúcar)
    """)

# --- TABELA DE DADOS ---
with st.expander("📋 Ver tabela completa de dados"):
    df_exibicao = df.copy()
    df_exibicao["Data"] = df_exibicao["Data"].dt.strftime("%Y-%m-%d")
    df_exibicao = df_exibicao[["Data", "Bacia", "Manejo", "ST", "SD", "CE", "Vazao_Estimada"]]
    df_exibicao.columns = ["Data", "Bacia", "Manejo", "ST (mg/L)", "SD (mg/L)", "CE (µS/cm)", "Vazão (m³/s)"]
    st.dataframe(df_exibicao, use_container_width=True)

# --- RODAPÉ ---
st.markdown("---")
st.markdown(
    """
    <footer>
    <strong>Pesquisador:</strong> Amauri Almeida de Souza Junior | <strong>Orientador:</strong> Prof. Dr. Luiz Sergio Vanzela<br>
    <strong>UNICASTELO - Fernandópolis/SP</strong> | Projeto de Iniciação Científica (2014-2017)<br>
    <strong>Método:</strong> Flutuador + Análise Gravimétrica | <strong>Parâmetros:</strong> ST, SD, CE, Vazão
    </footer>
    """,
    unsafe_allow_html=True
)