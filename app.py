import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Real Madrid & Mbappe",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

BLANCO  = "#F5F5F5"
ORO     = "#C9A84C"
AZUL_RM = "#1A1A2E"
ROJO    = "#C81D25"
VERDE   = "#1D9E75"
GRIS    = "#B4B2A9"

@st.cache_data
def cargar():
    return pd.read_csv('real_madrid.csv')

df = cargar()
sin = df[df['mbappe'] == 'No']
con = df[df['mbappe'] == 'Si']

# Datos dinámicos temporadas antes de Mbappé

antes = (
    df[df['mbappe'] == 'No']
    .sort_values('temporada')
    .copy()
)

temporadas_antes = antes['temporada'].tolist()

puntos_antes = antes['liga_puntos'].tolist()

goles_contra_antes = antes['liga_goles_en_contra'].tolist()

fases_map = {
    'Octavos': 1,
    'Cuartos': 2,
    'Semifinal': 3,
    'Final': 4,
    'Campeon': 5
}

fases_antes = antes['ucl_fase'].map(fases_map)

textos_fase = antes['ucl_fase']

# ── PREGUNTA CENTRAL ───────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{AZUL_RM}; border-radius:12px; padding:1.5rem 2rem; margin-bottom:1rem;">
    <p style="color:{GRIS}; font-size:0.8rem; margin:0 0 0.3rem 0;
              text-transform:uppercase; letter-spacing:2px;">Proyecto · Visualizacion de Datos</p>
    <p style="color:{BLANCO}; font-size:1.4rem; font-weight:800; margin:0 0 0.3rem 0;">
        ¿El Real Madrid solucionó el problema correcto al fichar a Mbappé?
    </p>
    <p style="color:{ORO}; font-size:0.95rem; margin:0;">
        Analisis comparativo · LaLiga & Champions League · Temporadas 2022-23 a 2025-26
    </p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📋  Contexto",
    "⚽  ¿Habia problema de gol?",
    "📉  Lo que paso despues",
    "🏆  El veredicto"
])

