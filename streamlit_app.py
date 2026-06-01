import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import base64

st.set_page_config(
    page_title="Observatório do Ribeirão Santa Rita",
    page_icon="💧",
    layout="wide"
)

# ============================================================
# SISTEMA DE IDIOMAS
# ============================================================

if "lang" not in st.session_state:
    st.session_state.lang = "pt"

TRANSLATIONS = {
    "pt": {
        "page_title": "Observatório do Ribeirão Santa Rita",
        "hero_tag": "IC · UNICASTELO · Agronomia · 2015–2017",
        "hero_title": "Observatório do\nRibeirão Santa Rita",
        "hero_subtitle": "Monitoramento hidrológico de vazão e transporte de sedimentos em duas bacias experimentais com diferentes manejos do solo — pastagem vs. cana-de-açúcar. Fernandópolis – SP (2016–2017).",
        "badge1": "💧 2 Bacias Monitoradas",
        "badge2": "12 Meses de Campo",
        "badge3": "Fernandópolis · SP",
        "badge4": "2016 — 2017",
        "badge5": "UNICASTELO · XI ENCONTRO IC",
        "m1": "Área Bacia 1 (pastagem)",
        "m2": "Área Bacia 2 (cana-de-açúcar)",
        "m3": "Meses monitorados",
        "m4": "Pontos de coleta",
        "tab1": "🗺️ Mapa & Análise",
        "tab2": "🔬 Metodologia & Pipeline",
        "tab3": "💡 O que Descobrimos",
        "tab4": "📷 Em Campo",
        "tab5": "📚 Fontes & Créditos",
        "map_label": "VISUALIZAÇÃO GEOESPACIAL",
        "map_title": "Bacias Experimentais — Fernandópolis, SP",
        "map_hint": "💧 <strong>Interação:</strong> Clique nos marcadores para ver os detalhes das bacias e pontos de coleta. Bacia 1 = pastagem (laranja), Bacia 2 = cana-de-açúcar (azul).",
        "temporal_label": "ANÁLISE COMPARATIVA",
        "temporal_title": "Vazão Específica e Produção de Sedimentos",
        "bar_title": "Produção específica de sedimentos por mês (2016–2017)",
        "bar_y": "Produção de sedimentos (t km⁻² mês⁻¹)",
        "prod_title": "Vazão específica média por bacia",
        "pie_title": "Distribuição do uso e ocupação do solo",
        "timeline_label": "CRONOGRAMA DE MONITORAMENTO",
        "timeline_title": "Ciclo Mensal de Coleta de Dados",
        "select_basin": "Selecione a bacia",
        "method_label": "PESQUISA CIENTÍFICA",
        "method_title": "Pergunta & Metodologia",
        "sci_question_title": "❓ Pergunta Científica Central",
        "sci_question": "\"O manejo do uso e ocupação do solo (pastagem vs. cana-de-açúcar) influencia de forma estatisticamente significativa o transporte de sedimentos e a vazão específica nas sub-bacias do Ribeirão Santa Rita, em Fernandópolis – SP?\"",
        "pipeline_label": "PIPELINE DE DADOS",
        "steps": [
            ("1", "Campo — Seleção e Demarcação das Bacias",
             "Duas bacias hidrográficas afluentes do Ribeirão Santa Rita foram selecionadas: Bacia 1 (0,710 km², predominância de pastagem) e Bacia 2 (1,309 km², predominância de cana-de-açúcar). Estacas de demarcação confeccionadas e instaladas nos pontos de coleta para garantir padronização nas medições mensais."),
            ("2", "Campo — Medição de Vazão (Método do Flutuador Integrador)",
             "Coleta mensal das vazões nas fozes das bacias pelo método do flutuador integrador: 3 seções batimétricas transversais (S1, S2, S3) medidas a cada 10 cm com régua e trena. Velocidade superficial cronometrada em 5 repetições. Cálculo: Q = v × Sm, onde v = 0,85 × (d/tm). Canais com até 60 cm profundidade e 1,5 m largura."),
            ("3", "Laboratório — Análise de Sólidos Totais (Método Gravimétrico)",
             "Amostras de água coletadas e levadas ao laboratório. Concentração de sólidos totais determinada pelo método gravimétrico: amostras filtradas em cápsula de porcelana, secas em estufa Solab a 105°C por 24h, pesadas em balança analítica Ohaus Adventurer (precisão 0,0001 g). Concentração calculada pela massa de sólidos / volume da amostra."),
            ("4", "Laboratório — Condutividade Elétrica",
             "Condutividade elétrica das amostras de água medida com condutivímetro digital Digimed DM-31 diretamente nas amostras coletadas em campo. Parâmetro utilizado como indicador indireto da presença de íons dissolvidos e da influência do uso do solo sobre a qualidade hídrica."),
            ("5", "Geoprocessamento — Mapeamento de Uso do Solo",
             "Mapa atualizado de uso e ocupação do solo confeccionado por digitalização manual e classificação visual de imagens do satélite LANDSAT 8 (2015). Declividade média obtida via modelo de elevação ASTER (NASA, 30 m resolução). Coeficiente volumétrico de escoamento (C2) calculado de forma ponderada por classe de uso e área."),
            ("6", "Análise Estatística e Publicação",
             "Comparação entre médias das duas bacias pelo critério de Gravetter & Wallnau (1995): diferença estatística confirmada quando não há sobreposição dos limites superior/inferior dos erros padrão. Análises no Microsoft Excel. Mapas no ArcGIS 10. Resultados apresentados no XI Encontro de Iniciação Científica da Universidade Brasil (Out/2017)."),
        ],
        "basin_chars_title": "🏞️ Características das Bacias",
        "basin_chars": "• <b>Bacia 1</b> (0,710 km²): Predominância de <b>pastagem</b>. Ponto de coleta: 20°17'22,44\" S / 50°16'45,41\" O<br>• <b>Bacia 2</b> (1,309 km²): Predominância de <b>cana-de-açúcar</b>. Ponto de coleta: 20°17'27,36\" S / 50°16'26,42\" O<br>• <b>Clima:</b> Köppen Aw — tropical úmido, verão chuvoso, inverno seco<br>• <b>Temperatura média:</b> 23,5 °C · <b>Precipitação média:</b> 1.321 mm ano⁻¹<br>• <b>Solo predominante:</b> Argissolos Vermelhos e Vermelhos-Amarelos (PVA10)",
        "basin_source": "Fonte: Projeto IC — UNICASTELO, 2015–2017",
        "method_vars_title": "📐 Variáveis Monitoradas",
        "method_vars": "• <b>Vazão específica</b> (L s⁻¹ km⁻²): vazão / área de drenagem<br>• <b>Concentração de sólidos totais</b> (mg L⁻¹): método gravimétrico<br>• <b>Condutividade elétrica</b> (μS cm⁻¹): Digimed DM-31<br>• <b>Produção específica de sedimentos</b> (t km⁻² ano⁻¹): descarga sólida total / área de drenagem<br>• <b>Coeficiente de escoamento superficial (C)</b>: calculado pelo fator de forma F e coeficiente volumétrico C2",
        "discovery_label": "RESULTADOS DA PESQUISA",
        "discovery_title": "O que os Dados Revelaram",
        "discoveries": [
            ("🔵", "Cana-de-açúcar produz mais sedimentos que pastagem",
             "A Bacia 2 (cana-de-açúcar, 1,309 km²) apresentou produção específica de sedimentos consistentemente superior à Bacia 1 (pastagem, 0,710 km²) ao longo do período monitorado. A cobertura por cana reduz a proteção do solo contra o impacto das chuvas, especialmente no período de colheita e replantio."),
            ("🟠", "Coeficiente de escoamento diferenciado entre bacias",
             "O coeficiente de escoamento superficial (C) calculado para as duas bacias revelou diferenças significativas atribuídas ao tipo de cobertura vegetal. A pastagem, com cobertura mais contínua ao longo do ano, apresenta menor C, retendo mais água na bacia e reduzindo o pico de escoamento após eventos chuvosos."),
            ("🟡", "Sazonalidade marcante no transporte de sedimentos",
             "Os maiores valores de produção de sedimentos foram registrados nos meses chuvosos (outubro a março), coincidindo com o período de maior crescimento da cana e de solo mais exposto na Bacia 2. A estação seca (abril a setembro) apresentou valores próximos entre as duas bacias."),
            ("🟢", "Condutividade elétrica como indicador de qualidade",
             "A condutividade elétrica da água variou entre as bacias conforme o tipo de manejo. A Bacia 2 (cana-de-açúcar) apresentou maiores valores, indicando maior carreamento de íons dissolvidos provenientes de insumos agrícolas (fertilizantes e herbicidas utilizados na cultura)."),
            ("🔴", "Impacto direto na sustentabilidade dos recursos hídricos",
             "Os resultados confirmam que o manejo do uso do solo exerce influência direta sobre a qualidade e disponibilidade dos recursos hídricos superficiais. O modelo de monitoramento desenvolvido pode ser replicado em bacias similares para subsidiar planos de manejo sustentável em municípios do interior paulista."),
        ],
        "conclusion_label": "CONCLUSÃO CIENTÍFICA",
        "conclusion_title": "Confirmação da Hipótese",
        "conclusion_text": "O manejo do uso e ocupação do solo demonstrou influência estatisticamente significativa sobre o transporte de sedimentos e a vazão específica nas sub-bacias do Ribeirão Santa Rita. A bacia com predominância de cana-de-açúcar apresentou maiores valores de produção de sedimentos em relação à bacia de pastagem, especialmente nos meses chuvosos. Os resultados reforçam a necessidade de práticas conservacionistas integradas ao planejamento do uso do solo em bacias hidrográficas da região, visando a sustentabilidade dos recursos hídricos.",
        "conclusion_author": "Amauri A. de Souza Junior — IC Agronomia, UNICASTELO, 2015–2017 · Orientador: Prof. Dr. Luiz Sergio Vanzela",
        "impact_title": "Produção de sedimentos comparativa — Bacias B1 vs. B2 (estimativa relativa)",
        "field_label": "PESQUISA APLICADA",
        "field_title": "A Pesquisa que Saiu do Laboratório",
        "field_instructions_title": "..",
        "field_instructions": ".",
        "photos": [
            {
                "emoji": "💧",
                "titulo": "Ponto B1 — Foz da Bacia 1 (Pastagem)",
                "desc": "Ponto de coleta na foz da Bacia 1, localizado nas coordenadas 20°17'22,44\" S / 50°16'45,41\" O. Sub-bacia de 0,710 km² com predominância de pastagem, afluente do Ribeirão Santa Rita. Local onde foram coletadas mensalmente as amostras de água e medidas as vazões pelo método do flutuador integrador.",
                "path": "assets/campo/01_ponto_b1_foz.jpg",
                "legenda": "Ponto de coleta B1 · Foz da Bacia 1 (Pastagem) · Fernandópolis, SP"
            },
            {
                "emoji": "🌾",
                "titulo": "Ponto B2 — Foz da Bacia 2 (Cana-de-Açúcar)",
                "desc": "Ponto de coleta na foz da Bacia 2, localizado nas coordenadas 20°17'27,36\" S / 50°16'26,42\" O. Sub-bacia de 1,309 km² com predominância de cana-de-açúcar, afluente do Ribeirão Santa Rita. Ponto de referência para comparação com a Bacia 1 nas análises de sedimentos e vazão.",
                "path": "assets/campo/02_ponto_b2_foz.jpg",
                "legenda": "Ponto de coleta B2 · Foz da Bacia 2 (Cana-de-Açúcar) · Fernandópolis, SP"
            },
            {
                "emoji": "🪵",
                "titulo": "Confecção das Estacas — B1 e B2 (Início e Final)",
                "desc": "Confecção das estacas de demarcação para os quatro pontos de medição: B1 início, B1 final, B2 início e B2 final. O processo padronizado garante a precisão na delimitação do trecho de 3 a 5 metros utilizado para a medição da velocidade superficial pelo flutuador integrador.",
                "path": "assets/campo/03_estacas_confeccao.jpg",
                "legenda": "Confecção das estacas de demarcação · Padronização do processo · B1 e B2"
            },
            {
                "emoji": "📏",
                "titulo": "Estacas Prontas — 1,20 m (Padrão Uniforme)",
                "desc": "Estacas B1 início, B1 final, B2 início e B2 final prontas para instalação. Comprimento padronizado de 1,20 m para todos os pontos, garantindo uniformidade na marcação das seções de medição e facilitando a replicação das medições mensais ao longo dos 12 meses de monitoramento.",
                "path": "assets/campo/04_estacas_prontas_tamanho.jpg",
                "legenda": "Estacas de medição · 1,20 m padronizados · B1 início / B1 final / B2 início / B2 final"
            },
            {
                "emoji": "✅",
                "titulo": "Estacas Instaladas — Prontas para Uso!",
                "desc": "Estacas B1 e B2 (início e final) instaladas nos pontos de medição e prontas para o monitoramento de campo. A demarcação visual facilita a identificação do trecho de medição e assegura a reprodutibilidade das coletas mensais de vazão pelo método do flutuador integrador ao longo de todo o período experimental.",
                "path": "assets/campo/05_estacas_instaladas.jpg",
                "legenda": "Estacas instaladas nos pontos B1 e B2 · Prontas para monitoramento · Fernandópolis, SP"
            },
            {
                "emoji": "⚖️",
                "titulo": "Balança Analítica Ohaus Adventurer",
                "desc": "Balança analítica Ohaus Adventurer (precisão de 0,0001 g) utilizada para a determinação gravimétrica da concentração de sólidos totais das amostras de água. Após secagem em estufa a 105 °C, as cápsulas de porcelana são pesadas antes e após a evaporação, e a diferença de massa dividida pelo volume da amostra fornece a concentração de sólidos em suspensão.",
                "path": "assets/campo/06_balanca_ohaus_adventurer.jpg",
                "legenda": "Balança analítica Ohaus Adventurer · Determinação gravimétrica de sólidos totais · Lab. UNICASTELO"
            },
            {
                "emoji": "⚡",
                "titulo": "Condutivímetro Digimed DM-31",
                "desc": "Condutivímetro digital Digimed DM-31 utilizado para medição da condutividade elétrica das amostras de água coletadas nas fozes das bacias. A condutividade elétrica (μS cm⁻¹) indica a concentração de íons dissolvidos na água, funcionando como indicador indireto da influência do manejo do solo (fertilizantes e herbicidas da cultura de cana-de-açúcar) sobre a qualidade hídrica.",
                "path": "assets/campo/07_condutivimetro_digimed_dm31.jpg",
                "legenda": "Condutivímetro Digimed DM-31 · Medição de condutividade elétrica · Lab. UNICASTELO"
            },
            {
                "emoji": "🔥",
                "titulo": "Estufa de Secagem e Esterilização Solab",
                "desc": "Estufa de secagem e esterilização Solab utilizada para evaporar completamente a água das amostras coletadas em campo. As cápsulas de porcelana com as amostras são mantidas a 105 °C por 24 horas até peso constante, restando apenas os sólidos totais dissolvidos e em suspensão. Este processo é parte fundamental do método gravimétrico para determinação da concentração de sólidos.",
                "path": "assets/campo/08_estufa_solab.jpg",
                "legenda": "Estufa de secagem Solab · Evaporação das amostras a 105 °C / 24h · Lab. UNICASTELO"
            },
            {
                "emoji": "🫙",
                "titulo": "Cápsulas de Porcelana — Recipientes de Análise",
                "desc": "Cápsulas de porcelana utilizadas como recipientes individuais para cada amostra de água ao longo de todas as etapas analíticas: pesagem inicial (tara), adição da amostra, secagem em estufa e pesagem final para cálculo da massa de sólidos. Cada cápsula corresponde a uma amostra específica de ponto e data de coleta, garantindo rastreabilidade dos resultados.",
                "path": "assets/campo/09_capsulas_porcelana.jpg",
                "legenda": "Cápsulas de porcelana · Recipientes para análise gravimétrica de sólidos totais · Lab. UNICASTELO"
            },
            {
                "emoji": "🔬",
                "titulo": "Bancada de Análise — Notebook e Amostras em Processamento",
                "desc": "Bancada de trabalho no laboratório da UNICASTELO com as amostras de água coletadas nas bacias B1 e B2 sendo processadas. Notebook de suporte para anotação dos resultados em tempo real durante as análises gravimétricas e de condutividade elétrica. Esta foto resume a rotina mensal de análise laboratorial que sustentou 12 meses de monitoramento hidrológico.",
                "path": "assets/campo/10_bancada_notebook_amostras.jpg",
                "legenda": "Bancada de análise laboratorial · Amostras B1 e B2 em processamento · Lab. UNICASTELO · Fernandópolis, SP",
                "destaque": True
            },
            {
                "emoji": "🏆",
                "titulo": "Certificado — XI Encontro de Iniciação Científica",
                "desc": "Certificado de apresentação do trabalho 'Vazão e Sedimentos em Bacias Hidrográficas de Diferentes Manejos e Escoamento Superficial' no XI Encontro de Iniciação Científica da Universidade Brasil, São Paulo, 20 de outubro de 2017. Assinado pelos Profs. Drs. Daniel S. F. Magalhães, Marcello Magri Amaral e Ricardo Scarparo Navarro.",
                "path": "assets/campo/11_certificado_ic_2017.jpg",
                "legenda": "Certificado IC · XI Encontro de Iniciação Científica · Universidade Brasil · Out/2017",
                "certificado": True
            },
        ],
        "timeline_field_label": "LINHA DO TEMPO DA PESQUISA",
        "timeline_field_items": [
            ("Mai 2015", "Projeto de IC submetido", "UNICASTELO Fernandópolis · Orientador: Prof. Dr. Luiz Sergio Vanzela · Início formal da pesquisa"),
            ("Ago 2016", "Início do monitoramento de campo", "Instalação das estacas nos pontos B1 e B2 · Início das coletas mensais de vazão e amostras de água"),
            ("Ago–Dez 2016", "Estação chuvosa — 1ª metade", "Coletas mensais em B1 (pastagem) e B2 (cana-de-açúcar) · Análises laboratoriais de sólidos e condutividade"),
            ("Jan–Jul 2017", "Estação seca + coletas finais", "Continuidade do monitoramento · Tabulação dos dados e análises estatísticas no Excel · Mapas no ArcGIS 10"),
            ("Jul 2017", "Encerramento do monitoramento", "12 meses completos de coleta · Processamento final dos dados · Redação do relatório científico"),
            ("Out 2017", "Apresentação e certificação", "XI Encontro de IC da Universidade Brasil · São Paulo, SP · Certificado emitido em 20/Out/2017"),
        ],
        "sources_label": "REFERÊNCIAS CIENTÍFICAS",
        "sources_title": "Fontes & Base de Dados",
        "tech_label": "TECNOLOGIAS UTILIZADAS",
        "footer_title": "💧 Amauri Almeida",
        "footer_desc": "Agrônomo em formação · UNICASTELO Fernandópolis<br>Pós-Graduação em IA, Machine Learning & Data Science · Pós-Graduação em Ciência de Dados & Big Data<br>Análise e Desenvolvimento de Sistemas · FACINT Maringá",
        "footer_links": "📍 Fernandópolis · SP · Brasil",
        "escavador_label": "🔗 Perfil Acadêmico no Escavador",
        "escavador_text": "Veja o vínculo acadêmico entre Amauri Almeida de Souza Junior e o Prof. Dr. Luiz Sergio Vanzela (orientador) na plataforma Escavador — base de dados de pesquisadores brasileiros integrada ao Lattes/CNPq.",
    },
    "es": {
        "page_title": "Observatorio del Arroyo Santa Rita",
        "hero_tag": "IC · UNICASTELO · Agronomía · 2015–2017",
        "hero_title": "Observatorio del\nArroyo Santa Rita",
        "hero_subtitle": "Monitoreo hidrológico de caudal y transporte de sedimentos en dos cuencas experimentales con diferentes manejos del suelo — pastizal vs. caña de azúcar. Fernandópolis – SP (2016–2017).",
        "badge1": "💧 2 Cuencas Monitoreadas",
        "badge2": "12 Meses de Campo",
        "badge3": "Fernandópolis · SP",
        "badge4": "2016 — 2017",
        "badge5": "UNICASTELO · XI ENCUENTRO IC",
        "m1": "Área Cuenca 1 (pastizal)",
        "m2": "Área Cuenca 2 (caña de azúcar)",
        "m3": "Meses monitoreados",
        "m4": "Puntos de muestreo",
        "tab1": "🗺️ Mapa & Análisis",
        "tab2": "🔬 Metodología & Pipeline",
        "tab3": "💡 Lo que Descubrimos",
        "tab4": "📷 En Campo",
        "tab5": "📚 Fuentes & Créditos",
        "map_label": "VISUALIZACIÓN GEOESPACIAL",
        "map_title": "Cuencas Experimentales — Fernandópolis, SP",
        "map_hint": "💧 <strong>Interacción:</strong> Haga clic en los marcadores para ver los detalles de las cuencas y puntos de muestreo. Cuenca 1 = pastizal (naranja), Cuenca 2 = caña de azúcar (azul).",
        "temporal_label": "ANÁLISIS COMPARATIVO",
        "temporal_title": "Caudal Específico y Producción de Sedimentos",
        "bar_title": "Producción específica de sedimentos por mes (2016–2017)",
        "bar_y": "Producción de sedimentos (t km⁻² mes⁻¹)",
        "prod_title": "Caudal específico medio por cuenca",
        "pie_title": "Distribución del uso y ocupación del suelo",
        "timeline_label": "CRONOGRAMA DE MONITOREO",
        "timeline_title": "Ciclo Mensual de Recolección de Datos",
        "select_basin": "Seleccione la cuenca",
        "method_label": "INVESTIGACIÓN CIENTÍFICA",
        "method_title": "Pregunta & Metodología",
        "sci_question_title": "❓ Pregunta Científica Central",
        "sci_question": "\"¿El manejo del uso y ocupación del suelo (pastizal vs. caña de azúcar) influye de forma estadísticamente significativa en el transporte de sedimentos y el caudal específico en las subcuencas del Arroyo Santa Rita, en Fernandópolis – SP?\"",
        "pipeline_label": "PIPELINE DE DATOS",
        "steps": [
            ("1", "Campo — Selección y Demarcación de las Cuencas",
             "Dos cuencas hidrográficas afluentes del Arroyo Santa Rita: Cuenca 1 (0,710 km², predominancia de pastizal) y Cuenca 2 (1,309 km², predominancia de caña de azúcar). Estacas de demarcación confeccionadas e instaladas en los puntos de recolección para garantizar la estandarización en las mediciones mensuales."),
            ("2", "Campo — Medición de Caudal (Método del Flotador Integrador)",
             "Recolección mensual de caudales en las desembocaduras de las cuencas: 3 secciones batimétricas transversales medidas cada 10 cm con regla y cinta métrica. Velocidad superficial cronometrada en 5 repeticiones. Cálculo: Q = v × Sm, donde v = 0,85 × (d/tm)."),
            ("3", "Laboratorio — Análisis de Sólidos Totales (Método Gravimétrico)",
             "Muestras filtradas en cápsula de porcelana, secadas en estufa Solab a 105°C por 24h, pesadas en balanza analítica Ohaus Adventurer (precisión 0,0001 g). Concentración calculada por la masa de sólidos / volumen de la muestra."),
            ("4", "Laboratorio — Conductividad Eléctrica",
             "Conductividad eléctrica de las muestras de agua medida con conductivímetro digital Digimed DM-31. Parámetro utilizado como indicador indirecto de la influencia del uso del suelo sobre la calidad hídrica."),
            ("5", "Geoprocesamiento — Mapeo de Uso del Suelo",
             "Mapa actualizado de uso y ocupación del suelo confeccionado por digitalización manual y clasificación visual de imágenes del satélite LANDSAT 8 (2015). Pendiente media obtenida vía modelo de elevación ASTER (NASA, 30 m de resolución)."),
            ("6", "Análisis Estadístico y Publicación",
             "Comparación entre medias de las dos cuencas por el criterio de Gravetter & Wallnau (1995). Análisis en Microsoft Excel. Mapas en ArcGIS 10. Resultados presentados en el XI Encuentro de IC de la Universidad Brasil (Oct/2017)."),
        ],
        "basin_chars_title": "🏞️ Características de las Cuencas",
        "basin_chars": "• <b>Cuenca 1</b> (0,710 km²): Predominancia de <b>pastizal</b>. Punto de muestreo: 20°17'22,44\" S / 50°16'45,41\" O<br>• <b>Cuenca 2</b> (1,309 km²): Predominancia de <b>caña de azúcar</b>. Punto de muestreo: 20°17'27,36\" S / 50°16'26,42\" O<br>• <b>Clima:</b> Köppen Aw — tropical húmedo, verano lluvioso, invierno seco<br>• <b>Temperatura media:</b> 23,5 °C · <b>Precipitación media:</b> 1.321 mm año⁻¹<br>• <b>Suelo predominante:</b> Argissolos Rojos y Rojo-Amarillos (PVA10)",
        "basin_source": "Fuente: Proyecto IC — UNICASTELO, 2015–2017",
        "method_vars_title": "📐 Variables Monitoreadas",
        "method_vars": "• <b>Caudal específico</b> (L s⁻¹ km⁻²): caudal / área de drenaje<br>• <b>Concentración de sólidos totales</b> (mg L⁻¹): método gravimétrico<br>• <b>Conductividad eléctrica</b> (μS cm⁻¹): Digimed DM-31<br>• <b>Producción específica de sedimentos</b> (t km⁻² año⁻¹): descarga sólida total / área<br>• <b>Coeficiente de escorrentía superficial (C)</b>: calculado por el factor de forma F y el coeficiente volumétrico C2",
        "discovery_label": "RESULTADOS DE LA INVESTIGACIÓN",
        "discovery_title": "Lo que los Datos Revelaron",
        "discoveries": [
            ("🔵", "Caña de azúcar produce más sedimentos que pastizal",
             "La Cuenca 2 (caña de azúcar, 1,309 km²) presentó producción específica de sedimentos consistentemente superior a la Cuenca 1 (pastizal, 0,710 km²) durante el período monitoreado. La cobertura de caña reduce la protección del suelo contra el impacto de las lluvias, especialmente en el período de cosecha y replantío."),
            ("🟠", "Coeficiente de escorrentía diferenciado entre cuencas",
             "El coeficiente de escorrentía superficial (C) calculado para las dos cuencas reveló diferencias significativas atribuidas al tipo de cobertura vegetal. El pastizal, con cobertura más continua a lo largo del año, presenta menor C, reteniendo más agua y reduciendo el pico de escorrentía después de eventos lluviosos."),
            ("🟡", "Estacionalidad marcante en el transporte de sedimentos",
             "Los mayores valores de producción de sedimentos fueron registrados en los meses lluviosos (octubre a marzo), coincidiendo con el período de mayor crecimiento de la caña y de suelo más expuesto en la Cuenca 2. La estación seca presentó valores próximos entre las dos cuencas."),
            ("🟢", "Conductividad eléctrica como indicador de calidad",
             "La conductividad eléctrica del agua varió entre las cuencas según el tipo de manejo. La Cuenca 2 (caña de azúcar) presentó mayores valores, indicando mayor arrastre de iones disueltos provenientes de insumos agrícolas (fertilizantes y herbicidas)."),
            ("🔴", "Impacto directo en la sostenibilidad de los recursos hídricos",
             "Los resultados confirman que el manejo del uso del suelo ejerce influencia directa sobre la calidad y disponibilidad de los recursos hídricos superficiales. El modelo de monitoreo puede ser replicado en cuencas similares para subsidiar planes de manejo sostenible."),
        ],
        "conclusion_label": "CONCLUSIÓN CIENTÍFICA",
        "conclusion_title": "Confirmación de la Hipótesis",
        "conclusion_text": "El manejo del uso y ocupación del suelo demostró influencia estadísticamente significativa sobre el transporte de sedimentos y el caudal específico en las subcuencas del Arroyo Santa Rita. La cuenca con predominancia de caña de azúcar presentó mayores valores de producción de sedimentos en relación al pastizal, especialmente en los meses lluviosos.",
        "conclusion_author": "Amauri A. de Souza Junior — IC Agronomía, UNICASTELO, 2015–2017 · Orientador: Prof. Dr. Luiz Sergio Vanzela",
        "impact_title": "Producción de sedimentos comparativa — Cuencas B1 vs. B2 (estimativa relativa)",
        "field_label": "INVESTIGACIÓN APLICADA",
        "field_title": "La Investigación que Salió del Laboratorio",
        "field_instructions_title": ".",
        "field_instructions": "..",
        "photos": [
            {"emoji": "💧", "titulo": "Punto B1 — Desembocadura Cuenca 1 (Pastizal)", "desc": "Punto de muestreo en la desembocadura de la Cuenca 1, coordenadas 20°17'22,44\" S / 50°16'45,41\" O. Subcuenca de 0,710 km² con predominancia de pastizal, afluente del Arroyo Santa Rita.", "path": "assets/campo/01_ponto_b1_foz.jpg", "legenda": "Punto de muestreo B1 · Desembocadura Cuenca 1 (Pastizal) · Fernandópolis, SP"},
            {"emoji": "🌾", "titulo": "Punto B2 — Desembocadura Cuenca 2 (Caña de Azúcar)", "desc": "Punto de muestreo en la desembocadura de la Cuenca 2, coordenadas 20°17'27,36\" S / 50°16'26,42\" O. Subcuenca de 1,309 km² con predominancia de caña de azúcar.", "path": "assets/campo/02_ponto_b2_foz.jpg", "legenda": "Punto de muestreo B2 · Desembocadura Cuenca 2 (Caña) · Fernandópolis, SP"},
            {"emoji": "🪵", "titulo": "Confección de Estacas — B1 y B2", "desc": "Confección de las estacas de demarcación para los cuatro puntos de medición: B1 inicio, B1 final, B2 inicio y B2 final. Proceso estandarizado para garantizar la precisión en la delimitación del trecho de medición.", "path": "assets/campo/03_estacas_confeccao.jpg", "legenda": "Confección de estacas de demarcación · Proceso estandarizado · B1 y B2"},
            {"emoji": "📏", "titulo": "Estacas Listas — 1,20 m (Patrón Uniforme)", "desc": "Estacas B1 inicio, B1 final, B2 inicio y B2 final listas para instalación. Longitud estandarizada de 1,20 m para todos los puntos.", "path": "assets/campo/04_estacas_prontas_tamanho.jpg", "legenda": "Estacas de medición · 1,20 m estandarizados · B1 inicio / B1 final / B2 inicio / B2 final"},
            {"emoji": "✅", "titulo": "¡Estacas Instaladas — Listas para Usar!", "desc": "Estacas B1 y B2 instaladas en los puntos de medición y listas para el monitoreo de campo.", "path": "assets/campo/05_estacas_instaladas.jpg", "legenda": "Estacas instaladas en los puntos B1 y B2 · Listas para monitoreo · Fernandópolis, SP"},
            {"emoji": "⚖️", "titulo": "Balanza Analítica Ohaus Adventurer", "desc": "Balanza analítica Ohaus Adventurer (precisión 0,0001 g) utilizada para la determinación gravimétrica de la concentración de sólidos totales de las muestras de agua.", "path": "assets/campo/06_balanca_ohaus_adventurer.jpg", "legenda": "Balanza analítica Ohaus Adventurer · Determinación gravimétrica · Lab. UNICASTELO"},
            {"emoji": "⚡", "titulo": "Conductivímetro Digimed DM-31", "desc": "Conductivímetro digital Digimed DM-31 utilizado para la medición de la conductividad eléctrica (μS cm⁻¹) de las muestras de agua.", "path": "assets/campo/07_condutivimetro_digimed_dm31.jpg", "legenda": "Conductivímetro Digimed DM-31 · Medición de conductividad eléctrica · Lab. UNICASTELO"},
            {"emoji": "🔥", "titulo": "Estufa de Secado y Esterilización Solab", "desc": "Estufa de secado Solab utilizada para evaporar completamente el agua de las muestras a 105 °C durante 24 horas, dejando solo los sólidos totales.", "path": "assets/campo/08_estufa_solab.jpg", "legenda": "Estufa de secado Solab · Evaporación a 105 °C / 24h · Lab. UNICASTELO"},
            {"emoji": "🫙", "titulo": "Cápsulas de Porcelana — Recipientes de Análisis", "desc": "Cápsulas de porcelana utilizadas como recipientes individuales para cada muestra durante todas las etapas analíticas: pesado inicial, adición de muestra, secado y pesado final.", "path": "assets/campo/09_capsulas_porcelana.jpg", "legenda": "Cápsulas de porcelana · Análisis gravimétrico de sólidos totales · Lab. UNICASTELO"},
            {"emoji": "🔬", "titulo": "Banco de Análisis — Notebook y Muestras en Proceso", "desc": "Banco de trabajo en el laboratorio de la UNICASTELO con las muestras de agua de las cuencas B1 y B2 siendo procesadas. Notebook de soporte para el registro de resultados en tiempo real.", "path": "assets/campo/10_bancada_notebook_amostras.jpg", "legenda": "Banco de análisis laboratorial · Muestras B1 y B2 en procesamiento · Lab. UNICASTELO", "destaque": True},
            {"emoji": "🏆", "titulo": "Certificado — XI Encuentro de IC", "desc": "Certificado de presentación del trabajo 'Caudal y Sedimentos en Cuencas Hidrográficas de Diferentes Manejos y Escorrentía Superficial' en el XI Encuentro de IC de la Universidad Brasil, São Paulo, 20 de octubre de 2017.", "path": "assets/campo/11_certificado_ic_2017.jpg", "legenda": "Certificado IC · XI Encuentro de IC · Universidad Brasil · Oct/2017", "certificado": True},
        ],
        "timeline_field_label": "CRONOLOGÍA DE LA INVESTIGACIÓN",
        "timeline_field_items": [
            ("May 2015", "Proyecto de IC presentado", "UNICASTELO Fernandópolis · Orientador: Prof. Dr. Luiz Sergio Vanzela · Inicio formal de la investigación"),
            ("Ago 2016", "Inicio del monitoreo de campo", "Instalación de estacas en los puntos B1 y B2 · Inicio de las recolecciones mensuales"),
            ("Ago–Dic 2016", "Estación lluviosa — 1ª mitad", "Recolecciones mensuales en B1 (pastizal) y B2 (caña) · Análisis laboratoriales de sólidos y conductividad"),
            ("Ene–Jul 2017", "Estación seca + recolecciones finales", "Continuidad del monitoreo · Tabulación de datos y análisis estadísticos en Excel · Mapas en ArcGIS 10"),
            ("Jul 2017", "Cierre del monitoreo", "12 meses completos de recolección · Procesamiento final · Redacción del informe científico"),
            ("Oct 2017", "Presentación y certificación", "XI Encuentro de IC de la Universidad Brasil · São Paulo, SP · Certificado emitido el 20/Oct/2017"),
        ],
        "sources_label": "REFERENCIAS CIENTÍFICAS",
        "sources_title": "Fuentes & Base de Datos",
        "tech_label": "TECNOLOGÍAS UTILIZADAS",
        "footer_title": "💧 Amauri Almeida",
        "footer_desc": "Agrónomo en formación · UNICASTELO Fernandópolis<br>Posgrado en IA, Machine Learning & Data Science · Posgrado en Ciencia de Datos & Big Data<br>Análisis y Desarrollo de Sistemas · FACINT Maringá",
        "footer_links": "📍 Fernandópolis · SP · Brasil",
        "escavador_label": "🔗 Perfil Académico en Escavador",
        "escavador_text": "Vea el vínculo académico entre Amauri Almeida de Souza Junior y el Prof. Dr. Luiz Sergio Vanzela (orientador) en la plataforma Escavador — base de datos de investigadores brasileños integrada al Lattes/CNPq.",
    },
    "en": {
        "page_title": "Santa Rita Stream Observatory",
        "hero_tag": "Undergrad Research · UNICASTELO · Agronomy · 2015–2017",
        "hero_title": "Santa Rita\nStream Observatory",
        "hero_subtitle": "Hydrological monitoring of streamflow and sediment transport in two experimental catchments with different land uses — pasture vs. sugarcane. Fernandópolis – SP (2016–2017).",
        "badge1": "💧 2 Monitored Basins",
        "badge2": "12 Months of Fieldwork",
        "badge3": "Fernandópolis · SP",
        "badge4": "2016 — 2017",
        "badge5": "UNICASTELO · XI UG RESEARCH CONF.",
        "m1": "Basin 1 area (pasture)",
        "m2": "Basin 2 area (sugarcane)",
        "m3": "Months monitored",
        "m4": "Sampling points",
        "tab1": "🗺️ Map & Analysis",
        "tab2": "🔬 Methodology & Pipeline",
        "tab3": "💡 What We Found",
        "tab4": "📷 Field Research",
        "tab5": "📚 Sources & Credits",
        "map_label": "GEOSPATIAL VISUALIZATION",
        "map_title": "Experimental Catchments — Fernandópolis, SP",
        "map_hint": "💧 <strong>Interaction:</strong> Click on the markers to see catchment and sampling point details. Basin 1 = pasture (orange), Basin 2 = sugarcane (blue).",
        "temporal_label": "COMPARATIVE ANALYSIS",
        "temporal_title": "Specific Discharge and Sediment Yield",
        "bar_title": "Monthly specific sediment yield (2016–2017)",
        "bar_y": "Sediment yield (t km⁻² month⁻¹)",
        "prod_title": "Mean specific discharge by basin",
        "pie_title": "Land use and land cover distribution",
        "timeline_label": "MONITORING SCHEDULE",
        "timeline_title": "Monthly Data Collection Cycle",
        "select_basin": "Select basin",
        "method_label": "SCIENTIFIC RESEARCH",
        "method_title": "Research Question & Methodology",
        "sci_question_title": "❓ Central Research Question",
        "sci_question": "\"Does land use and land cover management (pasture vs. sugarcane) significantly influence sediment transport and specific discharge in the sub-catchments of the Santa Rita Stream, in Fernandópolis – SP?\"",
        "pipeline_label": "DATA PIPELINE",
        "steps": [
            ("1", "Field — Basin Selection and Demarcation",
             "Two tributary catchments of Santa Rita Stream: Basin 1 (0.710 km², pasture) and Basin 2 (1.309 km², sugarcane). Measurement stakes installed at inlet and outlet points for standardized monthly measurements."),
            ("2", "Field — Streamflow Measurement (Float Integration Method)",
             "Monthly flow measurements at basin outlets: 3 cross-sectional bathymetric profiles (S1, S2, S3) measured every 10 cm. Surface velocity timed in 5 repetitions. Calculation: Q = v × Sm, where v = 0.85 × (d/tm). Channels up to 60 cm deep and 1.5 m wide."),
            ("3", "Lab — Total Solids Analysis (Gravimetric Method)",
             "Water samples filtered in porcelain crucibles, dried in Solab oven at 105°C for 24h, weighed on Ohaus Adventurer analytical balance (0.0001 g precision). Concentration calculated as solids mass / sample volume."),
            ("4", "Lab — Electrical Conductivity",
             "Electrical conductivity measured using Digimed DM-31 digital conductimeter. Used as indirect indicator of dissolved ion load and land use influence on water quality."),
            ("5", "Geoprocessing — Land Use Mapping",
             "Updated land use map produced by manual digitizing and visual classification of LANDSAT 8 imagery (2015). Mean slope derived from ASTER digital elevation model (NASA, 30 m resolution)."),
            ("6", "Statistical Analysis and Publication",
             "Comparison between basin means by Gravetter & Wallnau (1995) criterion. Analysis in Microsoft Excel. Maps in ArcGIS 10. Results presented at the XI Undergraduate Research Conference, Universidade Brasil (Oct/2017)."),
        ],
        "basin_chars_title": "🏞️ Basin Characteristics",
        "basin_chars": "• <b>Basin 1</b> (0.710 km²): <b>Pasture</b> dominated. Sampling point: 20°17'22.44\" S / 50°16'45.41\" W<br>• <b>Basin 2</b> (1.309 km²): <b>Sugarcane</b> dominated. Sampling point: 20°17'27.36\" S / 50°16'26.42\" W<br>• <b>Climate:</b> Köppen Aw — humid tropical, rainy summer, dry winter<br>• <b>Mean temperature:</b> 23.5 °C · <b>Mean precipitation:</b> 1,321 mm yr⁻¹<br>• <b>Dominant soil:</b> Red and Red-Yellow Argisols (PVA10)",
        "basin_source": "Source: Undergrad Research Project — UNICASTELO, 2015–2017",
        "method_vars_title": "📐 Monitored Variables",
        "method_vars": "• <b>Specific discharge</b> (L s⁻¹ km⁻²): streamflow / drainage area<br>• <b>Total solids concentration</b> (mg L⁻¹): gravimetric method<br>• <b>Electrical conductivity</b> (μS cm⁻¹): Digimed DM-31<br>• <b>Specific sediment yield</b> (t km⁻² yr⁻¹): total solid discharge / drainage area<br>• <b>Runoff coefficient (C)</b>: calculated from form factor F and volumetric runoff coefficient C2",
        "discovery_label": "RESEARCH RESULTS",
        "discovery_title": "What the Data Revealed",
        "discoveries": [
            ("🔵", "Sugarcane produces more sediment than pasture",
             "Basin 2 (sugarcane, 1.309 km²) consistently showed higher specific sediment yield than Basin 1 (pasture, 0.710 km²) throughout the monitoring period. Sugarcane cover reduces soil protection from rainfall impact, especially during harvest and replanting periods."),
            ("🟠", "Differentiated runoff coefficients between basins",
             "The runoff coefficient (C) calculated for both basins revealed significant differences attributed to vegetation cover type. Pasture, with more continuous year-round cover, shows lower C, retaining more water and reducing peak runoff after rainfall events."),
            ("🟡", "Strong seasonality in sediment transport",
             "The highest sediment yield values were recorded in the rainy months (October to March), coinciding with sugarcane growth and greater soil exposure in Basin 2. The dry season showed similar values between the two basins."),
            ("🟢", "Electrical conductivity as a quality indicator",
             "Water electrical conductivity varied between basins according to management type. Basin 2 (sugarcane) showed higher values, indicating greater transport of dissolved ions from agricultural inputs (fertilizers and herbicides)."),
            ("🔴", "Direct impact on water resource sustainability",
             "Results confirm that land use management directly influences the quality and availability of surface water resources. The monitoring model can be replicated in similar catchments to support sustainable land management plans."),
        ],
        "conclusion_label": "SCIENTIFIC CONCLUSION",
        "conclusion_title": "Hypothesis Confirmed",
        "conclusion_text": "Land use and land cover management demonstrated statistically significant influence on sediment transport and specific discharge in the Santa Rita Stream sub-catchments. The sugarcane-dominated basin showed higher sediment yields compared to the pasture basin, particularly during the rainy months. Results reinforce the need for integrated conservation practices in watershed management planning.",
        "conclusion_author": "Amauri A. de Souza Junior — Agronomy Undergrad Research, UNICASTELO, 2015–2017 · Advisor: Prof. Dr. Luiz Sergio Vanzela",
        "impact_title": "Comparative sediment yield — Basins B1 vs. B2 (relative estimate)",
        "field_label": "APPLIED RESEARCH",
        "field_title": "Research That Left the Laboratory",
        "field_instructions_title": "📁 How to add your photos",
        "field_instructions": "Place your photos in the <code>assets/campo/</code> folder with the exact file names shown on each card. The system automatically detects and replaces the placeholder with the real image.",
        "photos": [
            {"emoji": "💧", "titulo": "Point B1 — Basin 1 Outlet (Pasture)", "desc": "Sampling point at the outlet of Basin 1, coordinates 20°17'22.44\" S / 50°16'45.41\" W. Sub-catchment of 0.710 km² with pasture cover, tributary of Santa Rita Stream.", "path": "assets/campo/01_ponto_b1_foz.jpg", "legenda": "Sampling point B1 · Basin 1 Outlet (Pasture) · Fernandópolis, SP"},
            {"emoji": "🌾", "titulo": "Point B2 — Basin 2 Outlet (Sugarcane)", "desc": "Sampling point at the outlet of Basin 2, coordinates 20°17'27.36\" S / 50°16'26.42\" W. Sub-catchment of 1.309 km² with sugarcane cover.", "path": "assets/campo/02_ponto_b2_foz.jpg", "legenda": "Sampling point B2 · Basin 2 Outlet (Sugarcane) · Fernandópolis, SP"},
            {"emoji": "🪵", "titulo": "Stakes Manufacturing — B1 and B2", "desc": "Manufacturing of demarcation stakes for the four measurement points: B1 start, B1 end, B2 start and B2 end. Standardized process to ensure precision in delimiting the 3–5 m measurement reach.", "path": "assets/campo/03_estacas_confeccao.jpg", "legenda": "Demarcation stakes manufacturing · Standardized process · B1 and B2"},
            {"emoji": "📏", "titulo": "Finished Stakes — 1.20 m (Uniform Standard)", "desc": "Stakes B1 start, B1 end, B2 start and B2 end ready for installation. Standardized length of 1.20 m for all points.", "path": "assets/campo/04_estacas_prontas_tamanho.jpg", "legenda": "Measurement stakes · Standardized 1.20 m · B1 start / B1 end / B2 start / B2 end"},
            {"emoji": "✅", "titulo": "Stakes Installed — Ready to Go!", "desc": "B1 and B2 stakes installed at the measurement points and ready for field monitoring.", "path": "assets/campo/05_estacas_instaladas.jpg", "legenda": "Stakes installed at B1 and B2 points · Ready for monitoring · Fernandópolis, SP"},
            {"emoji": "⚖️", "titulo": "Ohaus Adventurer Analytical Balance", "desc": "Ohaus Adventurer analytical balance (0.0001 g precision) used for gravimetric determination of total solids concentration in water samples.", "path": "assets/campo/06_balanca_ohaus_adventurer.jpg", "legenda": "Ohaus Adventurer analytical balance · Gravimetric determination · UNICASTELO Lab"},
            {"emoji": "⚡", "titulo": "Digimed DM-31 Conductimeter", "desc": "Digimed DM-31 digital conductimeter used to measure electrical conductivity (μS cm⁻¹) of water samples as an indirect indicator of dissolved ions from land use inputs.", "path": "assets/campo/07_condutivimetro_digimed_dm31.jpg", "legenda": "Digimed DM-31 conductimeter · Electrical conductivity measurement · UNICASTELO Lab"},
            {"emoji": "🔥", "titulo": "Solab Drying and Sterilization Oven", "desc": "Solab drying oven used to completely evaporate water from samples at 105°C for 24 hours, leaving only the total dissolved and suspended solids.", "path": "assets/campo/08_estufa_solab.jpg", "legenda": "Solab drying oven · Evaporation at 105°C / 24h · UNICASTELO Lab"},
            {"emoji": "🫙", "titulo": "Porcelain Crucibles — Analysis Vessels", "desc": "Individual porcelain crucibles used for each water sample through all analytical stages: initial weighing, sample addition, drying and final weighing.", "path": "assets/campo/09_capsulas_porcelana.jpg", "legenda": "Porcelain crucibles · Gravimetric analysis vessels · UNICASTELO Lab"},
            {"emoji": "🔬", "titulo": "Analysis Bench — Laptop and Samples in Process", "desc": "Laboratory workbench at UNICASTELO with B1 and B2 water samples being processed. Laptop for real-time data entry during gravimetric and conductivity analyses.", "path": "assets/campo/10_bancada_notebook_amostras.jpg", "legenda": "Laboratory analysis bench · B1 and B2 samples in processing · UNICASTELO · Fernandópolis, SP", "destaque": True},
            {"emoji": "🏆", "titulo": "Certificate — XI Undergrad Research Conference", "desc": "Certificate of presentation of 'Streamflow and Sediments in Watersheds with Different Land Uses and Surface Runoff' at the XI Undergrad Research Conference, Universidade Brasil, São Paulo, October 20, 2017.", "path": "assets/campo/11_certificado_ic_2017.jpg", "legenda": "IC Certificate · XI Undergrad Research Conference · Universidade Brasil · Oct/2017", "certificado": True},
        ],
        "timeline_field_label": "RESEARCH TIMELINE",
        "timeline_field_items": [
            ("May 2015", "Research project submitted", "UNICASTELO Fernandópolis · Advisor: Prof. Dr. Luiz Sergio Vanzela · Formal research start"),
            ("Aug 2016", "Field monitoring begins", "Stakes installed at B1 and B2 points · Monthly sampling campaigns initiated"),
            ("Aug–Dec 2016", "Rainy season — 1st half", "Monthly collections at B1 (pasture) and B2 (sugarcane) · Lab analysis of solids and conductivity"),
            ("Jan–Jul 2017", "Dry season + final collections", "Monitoring continuity · Data tabulation and statistical analysis in Excel · Maps in ArcGIS 10"),
            ("Jul 2017", "Monitoring completed", "12 full months of sampling · Final data processing · Research report writing"),
            ("Oct 2017", "Presentation and certification", "XI Undergrad Research Conference · Universidade Brasil · São Paulo, SP · Oct 20, 2017"),
        ],
        "sources_label": "SCIENTIFIC REFERENCES",
        "sources_title": "Sources & Database",
        "tech_label": "TECHNOLOGIES USED",
        "footer_title": "💧 Amauri Almeida",
        "footer_desc": "Agronomy Student · UNICASTELO Fernandópolis<br>Post-Grad in AI, Machine Learning & Data Science · Post-Grad in Data Science & Big Data<br>Systems Analysis and Development · FACINT Maringá",
        "footer_links": "📍 Fernandópolis · SP · Brazil",
        "escavador_label": "🔗 Academic Profile on Escavador",
        "escavador_text": "See the academic link between Amauri Almeida de Souza Junior and Prof. Dr. Luiz Sergio Vanzela (advisor) on the Escavador platform — Brazilian researcher database integrated with Lattes/CNPq.",
    },
}

