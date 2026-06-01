import plotly.graph_objects as go

def barra_simple(
    x,
    y,
    colores,
    titulo_y,
    altura=320,
    rango=None
):
    """
    Gráfica de barras estándar para variables discretas.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=x,
            y=y,
            marker_color=colores,
            text=y,
            textposition="outside"
        )
    )

    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title=titulo_y,
            showgrid=True,
            gridcolor="#E2E8F0",
            range=rango
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        height=altura,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=30
        )
    )

    return fig

def barra_con_promedio(
    x,
    y,
    colores,
    promedio,
    titulo_y,
    color_promedio,
    texto_promedio,
    altura=320,
    rango=None
):

    fig = barra_simple(
        x,
        y,
        colores,
        titulo_y,
        altura,
        rango
    )

    fig.add_hline(
        y=promedio,
        line_dash="dash",
        line_color=color_promedio,
        line_width=2,
        annotation_text=texto_promedio,
        annotation_font_color=color_promedio,
        annotation_position="top left"
    )

    return fig

def linea_temporal(
    x,
    y,
    color,
    titulo_y,
    altura=320
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers+text",
            line=dict(
                width=4,
                color=color
            ),
            text=y,
            textposition="top center"
        )
    )

    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title=titulo_y,
            showgrid=True,
            gridcolor="#E2E8F0"
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        height=altura
    )

    return fig

def barras_apiladas(
    temporadas,
    mbappe,
    resto,
    rojo,
    gris
):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Mbappé",
            x=temporadas,
            y=mbappe,
            marker_color=rojo
        )
    )

    fig.add_trace(
        go.Bar(
            name="Resto del equipo",
            x=temporadas,
            y=resto,
            marker_color=gris
        )
    )

    fig.update_layout(
        barmode="stack",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=320,
        legend=dict(
            orientation="h",
            y=1.08
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title="Goles",
            showgrid=True,
            gridcolor="#E2E8F0"
        )
    )

    return fig

def tarjeta_metrica(
    titulo,
    valor,
    color_fondo,
    color_texto="white"
):

    return f"""
    <div style="
        background:{color_fondo};
        border-radius:12px;
        padding:1.5rem;
        text-align:center;
    ">
        <h4 style="color:{color_texto}; margin:0;">
            {titulo}
        </h4>

        <h2 style="color:{color_texto}; margin-top:10px;">
            {valor}
        </h2>
    </div>
    """
