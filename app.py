import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Real Madrid",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Custom
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #F0F0EE;
        border-radius: 8px 8px 0 0;
        padding: 8px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1A1A2E !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Paleta de colores
BLANCO  = "#F5F5F5"
ORO     = "#C9A84C"
AZUL_RM = "#1A1A2E"
ROJO    = "#C81D25"
VERDE   = "#1D9E75"
GRIS    = "#B4B2A9"

# CONFIGURACIÓN BASE INMUTABLE
LAYOUT_BASE = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20, r=20, t=40, b=40),
    font=dict(family="Arial, sans-serif"),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#E2E8F0"),
)

@st.cache_data
def cargar():
    return pd.read_csv('real_madrid.csv')

df = cargar()
sin = df[df['mbappe'] == 'No']
con = df[df['mbappe'] == 'Si']

def color_mbappe(df_col, color_con=ORO, color_sin=GRIS):
    return [color_sin if m == 'No' else color_con for m in df_col]

# ── PREGUNTA CENTRAL ───────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{AZUL_RM}; border-radius:12px; padding:1.5rem 2rem; margin-bottom:1rem;">
    <p style="color:{GRIS}; font-size:0.8rem; margin:0 0 0.3rem 0;
              text-transform:uppercase; letter-spacing:2px;">Proyecto · Visualización de Datos</p>
    <p style="color:{BLANCO}; font-size:1.4rem; font-weight:800; margin:0 0 0.3rem 0;">
        ¿El Real Madrid solucionó el problema correcto al fichar a Mbappé?
    </p>
    <p style="color:{ORO}; font-size:0.95rem; margin:0;">
        Análisis comparativo · LaLiga & Champions League · Temporadas 2022-23 a 2025-26
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📋  Contexto",
    "⚽  ¿Había problema de gol?",
    "📉  Lo que pasó después",
    "🏆  El veredicto"
])