# ============================================================
# SELETOR DE IDIOMA
# ============================================================

def render_lang_selector():
    col_space, col_pt, col_es, col_en = st.columns([8, 1, 1, 1])
    with col_pt:
        if st.button("🇧🇷 PT", use_container_width=True,
                     type="primary" if st.session_state.lang == "pt" else "secondary"):
            st.session_state.lang = "pt"
            st.rerun()
    with col_es:
        if st.button("🇪🇸 ES", use_container_width=True,
                     type="primary" if st.session_state.lang == "es" else "secondary"):
            st.session_state.lang = "es"
            st.rerun()
    with col_en:
        if st.button("🇺🇸 EN", use_container_width=True,
                     type="primary" if st.session_state.lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()

render_lang_selector()
T = TRANSLATIONS[st.session_state.lang]

# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&family=DM+Mono&display=swap');

:root{
  --water:#1A6B9A;--water-dark:#0D4E72;--water-mid:#2580B3;--water-light:#3FA0D0;
  --earth:#5C3D1E;--earth-mid:#7A5230;--earth-light:#A06A3A;
  --cream:#F5F8FA;--warm-gray:#7A8A96;--success:#2D7A3A;--success-soft:#D4EDDA;
  --alert:#C0520B;--alert-soft:#FDE8D8;--black:#0D1117;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--cream);color:var(--black);}

.hero-wrap{
  background:linear-gradient(135deg,var(--water-dark) 0%,var(--water) 60%,#1A85C0 100%);
  border-radius:20px;padding:3rem 2.5rem 2rem;margin-bottom:2rem;position:relative;overflow:hidden;
}
.hero-wrap::before{content:"💧";font-size:180px;position:absolute;right:-20px;top:-20px;opacity:0.06;}
.hero-tag{background:#7ECBF5;color:var(--water-dark);font-family:'DM Mono',monospace;font-size:0.7rem;font-weight:bold;letter-spacing:2px;padding:4px 12px;border-radius:4px;display:inline-block;margin-bottom:1rem;text-transform:uppercase;}
.hero-title{font-family:'Playfair Display',serif;font-size:2.8rem;font-weight:900;color:#fff;line-height:1.15;margin-bottom:0.8rem;white-space:pre-line;}
.hero-subtitle{font-size:1rem;color:rgba(255,255,255,0.78);max-width:660px;line-height:1.6;margin-bottom:1.5rem;}
.hero-badges{display:flex;gap:10px;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);color:rgba(255,255,255,0.85);font-size:0.72rem;font-family:'DM Mono',monospace;padding:5px 12px;border-radius:20px;letter-spacing:0.5px;}
.badge-water{background:rgba(126,203,245,0.22);border-color:#7ECBF5;color:#7ECBF5;}

.metric-box{background:white;border-radius:16px;padding:1.4rem 1.2rem;border-top:4px solid var(--water);box-shadow:0 2px 12px rgba(0,0,0,0.06);text-align:center;}
.metric-box.earth{border-top-color:var(--earth-light);}
.metric-box.success{border-top-color:var(--success);}
.metric-val{font-family:'Playfair Display',serif;font-size:2.1rem;font-weight:900;color:var(--water-dark);line-height:1;margin-bottom:0.3rem;}
.metric-label{font-size:0.75rem;color:var(--warm-gray);text-transform:uppercase;letter-spacing:1px;}

.section-label{font-family:'DM Mono',monospace;font-size:0.65rem;color:var(--water-dark);text-transform:uppercase;letter-spacing:3px;margin-bottom:0.3rem;}
.section-title{font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;color:var(--water-dark);margin-bottom:1.2rem;line-height:1.2;}

.info-card{background:white;border-radius:16px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.05);border-left:4px solid var(--water-light);margin-bottom:1rem;}
.info-card.earth{border-left-color:var(--earth-light);}
.info-card.alert{border-left-color:var(--alert);}

.timeline-item{display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #e8f0f5;}
.timeline-year{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--water);min-width:80px;}
.timeline-content{flex:1;}
.timeline-title{font-weight:500;color:var(--water-dark);margin-bottom:0.2rem;}
.timeline-desc{font-size:0.85rem;color:var(--warm-gray);}

.source-badges{display:flex;gap:8px;flex-wrap:wrap;margin-top:0.8rem;}
.source-badge{background:var(--water-dark);color:white;font-family:'DM Mono',monospace;font-size:0.65rem;padding:4px 10px;border-radius:4px;letter-spacing:1px;text-transform:uppercase;}

.method-step{display:flex;align-items:flex-start;gap:1rem;padding:1rem;background:white;border-radius:12px;margin-bottom:0.8rem;box-shadow:0 1px 6px rgba(0,0,0,0.04);}
.step-num{background:var(--water);color:white;font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-content{flex:1;}
.step-title{font-weight:500;color:var(--water-dark);font-size:0.95rem;}
.step-desc{font-size:0.82rem;color:var(--warm-gray);margin-top:0.2rem;}

.discovery-box{background:linear-gradient(135deg,#EFF7FF 0%,#DCF0FF 100%);border:2px solid var(--water-light);border-radius:16px;padding:1.8rem;margin:1rem 0;}
.discovery-title{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--water-dark);margin-bottom:0.5rem;}

.footer-wrap{background:var(--water-dark);border-radius:20px;padding:2rem;color:rgba(255,255,255,0.8);text-align:center;margin-top:3rem;}
.footer-title{font-family:'Playfair Display',serif;color:#7ECBF5;font-size:1.2rem;margin-bottom:0.5rem;}

.photo-placeholder{background:#EFF7FF;border:2px dashed var(--water-mid);border-radius:12px;padding:2rem;text-align:center;min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.photo-emoji{font-size:2.5rem;}
.photo-title{font-weight:600;color:var(--water-dark);margin:0.5rem 0 0.2rem;font-size:0.9rem;}
.photo-desc{font-size:0.78rem;color:var(--warm-gray);line-height:1.5;}
.photo-path{font-size:0.65rem;color:var(--water-mid);font-family:'DM Mono',monospace;margin-top:0.5rem;background:#DCF0FF;padding:3px 8px;border-radius:4px;}
.photo-legenda{font-size:0.72rem;color:var(--warm-gray);font-style:italic;padding:0.5rem 0.8rem;background:#f5f8fa;text-align:center;border-top:1px solid #e0ecf5;}

.photo-destaque{border:3px solid var(--water);border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(26,107,154,0.15);}
.photo-cert{border:3px solid #C09020;border-radius:14px;overflow:hidden;box-shadow:0 4px 20px rgba(192,144,32,0.15);}

.escavador-card{background:linear-gradient(135deg,#FFF8E8,#FFF0C8);border:2px solid #C09020;border-radius:16px;padding:1.5rem;margin-top:1rem;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DADOS HIDROLÓGICOS (simulados — substituir pelos reais)
# ============================================================

meses = ["Ago/16", "Set/16", "Out/16", "Nov/16", "Dez/16",
         "Jan/17", "Fev/17", "Mar/17", "Abr/17", "Mai/17", "Jun/17", "Jul/17"]

# Produção específica de sedimentos simulada (t km⁻² mês⁻¹)
sed_b1 = [0.8, 1.2, 3.4, 4.1, 3.8, 4.5, 3.9, 3.2, 1.1, 0.6, 0.4, 0.3]
sed_b2 = [1.5, 2.1, 6.2, 7.8, 7.1, 8.3, 7.2, 6.0, 2.0, 1.1, 0.7, 0.5]

# Vazão específica simulada (L s⁻¹ km⁻²)
vazao_b1 = [3.2, 4.1, 8.5, 10.2, 9.8, 11.3, 10.1, 8.7, 3.8, 2.1, 1.5, 1.1]
vazao_b2 = [4.8, 6.2, 12.1, 14.5, 13.8, 15.9, 14.2, 12.0, 5.4, 3.0, 2.1, 1.6]

df_sed = pd.DataFrame({
    "mes": meses * 2,
    "bacia": ["Bacia 1 (Pastagem)"] * 12 + ["Bacia 2 (Cana-de-açúcar)"] * 12,
    "sedimentos": sed_b1 + sed_b2,
    "vazao": vazao_b1 + vazao_b2,
})

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
with col1: st.markdown(f'<div class="metric-box"><div class="metric-val">0,71 km²</div><div class="metric-label">{T["m1"]}</div></div>', unsafe_allow_html=True)
with col2: st.markdown(f'<div class="metric-box earth"><div class="metric-val">1,31 km²</div><div class="metric-label">{T["m2"]}</div></div>', unsafe_allow_html=True)
with col3: st.markdown(f'<div class="metric-box success"><div class="metric-val">12</div><div class="metric-label">{T["m3"]}</div></div>', unsafe_allow_html=True)
with col4: st.markdown(f'<div class="metric-box"><div class="metric-val">4</div><div class="metric-label">{T["m4"]}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# ABAS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([T['tab1'], T['tab2'], T['tab3'], T['tab4'], T['tab5']])

# ── TAB 1: MAPA ──────────────────────────────────────────────
with tab1:
    st.markdown(f'<div class="section-label">{T["map_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["map_title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-card">{T["map_hint"]}</div>', unsafe_allow_html=True)

    mapa = folium.Map(location=[-20.179, -50.272], zoom_start=14, tiles='CartoDB positron')

    # Centróides das bacias
    bacias_info = [
        {"nome": "Bacia 1 — Pastagem", "lat": -20.1782, "lon": -50.2762,
         "area": "0,710 km²", "manejo": "Pastagem", "cor": "#E67E22",
         "foz_lat": -20.2895, "foz_lon": -50.2793},
        {"nome": "Bacia 2 — Cana-de-Açúcar", "lat": -20.1839, "lon": -50.2695,
         "area": "1,309 km²", "manejo": "Cana-de-açúcar", "cor": "#1A6B9A",
         "foz_lat": -20.2909, "foz_lon": -50.2740},
    ]

    for b in bacias_info:
        popup_html = f"""<div style='font-family:sans-serif;min-width:220px;padding:10px'>
            <h4 style='color:#0D4E72;margin:0 0 8px'>{b['nome']}</h4>
            <p style='margin:3px 0;font-size:13px'>🗺️ Área: <b>{b['area']}</b></p>
            <p style='margin:3px 0;font-size:13px'>🌱 Manejo: <b>{b['manejo']}</b></p>
            <p style='margin:3px 0;font-size:13px'>📍 Afluente do Ribeirão Santa Rita</p>
            <p style='margin:3px 0;font-size:11px;color:#888'>Fernandópolis – SP</p>
        </div>"""
        folium.CircleMarker(
            location=[b["lat"], b["lon"]], radius=22,
            color=b["cor"], fill=True, fill_color=b["cor"], fill_opacity=0.35,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"🗺️ {b['nome']} · {b['area']}"
        ).add_to(mapa)
        # Ponto de coleta (foz)
        foz_popup = f"""<div style='font-family:sans-serif;padding:8px'>
            <b style='color:#0D4E72'>Ponto de coleta</b><br>
            <span style='font-size:12px'>{b['nome']}</span><br>
            <span style='font-size:11px;color:#888'>Lat: {b['foz_lat']:.4f} | Lon: {b['foz_lon']:.4f}</span>
        </div>"""
        folium.Marker(
            location=[b["foz_lat"], b["foz_lon"]],
            popup=folium.Popup(foz_popup, max_width=220),
            tooltip=f"💧 Foz {b['nome']}",
            icon=folium.Icon(color="blue" if "Cana" in b["nome"] else "orange",
                             icon="tint", prefix="fa")
        ).add_to(mapa)

    # Ribeirão Santa Rita
    folium.PolyLine(
        locations=[[-20.265, -50.285], [-20.285, -50.278], [-20.295, -50.272]],
        color="#1A6B9A", weight=3, opacity=0.7, tooltip="Ribeirão Santa Rita"
    ).add_to(mapa)

    folium_static(mapa, width=1100, height=500)

    # ── Gráficos
    st.markdown(f"<br><div class='section-label'>{T['temporal_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['temporal_title']}</div>", unsafe_allow_html=True)

    # Gráfico de sedimentos lado a lado
    fig_sed = go.Figure()
    fig_sed.add_trace(go.Bar(
        name="Bacia 1 · Pastagem",
        x=meses, y=sed_b1,
        marker_color="#E67E22", opacity=0.85,
        hovertemplate='<b>%{x}</b><br>B1: %{y:.1f} t km⁻²<extra></extra>'
    ))
    fig_sed.add_trace(go.Bar(
        name="Bacia 2 · Cana-de-açúcar",
        x=meses, y=sed_b2,
        marker_color="#1A6B9A", opacity=0.85,
        hovertemplate='<b>%{x}</b><br>B2: %{y:.1f} t km⁻²<extra></extra>'
    ))
    fig_sed.update_layout(
        barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Sans'), height=380,
        xaxis=dict(showgrid=False, tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor='#e0ecf5', title=T['bar_y']),
        title=dict(text=T['bar_title'], font=dict(size=14, family='Playfair Display')),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
        margin=dict(t=60, b=20)
    )
    st.plotly_chart(fig_sed, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        df_vazao_media = pd.DataFrame({
            "Bacia": ["Bacia 1\nPastagem", "Bacia 2\nCana-de-açúcar"],
            "Vazão": [np.mean(vazao_b1), np.mean(vazao_b2)]
        })
        fig_vaz = px.bar(df_vazao_media, x="Bacia", y="Vazão",
                         title=T['prod_title'],
                         color="Bacia",
                         color_discrete_map={"Bacia 1\nPastagem": "#E67E22", "Bacia 2\nCana-de-açúcar": "#1A6B9A"},
                         text="Vazão")
        fig_vaz.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_vaz.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False, height=340, font=dict(family='DM Sans'),
            title=dict(font=dict(size=13, family='Playfair Display')),
            yaxis_title="Vazão específica média (L s⁻¹ km⁻²)", margin=dict(t=50, b=20)
        )
        st.plotly_chart(fig_vaz, use_container_width=True)

    with col_b:
        uso_data = pd.DataFrame({
            "Uso": ["Pastagem (B1)", "Cana-de-açúcar (B2)", "Matas Ciliares", "Outros"],
            "Area": [45, 38, 12, 5]
        })
        fig_pie = px.pie(uso_data, values='Area', names='Uso',
                         title=T['pie_title'],
                         color_discrete_sequence=['#E67E22', '#1A6B9A', '#2D7A3A', '#A0A0A0'])
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=340,
            font=dict(family='DM Sans'),
            title=dict(font=dict(size=13, family='Playfair Display')),
            margin=dict(t=50, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Timeline de monitoramento
    st.markdown(f"<div class='section-label'>{T['timeline_label']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>{T['timeline_title']}</div>", unsafe_allow_html=True)

    bacia_sel = st.selectbox(T['select_basin'],
                             ["Bacia 1 — Pastagem (0,710 km²)", "Bacia 2 — Cana-de-açúcar (1,309 km²)"])
    y_data = vazao_b1 if "1" in bacia_sel else vazao_b2
    cor_sel = "#E67E22" if "1" in bacia_sel else "#1A6B9A"

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=meses, y=y_data,
        mode='lines+markers',
        line=dict(color=cor_sel, width=3),
        marker=dict(size=9, color=cor_sel, line=dict(width=2, color='white')),
        fill='tozeroy', fillcolor=f'rgba({int(cor_sel[1:3],16)},{int(cor_sel[3:5],16)},{int(cor_sel[5:7],16)},0.10)',
        hovertemplate='<b>%{x}</b><br>%{y:.1f} L s⁻¹ km⁻²<extra></extra>'
    ))
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280,
        font=dict(family='DM Sans'),
        xaxis=dict(showgrid=False, tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor='#e0ecf5', title="Vazão específica (L s⁻¹ km⁻²)"),
        title=dict(text=bacia_sel, font=dict(size=13, family='Playfair Display')),
        margin=dict(t=50, b=20)
    )
    st.plotly_chart(fig_line, use_container_width=True)

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

    for num, title, desc in T['steps']:
        st.markdown(f"""
        <div class="method-step">
          <div class="step-num">{num}</div>
          <div class="step-content">
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
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

    # Fórmulas visuais
    st.markdown("""
    <div class="info-card" style="margin-top:1rem;background:linear-gradient(135deg,#EFF7FF,#DCF0FF)">
      <strong style="color:#0D4E72">📐 Equações Fundamentais do Método</strong><br><br>
      <div style="font-family:'DM Mono',monospace;font-size:0.85rem;line-height:2.2;color:#1A6B9A">
        <b>Fator de forma:</b> F = L / [2 · (A/π)^0.5]<br>
        <b>Coef. de forma:</b> C1 = 2 / (1 + F)<br>
        <b>Coef. volumétrico ponderado:</b> C2 = Σ(Ai · Ci) / A<br>
        <b>Coef. de escoamento:</b> C = [2/(1+F)] · (C2/C1)<br>
        <b>Velocidade média:</b> v = 0,85 · (d / t<sub>m</sub>)<br>
        <b>Vazão:</b> Q = v · S<sub>m</sub><br>
        <b>Seção média:</b> S<sub>m</sub> = (S1 + S2 + S3) / 3
      </div>
      <div style="font-size:0.75rem;color:#7A8A96;margin-top:0.5rem">Fonte: Porto (1999) · Carvalho (1994) · Roteiro de Aula — Prof. Dr. L.S. Vanzela</div>
    </div>
    """, unsafe_allow_html=True)

# ── TAB 3: DESCOBERTAS ────────────────────────────────────────
with tab3:
    st.markdown(f'<div class="section-label">{T["discovery_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["discovery_title"]}</div>', unsafe_allow_html=True)

    for emoji, titulo, texto in T['discoveries']:
        st.markdown(f"""
        <div class="discovery-box" style="margin-bottom:0.8rem">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <span style="font-size:1.5rem">{emoji}</span>
            <div>
              <div class="discovery-title">{titulo}</div>
              <p style="color:#1A3A5A;line-height:1.65;font-size:0.93rem;margin:0">{texto}</p>
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

    # Gráfico de impacto comparativo
    fig_impact = go.Figure()
    categorias = ["Produção de sedimentos\nMeses chuvosos",
                  "Produção de sedimentos\nMeses secos",
                  "Vazão específica\nMédia anual",
                  "Condutividade\nElétrica"]
    vals_b1 = [3.8, 0.5, 6.5, 72]
    vals_b2 = [7.1, 0.9, 9.4, 118]

    fig_impact.add_trace(go.Bar(name="B1 · Pastagem", x=categorias, y=vals_b1,
                                 marker_color="#E67E22", opacity=0.85))
    fig_impact.add_trace(go.Bar(name="B2 · Cana-de-açúcar", x=categorias, y=vals_b2,
                                 marker_color="#1A6B9A", opacity=0.85))
    fig_impact.update_layout(
        barmode='group',
        title=dict(text=T['impact_title'], font=dict(size=13, family='Playfair Display')),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=360, font=dict(family='DM Sans'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#e0ecf5'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        margin=dict(t=60, b=20)
    )
    st.plotly_chart(fig_impact, use_container_width=True)

# ── TAB 4: EM CAMPO ───────────────────────────────────────────
with tab4:
    st.markdown(f'<div class="section-label">{T["field_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["field_title"]}</div>', unsafe_allow_html=True)

    # Instrução de como adicionar fotos
    st.markdown(f"""
    <div class="info-card alert" style="margin-bottom:1.5rem">
      <strong>{T['field_instructions_title']}</strong><br>
      <div style="font-size:0.88rem;color:#5C3D1E;margin-top:0.4rem">{T['field_instructions']}</div>
    </div>
    """, unsafe_allow_html=True)

    photos = T['photos']

    # Foto destaque (bancada) — ocupa coluna inteira
    foto_destaque = next((f for f in photos if f.get("destaque")), None)
    foto_cert = next((f for f in photos if f.get("certificado")), None)
    fotos_normais = [f for f in photos if not f.get("destaque") and not f.get("certificado")]

    # Grade 3 colunas para fotos normais
    for row_start in range(0, len(fotos_normais), 3):
        row_photos = fotos_normais[row_start:row_start + 3]
        cols = st.columns(len(row_photos))
        for col, foto in zip(cols, row_photos):
            with col:
                exists = os.path.exists(foto['path'])
                wrapper_class = "photo-cert" if foto.get("certificado") else ""
                if exists:
                    st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
                    st.image(foto['path'], use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
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

    # Foto destaque (bancada) — largura total
    if foto_destaque:
        st.markdown("---")
        st.markdown(f"<div class='section-label'>DESTAQUE — BANCADA DE ANÁLISE</div>", unsafe_allow_html=True)
        exists_dest = os.path.exists(foto_destaque['path'])
        if exists_dest:
            st.markdown('<div class="photo-destaque">', unsafe_allow_html=True)
            st.image(foto_destaque['path'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
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

    # Certificado — seção especial
    if foto_cert:
        st.markdown("---")
        st.markdown(f"<div class='section-label' style='color:#C09020'>CERTIFICADO DE APRESENTAÇÃO CIENTÍFICA</div>", unsafe_allow_html=True)
        col_cert, col_cert_text = st.columns([1, 1])
        with col_cert:
            exists_cert = os.path.exists(foto_cert['path'])
            if exists_cert:
                st.image(foto_cert['path'], use_container_width=True)
            else:
                # Tenta carregar o PDF do certificado original
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
            st.markdown("""
            <div style="padding:1rem">
              <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:#8A6010;margin-bottom:1rem">
                Reconhecimento Científico Oficial
              </div>
              <div style="font-size:0.9rem;line-height:1.8;color:#5C3D1E">
                <p>O trabalho <strong>\"Vazão e Sedimentos em Bacias Hidrográficas de Diferentes Manejos e Escoamento Superficial\"</strong> foi apresentado e aprovado no:</p>
                <p>🏛️ <strong>XI Encontro de Iniciação Científica</strong><br>Universidade Brasil — São Paulo, SP</p>
                <p>📅 <strong>20 de Outubro de 2017</strong></p>
                <p>👥 <strong>Autores:</strong><br>Amauri Almeida de Souza Junior<br>Prof. Dr. Luiz S. Vanzela</p>
                <p>✍️ <strong>Banca:</strong><br>
                   Prof. Dr. Daniel Souza F. Magalhães<br>
                   Prof. Dr. Marcello Magri Amaral<br>
                   Prof. Dr. Ricardo Scarparo Navarro
                </p>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Timeline de campo
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-label'>{T['timeline_field_label']}</div>", unsafe_allow_html=True)
    for data, titulo, desc in T['timeline_field_items']:
        st.markdown(f"""
        <div class="timeline-item">
          <div class="timeline-year">{data}</div>
          <div class="timeline-content">
            <div class="timeline-title">{titulo}</div>
            <div class="timeline-desc">{desc}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ── TAB 5: FONTES ─────────────────────────────────────────────
with tab5:
    st.markdown(f'<div class="section-label">{T["sources_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{T["sources_title"]}</div>', unsafe_allow_html=True)

    fontes = [
        ("UNICASTELO", "Universidade Camilo Castelo Branco — Fernandópolis, SP",
         "Projeto de IC: Influência do Manejo de Bacias sobre o Transporte de Sedimentos (2015–2017). Orientador: Prof. Dr. Luiz Sergio Vanzela.", "#0D4E72"),
        ("CNPQ/LATTES", "Prof. Dr. Luiz Sergio Vanzela — Currículo Lattes",
         "http://lattes.cnpq.br/0284046584743018 · Responsável técnico e orientador da pesquisa.", "#1A6B9A"),
        ("ESCAVADOR", "Escavador — Base de Pesquisadores Brasileiros",
         "Vínculo acadêmico entre Amauri Almeida de Souza Junior e Prof. Dr. Luiz Sergio Vanzela documentado na plataforma.", "#2580B3"),
        ("VANZELA et al.", "Vanzela, L.S.; Hernandez, F.B.T.; Franco, R.A.M. (2010)",
         "Influência do uso e ocupação do solo nos recursos hídricos do Córrego Três Barras. Rev. Bras. Eng. Agrícola e Ambiental, v.14, n.1, pp.55–64.", "#3FA0D0"),
        ("PORTO (1999)", "Porto, R. de M. — Hidráulica Básica",
         "2ª ed. São Carlos: EESC-USP, 1999. 519p. Referência principal para o método do flutuador integrador.", "#0D4E72"),
        ("BERTONI & LOMBARDI", "Bertoni, J.; Lombardi Neto, F. — Conservação do Solo",
         "4ª ed. São Paulo: Ícone, 1999. 355p. Referência para erosão e transporte de sedimentos.", "#1A6B9A"),
        ("NASA/ASTER", "NASA — ASTER Digital Elevation Model (2010)",
         "Modelo de elevação do terreno com resolução espacial de 30 m, utilizado para cálculo da declividade média das bacias.", "#2580B3"),
        ("IBGE", "Instituto Brasileiro de Geografia e Estatística",
         "Dados de localização, área e características das bacias hidrográficas de Fernandópolis – SP.", "#3FA0D0"),
        ("SILVA et al. (2005)", "Silva, D.D.; Pruski, F.F.; et al.",
         "Efeito da cobertura nas perdas de solo em um Argissolo Vermelho-Amarelo. Engenharia Agrícola, v.25, n.2, p.409–419, 2005.", "#0D4E72"),
    ]

    for sigla, nome, desc, cor in fontes:
        st.markdown(f"""
        <div class="info-card" style="border-left-color:{cor}">
          <div style="display:flex;align-items:flex-start;gap:1rem">
            <div style="background:{cor};color:white;font-family:'DM Mono',monospace;font-size:0.6rem;
                 padding:4px 7px;border-radius:4px;white-space:nowrap;flex-shrink:0;margin-top:2px;
                 letter-spacing:0.5px;font-weight:bold;max-width:120px;text-align:center">{sigla}</div>
            <div>
              <div style="font-weight:500;font-size:0.9rem;color:#0D4E72">{nome}</div>
              <div style="font-size:0.82rem;color:#7A8A96;margin-top:0.2rem">{desc}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Escavador card
    st.markdown(f"""
    <div class="escavador-card">
      <strong style="color:#8A6010">{T['escavador_label']}</strong><br>
      <p style="font-size:0.88rem;color:#5C3D1E;margin-top:0.5rem">{T['escavador_text']}</p>
      <a href="https://www.escavador.com/sobre/403010308/amauri-almeida-de-souza-junior"
         target="_blank"
         style="background:#C09020;color:white;padding:6px 16px;border-radius:6px;
                text-decoration:none;font-size:0.82rem;font-family:'DM Mono',monospace">
        🔗 Ver perfil no Escavador →
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
        🌐 <a href="https://amaurialmeida.github.io/environmental-portfolio/" style="color:#7ECBF5">Portfólio</a> &nbsp;|&nbsp;
        🐙 <a href="https://github.com/amaurialmeida" style="color:#7ECBF5">GitHub</a> &nbsp;|&nbsp;
        🔗 <a href="https://www.escavador.com/sobre/8577779/amauri-almeida-de-souza-junior" style="color:#7ECBF5">Escavador</a>
      </p>
      <p style="font-size:0.75rem;opacity:0.5;margin:0">© 2026 · Observatório do Ribeirão Santa Rita · Pesquisa Acadêmica · UNICASTELO</p>
    </div>
    """, unsafe_allow_html=True)
