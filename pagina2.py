from dash import dcc, html
import dash_bootstrap_components as dbc

layout = dbc.Container(fluid=True, children=[
    dbc.Button("🏠 Volver al Inicio", href="/", color="light", className="mb-3"),
    html.H1("Exploración de Proyectos", style={'text-align': 'center'}),
    html.P("Aquí puedes explorar todos los proyectos y papers destacados.", style={'text-align': 'center'}),
    # Agregar más contenido de la página aquí
])
