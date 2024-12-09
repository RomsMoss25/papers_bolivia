import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Cargar los datos reales desde el archivo CSV
file_path = '/Users/romi_1/Downloads/Papers_proyectos_STEM.csv'
df_real_data = pd.read_csv(file_path)

# Limpiar los nombres de las columnas (opcional, elimina espacios extra)
df_real_data.columns = df_real_data.columns.str.strip()

# Transformar los datos reales al formato del dashboard
data = {
    "Área STEM": df_real_data["ÁREA STEM"].tolist(),
    "Categoría": df_real_data["CATEGORÍA"].tolist(),
    "Título": df_real_data["TÍTULO"].tolist(),
    "Autoras": df_real_data["AUTORAS"].tolist(),
    "Institución": df_real_data["INSTITUCIÓN"].tolist(),
    "Impacto": ["Educativo" if area == "Ciencia" else "Social" if area == "Tecnología"
                else "Ambiental" if area == "Ingeniería" else "Tecnológico" for area in df_real_data["ÁREA STEM"]],
    "Colaboradoras": [5 if area == "Ciencia" else 3 if area == "Tecnología"
                      else 8 if area == "Ingeniería" else 7 for area in df_real_data["ÁREA STEM"]],
    "Año": df_real_data["AÑO"].tolist(),
    "Enlace": df_real_data["LINK"].tolist()
}

# Crear un DataFrame con los datos reales
df = pd.DataFrame(data)

# Definir colores por área de STEM
area_colors = {
    "Ciencia": "#3498db",  # Azul
    "Tecnología": "#2ecc71",  # Verde
    "Ingeniería": "#e67e22",  # Naranja
    "Matemáticas": "#e74c3c",  # Rojo
}

# Crear la app de Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Mujeres STEM"

# Layout del dashboard
app.layout = dbc.Container(fluid=True, children=[
    # Encabezado con letras interactivas
    dbc.Row([
        dbc.Col(html.Div([
            html.Button("S", id="btn-S", n_clicks=0, style={
                'font-size': '40px',
                'background-color': area_colors["Ciencia"],
                'color': 'white',
                'border': 'none',
                'border-radius': '50%',
                'padding': '20px 30px',
                'cursor': 'pointer',
                'margin': '10px',
                'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
            }),
            html.Button("T", id="btn-T", n_clicks=0, style={
                'font-size': '40px',
                'background-color': area_colors["Tecnología"],
                'color': 'white',
                'border': 'none',
                'border-radius': '50%',
                'padding': '20px 30px',
                'cursor': 'pointer',
                'margin': '10px',
                'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
            }),
            html.Button("E", id="btn-E", n_clicks=0, style={
                'font-size': '40px',
                'background-color': area_colors["Ingeniería"],
                'color': 'white',
                'border': 'none',
                'border-radius': '50%',
                'padding': '20px 30px',
                'cursor': 'pointer',
                'margin': '10px',
                'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
            }),
            html.Button("M", id="btn-M", n_clicks=0, style={
                'font-size': '40px',
                'background-color': area_colors["Matemáticas"],
                'color': 'white',
                'border': 'none',
                'border-radius': '50%',
                'padding': '20px 30px',
                'cursor': 'pointer',
                'margin': '10px',
                'box-shadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
            }),
        ], style={'text-align': 'center', 'margin': '30px 0'})
        )
    ]),

    # Galería
    dbc.Row([
        dbc.Col(html.H3("Proyectos y Papers", className="text-center text-secondary mb-4"), width=12),
        dbc.Col([
            html.Div(id='gallery', style={
                'display': 'grid',
                'grid-template-columns': 'repeat(auto-fit, minmax(300px, 1fr))',
                'gap': '20px',
            })
        ], width=12),
    ], className="mb-5"),

    # Gráfico interactivo
    dbc.Row([
        dbc.Col(html.H3("Impacto por Categoría y Área STEM", className="text-center text-secondary mb-4"), width=12),
        dbc.Col(dcc.Graph(id='bubble_chart'), width=12)
    ]),
], style={'background-color': '#f8f9fa', 'padding': '20px'})


# Callback para manejar los clics en las letras y actualizar la visualización
@app.callback(
    [Output('gallery', 'children'),
     Output('bubble_chart', 'figure')],
    [Input('btn-S', 'n_clicks'),
     Input('btn-T', 'n_clicks'),
     Input('btn-E', 'n_clicks'),
     Input('btn-M', 'n_clicks')]
)
def update_visualizations(n_s, n_t, n_e, n_m):
    # Determinar qué letra fue clickeada
    ctx = dash.callback_context
    if not ctx.triggered:
        selected_area = "Ciencia"  # Valor por defecto
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        selected_area = {
            "btn-S": "Ciencia",
            "btn-T": "Tecnología",
            "btn-E": "Ingeniería",
            "btn-M": "Matemáticas"
        }.get(button_id, "Ciencia")

    # Filtrar datos por área STEM
    filtered_df = df[df['Área STEM'] == selected_area]

    # Galería
    gallery_items = []
    for _, row in filtered_df.iterrows():
        card = dbc.Card(
            [
                dbc.CardBody([
                    html.H5(row['Título'], className="card-title", style={'color': area_colors[row['Área STEM']]}),
                    html.P(f"Área STEM: {row['Área STEM']}", className="card-text text-secondary"),
                    html.P(f"Categoría: {row['Categoría']}", className="card-text text-secondary"),
                    html.P(f"Año: {row['Año']}", className="card-text text-secondary"),
                    dbc.Button("Ver más", href=row['Enlace'], target="_blank", color="primary", className="mt-2")
                ])
            ],
            style={"width": "100%", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"}
        )
        gallery_items.append(card)

    # Gráfico de burbujas
    bubble_fig = px.scatter(
        filtered_df,
        x="Categoría",
        y="Impacto",
        size="Colaboradoras",
        color="Área STEM",
        color_discrete_map=area_colors,
        hover_name="Título",
        title=f"Impacto en {selected_area}",
    )
    bubble_fig.update_layout(template="simple_white", xaxis_title="Categoría", yaxis_title="Impacto")

    return gallery_items, bubble_fig


# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