# ==========================================================================
# TAB 1 — CONTEXTO
# ==========================================================================
with tab1:
    st.subheader("El Madrid antes de Mbappé")
    st.caption("2022-23 y 2023-24 — el equipo que recibió al francés")
    st.divider()

    st.markdown(f"""
<div style="background:#F0FFF4; border-left:4px solid {VERDE};
            border-radius:6px; padding:1.2rem 1.5rem; margin-bottom:1.5rem;">
    <p style="color:#276749; font-weight:800; font-size:1rem; margin:0 0 0.4rem 0;">
        Necesidad percibida por el club
    </p>
    <p style="color:#1A202C; font-size:0.92rem; margin:0; line-height:1.7;">
        Tras ganar LaLiga 2023-24 con <strong>95 puntos</strong> y la <strong>Champions League</strong>,
        el Real Madrid creía que añadir al mejor delantero del mundo los llevaría al siguiente nivel.
        La lógica era simple: más gol = más títulos. ¿Pero era el gol realmente su problema?
    </p>
</div>
""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("LaLiga 2022-23", "78 pts", "2do lugar")
    c2.metric("LaLiga 2023-24", "95 pts", "Campeón")
    c3.metric("Champions 2022-23", "Semifinal", "Eliminado por Man City")
    c4.metric("Champions 2023-24", "Campeón", "15vo título europeo")

    st.divider()

    # --- LALIGA CONTEXTO ---
    st.markdown("### LaLiga — Evolución del Rendimiento")
    
    st.markdown("#### Puntos en LaLiga")
    fig_pts = go.Figure(go.Bar(
        x=sin['temporada'], y=sin['liga_puntos'],
        marker_color=[GRIS, ORO], text=sin['liga_puntos'],
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>%{y} puntos<extra></extra>"
    ))
    fig_pts.update_layout(LAYOUT_BASE)
    fig_pts.update_layout(height=280)
    st.plotly_chart(fig_pts, use_container_width=True)
    st.caption("El pico de 95 puntos muestra un equipo que ya rozaba la excelencia en el torneo doméstico.")

    st.markdown("#### Resultados en LaLiga (V / E / D)")
    fig_res = go.Figure()
    fig_res.add_trace(go.Bar(
        name='Victorias', x=sin['temporada'], y=sin['liga_victorias'],
        marker_color=VERDE, text=sin['liga_victorias'], textposition='inside', textfont_color='white'
    ))
    fig_res.add_trace(go.Bar(
        name='Empates', x=sin['temporada'], y=sin['liga_empates'],
        marker_color=ORO, text=sin['liga_empates'], textposition='inside'
    ))
    fig_res.add_trace(go.Bar(
        name='Derrotas', x=sin['temporada'], y=sin['liga_derrotas'],
        marker_color=ROJO, text=sin['liga_derrotas'], textposition='inside', textfont_color='white'
    ))
    fig_res.update_layout(LAYOUT_BASE)
    fig_res.update_layout(barmode='stack', height=280, yaxis=dict(range=[0, 42]), legend=dict(orientation="h", y=1.12))
    st.plotly_chart(fig_res, use_container_width=True)
    st.caption("La consistencia competitiva: una única derrota en toda la campaña 2023-24.")

    st.divider()

    # COMPARATIVA DIRECTA: Goles anotados vs Goles encajados (LADO A LADO)
    st.markdown("### LaLiga — Balance de Goles (Comparativo)")
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("#### Goles anotados (LaLiga)")
        fig_gf = go.Figure(go.Bar(
            x=sin['temporada'], y=sin['liga_goles_a_favor'], marker_color=[GRIS, ORO],
            text=sin['liga_goles_a_favor'], textposition='outside'
        ))
        fig_gf.add_hline(y=sin['liga_goles_a_favor'].mean(), line_dash="dash", line_color=VERDE,
                         annotation_text=f"Promedio: {sin['liga_goles_a_favor'].mean():.0f}")
        fig_gf.update_layout(LAYOUT_BASE)
        fig_gf.update_layout(height=300, yaxis=dict(range=[0, 105], title="Goles"))
        st.plotly_chart(fig_gf, use_container_width=True)

    with col_d:
        st.markdown("#### Goles encajados (LaLiga)")
        fig_gc = go.Figure(go.Bar(
            x=sin['temporada'], y=sin['liga_goles_en_contra'], marker_color=[GRIS, ORO],
            text=sin['liga_goles_en_contra'], textposition='outside'
        ))
        fig_gc.add_hline(y=sin['liga_goles_en_contra'].mean(), line_dash="dash", line_color=VERDE,
                         annotation_text=f"Promedio: {sin['liga_goles_en_contra'].mean():.0f}")
        fig_gc.update_layout(LAYOUT_BASE)
        fig_gc.update_layout(height=300, yaxis=dict(range=[0, 105], title="Goles"))
        st.plotly_chart(fig_gc, use_container_width=True)

    st.caption("Nótese cómo el título de la 2023-24 se cimentó en una defensa histórica (solo 26 goles en contra), no en un aumento drástico de goles a favor.")
    st.divider()

    # --- CHAMPIONS CONTEXTO ---
    st.markdown("### Champions League — Balance de Goles (Comparativo)")
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown("#### Goles anotados (Champions)")
        fig_ucl_gf = go.Figure(go.Bar(
            x=sin['temporada'], y=sin['ucl_goles_a_favor'], marker_color=[GRIS, ORO],
            text=sin['ucl_goles_a_favor'], textposition='outside'
        ))
        fig_ucl_gf.add_hline(y=sin['ucl_goles_a_favor'].mean(), line_dash="dash", line_color=VERDE,
                              annotation_text=f"Promedio: {sin['ucl_goles_a_favor'].mean():.0f}")
        fig_ucl_gf.update_layout(LAYOUT_BASE)
        fig_ucl_gf.update_layout(height=300, yaxis=dict(range=[0, 35], title="Goles"))
        st.plotly_chart(fig_ucl_gf, use_container_width=True)

    with col_f:
        st.markdown("#### Goles encajados (Champions)")
        fig_ucl_gc = go.Figure(go.Bar(
            x=sin['temporada'], y=sin['ucl_goles_en_contra'], marker_color=[GRIS, ORO],
            text=sin['ucl_goles_en_contra'], textposition='outside'
        ))
        fig_ucl_gc.add_hline(y=sin['ucl_goles_en_contra'].mean(), line_dash="dash", line_color=VERDE,
                              annotation_text=f"Promedio: {sin['ucl_goles_en_contra'].mean():.0f}")
        fig_ucl_gc.update_layout(LAYOUT_BASE)
        fig_ucl_gc.update_layout(height=300, yaxis=dict(range=[0, 35], title="Goles"))
        st.plotly_chart(fig_ucl_gc, use_container_width=True)


# ==========================================================================
# TAB 2 — ¿HABÍA PROBLEMA DE GOL?
# ==========================================================================
with tab2:
    st.subheader("¿El Real Madrid tenía un problema de gol?")
    st.caption("La hipótesis que justificó el fichaje — vs. la realidad de los datos")
    st.divider()

    st.markdown("### Volumen ofensivo histórico y actual")
    
    st.markdown("#### LaLiga — Goles anotados")
    col = color_mbappe(df['mbappe'])
    fig1 = go.Figure(go.Bar(
        x=df['temporada'], y=df['liga_goles_a_favor'], marker_color=col,
        text=df['liga_goles_a_favor'], textposition='outside'
    ))
    fig1.add_hline(y=sin['liga_goles_a_favor'].mean(), line_dash="dash", line_color=VERDE,
                   annotation_text=f"Promedio sin Mbappé: {sin['liga_goles_a_favor'].mean():.0f}")
    fig1.update_layout(LAYOUT_BASE)
    fig1.update_layout(height=280, yaxis=dict(range=[0, 105], title="Goles"), showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)
    st.caption("La producción de goles en liga se mantiene estable; la llegada del francés no disparó el poder de cara al arco.")

    st.markdown("#### Champions — Goles anotados")
    fig2 = go.Figure(go.Bar(
        x=df['temporada'], y=df['ucl_goles_a_favor'], marker_color=color_mbappe(df['mbappe']),
        text=df['ucl_goles_a_favor'], textposition='outside'
    ))
    fig2.add_hline(y=sin['ucl_goles_a_favor'].mean(), line_dash="dash", line_color=VERDE,
                   annotation_text=f"Promedio sin Mbappé: {sin['ucl_goles_a_favor'].mean():.0f}")
    fig2.update_layout(LAYOUT_BASE)
    fig2.update_layout(height=280, yaxis=dict(range=[0, 40], title="Goles"), showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Incluso con la adición de una estrella mundial, la efectividad total en Europa se ha quedado por debajo del promedio previo.")

    st.caption("🟡 Temporadas con Mbappé  |  Gris: sin Mbappé")
    st.divider()

    avg_liga_sin = sin['liga_goles_a_favor'].mean()
    avg_liga_con = con['liga_goles_a_favor'].mean()
    avg_ucl_sin  = sin['ucl_goles_a_favor'].mean()
    avg_ucl_con  = con['ucl_goles_a_favor'].mean()

    st.markdown(f"""
<div style="background:{AZUL_RM}; border-radius:10px; padding:1.5rem 2rem;">
    <p style="color:{ORO}; font-weight:800; font-size:1rem; margin:0 0 0.6rem 0;">
        Lo que dicen los números
    </p>
    <p style="color:{BLANCO}; font-size:0.95rem; margin:0; line-height:1.8;">
        Sin Mbappé el Madrid promediaba <strong style="color:{ORO};">{avg_liga_sin:.0f} goles en LaLiga</strong>
        y <strong style="color:{ORO};">{avg_ucl_sin:.0f} en Champions</strong> por temporada.<br>
        Con Mbappé promedia <strong style="color:{ROJO};">{avg_liga_con:.0f} en LaLiga</strong>
        y <strong style="color:{ROJO};">{avg_ucl_con:.0f} en Champions</strong>.<br><br>
        <strong style="color:{BLANCO};">El Madrid no tenía un problema de gol.
        Tenía la mejor temporada de su historia justo antes de ficharlo.
        El fichaje fue la respuesta a una pregunta que nadie había formulado.</strong>
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================================================
# TAB 3 — LO QUE PASÓ DESPUÉS
# ==========================================================================
# ==========================================================================
# TAB 3 — LO QUE PASÓ DESPUÉS
# ==========================================================================
with tab3:
    st.subheader("Lo que cambió con Mbappé")
    st.caption("Goles encajados y rendimiento en la Champions League")
    st.divider()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Goles encajados/partido LaLiga sin Mbappé", f"{sin['liga_goles_en_contra'].mean()/38:.2f}", "promedio 2022-2024")
    k2.metric("Goles encajados/partido LaLiga con Mbappé", f"{con['liga_goles_en_contra'].mean()/38:.2f}",
              f"+{con['liga_goles_en_contra'].mean()/38 - sin['liga_goles_en_contra'].mean()/38:.2f} por partido", delta_color="inverse")
    k3.metric("Champions sin Mbappé", "1 título", "Final + Semifinal")
    k4.metric("Champions con Mbappé", "0 títulos", "Cuartos + Cuartos", delta_color="inverse")

    st.divider()
    
    # Goles encajados uno encima del otro (LaLiga arriba, Champions abajo)
    st.markdown("### El Impacto Negativo — Goles Encajados por Competición")
    
    st.markdown("#### Goles encajados en LaLiga")
    col_e = color_mbappe(df['mbappe'], color_con=ROJO)
    fig_enc = go.Figure(go.Bar(
        x=df['temporada'], y=df['liga_goles_en_contra'], marker_color=col_e,
        text=df['liga_goles_en_contra'], textposition='outside'
    ))
    fig_enc.add_hline(y=sin['liga_goles_en_contra'].mean(), line_dash="dash", line_color=VERDE,
                      annotation_text=f"Promedio sin Mbappé: {sin['liga_goles_en_contra'].mean():.0f}")
    fig_enc.add_annotation(
        x='2024-25', y=37, text="<b>+43% vs temporada<br>campeona 2023-24</b>",
        showarrow=True, arrowhead=2, arrowcolor=ROJO, ax=60, ay=-50, font=dict(color=ROJO, size=10),
        bgcolor="#FFF5F5", bordercolor=ROJO, borderwidth=1
    )
    fig_enc.update_layout(LAYOUT_BASE)
    fig_enc.update_layout(height=280, yaxis=dict(range=[0, 50], title="Goles encajados"), showlegend=False)
    st.plotly_chart(fig_enc, use_container_width=True)
    st.caption("Aumento drástico en la cantidad de goles recibidos localmente tras la reestructuración del ataque.")

    st.markdown("#### Goles encajados en Champions")
    fig_ucl_enc = go.Figure(go.Bar(
        x=df['temporada'], y=df['ucl_goles_en_contra'], marker_color=color_mbappe(df['mbappe'], color_con=ROJO),
        text=df['ucl_goles_en_contra'], textposition='outside'
    ))
    fig_ucl_enc.add_hline(y=sin['ucl_goles_en_contra'].mean(), line_dash="dash", line_color=VERDE,
                          annotation_text=f"Promedio sin Mbappé: {sin['ucl_goles_en_contra'].mean():.0f}")
    fig_ucl_enc.update_layout(LAYOUT_BASE)
    fig_ucl_enc.update_layout(height=280, yaxis=dict(range=[0, 28], title="Goles encajados"), showlegend=False)
    st.plotly_chart(fig_ucl_enc, use_container_width=True)
    st.caption("La vulnerabilidad también se trasladó a Europa, superando sistemáticamente los registros defensivos previos.")

    st.caption("🔴 Temporadas con Mbappé  |  Gris: sin Mbappé")
    st.divider()

    # MÉTRICAS COMPLEMENTARIAS
    st.markdown("### Métricas de Diagnóstico Complementarias")
    
    st.markdown("#### Champions — Fase alcanzada")
    
    fases_orden = {'Octavos': 1, 'Cuartos': 2, 'Semifinal': 3, 'Final': 4, 'Campeon': 5}
    semaforo = {1: '#C81D25', 2: '#E07B39', 3: '#F5C518', 4: '#1D9E75', 5: '#155E3B'}
    
    fases_corregidas = []
    for idx, fila in df.iterrows():
        if str(fila['ucl_titulo']).strip().lower() == 'si':
            fases_corregidas.append('Campeon')
        else:
            fases_corregidas.append(fila['ucl_fase'])
            
    df['fase_limpia'] = fases_corregidas
    df['fase_num'] = df['fase_limpia'].map(fases_orden)
    
    col_cl = [semaforo[v] for v in df['fase_num']]
    fig_cl = go.Figure(go.Bar(
        x=df['temporada'], y=df['fase_num'], marker_color=col_cl,
        text=df['fase_limpia'].replace('Campeon', 'Campeón'), textposition='outside'
    ))
    fig_cl.update_layout(LAYOUT_BASE)
    fig_cl.update_layout(
        yaxis=dict(tickvals=[1, 2, 3, 4, 5], ticktext=['Octavos', 'Cuartos', 'Semifinal', 'Final', 'Campeón'], range=[0, 6.5]),
        height=280, showlegend=False
    )
    st.plotly_chart(fig_cl, use_container_width=True)
    st.caption("Caída en el techo competitivo europeo: el club pasó de levantar la copa en 2023-24 a estancarse en Cuartos de Final.")

    st.divider()

    # NUEVO TEXTO DE CIERRE REQUERIDO (Sustituye la gráfica eliminada)
    st.markdown(f"""
    <div style="background:#FFF5F5; border-left:4px solid {ROJO}; border-radius:6px; padding:1.2rem 1.5rem; margin-top:1rem;">
        <p style="color:{ROJO}; font-weight:800; font-size:1.05rem; margin:0 0 0.5rem 0;">
            Diagnóstico Táctico: El "Efecto Mariposa" del Fichaje Galáctico
        </p>
        <p style="color:#1A202C; font-size:0.92rem; margin:0; line-height:1.7;">
            <strong>El problema del Real Madrid actual no es de efectividad individual, sino de estructura colectiva.</strong><br><br>
            La incorporación de una pieza de alto volumen ofensivo que exige libertad posicional fracturó el bloque de presión media y baja que hizo al equipo campeón en la 2023-24. El aumento drástico de goles encajados (tanto en LaLiga como en Champions) demuestra que el equipo sacrificó el equilibrio defensivo por una acumulación de talento en ataque que, irónicamente, no generó más goles netos. El sistema se volvió predecible y frágil.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================================
# TAB 4 — EL VEREDICTO
# ==========================================================================
with tab4:
    st.subheader("El veredicto")
    st.caption("Contexto → Necesidad → Problema → Solución")
    st.divider()

    st.markdown("### Resumen comparativo — las 4 temporadas")
    df_show = df[[
        'temporada','liga_goles_a_favor','liga_goles_en_contra','liga_puntos',
        'liga_posicion','liga_titulo',
        'ucl_goles_a_favor','ucl_goles_en_contra','ucl_partidos',
        'ucl_fase','ucl_eliminado_por','ucl_titulo','mbappe'
    ]].copy()
    df_show.columns = [
        'Temporada','Liga GF','Liga GC','Puntos','Pos.',
        'Título Liga','UCL GF','UCL GC','UCL Partidos',
        'UCL Fase','Eliminado por','Título UCL','Mbappé'
    ]
    st.dataframe(df_show, use_container_width=True, hide_index=True)
    
    st.divider()

    avg_pts_sin  = sin['liga_puntos'].mean()
    avg_pts_con  = con['liga_puntos'].mean()
    avg_enc_sin  = sin['liga_goles_en_contra'].mean()
    avg_enc_con  = con['liga_goles_en_contra'].mean()
    avg_ucl_enc_sin = sin['ucl_goles_en_contra'].mean()
    avg_ucl_enc_con = con['ucl_goles_en_contra'].mean()

    st.markdown(f"""
<div style="background:{AZUL_RM}; border-radius:12px; padding:2rem 2.5rem; margin-bottom:1.5rem;">
    <p style="color:{ORO}; font-size:1.3rem; font-weight:800; margin:0 0 1rem 0;">
        Conclusión: El Real Madrid no solucionó el problema correcto.
    </p>
    <p style="color:#FFFFFF; font-size:1rem; line-height:1.9; margin:0;">
        <strong style="color:{ORO};">1. Contexto inicial:</strong>
        El Madrid llegó a 2024 en la cúspide del fútbol mundial: campeón de Liga con 95 puntos y dueño de una Champions League invicta. El ecosistema táctico funcionaba de memoria.<br><br>
        <strong style="color:{ORO};">2. El error de diagnóstico:</strong>
        La directiva asumió que añadir la pieza individual más cotizada del mercado resolvería el techo goleador del equipo. Sin embargo, el equipo ya promediaba {sin['liga_goles_a_favor'].mean():.0f} goles por torneo. No faltaban goles.<br><br>
        <strong style="color:{ROJO};">3. El desajuste estructural:</strong>
        Los datos evidencian que el verdadero impacto del cambio se sufrió en la fase de contención. Los goles recibidos en LaLiga se dispararon de {avg_enc_sin:.0f} a {avg_enc_con:.0f} anuales, mientras que el ritmo en Europa bajó el listón, sufriendo eliminaciones tempranas en Cuartos de Final.<br><br>
        <strong style="color:{BLANCO};">Veredictos Final:</strong> El fútbol es un deporte de equilibrios y balance, no de acumulación de nombres. Mbappé fue una solución estelar para un problema ofensivo inexistente, cuyo costo indirecto fue fracturar la solidez defensiva y colectiva que hacía al Real Madrid un equipo imbatible.
    </p>
</div>
""", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown(f"""
<div style="background:#F0FFF4; border-left:4px solid {VERDE};
            border-radius:6px; padding:1.2rem 1.5rem;">
    <p style="color:#276749; font-weight:800; font-size:0.95rem; margin:0 0 0.4rem 0;">
        Balance estadístico de la era previa (2022-24)
    </p>
    <p style="color:#1A202C; font-size:0.88rem; margin:0; line-height:1.6;">
        • <b>Títulos mayores:</b> 1 Champions League, 1 LaLiga.<br>
        • <b>Rendimiento regular:</b> {avg_pts_sin:.0f} puntos promedio en Liga.<br>
        • <b>Solidez atrás:</b> Solo {avg_enc_sin:.0f} goles en contra en el año del doblete.
    </p>
</div>
""", unsafe_allow_html=True)

    with col_r2:
        st.markdown(f"""
<div style="background:#FFF5F5; border-left:4px solid {ROJO};
            border-radius:6px; padding:1.2rem 1.5rem;">
    <p style="color:{ROJO}; font-weight:800; font-size:0.95rem; margin:0 0 0.4rem 0;">
        Lección de Ciencia de Datos aplicada al Deporte
    </p>
    <p style="color:#1A202C; font-size:0.88rem; margin:0; line-height:1.6;">
        Optimizar un indicador que ya está sano (goles a favor) a expensas de descuidar la métrica crítica del éxito anterior (goles en contra) debilita el sistema entero. 
        <strong>Los datos demuestran que el bloque colectivo superaba la suma de sus individualidades.</strong>
    </p>
</div>
""", unsafe_allow_html=True)
