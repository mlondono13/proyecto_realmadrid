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
# Todas las variables son discretas (conteos de goles, puntos, partidos).
# → Barras separadas por categoría homogénea (mismas unidades en cada gráfica)
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

    # ── Bloque 1: LaLiga — variables de mismo tipo (puntos)
    st.markdown("### LaLiga — Rendimiento antes del fichaje")
    col_a, col_b = st.columns(2)

    with col_a:
        # Variable discreta: puntos por temporada → barras separadas
        st.markdown("#### Puntos en LaLiga")
        df_sin = df[df['mbappe'] == 'No']
        fig_pts = go.Figure(go.Bar(
            x=df_sin['temporada'],
            y=df_sin['liga_puntos'],
            marker_color=[GRIS, ORO],
            text=df_sin['liga_puntos'],
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} puntos<extra></extra>"
        ))
        LAYOUT_BASE = dict(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=40, b=40),
            font=dict(family="Arial, sans-serif"),
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig_pts, use_container_width=True)
        st.caption("Variable discreta → barras separadas")

    with col_b:
        # Variable discreta: victorias/empates/derrotas → barras apiladas (misma unidad: partidos)
        st.markdown("#### Resultados en LaLiga (V / E / D)")
        fig_res = go.Figure()
        fig_res.add_trace(go.Bar(
            name='Victorias', x=df_sin['temporada'], y=df_sin['liga_victorias'],
            marker_color=VERDE, text=df_sin['liga_victorias'],
            textposition='inside', textfont_color='white',
            hovertemplate="<b>%{x}</b><br>Victorias: %{y}<extra></extra>"
        ))
        fig_res.add_trace(go.Bar(
            name='Empates', x=df_sin['temporada'], y=df_sin['liga_empates'],
            marker_color=ORO, text=df_sin['liga_empates'],
            textposition='inside',
            hovertemplate="<b>%{x}</b><br>Empates: %{y}<extra></extra>"
        ))
        fig_res.add_trace(go.Bar(
            name='Derrotas', x=df_sin['temporada'], y=df_sin['liga_derrotas'],
            marker_color=ROJO, text=df_sin['liga_derrotas'],
            textposition='inside', textfont_color='white',
            hovertemplate="<b>%{x}</b><br>Derrotas: %{y}<extra></extra>"
        ))
        fig_res.update_layout(
            **LAYOUT_BASE,
            barmode='stack', height=300,
            yaxis=dict(range=[0, 42], showgrid=True, gridcolor="#E2E8F0", title="Partidos"),
            legend=dict(orientation="h", y=1.12)
        )
        st.plotly_chart(fig_res, use_container_width=True)
        st.caption("Variable discreta (conteo de partidos) → barras apiladas por categoría nominal")

    st.divider()

    # ── Bloque 2: LaLiga — Goles (misma unidad, separados ataque vs defensa)
    st.markdown("### LaLiga — Producción ofensiva vs solidez defensiva")
    col_c, col_d = st.columns(2)

    with col_c:
        # Variable discreta: goles a favor → barras separadas
        st.markdown("#### Goles anotados (LaLiga)")
        fig_gf = go.Figure(go.Bar(
            x=df_sin['temporada'], y=df_sin['liga_goles_a_favor'],
            marker_color=[GRIS, ORO],
            text=df_sin['liga_goles_a_favor'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles a favor<extra></extra>"
        ))
        fig_gf.add_hline(y=df_sin['liga_goles_a_favor'].mean(), line_dash="dash",
                         line_color=VERDE, line_width=2,
                         annotation_text=f"Promedio: {df_sin['liga_goles_a_favor'].mean():.0f}",
                         annotation_font_color=VERDE, annotation_position="top left")
        fig_gf.update_layout(
            **LAYOUT_BASE, height=300,
            yaxis=dict(range=[0, 105], showgrid=True, gridcolor="#E2E8F0", title="Goles")
        )
        st.plotly_chart(fig_gf, use_container_width=True)

    with col_d:
        # Variable discreta: goles en contra → barras separadas (mismo eje que arriba para comparar)
        st.markdown("#### Goles encajados (LaLiga)")
        fig_gc = go.Figure(go.Bar(
            x=df_sin['temporada'], y=df_sin['liga_goles_en_contra'],
            marker_color=[GRIS, ORO],
            text=df_sin['liga_goles_en_contra'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles en contra<extra></extra>"
        ))
        fig_gc.add_hline(y=df_sin['liga_goles_en_contra'].mean(), line_dash="dash",
                         line_color=VERDE, line_width=2,
                         annotation_text=f"Promedio: {df_sin['liga_goles_en_contra'].mean():.0f}",
                         annotation_font_color=VERDE, annotation_position="top left")
        fig_gc.update_layout(
            **LAYOUT_BASE, height=300,
            yaxis=dict(range=[0, 105], showgrid=True, gridcolor="#E2E8F0", title="Goles")
        )
        st.plotly_chart(fig_gc, use_container_width=True)

    st.caption("🟡 2023-24: Temporada campeona  |  Gris: 2022-23")
    st.divider()

    # ── Bloque 3: Champions — misma lógica, separados de LaLiga
    st.markdown("### Champions League — Rendimiento antes del fichaje")
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown("#### Goles anotados (Champions)")
        fig_ucl_gf = go.Figure(go.Bar(
            x=df_sin['temporada'], y=df_sin['ucl_goles_a_favor'],
            marker_color=[GRIS, ORO],
            text=df_sin['ucl_goles_a_favor'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles UCL<extra></extra>"
        ))
        fig_ucl_gf.add_hline(y=df_sin['ucl_goles_a_favor'].mean(), line_dash="dash",
                              line_color=VERDE, line_width=2,
                              annotation_text=f"Promedio: {df_sin['ucl_goles_a_favor'].mean():.0f}",
                              annotation_font_color=VERDE, annotation_position="top left")
        fig_ucl_gf.update_layout(
            **LAYOUT_BASE, height=300,
            yaxis=dict(range=[0, 35], showgrid=True, gridcolor="#E2E8F0", title="Goles")
        )
        st.plotly_chart(fig_ucl_gf, use_container_width=True)

    with col_f:
        st.markdown("#### Goles encajados (Champions)")
        fig_ucl_gc = go.Figure(go.Bar(
            x=df_sin['temporada'], y=df_sin['ucl_goles_en_contra'],
            marker_color=[GRIS, ORO],
            text=df_sin['ucl_goles_en_contra'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles encajados UCL<extra></extra>"
        ))
        fig_ucl_gc.add_hline(y=df_sin['ucl_goles_en_contra'].mean(), line_dash="dash",
                              line_color=VERDE, line_width=2,
                              annotation_text=f"Promedio: {df_sin['ucl_goles_en_contra'].mean():.0f}",
                              annotation_font_color=VERDE, annotation_position="top left")
        fig_ucl_gc.update_layout(
            **LAYOUT_BASE, height=300,
            yaxis=dict(range=[0, 35], showgrid=True, gridcolor="#E2E8F0", title="Goles")
        )
        st.plotly_chart(fig_ucl_gc, use_container_width=True)

    st.caption("🟡 2023-24: Temporada campeona  |  Gris: 2022-23")

    st.markdown(f"""
<div style="background:#FFFAF0; border-left:4px solid {ORO};
            border-radius:6px; padding:1rem 1.5rem; margin-top:1rem;">
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
        col = color_mbappe(df['mbappe'])
        fig1 = go.Figure(go.Bar(
            x=df['temporada'], y=df['liga_goles_a_favor'],
            marker_color=col, text=df['liga_goles_a_favor'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles<extra></extra>"
        ))
        fig1.add_hline(y=sin['liga_goles_a_favor'].mean(), line_dash="dash",
                       line_color=VERDE, line_width=2,
                       annotation_text=f"Promedio sin Mbappe: {sin['liga_goles_a_favor'].mean():.0f}",
                       annotation_font_color=VERDE, annotation_position="top left")
        fig1.update_layout(
            **LAYOUT_BASE, height=320,
            yaxis=dict(range=[0, 105], showgrid=True, gridcolor="#E2E8F0", title="Goles"),
            showlegend=False
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown("#### Champions — Goles anotados")
        fig2 = go.Figure(go.Bar(
            x=df['temporada'], y=df['ucl_goles_a_favor'],
            marker_color=color_mbappe(df['mbappe']), text=df['ucl_goles_a_favor'],
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles UCL<extra></extra>"
        ))
        fig2.add_hline(y=sin['ucl_goles_a_favor'].mean(), line_dash="dash",
                       line_color=VERDE, line_width=2,
                       annotation_text=f"Promedio sin Mbappe: {sin['ucl_goles_a_favor'].mean():.0f}",
                       annotation_font_color=VERDE, annotation_position="top left")
        fig2.update_layout(
            **LAYOUT_BASE, height=320,
            yaxis=dict(range=[0, 40], showgrid=True, gridcolor="#E2E8F0", title="Goles"),
            showlegend=False
        )
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
        st.markdown("#### Goles encajados en LaLiga — la anomalia defensiva")
        col_e = color_mbappe(df['mbappe'], color_con=ROJO)
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
            text="<b>+43% vs temporada<br>campeona 2023-24</b>",
            showarrow=True, arrowhead=2, arrowcolor=ROJO,
            ax=60, ay=-50, font=dict(color=ROJO, size=10),
            bgcolor="#FFF5F5", bordercolor=ROJO, borderwidth=1
        )
        fig_enc.update_layout(
            **LAYOUT_BASE, height=320,
            yaxis=dict(range=[0, 50], showgrid=True, gridcolor="#E2E8F0", title="Goles encajados"),
            showlegend=False
        )
        st.plotly_chart(fig_enc, use_container_width=True)

    with col2:
        st.markdown("#### Goles encajados en Champions")
        fig_ucl_enc = go.Figure(go.Bar(
            x=df['temporada'], y=df['ucl_goles_en_contra'],
            marker_color=color_mbappe(df['mbappe'], color_con=ROJO),
            text=df['ucl_goles_en_contra'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{y} goles encajados UCL<extra></extra>"
        ))
        fig_ucl_enc.add_hline(y=sin['ucl_goles_en_contra'].mean(), line_dash="dash",
                              line_color=VERDE, line_width=2,
                              annotation_text=f"Promedio sin Mbappe: {sin['ucl_goles_en_contra'].mean():.0f}",
                              annotation_font_color=VERDE, annotation_position="top left")
        fig_ucl_enc.update_layout(
            **LAYOUT_BASE, height=320,
            yaxis=dict(range=[0, 28], showgrid=True, gridcolor="#E2E8F0", title="Goles encajados"),
            showlegend=False
        )
        st.plotly_chart(fig_ucl_enc, use_container_width=True)

    st.caption("🔴 Temporadas con Mbappe  |  Gris: sin Mbappe")
    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        # Variable ORDINAL: fase UCL → barras ordenadas con semáforo de color
        st.markdown("#### Champions — Fase alcanzada (variable ordinal)")
        fases_orden = {'Octavos': 1, 'Cuartos': 2, 'Semifinal': 3, 'Final': 4, 'Campeon': 5}
        semaforo = {1: '#C81D25', 2: '#E07B39', 3: '#F5C518', 4: '#1D9E75', 5: '#155E3B'}
        df['fase_num'] = df['ucl_fase'].map(fases_orden)
        col_cl = [semaforo[v] for v in df['fase_num']]
        fig_cl = go.Figure(go.Bar(
            x=df['temporada'], y=df['fase_num'],
            marker_color=col_cl, text=df['ucl_fase'], textposition='outside',
            hovertemplate="<b>%{x}</b><br>%{text}<extra></extra>"
        ))
        fig_cl.update_layout(
            **LAYOUT_BASE,
            xaxis=dict(showgrid=False),
            yaxis=dict(
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['Octavos', 'Cuartos', 'Semifinal', 'Final', 'Campeon'],
                showgrid=True, gridcolor="#E2E8F0", range=[0, 6.5]
            ),
            height=320, showlegend=False
        )
        st.plotly_chart(fig_cl, use_container_width=True)
        st.caption("Variable ordinal → barras ordenadas con semáforo de color (rojo = peor, verde = mejor)")

    with col4:
        # Variable discreta: distribución goles → barras apiladas (misma unidad)
        st.markdown("#### Dependencia — % de goles de Mbappe en LaLiga")
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
            **LAYOUT_BASE,
            barmode='stack',
            yaxis=dict(range=[0, 90], showgrid=True, gridcolor="#E2E8F0", title="Goles LaLiga"),
            legend=dict(orientation="h", y=1.12),
            height=320
        )
        st.plotly_chart(fig_dep, use_container_width=True)

    st.info(
        f"**Lectura clave:** En 2024-25 Mbappe marcó el **{goles_mbappe[0]/goles_total[0]*100:.0f}%** "
        f"de los goles del Madrid en LaLiga. Cuando el no aparece, el equipo no tiene plan B. "
        "Eso no es fortaleza — es fragilidad."
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

    # Gráfica comparativa final: puntos y goles encajados con y sin Mbappe
    # Variable continua (promedios) → scatter + línea de referencia para comparar grupos
    st.markdown("### Comparativa de medias — Sin Mbappe vs. Con Mbappe")

    metricas_comp = ['Puntos LaLiga', 'Goles a favor\nLaLiga', 'Goles encajados\nLaLiga',
                     'Goles a favor\nChampions', 'Goles encajados\nChampions']
    vals_sin = [
        sin['liga_puntos'].mean(),
        sin['liga_goles_a_favor'].mean(),
        sin['liga_goles_en_contra'].mean(),
        sin['ucl_goles_a_favor'].mean(),
        sin['ucl_goles_en_contra'].mean()
    ]
    vals_con = [
        con['liga_puntos'].mean(),
        con['liga_goles_a_favor'].mean(),
        con['liga_goles_en_contra'].mean(),
        con['ucl_goles_a_favor'].mean(),
        con['ucl_goles_en_contra'].mean()
    ]

    # Barras horizontales para comparar dos grupos con categoría nominal
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        y=metricas_comp, x=vals_sin, name='Sin Mbappe (2022-24)',
        orientation='h', marker_color=ORO,
        text=[f"{v:.0f}" for v in vals_sin], textposition='outside',
        hovertemplate="Sin Mbappe · %{y}: %{x:.0f}<extra></extra>"
    ))
    fig_comp.add_trace(go.Bar(
        y=metricas_comp, x=vals_con, name='Con Mbappe (2024-26)',
        orientation='h', marker_color=ROJO,
        text=[f"{v:.0f}" for v in vals_con], textposition='outside',
        hovertemplate="Con Mbappe · %{y}: %{x:.0f}<extra></extra>"
    ))
    fig_comp.update_layout(
        barmode='group',
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=20, r=60, t=40, b=30),
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0", title="Valor promedio"),
        yaxis=dict(showgrid=False),
        legend=dict(orientation="h", y=1.1),
        height=380
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    st.caption("Variable nominal (grupo) + variable continua (promedios) → barras horizontales agrupadas")

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
        seguidas sin el. Ademas, creo un problema nuevo: dependencia extrema.<br><br>
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
