import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Cargar los datos reales desde el archivo CSV
file_path = 'Papers_proyectos STEM  (1).csv'
df_real_data = pd.read_csv(file_path)

# Limpiar los nombres de las columnas (opcional, elimina espacios extra)
df_real_data.columns = df_real_data.columns.str.strip()

# Transformar los datos reales al formato del dashboard
data = {
    "Área STEM": [str(area).strip() if not pd.isna(area) else "Sin Especificar" for area in df_real_data["ÁREA STEM"]],
    "Categoría": [str(cat).strip() if not pd.isna(cat) else "" for cat in df_real_data["CATEGORÍA"]],
    "Título": [str(title).strip() if not pd.isna(title) else "" for title in df_real_data["TÍTULO"]],
    "Autoras": [str(author).strip() if not pd.isna(author) else "" for author in df_real_data["AUTORAS"]],
    "Institución": [str(inst).strip() if not pd.isna(inst) else "" for inst in df_real_data["INSTITUCIÓN"]],
    "Impacto": ["Educativo" if str(area).strip() == "Ciencia" else "Social" if str(area).strip() == "Tecnología"
                else "Ambiental" if str(area).strip() == "Ingeniería" else "Tecnológico" for area in df_real_data["ÁREA STEM"]],
    "Colaboradoras": [5 if str(area).strip() == "Ciencia" else 3 if str(area).strip() == "Tecnología"
                      else 8 if str(area).strip() == "Ingeniería" else 7 for area in df_real_data["ÁREA STEM"]],
    "Año": [str(year).strip() if not pd.isna(year) else "" for year in df_real_data["AÑO"]],
    "Enlace": [str(link).strip() if not pd.isna(link) else "" for link in df_real_data["LINK"]]
}

# Crear un DataFrame con los datos reales
df = pd.DataFrame(data)

# Filtrar los datos para eliminar filas vacías o irrelevantes
df = df[(df['Título'] != "") & (df['Área STEM'] != "Sin Especificar")]

# Definir colores por área de STEM
area_colors = {
    "Ciencia": "#3498db",  # Azul
    "Tecnología": "#2ecc71",  # Verde
    "Ingeniería": "#e67e22",  # Naranja
    "Matemáticas": "#e74c3c",  # Rojo
    "STEM": "#8e44ad",  # Púrpura para la categoría general
    "Sin Especificar": "#95a5a6"  # Gris para valores no especificados
}

# Crear la app de Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Mujeres STEM"


 #Layout del dashboard
app.layout = dbc.Container(fluid=True, children=[
    # Botón "Volver al Inicio" en la parte superior
    dbc.Row([
        dbc.Col([
            html.A("🏠 Volver al Inicio", href="https://stem-bolivia.onrender.com", style={
                "color": "#007bff", 
                "font-size": "18px",
                "text-decoration": "none",
                "font-weight": "bold",
                "margin-bottom": "20px",
                "display": "inline-block"
            })
        ], width=12, style={"text-align": "left"})
    ]),

# Layout del dashboard
app.layout = dbc.Container(fluid=True, children=[
    # Encabezado con íconos interactivos
    dbc.Row([
        dbc.Col(html.Div([
            html.Button("STEM", id="btn-STEM", n_clicks=0, style={
                'font-size': '20px',
                'background-color': area_colors["STEM"],
                'color': 'white',
                'border': 'none',
                'border-radius': '50%',
                'padding': '20px 30px',
                'cursor': 'pointer',
                'margin': '10px'
            }),
            html.Button(html.Img(src="https://img.icons8.com/ios-filled/50/3498db/microscope.png", alt="Ciencia"), id="btn-S", n_clicks=0, style={
                'background-color': 'transparent',
                'border': 'none',
                'cursor': 'pointer',
                'margin': '10px'
            }),
            html.Button(html.Img(src="https://img.icons8.com/ios-filled/50/2ecc71/computer.png", alt="Tecnología"), id="btn-T", n_clicks=0, style={
                'background-color': 'transparent',
                'border': 'none',
                'cursor': 'pointer',
                'margin': '10px'
            }),
            html.Button(html.Img(src="https://img.icons8.com/ios-filled/50/e67e22/engineering.png", alt="Ingeniería"), id="btn-E", n_clicks=0, style={
                'background-color': 'transparent',
                'border': 'none',
                'cursor': 'pointer',
                'margin': '10px'
            }),
            html.Button(html.Img(src="https://img.icons8.com/ios-filled/50/e74c3c/math.png", alt="Matemáticas"), id="btn-M", n_clicks=0, style={
                'background-color': 'transparent',
                'border': 'none',
                'cursor': 'pointer',
                'margin': '10px'
            }),
        ], style={'text-align': 'center', 'margin': '30px 0'})
        )
    ]),

    # Texto dinámico
    dbc.Row([
        dbc.Col(html.H2(id="dynamic-text", className="text-center text-primary my-4"), width=12)
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
     Output('bubble_chart', 'figure'),
     Output('dynamic-text', 'children')],
    [Input('btn-STEM', 'n_clicks'),
     Input('btn-S', 'n_clicks'),
     Input('btn-T', 'n_clicks'),
     Input('btn-E', 'n_clicks'),
     Input('btn-M', 'n_clicks')]
)
def update_visualizations(n_stem, n_s, n_t, n_e, n_m):
    # Determinar qué botón fue clickeado
    ctx = dash.callback_context
    if not ctx.triggered:
        selected_area = "STEM"  # Valor por defecto
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        selected_area = {
            "btn-STEM": "STEM",
            "btn-S": "Ciencia",
            "btn-T": "Tecnología",
            "btn-E": "Ingeniería",
            "btn-M": "Matemáticas"
        }.get(button_id, "STEM")

    # Filtrar datos por área STEM
    if selected_area == "STEM":
        # Filtrar datos que tienen "STEM" en Área STEM
        filtered_df = df[df['Área STEM'].str.strip() == "STEM"]
        bubble_df = df  # Mostrar todas las categorías en el gráfico de burbujas
    else:
        # Filtrar por Área STEM específica
        filtered_df = df[df['Área STEM'].str.strip() == selected_area]
        bubble_df = filtered_df

    # Galería
    gallery_items = []
    for _, row in filtered_df.iterrows():
        area_color = area_colors.get(row['Área STEM'].strip(), area_colors["Sin Especificar"])
        card = dbc.Card(
            [
                dbc.CardBody([
                    html.H5(row['Título'], className="card-title", style={'color': area_color}),
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
        bubble_df,
        x="Categoría",
        y="Impacto",
        size="Colaboradoras",
        color="Área STEM",
        color_discrete_map=area_colors,
        hover_name="Título",
        title=f"Impacto en {selected_area}",
    )
    bubble_fig.update_layout(template="simple_white", xaxis_title="Categoría", yaxis_title="Impacto")

    # Texto dinámico
    dynamic_text = f"Proyectos en el área de {selected_area}"

    return gallery_items, bubble_fig, dynamic_text

server = app.server

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)