# ══════════════════════════════════════════════════════════════════════════
# TAB 1 — CONTEXTO
# ══════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("El Madrid antes de Mbappe")
    st.caption("2022-23 y 2023-24 — el equipo que recibio al frances")
    st.divider()

    st.markdown(f"""
<div style="background:#F0FFF4; border-left:4px solid {VERDE};
            border-radius:6px; padding:1.2rem 1.5rem; margin-bottom:1.5rem;">
    <p style="color:#276749; font-weight:800; font-size:1rem; margin:0 0 0.4rem 0;">
        Necesidad percibida por el club
    </p>
    <p style="color:#1A202C; font-size:0.92rem; margin:0; line-height:1.7;">
        Tras ganar LaLiga 2023-24 con <strong>95 puntos</strong> y la <strong>Champions League</strong>,
        el Real Madrid creia que anadir al mejor delantero del mundo los llevaria al siguiente nivel.
        La logica era simple: mas gol = mas titulos. ¿Pero era el gol realmente su problema?
    </p>
</div>
""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("LaLiga 2022-23", "78 pts", "2do lugar")
    c2.metric("LaLiga 2023-24", "95 pts", "Campeon")
    c3.metric("Champions 2022-23", "Semifinal", "Eliminado por Man City")
    c4.metric("Champions 2023-24", "Campeon", "15vo titulo europeo")

    st.divider()
    st.markdown("### Comparativa LaLiga y Champions — antes del fichaje")

    st.markdown("### ¿Qué tan bueno era el Madrid antes de Mbappé?")

    col1, col2 = st.columns(2)
    
    with col1:
    
        st.markdown("#### Rendimiento en LaLiga")
    
        fig_pts = go.Figure()
    
        fig_pts.add_trace(go.Bar(
            x=temporadas_antes,
            y=puntos_antes,
            marker_color=[GRIS, ORO],
            text=puntos_antes,
            textposition="outside"
        ))
    
        fig_pts.update_layout(
            yaxis=dict(
                title="Puntos",
                range=[0,110],
                gridcolor="#E2E8F0"
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            height=320
        )
    
        st.plotly_chart(fig_pts, use_container_width=True)
    
        st.caption(
            "El Madrid pasó de 78 a 95 puntos y conquistó LaLiga."
        )
    
    with col2:
    
        st.markdown("#### Solidez defensiva")
    
        fig_gc = go.Figure()
    
        fig_gc.add_trace(go.Bar(
            x=temporadas_antes,
            y=goles_contra_antes,
            marker_color=[GRIS, VERDE],
            text=goles_contra_antes,
            textposition="outside"
        ))
    
        fig_gc.update_layout(
            yaxis=dict(
                title="Goles encajados",
                range=[0,45],
                gridcolor="#E2E8F0"
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            height=320
        )
    
        st.plotly_chart(fig_gc, use_container_width=True)
    
        st.caption(
            "La defensa mejoró considerablemente en la temporada campeona."
        )
    
    st.divider()
    
    st.markdown("#### Rendimiento en Champions League")
    
    fig_ucl = go.Figure()
    
    fig_ucl.add_trace(go.Bar(
        x=temporadas_antes,
        y=fases_antes,
        marker_color=[GRIS, ORO],
        text=textos_fase,
        textposition="outside"
    ))
    
    fig_ucl.update_layout(
        yaxis=dict(
            tickvals=[1,2,3,4,5],
            ticktext=[
                "Octavos",
                "Cuartos",
                "Semifinal",
                "Final",
                "Campeón"
            ],
            range=[0,6]
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        height=350
    )

    st.plotly_chart(fig_ucl, use_container_width=True)
    st.markdown(f"""
<div style="background:#FFFAF0; border-left:4px solid {ORO};
            border-radius:6px; padding:1rem 1.5rem;">
    <p style="color:#744210; font-size:0.9rem; margin:0; line-height:1.7;">
        <strong>Lectura:</strong> En 2023-24 el Madrid fue casi perfecto — 1 sola derrota en LaLiga,
        13 partidos invicto en Champions ganando la final. La pregunta que nadie hizo fue:
        <em>¿que problema habia que resolver?</em>
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# TAB 2 — ¿HABIA PROBLEMA DE GOL?
# ══════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("¿El Madrid tenia un problema de gol?")
    st.caption("La hipotesis que justificó el fichaje — vs. la realidad de los datos")
    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### LaLiga — Goles anotados")
        col = [GRIS if m == 'No' else ORO for m in df['mbappe']]
        fig1 = go.Figure(go.Bar(
            x=df['temporada'], y=df['liga_goles_a_favor'],
            marker_color=col, text=df['liga_goles_a_favor'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles<extra></extra>"
        ))
        fig1.add_hline(y=sin['liga_goles_a_favor'].mean(), line_dash="dash",
                       line_color=VERDE, line_width=2,
                       annotation_text=f"Promedio sin Mbappe: {sin['liga_goles_a_favor'].mean():.0f}",
                       annotation_font_color=VERDE, annotation_position="top left")
        fig1.update_layout(xaxis=dict(showgrid=False),
                           yaxis=dict(range=[0,105], showgrid=True, gridcolor="#E2E8F0",
                                      title="Goles"),
                           plot_bgcolor="white", paper_bgcolor="white",
                           height=320, showlegend=False, margin=dict(l=20,r=20,t=20,b=30))
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown("#### Champions — Goles anotados")
        col2 = [GRIS if m == 'No' else ORO for m in df['mbappe']]
        fig2 = go.Figure(go.Bar(
            x=df['temporada'], y=df['ucl_goles_a_favor'],
            marker_color=col2, text=df['ucl_goles_a_favor'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles UCL<extra></extra>"
        ))
        fig2.add_hline(y=sin['ucl_goles_a_favor'].mean(), line_dash="dash",
                       line_color=VERDE, line_width=2,
                       annotation_text=f"Promedio sin Mbappe: {sin['ucl_goles_a_favor'].mean():.0f}",
                       annotation_font_color=VERDE, annotation_position="top left")
        fig2.update_layout(xaxis=dict(showgrid=False),
                           yaxis=dict(range=[0,40], showgrid=True, gridcolor="#E2E8F0",
                                      title="Goles"),
                           plot_bgcolor="white", paper_bgcolor="white",
                           height=320, showlegend=False, margin=dict(l=20,r=20,t=20,b=30))
        st.plotly_chart(fig2, use_container_width=True)

    st.caption("🟡 Temporadas con Mbappe  |  Gris: sin Mbappe")
    st.divider()

    avg_liga_sin = sin['liga_goles_a_favor'].mean()
    avg_liga_con = con['liga_goles_a_favor'].mean()
    avg_ucl_sin  = sin['ucl_goles_a_favor'].mean()
    avg_ucl_con  = con['ucl_goles_a_favor'].mean()

    st.markdown(f"""
<div style="background:{AZUL_RM}; border-radius:10px; padding:1.5rem 2rem;">
    <p style="color:{ORO}; font-weight:800; font-size:1rem; margin:0 0 0.6rem 0;">
        Lo que dicen los numeros
    </p>
    <p style="color:{BLANCO}; font-size:0.95rem; margin:0; line-height:1.8;">
        Sin Mbappe el Madrid promediaba <strong style="color:{ORO};">{avg_liga_sin:.0f} goles en LaLiga</strong>
        y <strong style="color:{ORO};">{avg_ucl_sin:.0f} en Champions</strong> por temporada.<br>
        Con Mbappe promedia <strong style="color:{ROJO};">{avg_liga_con:.0f} en LaLiga</strong>
        y <strong style="color:{ROJO};">{avg_ucl_con:.0f} en Champions</strong>.<br><br>
        <strong style="color:{BLANCO};">El Madrid no tenia un problema de gol.
        Tenia la mejor temporada de su historia justo antes de ficharlo.
        El fichaje fue la respuesta a una pregunta que nadie habia formulado.</strong>
    </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# TAB 3 — LO QUE PASO DESPUES
# ══════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Lo que cambio con Mbappe")
    st.caption("Goles encajados, rendimiento en Champions y dependencia individual")
    st.divider()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Goles encajados/partido LaLiga sin Mbappe",
              f"{sin['liga_goles_en_contra'].mean()/38:.2f}", "promedio 2022-2024")
    k2.metric("Goles encajados/partido LaLiga con Mbappe",
              f"{con['liga_goles_en_contra'].mean()/38:.2f}",
              f"+{con['liga_goles_en_contra'].mean()/38 - sin['liga_goles_en_contra'].mean()/38:.2f} por partido",
              delta_color="inverse")
    k3.metric("Champions sin Mbappe", "1 titulo", "Final + Semifinal")
    k4.metric("Champions con Mbappe", "0 titulos", "Cuartos + Cuartos",
              delta_color="inverse")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Anomalia — goles encajados en LaLiga")
        col_e = [GRIS if m == 'No' else ROJO for m in df['mbappe']]
        fig_enc = go.Figure(go.Bar(
            x=df['temporada'], y=df['liga_goles_en_contra'],
            marker_color=col_e, text=df['liga_goles_en_contra'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles encajados<extra></extra>"
        ))
        fig_enc.add_hline(y=sin['liga_goles_en_contra'].mean(), line_dash="dash",
                          line_color=VERDE, line_width=2,
                          annotation_text=f"Promedio sin Mbappe: {sin['liga_goles_en_contra'].mean():.0f}",
                          annotation_font_color=VERDE, annotation_position="top left")
        fig_enc.add_annotation(
            x='2024-25', y=37,
            text="<b>+43% vs temporada\ncampeona 2023-24</b>",
            showarrow=True, arrowhead=2, arrowcolor=ROJO,
            ax=60, ay=-50, font=dict(color=ROJO, size=10),
            bgcolor="#FFF5F5", bordercolor=ROJO, borderwidth=1
        )
        fig_enc.update_layout(xaxis=dict(showgrid=False),
                              yaxis=dict(range=[0,50], showgrid=True, gridcolor="#E2E8F0",
                                         title="Goles encajados"),
                              plot_bgcolor="white", paper_bgcolor="white",
                              height=320, showlegend=False, margin=dict(l=20,r=20,t=20,b=30))
        st.plotly_chart(fig_enc, use_container_width=True)

    with col2:
        st.markdown("#### Anomalia — goles encajados en Champions")
        col_ucl = [GRIS if m == 'No' else ROJO for m in df['mbappe']]
        fig_ucl_enc = go.Figure(go.Bar(
            x=df['temporada'], y=df['ucl_goles_en_contra'],
            marker_color=col_ucl, text=df['ucl_goles_en_contra'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles encajados UCL<extra></extra>"
        ))
        fig_ucl_enc.add_hline(y=sin['ucl_goles_en_contra'].mean(), line_dash="dash",
                              line_color=VERDE, line_width=2,
                              annotation_text=f"Promedio sin Mbappe: {sin['ucl_goles_en_contra'].mean():.0f}",
                              annotation_font_color=VERDE, annotation_position="top left")
        fig_ucl_enc.update_layout(xaxis=dict(showgrid=False),
                                  yaxis=dict(range=[0,28], showgrid=True, gridcolor="#E2E8F0",
                                             title="Goles encajados"),
                                  plot_bgcolor="white", paper_bgcolor="white",
                                  height=320, showlegend=False, margin=dict(l=20,r=20,t=20,b=30))
        st.plotly_chart(fig_ucl_enc, use_container_width=True)

    st.caption("🔴 Temporadas con Mbappe  |  Gris: sin Mbappe")
    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Champions — hasta donde llego el Madrid")
        fases = {'Semifinal': 3, 'Final': 4, 'Campeon': 5, 'Cuartos': 2, 'Octavos': 1}
        df['fase_num'] = df['ucl_fase'].map(fases)
        col_cl = [GRIS if m == 'No' else ROJO for m in df['mbappe']]
        col_cl[1] = ORO  # 2023-24 campeón
        fig_cl = go.Figure(go.Bar(
            x=df['temporada'], y=df['fase_num'],
            marker_color=col_cl, text=df['ucl_fase'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>"
        ))
        fig_cl.update_layout(
            xaxis=dict(showgrid=False),
            yaxis=dict(tickvals=[1,2,3,4,5],
                       ticktext=['Octavos','Cuartos','Semifinal','Final','Campeon'],
                       showgrid=True, gridcolor="#E2E8F0", range=[0,6.5]),
            plot_bgcolor="white", paper_bgcolor="white",
            height=320, showlegend=False, margin=dict(l=20,r=80,t=20,b=30)
        )
        st.plotly_chart(fig_cl, use_container_width=True)
        st.caption("🟡 Campeon 2023-24  |  🔴 Con Mbappe  |  Gris: sin Mbappe")

    with col4:
        st.markdown("#### Dependencia — % de goles de Mbappe")
        temporadas_con = con['temporada'].tolist()
        goles_mbappe   = con['liga_goles_top'].tolist()
        goles_total    = con['liga_goles_a_favor'].tolist()
        goles_resto    = [t - m for t, m in zip(goles_total, goles_mbappe)]
        pcts           = [m/t*100 for m, t in zip(goles_mbappe, goles_total)]

        fig_dep = go.Figure()
        fig_dep.add_trace(go.Bar(
            name='Mbappe', x=temporadas_con, y=goles_mbappe,
            marker_color=ROJO, text=[f"Mbappe: {g} ({p:.0f}%)"
                                      for g, p in zip(goles_mbappe, pcts)],
            textposition='inside', textfont_color='white',
            hovertemplate="<b>%{x}</b><br>Mbappe: %{y} goles<extra></extra>"
        ))
        fig_dep.add_trace(go.Bar(
            name='Resto del equipo', x=temporadas_con, y=goles_resto,
            marker_color=GRIS,
            text=[f"Resto: {g}" for g in goles_resto],
            textposition='inside',
            hovertemplate="<b>%{x}</b><br>Resto: %{y} goles<extra></extra>"
        ))
        fig_dep.update_layout(
            barmode='stack',
            xaxis=dict(showgrid=False),
            yaxis=dict(range=[0,90], showgrid=True, gridcolor="#E2E8F0",
                       title="Goles LaLiga"),
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(orientation="h", y=1.08),
            height=320, margin=dict(l=20,r=20,t=30,b=30)
        )
        st.plotly_chart(fig_dep, use_container_width=True)

        promedio_dependencia = sum(pcts) / len(pcts)

        st.info(
            f"**Lectura clave:** Mbappé aporta en promedio el "
            f"**{promedio_dependencia:.0f}%** de los goles del Madrid en LaLiga. "
            f"Esto evidencia una dependencia ofensiva creciente. "
            "Cuando una parte tan grande de la producción recae en un solo jugador, "
            "el equipo se vuelve más vulnerable."
        )

# ══════════════════════════════════════════════════════════════════════════
# TAB 4 — EL VEREDICTO
# ══════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("El veredicto")
    st.caption("Contexto → Necesidad → Problema → Solucion")
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
        'Titulo Liga','UCL GF','UCL GC','UCL Partidos',
        'UCL Fase','Eliminado por','Titulo UCL','Mbappe'
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
    <p style="color:{ORO}; font-size:1.2rem; font-weight:800; margin:0 0 1rem 0;">
        No. El Real Madrid no solucionó el problema correcto.
    </p>
    <p style="color:{BLANCO}; font-size:0.97rem; line-height:1.9; margin:0;">
        <strong style="color:{ORO};">Contexto:</strong>
        El Madrid llego a 2024 como el mejor equipo de Europa — 95 puntos en LaLiga,
        campeon de Champions sin perder un solo partido, y apenas 13 goles encajados en
        toda la Champions. Era practicamente perfecto.<br><br>
        <strong style="color:{ORO};">Necesidad percibida:</strong>
        La directiva creia que fichar al mejor delantero del mundo los elevaria aun mas.
        Logica simple: mas gol = mas titulos. Pero los datos ya mostraban que el gol
        no era el problema — promediaban {sin['liga_goles_a_favor'].mean():.0f} goles
        por temporada en LaLiga y {sin['ucl_goles_a_favor'].mean():.0f} en Champions
        sin Mbappe.<br><br>
        <strong style="color:{ROJO};">Problema real:</strong>
        Con Mbappe, los goles encajados en LaLiga subieron de {avg_enc_sin:.0f} a
        {avg_enc_con:.0f} por temporada. En Champions, de {avg_ucl_enc_sin:.0f} a
        {avg_ucl_enc_con:.0f}. Los puntos cayeron de {avg_pts_sin:.0f} a {avg_pts_con:.0f}.
        Y en Europa, dos eliminaciones consecutivas en cuartos de final tras dos finales
        seguidas sin el. Ademas, creo un problema nuevo: dependencia extrema.
        En 2024-25 marco casi la mitad de los goles del equipo. Eso no es fortaleza.<br><br>
        <strong style="color:{BLANCO};">Mbappe es un jugador excepcional. Pero fue la respuesta
        a una pregunta que nadie habia formulado. El Madrid no necesitaba mas gol —
        necesitaba mantener la solidez que los habia hecho campeones.</strong>
    </p>
</div>
""", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown(f"""
<div style="background:#F0FFF4; border-left:4px solid {VERDE};
            border-radius:6px; padding:1.2rem 1.5rem;">
    <p style="color:#276749; font-weight:800; font-size:0.95rem; margin:0 0 0.4rem 0;">
        Lo que los datos confirman
    </p>
    <p style="color:#1A202C; font-size:0.88rem; margin:0; line-height:1.6;">
        • Sin Mbappe: 1 Champions, 1 LaLiga, {avg_pts_sin:.0f} puntos promedio<br>
        • Con Mbappe: 0 Champions, 0 LaLiga, {avg_pts_con:.0f} puntos promedio<br>
        • Goles encajados LaLiga: +{avg_enc_con-avg_enc_sin:.0f} por temporada<br>
        • Goles encajados UCL: +{avg_ucl_enc_con-avg_ucl_enc_sin:.0f} por temporada<br>
        • Champions: 2 cuartos de final consecutivos vs. 1 campeonato
    </p>
</div>
""", unsafe_allow_html=True)

    with col_r2:
        st.markdown(f"""
<div style="background:#FFF5F5; border-left:4px solid {ROJO};
            border-radius:6px; padding:1.2rem 1.5rem;">
    <p style="color:{ROJO}; font-weight:800; font-size:0.95rem; margin:0 0 0.4rem 0;">
        La leccion para cualquier club
    </p>
    <p style="color:#1A202C; font-size:0.88rem; margin:0; line-height:1.6;">
        Antes de fichar una estrella, diagnostica correctamente el problema.
        Un fichaje brillante que resuelve la pregunta equivocada no solo no ayuda —
        puede romper lo que ya funcionaba.
        <strong>Los datos no mienten: el Madrid era mejor antes de Mbappe.</strong>
    </p>
</div>
""", unsafe_allow_html=True)
