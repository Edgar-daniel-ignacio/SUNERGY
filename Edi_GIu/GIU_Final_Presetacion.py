import Primer_Funcion_Clima as pf
import Clima_Car as cl
import Posicion_Solar as ps
import Parametros_Electricos as pe
from pvlib._deprecation import pvlibDeprecationWarning
import warnings
import CurvaIV as iv
import plotly as py
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
import pvlib
import pandas as pd
import Input_File_DIV_Mac_Informe as input
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.subplots import make_subplots
import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

for i in range(1):
    cf.set_config_file(dimensions=(1000, 1000))
    warnings.filterwarnings(action='ignore', category=RuntimeWarning)
    warnings.filterwarnings(action='ignore', category=pvlibDeprecationWarning)
    # Configuración para usar Plotly de manera offline
    py.offline.init_notebook_mode(connected=True)
    init_notebook_mode(connected=True)
for i in range(1):
    from dash import html, dcc
    from dash.dependencies import Input, Output, State
    import plotly.express as px
    from scipy.special import expit

import dash_leaflet as dl
import numpy as np
from dash.exceptions import PreventUpdate

cf.go_offline()
import pvlib
import numpy as np
from scipy import special, constants
import pandas as pd
import random
from dash import dash_table
from random import randint
import io
import base64
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
import base64

allow_duplicate = True

# Dev devolpment:

app = dash.Dash()
years = ['1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
         '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
meses = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

slider_marks_style = {
    'transform': 'rotate(-35deg)',
    'whiteSpace': 'nowrap',
    'fontSize': '10px',
    'color': 'white'  # Ajusta el tamaño de la fuente si es necesario
}

tables = ""
dataframes = []
df = pd.DataFrame([
    {'index': 0, 'value': 'col2-0'},
    {'index': 1, 'value': 'col2-1'},
    {'index': 2, 'value': 'col2-2'},
    {'index': 3, 'value': 'col2-3'},
    {'index': 4, 'value': 'col2-4'},
])

cases = [
    (1098.160944, 57.447914),
    (375.491531, 24.069324),
    (1098.160944, 57.447914),
    (1073.095209, 67.377506),
    (1098.160944, 57.447914),
    (1001, 27.5)
]

Pot = 250
Vm = 30.12
Im = 8.30
Voc = 37.85
Isc = 8.65
alpha = 0.01
beta = -0.31
gamma = -0.5
Numero_celda = 60
Tempref = 25
Tc = "polySi"

# Build App
app = Dash(external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div(children=[
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Solar-reference", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Page 2", href="#"),
                    dbc.DropdownMenuItem("Page 3", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="SuNLiER",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    dbc.Row([
        dbc.Col([html.H1("Prediccion energetica"),
                 html.Br()
                    ,
                 input.lat(18.84045),  # latitud base
                 input.lon(-99.23625),  # longitud base,
                 html.H2("Datos modulo"),
                 dcc.Dropdown(
                     id='selection-dropdown',
                     options=[
                         {'label': 'Prueba(Temixco)', 'value': 'SELEC'},

                         {'label': 'Insertar Datos', 'value': 'INSERT'},

                         {'label': 'Base de Datos CEC', 'value': 'CEC'}
                     ],
                     value='SELEC',

                     style={
                         'margin-bottom': '10px',
                         'margin-right': '10px',
                         'width': '100%',
                         'color': '#000000',
                         'font-size': 15
                     }
                 ), dcc.Loading([html.Div(id="loading")]),

                 input.table_module(Pot, Vm, Im, Voc, Isc, alpha, beta, gamma, Numero_celda, Tempref, Tc)
                 # modulo de prueba.
                    ,

                 dcc.Loading([html.Div(id="loading-1")])

                    ,

                 # Gestion de drowpdown para los filtros
                 dbc.Card(
                     dbc.CardBody([
                         dbc.Row([
                             dbc.Col(input.filter_selector(0), width=6),
                             dbc.Col(input.Dropdown_1())

                         ], align='center'),
                         dbc.Row([
                             dbc.Col(input.Dropdown_2()),
                             dbc.Col(input.Dropdown_3()),
                             dbc.Col(input.Dropdown_4())
                         ], align='center')

                     ])
                     , color="secondary"),

                 dbc.Card(color="secondary")
                 ], width=5),

        ###Columna del mapa gestion
        dbc.Col([
            html.H3("Mapa de la zona"),
            dbc.Card(
                dl.Map(center=[18.84045, -99.23625], zoom=15, children=[
                    dl.TileLayer(), dl.LocateControl(locateOptions={'enableHighAccuracy': True}),
                    dl.FeatureGroup([
                        dl.EditControl(id="edit_control")]),
                    dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                                      activeColor="#214097", completedColor="#972158")
                    ,
                    dl.Marker(position=[18.84045, -99.23625], id='marker')
                ], id='map', style={'width': '170%', 'height': '470px'}),
                color="secondary"), html.Br()

        ], width=4, style={'padding': 0}

        )
    ])

    ,
    # tabla donde se generan los modulos
    html.Div(id='Tabla_modulos', children=[
        dbc.Card([
            input.tabla_modulos_base(),  # Asumiendo que esto devuelve un componente de Dash
            dcc.Loading([html.Div(id="loading-2")]),
            dcc.Store(id='selected-rows-store'),
            html.Div(id='datos Modulos', children=[
                html.H1('Modulos seleccionados (Maximo numero de modulos 2)'),

                dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
                    dcc.Tab(
                        id='Tab One',
                        label='Modulo 1',
                        value='tab-1-example-graph',
                        style={'display': 'block', 'backgroundColor': '#0000A0', 'color': '#000000',
                               'fontWeight': 'bold'}
                    ),
                    dcc.Tab(
                        id='Tab Two',
                        label='Modulo 2',
                        value='tab-2-example-graph',
                        style={'display': 'block', 'backgroundColor': '#0000A0', 'color': '#000000',
                               'fontWeight': 'bold'}
                    ),
                ], colors={
                    'border': 'black',
                    'primary': 'blue',
                    'background': "black"
                }),
                html.Div(id='tabs-content-example-graph')
            ], style={'display': 'none'})
        ], color="secondary")
    ], style={'display': 'none'})

    # Creacion de datos de modulo (Inputs_Files)
    ,

    dcc.Loading([html.Div(id="loading-demo")])
    ,
    dbc.Card(
        dbc.CardBody([html.H2("Tipo de Metodologia"),
                      dbc.Row([dbc.Col(input.temperature_items()),
                               html.Br(),
                               dbc.Col(html.Div(id='output-div')),
                               dbc.Col(input.Feinman_options()),
                               dbc.Col(input.Sandia_options()),
                               dbc.Col(input.NOCT_In())
                               ]

                              ), html.Br(),
                      dbc.Row(dbc.Col(input.Pos_modulo(0), md=2)),
                      html.Br(),
                      html.Div(id='TA_M', children=[
                          dbc.Row(dbc.Col(input.tilt(0))),
                          dbc.Row(dbc.Col(input.Azimuth(0)))],
                               style={'display': 'none'}
                               )

                         , html.Br(),
                      dbc.Row([html.H3("Tiempo"),
                               dbc.Col(input.type_year(0), width=3),
                               dbc.Col(input.year_time(0), width=3),
                               dbc.Col(input.time_range(0), width=3)

                               ], align='center'),

                      dbc.Row([
                          dbc.Col([
                              html.Div(html.Div(id='tables-container'))
                          ], width=10.5)
                      ], align='center')
                      ])

    )
    ,
    dcc.Store(id='store-ndh')
    ,
    # Creacion de la obtencion de temperaturas para los parametros electricos.

    html.Div(id='output-div_1'),
    dcc.Store(id='Prueba'),
    dcc.Store(id='Database1'),
    dcc.Store(id='Database2'),
    # Tengo que crear los data frames para guardas los valores que se creen de los años que se muestren.
    html.Div(html.Div(id='PE-TMY')),  ##Estas son las tablas de los parametros electricos
    html.Div(html.Div(id='PE-SY')),  ## Son clave ya que son generadas desde el CSV
    dcc.Store(id='Datos_PE'),  ### Tienes que hacer lo mismo y procesarlas
    dcc.Store(id='Datos_PE2'),
    html.Div(id="Grafica", children=[dbc.Container(
        [
            html.H1("Parametros Electricos"),
            dbc.Card(
                [dbc.Row([dbc.Col(md=1),
                          html.Br(), html.Br()
                             ,
                          dbc.Col(children=input.column_Pe(), id="output-column", md=2),
                          dbc.Col(

                              html.Div([html.Br(), html.Br(),

                                        html.H4("Meses del año"),
                                        dbc.Label("Mes"),
                                        dcc.RangeSlider(
                                            id='my-range-slider',
                                            min=1,
                                            max=12,
                                            step=1,
                                            value=[1, 12],
                                            marks={i: {'label': meses[i], 'style': slider_marks_style} for i in
                                                   range(1, 13)}
                                            ,
                                            allowCross=False
                                        ),
                                        html.Div(id='output-container-range-slider', style={'margin-top': '50px'})
                                        # Agrega margen superior
                                        ])
                              , md=5
                          ),

                          dbc.Col(
                              html.Div(id="IV_selector", children=[html.H4("Voltaje vs Corriente"), html.Label("Año"),
                                                                   dcc.Dropdown(
                                                                       id='Year-Time_h',
                                                                       ### Esto es para la curva,  para la tercer grafica el contenedor de la derecha.
                                                                       options=[],
                                                                       value=[],

                                                                       style={
                                                                           'margin-bottom': '10px',
                                                                           'margin-right': '10px',
                                                                           'width': '100%',
                                                                           'color': '#000000',
                                                                           'font-size': 15
                                                                       }
                                                                   )], style={'display': 'none'})
                              , md=2)

                             ,

                          ]),
                 dbc.Row(
                     [
                         dbc.Col(dcc.Graph(id="cluster-graph", figure={}))
                     ],
                     align="center",
                 ),

                 dbc.Row(
                     dbc.Col(dcc.Graph(id="histogram_dist", figure={}))
                 ),

                 dbc.Row(
                     [
                         dbc.Col(dcc.Graph(id="Volt-Corr", figure={}))
                     ],
                     align="center",
                 )
                    ,
                 dbc.Row(
                     [
                         dbc.Col(dcc.Graph(id="Volt-Corr2", figure={}, style={'display': 'none'}))
                     ],
                     align="center",
                 )
                    , html.Br(),

                 html.Div(children=[
                     dbc.Row(children=[
                         dbc.Col(children=[
                             dbc.Row(children=[dbc.Col(html.H1("Curva IV"), md=12)]),
                             dbc.Row(children=[
                                 dbc.Col(input.M_IV(), md=12)
                             ]),
                             dbc.Row(children=[
                                 dbc.Col(html.Div([
                                     html.H4("Meses del año"),
                                     dbc.Label("Mes"),
                                     dcc.RangeSlider(
                                         id='my-range-slider-IV',
                                         min=1,
                                         max=12,
                                         step=1,
                                         value=[1, 12],
                                         marks={i: {'label': meses[i], 'style': slider_marks_style} for i in
                                                range(1, 13)},
                                         allowCross=False
                                     ),
                                     html.Div(id='output-container-range-slider-IV', style={'margin-top': '50px'})
                                 ]), md=12)
                             ]),

                             ### Tabla para camnbio de temperaturas.
                             dbc.Row(html.Div(id="IV_Tabla_Selector", children=[

                                 dbc.Row(children=[dbc.Col(
                                     dash_table.DataTable(
                                         id='loading-states-table',
                                         columns=[

                                             {'name': 'Irradiancia Específica W/m2', 'id': 'irradiancia',
                                              'deletable': False, 'renamable': False},
                                             {'name': 'Temperatura C°', 'id': 'temperatura', 'deletable': False,
                                              'renamable': False}
                                         ],
                                         data=[
                                             {'irradiancia': float(irr), 'temperatura': float(temp)} for irr, temp in
                                             cases
                                         ],
                                         editable=True,
                                         row_deletable=True
                                         ,
                                         style_data={
                                             'color': 'black',
                                             'backgroundColor': 'white'
                                         },
                                         style_data_conditional=[
                                             {
                                                 'if': {'state': 'active'},  # Cuando una celda es seleccionada
                                                 'backgroundColor': '#ADD8E6',  # Azul claro
                                                 'border': '1px solid #ADD8E6'
                                             }
                                         ],
                                         style_header={
                                             'backgroundColor': 'rgb(210, 210, 210)',
                                             'color': 'black',
                                             'fontWeight': 'bold'
                                         },
                                         page_action="native",
                                         page_current=0,
                                         page_size=10,
                                         style_table={'width': '100%', 'overflowX': 'auto', 'maxHeight': '500px',
                                                      'overflowY': 'auto'},
                                         style_cell={
                                             'minWidth': '100px', 'maxWidth': '200px',
                                             'whiteSpace': 'normal',
                                             'textAlign': 'center'
                                         },
                                         css=[{
                                             'selector': '.dash-spreadsheet-container .pagination',
                                             'rule': 'text-align: center;'
                                         }]

                                     ), md=12)

                                 ])

                                 , html.Br()
                                 , html.Button('Agregar Fila', id='add-column-button', n_clicks=0)

                                 # aquiii
                             ], style={'display': 'none'}))

                         ], md=3), dbc.Col(md=1),  # Ajusta el tamaño de la columna según sea necesario
                         dbc.Col(html.Div(id="PE-IV"), md=7)
                         # Primer tabla, esta siempre esta visible ya que toda condicion es suficiente para su aparicion.
                     ]),
                     html.Div(id="IV-Tab2", children=[
                         dbc.Row(children=[
                             dbc.Col(md=4),
                             dbc.Col(html.Div(id="PE-IV2"), md=7)  ## Segunda tabla para cuando seleccionas dos modulos.
                         ])
                     ], style={'display': 'none'}), html.Br(),

                     ### Esta es el div, que se utiliza para poder hacer la parte de integración por datos.
                     html.Div(id="IV_BASE", children=[
                         dbc.Col(
                             dcc.Upload(
                                 id='upload-data',
                                 children=html.Div([
                                     'Drag and Drop or ',
                                     html.A('Select Files')
                                 ]),
                                 style={
                                     'width': '100%',
                                     'height': '60px',
                                     'lineHeight': '60px',
                                     'borderWidth': '1px',
                                     'borderStyle': 'dashed',
                                     'borderRadius': '5px',
                                     'textAlign': 'center',
                                     'margin': '10px'
                                 }
                                 ,
                                 multiple=False
                             ))
                         ,
                         dbc.Row([
                             dbc.Col(html.Div(id='output-data-upload'), width=14)
                         ]),
                         html.Br()
                         ,
                         dbc.Row(input.correcion_IV())
                         ,

                         dbc.Col(html.H1("Condiciones de la Medición")),
                         dbc.Col(children=[dbc.InputGroup(
                             [dbc.InputGroupText("Irradiancia "),
                              dbc.Input(id="Irradiancia_IV", placeholder="W/m2", value=0)],
                             className="mb-3",
                         ),
                             dbc.Col(dbc.InputGroup(
                                 [dbc.InputGroupText("Temperatura"),
                                  dbc.Input(id="Temperatura_IV", placeholder="C°", value=0)],
                                 className="mb-3",
                             ))
                         ], md=3)
                         ,

                     ], style={'display': 'block'})  ## Esto solo hace display cuando de

                     ,
                     html.Br()
                     ,
                     html.Div(
                         id="TdM",
                         # con esto lo mandas a llamar para que solo se muestre cuando se seleccione el meotod de comparacion y para un modulo.
                         children=[dbc.Row(children=[

                             dbc.Col(children=[html.H4("Seleccion de metodo"),
                                               dcc.Dropdown(
                                                   id="Tipo_d_Metodo",
                                                   options=[
                                                       {'label': html.Span(['Metodo 2'],
                                                                           style={'color': 'Black', 'font-size': 15}),
                                                        'value': 'M2'},

                                                       {'label': html.Span(['Metodo 2 actulizado'],
                                                                           style={'color': 'Black', 'font-size': 15}),
                                                        'value': 'M2N'}
                                                   ]
                                               )]
                                     , md=2),
                             dbc.Col(children=[html.H4("Seleccion tipo de Medicion"),
                                               dcc.Dropdown(
                                                   id="Tipo_d_Medicion",
                                                   options=[
                                                       {'label': html.Span(['Mostrar datos completos'],
                                                                           style={'color': 'Black', 'font-size': 15}),
                                                        'value': 'Completos'},

                                                       {'label': html.Span(['Mostrar datos promedio'],
                                                                           style={'color': 'Black', 'font-size': 15}),
                                                        'value': 'Promedio'}
                                                   ]
                                               )]
                                     , md=2),
                             dbc.Col(children=[html.H4("Accion:"),
                                               dcc.Dropdown(
                                                   id="Tipo_d_Analisis",
                                                   options=[
                                                       {'label': html.Span(['Corregir datos medidos'],
                                                                           style={'color': 'Black', 'font-size': 15}),
                                                        'value': 'Medidos'},

                                                       {'label': html.Span(['Simular datos y corregirlos'],
                                                                           style={'color': 'Black', 'font-size': 15}),
                                                        'value': 'Simulados'},
                                                       {'label': html.Span(['Corregir Simulacion y Datos medidos'],
                                                                           style={'color': 'Black', 'font-size': 15}),
                                                        'value': 'Simu_Med'}
                                                   ]
                                               )]
                                     , md=2)
                         ]
                         )
                         ]
                         ,
                         style={"display": "none"}
                     ), html.Br()
                     ,
                     dbc.Row(dcc.Graph(id="IV-G0C", figure={}, style={'display': 'none'})),
                     dbc.Row(dcc.Graph(id="IV-G0C1", figure={}, style={'display': 'none'}))

                     ,
                     dbc.Row(dcc.Graph(id="IV-G0", figure={}, style={'display': 'block'})),
                     html.Br(),
                     dbc.Row(dcc.Graph(id="IV-G02C", figure={}, style={'display': 'none'}))
                     ,
                     dbc.Row(dcc.Graph(id="IV-G02", figure={}, style={'display': 'none'})),
                     dcc.Store(id="Tabla_Info"),dcc.Store(id="Tabla_Info_m"),dcc.Store(id="Tabla_Info_s"),dcc.Store(id="Tablarm"),dcc.Store(id="Tablars"),
                     # Se necesitan dos outputs el de visibilidad y el de la figura
                     html.Div(html.Div(id='Table_Type',children=[dbc.Row(children=[
                                            dbc.Col(children=[html.H4("Seleccion de metodo"),
                                                                                           dcc.Dropdown(
                                                                                               id="Table_Selection",
                                                                                               options=[
                                                                                                   {'label': html.Span(['Medicion'],
                                                                                                                       style={'color': 'Black', 'font-size': 15}),
                                                                                                    'value': 'Med_i'},

                                                                                                   {'label': html.Span(['Simulacion'],
                                                                                                                       style={'color': 'Black', 'font-size': 15}),
                                                                                                    'value': 'Sim_u'},

                                                                                                    {'label': html.Span(['Medicion vs Simulacion'],
                                                                                                                       style={'color': 'Black', 'font-size': 15}),
                                                                                                    'value': 'Med_i/Sim_u'}
                                                                                               ]
                                                                                               ,value=0
                                                                                           )]
                                                                                 , md=2)
                     ])], style={"display": "none"}))
                     ,
                     html.Div(html.Div(id='IV_CI_Table', style={"display": "none"})),
                     html.Div(html.Div(id='IV_CI_TableC', style={"display": "none"})),
                     html.Div(html.Div(id='IV_CI_Table2C', style={"display": "none"})),# Este es el input para la tabla.
                     html.Div(html.Div(id='IV_CI_Table2', style={"display": "none"})),
                     html.Div(id="Real_Average_s",children=[
                         dbc.Label(
                             "Curva representativa: El proceso de comprobacion sirve  mejor mientras mas mediciones se hace. Minimo 5, pero no se garantiza"
                             "un resultado bueno, 10 mediciones es un poco mejor, pero si se pueden realizar 30 o mas es perfecto. Esto por la metodologia"
                             "que se utiliza para obtener la curva representativa."),
                         dbc.Checklist(
                             options=[
                                 {"label": "Curva representativa", "value": 1},
                                 {"label": "Sin curva representativa", "value": 2}
                             ],
                             value=[2],
                             id="Real_Average"
                            ),html.Div(html.Div(id='IV_CI_TableRm', style={"display": "none"})),
                             html.Div(html.Div(id='IV_CI_TableRs', style={"display": "none"})), # CÓDIGO CORREGIDO
                            html.Div(
                            dcc.Graph(id="IV-RP", figure={},style={'display': 'none'}),  # Ya no necesitas el style aquí
                            id="contenedor-grafica-rp",       # <-- 1. ID para el marco
                            style={'display': 'none'}        # <-- 2. Oculta el marco por defecto
                                         )
                                ],style={"display": "none"}),
                            html.Div(
                            dcc.Graph(id="IV-RP2", figure={},style={'display': 'none'}),  # Ya no necesitas el style aquí
                            id="contenedor-grafica-rp2",       # <-- 1. ID para el marco
                            style={
                                    'display': 'none',
                                    'height': '0',
                                    'padding': '0',
                                    'margin': '0',
                                    'border': 'none'}     # <-- 2. Oculta el marco por defecto
                                         )



                     , html.Br(), html.Br(), html.Br(),
                     html.Br(), html.Br(), html.Br(), html.Br()
                 ])

                 ], color="Dark"),  ##DBC Card Close parenthesys
        ],
        fluid=True,  ##DBC Card Close parenthesys
    )

    ])

])


# Callback que escucha el valor del dropdown y actualiza la visibilidad de los inputs
@app.callback(
    [Output('inputs-container', 'style'),
     Output('Pm', 'value'),
     Output('Vm', 'value'),
     Output('Im', 'value'),
     Output('Voc', 'value'),
     Output('Isc', 'value'),
     Output('Alpha', 'value'),
     Output('Beta', 'value'),
     Output('Gamma', 'value'),
     Output('CS', 'value'),
     Output('T', 'value'),
     Output('monosi', 'value'),
     Output('Prueba', 'data')
     ],
    Input('selection-dropdown', 'value')
)
def toggle_inputs(selected_value):
    if selected_value == 'SELEC':
        Prueba = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "polySi")
        Pot, Vm, Im, Voc, Isc, alpha, beta, gamma, Numero_celda, Tempref, Tc
        return {'display': 'block'}, Pot, Vm, Im, Voc, Isc, alpha, beta, gamma, Numero_celda, Tempref, Tc, Prueba
    if selected_value == 'INSERT':
        return {'display': 'block'}, "", "", "", "", "", "", "", "", "", "", "", []
    if selected_value == "CEC":
        return {'display': 'none'}, "", "", "", "", "", "", "", "", "", "", "", []




    else:
        return {'display': 'none'}


# App call back para la creacion de la tabla del clima.

@app.callback(
    Output('filter_selector', 'style'),
    Input('selection-dropdown', 'value')
)
def filter_data(Data_base):
    if Data_base == 'CEC':
        return {'display': 'block'}
    return {'display': 'none'}


## Funcion para la creacion de las listas de los valores del modulo:

@app.callback(
    [Output("loading", "children"),
     Output("D1", 'style'),
     Output('Drop_1', 'options'),
     Output('Etiqueta', 'children'),
     Output("D2", 'style'),  # potencia
     Output('Drop_2', 'options'),
     Output('Etiqueta2', 'children'),
     Output("D3", 'style'),  # modelo
     Output('Drop_3', 'options'),
     Output('Etiqueta3', 'children'),
     Output("D4", 'style'),
     Output('Drop_4', 'options'),  # marca
     Output('Etiqueta4', 'children')]
    ,
    [Input('filter_selector_', 'value'),
     Input('selection-dropdown', 'value')
     ]
)
def shower_list(data_bases, k):
    if k == 'SELEC' or k == 'INSERT':
        return [], {'display': 'none'}, [], "", {'display': 'none'}, [], "", {'display': 'none'}, [], "", {
            'display': 'none'}, [], ""
    m = input.creador_de_filtros(data_bases)
    return m


# funcion para regresar los dataframes filtrados:

@app.callback(

    [Output('Table_modulos_base', 'data'),
     Output('Table_modulos_base', 'columns'),
     Output('Tabla_modulos', 'style'),
     Output("loading-2", "children")]

    ,
    [Input('Etiqueta', 'children'),
     Input('Etiqueta2', 'children'),
     Input('Etiqueta3', 'children'),
     Input('Etiqueta4', 'children'),
     Input('Drop_1', 'value'),  #
     Input('Drop_2', 'value'),  # Potencia
     Input('Drop_3', 'value'),  # modelo
     Input('Drop_4', 'value'),  # marca
     Input('selection-dropdown', 'value')
     ])
def data_handler(A1, A, B, C, F, G, H, J, k):
    # Convertir las entradas a listas si no lo son
    if k == 'SELEC' or k == 'INSERT':
        return [], [], {'display': 'none'}, []
    if isinstance(G, str):
        G = [G]
    if isinstance(H, str):
        H = [H]
    if isinstance(J, str):
        J = [J]

    # Cargar el archivo Excel una vez
    l = pd.read_excel("Libro1.xlsx")

    # Filtrar por "Potencia Modulo"
    if A1 == "Potencia Modulo" and A == "" and B == "" and C == "":
        df_filtrado = l.loc[l["Nameplate Pmax"].isin(F)]
    # Filtrar por "Modelo"
    elif A1 == "Modelo" and A == "" and B == "" and C == "":
        df_filtrado = l.loc[l["Model Number"].isin(F)]
    # Filtrar por "Marca"
    elif A1 == "Marca" and A == "" and B == "" and C == "":
        df_filtrado = l.loc[l["Manufacturer"].isin(F)]
    # Filtrar por "Potencia Modulo" y "Modelo"
    elif A == "Potencia Modulo" and B == "Modelo" and C == "" and A1 == "":
        df_filtrado = l.loc[
            l["Nameplate Pmax"].isin(G) &
            l["Model Number"].isin(H)
            ]
    # Filtrar por "Potencia Modulo" y "Marca"
    elif A == "Potencia Modulo" and C == "Marca" and A1 == "" and B == "":
        df_filtrado = l.loc[
            l["Nameplate Pmax"].isin(G) &
            l["Manufacturer"].isin(J)
            ]
    # Filtrar por "Potencia Modulo", "Modelo" y "Marca"
    elif A == "Potencia Modulo" and B == "Modelo" and C == "Marca" and A1 == "":
        df_filtrado = l.loc[
            l["Nameplate Pmax"].isin(G) &
            l["Manufacturer"].isin(J) &
            l["Model Number"].isin(H)
            ]
    else:
        # Retornar una tabla vacía si no se cumple ninguna condición
        return [], [], {'display': 'none'}, dcc.Loading([html.Div(id="loading-output")])

    # Convertir los datos filtrados en el formato requerido
    columns = [
        {"name": i, "id": i, "deletable": True, "selectable": True} for i in df_filtrado.columns
    ]
    data = df_filtrado.to_dict('records')

    return data, columns, {'display': 'block'}, dcc.Loading([html.Div(id="loading-output")])


## Selection feynman techniqes.
# aqui es donde tengo que meter lo de la temperatura NOCT.
## Aqui puedes tomar el selector de metodo de temperatura que quieres.
# es impoortante que uses esta parte ya que auqi, sera donde puedas dividir la graficas para cuando sea temperatura feinman y no .

@app.callback([Output("Posicion_Mod", "style"), Output("TA_M", "style")],
              Input("Posicion_Mod", "value")
              )
def angles_show(Pos):
    if Pos == 'Pos_i':
        return {"display": "block"}, {"display": "none"}

    if Pos == 'Pos_e':
        return {"display": "block"}, {"display": "block"}

    return {"display": "block"}, {"display": "none"}


@app.callback(
    [Output("tables-container", "children"),
     Output("loading-demo", "children"),
     Output('output-div', 'children'),

     Output("feinman", 'style'),
     Output("sandia", 'style'),
     Output('store-ndh', 'data'),
     Output("NOCT", "style")

     ],
    [Input('Latitude', 'value'),
     Input('Longitude', 'value'),
     Input('Tipo_A', 'value'),
     Input('Years_Selected', 'value'),
     Input('Diferencial de tiempo', 'value'),
     Input('checklist-input', 'value'),
     Input("sandia", 'style'),
     Input("radio-sandia", 'value'),
     Input("feinman", 'style'),
     Input("U_1", 'value'),
     Input("U_0", 'value'),
     Input("noct", "value"),
     Input("Posicion_Mod", "value"),
     Input("tilt", "value"),
     Input("azimuth", "value")]
)
def clima(lat, lon, A, tiempos, intervalos, selected_methods, sandia_style, Sandia, feinman_style, U1, U0, Noct, Pos,
          tilt, azimuth):
    global tables

    # Default values to be returned
    tables = []
    loading_component = dcc.Loading([html.Div(id="loading-output")])
    result = "Please select at least one method."
    style_feinman = {'display': 'none'}
    style_sandia = {'display': 'none'}
    style_NOCT = {'display': 'none'}
    components = []
    NDH_o = []
    # Ensure required inputs are provided
    if not lat or not lon:
        return tables, loading_component, result, style_feinman, style_sandia, NDH_o, style_NOCT

    # Check if at least one method is selected
    if not selected_methods:
        return tables, loading_component, result, style_feinman, style_sandia, NDH_o, style_NOCT

    # Handle method-specific logic
    result_list = []

    if 1 in selected_methods:
        result_list.append("Feinman method selected.")
        style_feinman = {'display': 'block'}

    if 2 in selected_methods:
        result_list.append("Sandia method selected.")
        style_sandia = {'display': 'block'}

    if 3 in selected_methods:
        result_list.append("NOCT method selected.")
        style_NOCT = {'display': 'block'}

    if result_list:
        result = html.Ul([html.Li(method) for method in result_list])

    # Ensure Tipo_A is provided before proceeding
    if not A:
        return tables, loading_component, result, style_feinman, style_sandia, NDH_o, style_NOCT

    # Fetch climate data based on input values after method selection
    NDH = None
    if A == "SY" and tiempos and intervalos:
        NDH = pf.Clima(lat, lon, A, tiempos, intervalos)  # esta funcion descarga los climas.

    elif A == "TMY":
        NDH = pf.Clima(lat, lon, A, 0, 0)  # Esta la funcion que descarga los climas.

    if NDH:
        if Pos == 'Pos_i':
            CLC = cl.clc(NDH)
            Effective_irradiance = ps.Solar_pos(NDH, lat, lon)

        if Pos == 'Pos_e':
            CLC = cl.clc(NDH)
            Effective_irradiance = ps.Solar_pos_e(NDH, lat, lon, tilt, azimuth)

    # Process temperature calculations if NDH is available
    if NDH:
        if 1 in selected_methods and feinman_style is not None and U1 > 0 and U0 > 0:
            Temperaturas = input.Temperature_feinman(U0, U1, NDH)

        if 2 in selected_methods and Sandia is not None and Sandia > 0:
            Temperaturas = input.Temperature_sandia(Sandia, NDH)

        if 3 in selected_methods:
            Temperaturas = input.Temperature_NOCT(float(Noct), NDH)

        # Generate tables if NDH is available and valid
        if A == "SY":
            tables = input.table_e(NDH)
            NDH_o = input.creador_csv_clima(NDH)




        elif A == "TMY":
            tables = input.TMY(NDH)
            NDH_o = input.creador_csv_clima(NDH)

    return tables, loading_component, result, style_feinman, style_sandia, NDH_o, style_NOCT


##### Dev_muestra que año seleccionaste:
@app.callback(
    [Output("CY", "style"),
     Output("Time", "style")],
    Input("Tipo_A", "value")
)
# Listen for changes to the Tipo_A dropdown:

def update_year_dropdown_visibility(selected_type):
    if selected_type == "SY":
        return {'display': 'block'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'none'}  # Always return a dictionary for the style, never None


# Muestra el html div, que muestre las opciones de contenido para la base de datos.
###Base de datos obtenida de los modulos. Aqui se muestra los datos seleccionados del modulo que se ocupo.
@app.callback(
    [Output('datos Modulos', 'style'),
     Output('Tab One', 'style'),
     Output('Tab Two', 'style'),
     Output('tabs-content-example-graph', 'children'),
     Output('Database1', 'data'),
     Output('Database2', 'data')],
    [Input('Table_modulos_base', "derived_virtual_selected_rows"),
     Input('tabs-example-graph', 'value'),
     Input('Table_modulos_base', "derived_virtual_selected_rows"),
     Input('Table_modulos_base', 'data'),
     Input('Table_modulos_base', 'columns')
     ]
)
def render_content(rows, tab, actual_r, data, columns):
    # Verificar si 'rows' es None y asignar una lista vacía si es necesario
    if rows is None:
        rows = []

    # Inicializar estilos y contenido por defecto
    datos_modulos_style = {'display': 'none'}
    tab_one_style = {'display': 'none'}
    tab_two_style = {'display': 'none'}
    content = html.Div()
    Database_1 = []
    Database_2 = []
    # Mostrar el contenedor si se seleccionan filas
    if len(rows) > 0:
        datos_modulos_style = {'display': 'block'}

    # Determinar qué tab mostrar según la longitud de las filas seleccionadas
    if len(rows) == 1:
        tab_one_style = {'display': 'block'}
        if tab == 'tab-1-example-graph':
            for i in actual_r:
                content = html.Div([
                    html.H3('Modulo 1'),
                    input.table_module_b(
                        data[i]['Nameplate Pmax'],
                        data[i]['Nameplate Vpmax'],
                        data[i]['Nameplate Ipmax'],
                        data[i]['Nameplate Voc'],
                        data[i]['Nameplate Isc'],
                        data[i]['αIsc'],
                        data[i]['βVoc'],
                        data[i]['γPmax'],
                        data[i]['N_s'],
                        data[i]['Average NOCT'],
                        data[i]['Technology'])])

                Database_1 = [data[i]['Nameplate Pmax'],
                              data[i]['Nameplate Vpmax'],
                              data[i]['Nameplate Ipmax'],
                              data[i]['Nameplate Voc'],
                              data[i]['Nameplate Isc'],
                              data[i]['αIsc'],
                              data[i]['βVoc'],
                              data[i]['γPmax'],
                              data[i]['N_s'],
                              data[i]['Average NOCT'],
                              data[i]['Technology']]

    elif len(rows) == 2:

        tab_one_style = {'display': 'block'}
        tab_two_style = {'display': 'block'}
        if tab == 'tab-1-example-graph':
            content = html.Div([
                html.H3('Modulo 1'),
                input.table_module_b(
                    data[actual_r[0]]['Nameplate Pmax'],
                    data[actual_r[0]]['Nameplate Vpmax'],
                    data[actual_r[0]]['Nameplate Ipmax'],
                    data[actual_r[0]]['Nameplate Voc'],
                    data[actual_r[0]]['Nameplate Isc'],
                    data[actual_r[0]]['αIsc'],
                    data[actual_r[0]]['βVoc'],
                    data[actual_r[0]]['γPmax'],
                    data[actual_r[0]]['N_s'],
                    data[actual_r[0]]['Average NOCT'],
                    data[actual_r[0]]['Technology']
                )
            ])
            Database_1 = [data[actual_r[0]]['Nameplate Pmax'],
                          data[actual_r[0]]['Nameplate Vpmax'],
                          data[actual_r[0]]['Nameplate Ipmax'],
                          data[actual_r[0]]['Nameplate Voc'],
                          data[actual_r[0]]['Nameplate Isc'],
                          data[actual_r[0]]['αIsc'],
                          data[actual_r[0]]['βVoc'],
                          data[actual_r[0]]['γPmax'],
                          data[actual_r[0]]['N_s'],
                          data[actual_r[0]]['Average NOCT'],
                          data[actual_r[0]]['Technology']]

            Database_2 = [data[actual_r[1]]['Nameplate Pmax'],
                          data[actual_r[1]]['Nameplate Vpmax'],
                          data[actual_r[1]]['Nameplate Ipmax'],
                          data[actual_r[1]]['Nameplate Voc'],
                          data[actual_r[1]]['Nameplate Isc'],
                          data[actual_r[1]]['αIsc'],
                          data[actual_r[1]]['βVoc'],
                          data[actual_r[1]]['γPmax'],
                          data[actual_r[1]]['N_s'],
                          data[actual_r[1]]['Average NOCT'],
                          data[actual_r[1]]['Technology']]

        elif tab == 'tab-2-example-graph':
            content = html.Div([
                html.H3('Modulo 2'),
                input.table_module_b2(
                    data[actual_r[1]]['Nameplate Pmax'],
                    data[actual_r[1]]['Nameplate Vpmax'],
                    data[actual_r[1]]['Nameplate Ipmax'],
                    data[actual_r[1]]['Nameplate Voc'],
                    data[actual_r[1]]['Nameplate Isc'],
                    data[actual_r[1]]['αIsc'],
                    data[actual_r[1]]['βVoc'],
                    data[actual_r[1]]['γPmax'],
                    data[actual_r[1]]['N_s'],
                    data[actual_r[1]]['Average NOCT'],
                    data[actual_r[1]]['Technology']
                )
            ])

    return datos_modulos_style, tab_one_style, tab_two_style, content, Database_1, Database_2


### Siguiente paso obtencion de temperatura Feynmann, Sandia y NOCt, para el modulo que se halla selecciondo
### Asi tambien obtener los parametros electricos para poder graficarlos.
### Al final que se de la opcion de descargar los generados de clima y del modulo.

@app.callback(
    Output('map', 'center'),
    Output('marker', 'position'),
    Input('Latitude', 'value'),
    Input('Longitude', 'value')
)
def update_map_center(latitud, longitud):
    if latitud is None or longitud is None:
        raise PreventUpdate
    return [latitud, longitud], [latitud, longitud]


# Callback para manejar la lógica de selección
@app.callback(
    Output('output-div_1', 'children'),
    [Input("checklist-input", 'value'),
     Input('store-ndh', 'data')]
)
def use_ndh(Seleccion, nombre):
    datos = []
    if Seleccion == [1]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            l = l.rename(index={"Unnamed: 0": 'Tiempo'})
            l = l.set_index("Unnamed: 0")
            l.index.names = ['Tiempo']
            l = l.drop(['Year', 'Month', 'Day', 'Hour', 'Minute'], axis=1)
            datos.append(l)


## Parametros electricos obtencion de los parametros electricos del modulo.Aqui se muestran las tablas para los parametros electricos

@app.callback(
    [Output('PE-TMY', "children"),  ## Aqui es lo que imprime la tabla
     Output('PE-SY', "children"),
     Output("Datos_PE", "data"),  ##Estos valores me dan el nombre del CSV
     Output('Datos_PE2', "data")  ## Esto es de vital importancia , ya que es  lo que me permite usarlos.
     ],
        [
        Input('selection-dropdown', 'value'),
        Input('Pm', 'value'),
        Input('Vm', 'value'),
        Input('Im', 'value'),
        Input('Voc', 'value'),
        Input('Isc', 'value'),
        Input('Alpha', 'value'),
        Input('Beta', 'value'),
        Input('Gamma', 'value'),
        Input('CS', 'value'),
        Input('T', 'value'),
        Input('monosi', 'value'),
        Input('Database1', 'data'), #Estos son los data base que hacen las operaciones,cel CEC
        Input('Database2', 'data'), #Estos son los data base que hacen las operaciones,cel CEC
        Input('Table_modulos_base', "derived_virtual_selected_rows"),
        Input("checklist-input", 'value'),
        Input('store-ndh', 'data'),
        Input("noct", "value")
        ])
# Aqui tengo que poner lo del modelo Sandia como seleccion unica. Tambien tengo que habilitar la parte en la cual se comparan los dos modelos.

def electric_parameters(selected_value, Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                        temp_ref, celltype, D1, D2, rows, Seleccion, nombre, NOCT):
    tables1 = []
    tables2 = []

    if selected_value == 'SELEC':
        if Seleccion == [1] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
            Ndh = input.df_creator(nombre, Seleccion)  ## NDH es el dataframe, tambien uso el nombre t,df,datos
            PE1 = input.PE(Prueba, Ndh)
            Pe_CSV = input.creador_csv_PE(PE1)

            tables1 = input.table_PE1(PE1, nombre)
            print(Pe_CSV)  ## Creador de los CSV y da los nombres
            print("Bien ahi compa")
            return tables1, [], Pe_CSV, []

        if Seleccion == [1, 2] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_t(Prueba, Ndh)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)
            return tables1, [], Pe_CSV, []

        if Seleccion == [2] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_t_S(Prueba, Ndh)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)
            return tables1, [], Pe_CSV, []

        if Seleccion == [3] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_NOCT(Prueba, Ndh, Seleccion)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)
            return tables1, [], Pe_CSV, []

        if Seleccion == [1, 3] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_NOCT(Prueba, Ndh, Seleccion)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)
            return tables1, [], Pe_CSV, []

        if Seleccion == [2, 3] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_NOCT(Prueba, Ndh, Seleccion)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)
            return tables1, [], Pe_CSV, []

        if Seleccion == [1, 2, 3] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_NOCT(Prueba, Ndh, Seleccion)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)

            return tables1, [], Pe_CSV, []

    if selected_value == 'INSERT':

        if Seleccion == [1] and len(nombre) > 0:
            Selector = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                                          temp_ref, celltype)
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE(Selector, Ndh)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)

            return tables1, [], Pe_CSV, []

        if Seleccion == [1, 2] and len(nombre) > 0:
            Selector = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                                          temp_ref, celltype)
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_t(Selector, Ndh)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)

            return tables1, [], Pe_CSV, []

        if Seleccion == [2] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                                        temp_ref, celltype)
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_t_S(Prueba, Ndh)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)
            return tables1, [], Pe_CSV, []

        if Seleccion == [3] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                                        temp_ref, celltype)
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_NOCT(Prueba, Ndh, Seleccion)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)
            return tables1, [], Pe_CSV, []

        if Seleccion == [1, 3] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                                        temp_ref, celltype)
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_NOCT(Prueba, Ndh, Seleccion)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)
            return tables1, [], Pe_CSV, []

        if Seleccion == [2, 3] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                                        temp_ref, celltype)
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_NOCT(Prueba, Ndh, Seleccion)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)
            return tables1, [], Pe_CSV, []

        if Seleccion == [1, 2, 3] and len(nombre) > 0:
            Prueba = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                                        temp_ref, celltype)
            Ndh = input.df_creator(nombre, Seleccion)
            PE1 = input.PE_NOCT(Prueba, Ndh, Seleccion)
            Pe_CSV = input.creador_csv_PE(PE1)
            tables1 = input.table_PE1(PE1, nombre)

            return tables1, [], Pe_CSV, []

    if selected_value == "CEC":

        if len(rows) == 2:

            Mod1 = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8], D1[9], D1[10])
            Mod2 = input.Placa_D2(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8], D2[9], D2[10])

            if Seleccion == [1] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                Mod2_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE(Mod1, Mod1_dat)
                PE2 = input.PE_1(Mod2, Mod2_dat)
                Pe_CSV = input.creador_csv_PE(PE1)
                Pe_CSV2 = input.creador_csv_PE2(PE2)
                tables1 = input.table_PE1(PE1, nombre)
                tables2 = input.table_PE2(PE2, nombre)

                return tables1, tables2, Pe_CSV, Pe_CSV2

            if Seleccion == [2] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                Mod2_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE_t_S(Mod1, Mod1_dat)  # PLaca,NDH
                PE2 = input.PE_t_S1(Mod2, Mod2_dat)
                Pe_CSV = input.creador_csv_PE(PE1)
                Pe_CSV2 = input.creador_csv_PE2(PE2)
                tables1 = input.table_PE1(PE1, nombre)
                tables2 = input.table_PE2(PE2, nombre)

                print(nombre)

                return tables1, tables2, Pe_CSV, Pe_CSV2

            if Seleccion == [1, 2] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                Mod2_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE_t(Mod1, Mod1_dat)
                PE2 = input.PE_t1(Mod2, Mod2_dat)
                Pe_CSV = input.creador_csv_PE(PE1)
                Pe_CSV2 = input.creador_csv_PE2(PE2)
                tables1 = input.table_PE1(PE1, nombre)
                tables2 = input.table_PE2(PE2, nombre)

                print(nombre)

                return tables1, tables2, Pe_CSV, Pe_CSV2

            if Seleccion == [3] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                Mod2_dat = input.df_creator(nombre, Seleccion)

                PE1 = input.PE_NOCT(Mod1, Mod1_dat, Seleccion)
                PE2 = input.PE_NOCT(Mod2, Mod2_dat, Seleccion)
                Pe_CSV = input.creador_csv_PE(PE1)
                Pe_CSV2 = input.creador_csv_PE2(PE2)
                tables1 = input.table_PE1(PE1, nombre)
                tables2 = input.table_PE2(PE2, nombre)

                return tables1, tables2, Pe_CSV, Pe_CSV2

            if Seleccion == [1, 3] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                Mod2_dat = input.df_creator(nombre, Seleccion)

                PE1 = input.PE_NOCT(Mod1, Mod1_dat, Seleccion)
                PE2 = input.PE_NOCT(Mod2, Mod2_dat, Seleccion)
                Pe_CSV = input.creador_csv_PE(PE1)
                Pe_CSV2 = input.creador_csv_PE2(PE2)
                tables1 = input.table_PE1(PE1, nombre)
                tables2 = input.table_PE2(PE2, nombre)

                return tables1, tables2, Pe_CSV, Pe_CSV2

            if Seleccion == [2, 3] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                Mod2_dat = input.df_creator(nombre, Seleccion)

                PE1 = input.PE_NOCT(Mod1, Mod1_dat, Seleccion)
                PE2 = input.PE_NOCT(Mod2, Mod2_dat, Seleccion)
                Pe_CSV = input.creador_csv_PE(PE1)
                Pe_CSV2 = input.creador_csv_PE2(PE2)
                tables1 = input.table_PE1(PE1, nombre)
                tables2 = input.table_PE2(PE2, nombre)

                return tables1, tables2, Pe_CSV, Pe_CSV2

            if Seleccion == [1, 2, 3] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                Mod2_dat = input.df_creator(nombre, Seleccion)

                PE1 = input.PE_NOCT(Mod1, Mod1_dat, Seleccion)
                PE2 = input.PE_NOCT(Mod2, Mod2_dat, Seleccion)
                Pe_CSV = input.creador_csv_PE(PE1)
                Pe_CSV2 = input.creador_csv_PE2(PE2)
                tables1 = input.table_PE1(PE1, nombre)
                tables2 = input.table_PE2(PE2, nombre)

                return tables1, tables2, Pe_CSV, Pe_CSV2

        if len(rows) == 1:

            Mod1 = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8], D1[9], D1[10])

            if Seleccion == [1] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE(Mod1, Mod1_dat)
                Pe_CSV = input.creador_csv_PE(PE1)
                tables1 = input.table_PE1(PE1, nombre)

                return tables1, [], Pe_CSV, []

            if Seleccion == [2] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE_t_S(Mod1, Mod1_dat)
                Pe_CSV = input.creador_csv_PE(PE1)
                tables1 = input.table_PE1(PE1, nombre)

                return tables1, [], Pe_CSV, []

            if Seleccion == [1, 2] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE_t(Mod1, Mod1_dat)
                Pe_CSV = input.creador_csv_PE(PE1)
                tables1 = input.table_PE1(PE1, nombre)

                return tables1, [], Pe_CSV, []

            if Seleccion == [3] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE_NOCT(Mod1, Mod1_dat, Seleccion)
                Pe_CSV = input.creador_csv_PE(PE1)
                tables1 = input.table_PE1(PE1, nombre)

                return tables1, [], Pe_CSV, []

            if Seleccion == [1, 3] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE_NOCT(Mod1, Mod1_dat, Seleccion)
                Pe_CSV = input.creador_csv_PE(PE1)
                tables1 = input.table_PE1(PE1, nombre)

                return tables1, [], Pe_CSV, []

            if Seleccion == [2, 3] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE_NOCT(Mod1, Mod1_dat, Seleccion)
                Pe_CSV = input.creador_csv_PE(PE1)
                tables1 = input.table_PE1(PE1, nombre)

                return tables1, [], Pe_CSV, []

            if Seleccion == [1, 2, 3] and len(nombre) > 0:
                Mod1_dat = input.df_creator(nombre, Seleccion)
                PE1 = input.PE_NOCT(Mod1, Mod1_dat, Seleccion)
                Pe_CSV = input.creador_csv_PE(PE1)
                tables1 = input.table_PE1(PE1, nombre)

                return tables1, [], Pe_CSV, []

    return tables1, tables2, [], []


## Las tablas ya contienen la temperatura NOCT
##
## Aqui se tiene que meter la tabla que se genera cuando son dos modulos.

### Creacion de graficas, se quiere una grafica donde se pueda comparar clima y parametros electricos
### por lo que la grafica debe de ser modificable par quitar y agregar informacion,segun plazca,
### Al usuario, en este  es importante que el usurario pueda seleccionar cuantos modulos quiere ver
### En el caso de ser mas un modelo y como quiero ver la informacion, ya que la informacion. Por esto mismo
### los inputs deben ser actulizables. La mayor cantidad de modulos que aparecen son dos, pero la cantidad
### De data frames, esta sujeto  a los tiempos y cantidad de tiempo seleccionado.

@app.callback(Output("output-column", "children"),
              [Input('selection-dropdown', 'value'),
               Input('Table_modulos_base', "derived_virtual_selected_rows")
               ]
              )
def Data_Base_selector(selected_value,
                       number_row):  # Esto lo que hace es  mostrar los Divs, queria que se mostrara mas opciones dependiendo  de la cantidad de modulos seleccionados, pero al final no lo use.
    ## La razon por la queno use este div, es porque preferi que siempre te muestra las informaciones cuando seleccionas mas de un modulo.
    ## Entonces no es necesario hacerlo asi, aun asi los inputs ya esta  y si en futuro se quieren cambiar, se puede cambiar.

    if selected_value == 'SELEC':
        return input.column_Pe()

    if selected_value == 'INSERT':
        return input.column_Pe()

    if selected_value == "CEC" and number_row:

        return input.column_Pe_CEC(number_row)


    else:

        return input.column_Pe()


# meter la opcionn de cuando es una base de datos, osea puede ser uno o dos modulos.
@app.callback([
    Output('Year-Time', "options"),
    Output("Grafica", "style"),
    Output('Column_Pe', "options"),
    Output('Year-Time_h', "options")
],
    [
        Input("Datos_PE", "data"),
        Input("Datos_PE2", "data"),
        Input('selection-dropdown', 'value')
    ]
)
def Graph_filter(nombres_Pe, nombres_Pe2, selected_value):
    opciones = []
    opciones2 = []

    if selected_value == 'SELEC' or selected_value == 'INSERT':
        if len(nombres_Pe) > 0 and len(nombres_Pe2) == 0:
            t = input.df_creator_1(nombres_Pe, [1])  # feynman method 1 module [1]

            for i in range(len(t)):
                nombre = f"Año {t[i].index.year.unique()[0]} [Horas: {len(t[i])}]"
                nombre2 = f"Año {t[i].index.year.unique()[0]} [Horas: {len(t[i])}]"
                opciones.append(nombre)
                opciones2.append(nombre2)

            if len(opciones) > 0:
                columns = [{'label': col, 'value': col} for col in t[0].columns.drop(["Year", "Month"])]
                style_columns = {'display': 'block'}
                return opciones, {'display': 'block'}, columns, opciones2
            else:
                return opciones, {'display': 'block'}, [], []

    if len(nombres_Pe) > 0 and len(nombres_Pe2) == 0:  ## Here  is where both names are created.

        t = input.df_creator_1(nombres_Pe, [1])  # feynman method 1 module [1]

        for i in range(len(t)):
            nombre = f"Año {t[i].index.year.unique()[0]} [Horas: {len(t[i])}]"
            nombre2 = f"Año {t[i].index.year.unique()[0]} [Horas: {len(t[i])}]"
            opciones.append(nombre)
            opciones2.append(nombre2)

        if len(opciones) > 0:
            columns = [{'label': col, 'value': col} for col in t[0].columns.drop(["Year", "Month"])]
            style_columns = {'display': 'block'}
            return opciones, {'display': 'block'}, columns, opciones2
        else:
            return opciones, {'display': 'block'}, [], []

    if len(nombres_Pe) > 0 and len(nombres_Pe2) > 0:

        t = input.df_creator_1(nombres_Pe, [1])  # feynman method 1 module [1]
        t2 = input.df_creator_1(nombres_Pe2, [1])  # feynman method 1 module [1]

        for i in range(len(t)):
            nombre = f"Año {t[i].index.year.unique()[0]} [Horas: {len(t[i])}]"
            nombre2 = f"Año {t[i].index.year.unique()[0]} [Horas: {len(t[i])}]"
            opciones.append(nombre)
            opciones2.append(nombre2)

        if len(opciones) > 0:
            columns = [{'label': col, 'value': col} for col in t[0].columns.drop(["Year", "Month"])]
            style_columns = {'display': 'block'}
            return opciones, {'display': 'block'}, columns, opciones2
        else:
            return opciones, {'display': 'block'}, [], []

        print("Vas bien")



    else:
        print("no")
        return opciones, {'display': 'none'}, [], []


@app.callback(
    [Output('cluster-graph', 'figure'),
     Output("histogram_dist", 'figure')],
    [Input("Datos_PE", "data"),
     Input("Datos_PE2", "data"),
     Input("Year-Time", "value"),
     Input('Column_Pe', "value"),
     Input('my-range-slider', "value")]
)
def update_graph(nombres_Pe, nombres_Pe2, graph_Year, graph_PE, Meses):
    fig = go.Figure()
    fig_hist = go.Figure()

    fig.update_layout(
        title='Parametros Electricos',
        xaxis_title='Fecha y Hora',
        yaxis_title='Valores',
        xaxis=dict(type='date'),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    fig_hist.update_layout(
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    meses = list(range(Meses[0], Meses[1] + 1))

    t = []
    t1 = []

    if graph_PE and graph_Year:
        if len(nombres_Pe2) > 0 and len(nombres_Pe) > 0:
            t = input.df_creator_1(nombres_Pe, [1])
            t1 = input.df_creator_1(nombres_Pe2, [1])
        if len(nombres_Pe) > 0 and len(nombres_Pe2) == 0:
            t = input.df_creator_1(nombres_Pe, [1])
            t1 = []
        if len(nombres_Pe2) > 0 and len(nombres_Pe) == 0:
            t = []
            t1 = input.df_creator_1(nombres_Pe2, [1])

        if len(t) > 0 and len(t1) == 0:
            for i, df in enumerate(t):
                for year in graph_Year:
                    if year in f"Año {df.index.year.unique()[0]} [Horas: {len(df)}]":
                        for column in graph_PE:
                            if column in df.columns:
                                opacity_value = random.uniform(0.5, 1)
                                filtered_df = df[df["Month"].isin(meses)]
                                info = filtered_df[column].replace(0, np.nan).dropna(how='any')

                                fig.add_trace(go.Scatter(
                                    x=info.index,
                                    y=info,
                                    mode='markers',
                                    name=f'{column}([{year}])',
                                    opacity=opacity_value
                                ))

                                info = df[df["Month"].isin(meses)]
                                info_df = info.replace(0, np.nan).dropna(how='any')

                                df_long = info_df.melt(value_vars=graph_PE, var_name='Parameter', value_name='Value')

                                fig_hist = px.histogram(df_long, x="Value", color="Parameter", marginal="box",
                                                        title=f"{graph_PE} de {year}", text_auto=True)
        if len(t) > 0 and len(t1) > 0:
            for (i1, df1), (i2, df2) in zip(enumerate(t), enumerate(t1)):
                for year in graph_Year:
                    if year in f"Año {df1.index.year.unique()[0]} [Horas: {len(df1)}]" or year in f"Año {df2.index.year.unique()[0]} [Horas: {len(df2)}]":
                        for column in graph_PE:
                            if column in df1.columns:
                                opacity_value = random.uniform(0.5, 1)
                                filtered_df1 = df1[df1["Month"].isin(meses)]
                                info1 = filtered_df1[column].replace(0, np.nan).dropna(how='any')

                                fig.add_trace(go.Scatter(
                                    x=info1.index,
                                    y=info1,
                                    mode='markers',
                                    name=f'{column}([Modulo 1:{year}])',
                                    opacity=opacity_value
                                ))

                                info1 = df1[df1["Month"].isin(meses)]
                                info_df = info1.replace(0, np.nan).dropna(how='any')

                                # Melt the DataFrame to long format
                                df_long = info_df.melt(value_vars=graph_PE, var_name='Parameter', value_name='Value')

                                fig_hist = px.histogram(df_long, x="Value", color="Parameter", marginal="box",
                                                        title=f"{graph_PE} de {year}", text_auto=True)

                            if column in df2.columns:
                                opacity_value = random.uniform(0.5, 1)
                                filtered_df2 = df2[df2["Month"].isin(meses)]
                                info2 = filtered_df2[column].replace(0, np.nan).dropna(how='any')

                                fig.add_trace(go.Scatter(
                                    x=info2.index,
                                    y=info2,
                                    mode='markers',
                                    name=f'{column}([Modulo 2:{year}])',
                                    opacity=opacity_value
                                ))

                                info2 = df1[df1["Month"].isin(meses)]
                                info1 = df2[df2["Month"].isin(meses)]
                                info1_df = info1.replace(0, np.nan).dropna(how='any')
                                info2_df = info2.replace(0, np.nan).dropna(how='any')

                                df_long = info1_df.melt(value_vars=graph_PE, var_name='Parametro',
                                                        value_name='Modulo1')
                                df1_long = info2_df.melt(value_vars=graph_PE, var_name='Parametro',
                                                         value_name='Modulo2')
                                dft = pd.concat([df_long, df1_long['Modulo2']], axis=1)
                                df_combined = dft.melt(id_vars=['Parametro'], value_vars=['Modulo1', 'Modulo2'],
                                                       var_name='Source', value_name='Valor')

                                # Crear el histograma combinado
                                fig_hist = px.histogram(
                                    df_combined,
                                    x="Valor",
                                    color="Parametro",
                                    facet_col="Source",
                                    marginal="box",
                                    title=f"Histograma de Modulo1 y Modulo2,{graph_PE} de {year} ",
                                    text_auto=True
                                )

        fig.update_layout(
            title='Parametros Electricos',
            xaxis_title='Fecha y Hora',
            yaxis_title='Valores',
            xaxis=dict(type='date'),
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white')
        )

        fig_hist.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white'),
            # Ancho de la gráfica
            height=650,  # Altura de la gráfica
            title_font_size=20  # Tamaño de la fuente del título
        )

    return fig, fig_hist


@app.callback(Output("IV_selector", "style"),
              [
                  Input("Datos_PE", "data"),
                  Input("Datos_PE2", "data"),
                  Input('Year-Time', "value"),
                  Input('Column_Pe', "value")

              ])
def Voltaje_Corriente_Selector(nombres_Pe, nombres_Pe2, Yt_h, Cp):
    if len(Yt_h) > 0 and len(Cp) > 0:

        return {'display': 'block'}

    else:

        return {'display': 'none'}


@app.callback([Output("Volt-Corr", 'figure'),
               Output("Volt-Corr2", 'style'),
               Output("Volt-Corr2", 'figure')],
              [Input("Datos_PE", "data"),
               Input("Datos_PE2", "data"),
               Input('Year-Time_h', "value"),  ## Estos son los inputs para seleccion
               Input('Column_Pe', "value"),  ## Con estos se permite extraer
               Input('my-range-slider', "value"),  ## Info especifica
               Input("checklist-input", 'value')])
def Voltaje_Corriente_Selector(nombres_Pe, nombres_Pe2, Yt_h, Cp, Meses, Seleccion):
    fig2 = go.Figure()
    fig3 = go.Figure()

    fig2.update_layout(
        xaxis_tickangle=30,
        title=dict(x=0.5),
        xaxis_tickfont=dict(size=9),
        yaxis_tickfont=dict(size=9),
        plot_bgcolor='black',  # Fondo del gráfico
        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
        font=dict(color='white')  # Color del texto
    )

    fig3.update_layout(
        xaxis_tickangle=30,
        title=dict(x=0.5),
        xaxis_tickfont=dict(size=9),
        yaxis_tickfont=dict(size=9),
        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
        font=dict(color='white')  # Color del texto
    )

    Yt_h = [Yt_h]
    meses = list(range(Meses[0], Meses[1] + 1))
    t = []
    t1 = []

    if len(nombres_Pe2) > 0 and len(nombres_Pe) > 0:
        t = input.df_creator_1(nombres_Pe, [1])
        t1 = input.df_creator_1(nombres_Pe2, [1])
    if len(nombres_Pe) > 0 and len(nombres_Pe2) == 0:
        t = input.df_creator_1(nombres_Pe, [1])
        t1 = []
    if len(nombres_Pe2) > 0 and len(nombres_Pe) == 0:
        t = []
        t1 = input.df_creator_1(nombres_Pe2, [1])

    if len(Yt_h) > 0:
        if len(t) > 0 and len(t1) == 0:
            print("DataFrames created:")

            for df in t:
                print("Processing DataFrame:")
                for year in Yt_h:
                    print("Processing year:", year)
                    if year == f"Año {df.index.year.unique()[0]} [Horas: {len(df)}]":
                        print("Year matches DataFrame")
                        for column in Cp:
                            print("Processing column:", column)
                            if column in df.columns:
                                print("Column found in DataFrame")

                                if Seleccion == [
                                    1]:  ## Tienes que modificar este para que sea solo para el metodo Feinman

                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    idF = df['Pmax_F'].idxmax()
                                    pot_F = df.loc[idF]['Pmax_F']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_F',
                                        y='Voc_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente{year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[idF]["Isc0_F"]],
                                        y=[df.loc[idF]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc y ISC"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]['Imax_F']],
                                        y=[df.loc[idF]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Potencia Max:<br>{pot_F}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                if Seleccion == [2]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    id_S = df['Pmax_S'].idxmax()
                                    pot_S = df.loc[id_S]['Pmax_S']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_S',
                                        y='Voc_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente{year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[id_S]["Isc0_S"]],
                                        y=[df.loc[id_S]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc y ISC"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_S]['Imax_S']],
                                        y=[df.loc[id_S]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Potencia Max:<br>{pot_S}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                if Seleccion == [1, 2]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    idS = df[
                                        'Pmax_S'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idF = df[
                                        'Pmax_F'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    # Se obteiene la potencia maxima en el voltaje maximo.
                                    pot_S = df.loc[idS]['Pmax_S']
                                    pot_F = df.loc[idF]['Pmax_F']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_S',
                                        y='Voc_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente{year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[idS]["Isc0_S"]],
                                        y=[df.loc[idS]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_S y ISC_S"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]["Isc0_F"]],
                                        y=[df.loc[idF]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_F y ISC_F"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idS]['Imax_S']],
                                        y=[df.loc[idS]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max Sandia:<br>{pot_S}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]['Imax_F']],
                                        y=[df.loc[idF]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Feinmann:<br>{pot_F}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                print("Returning figure 2")

                                if Seleccion == [3]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    id_NOCT = df['Pmax_NOCT'].idxmax()
                                    pot_NOCT = df.loc[id_NOCT]['Pmax_NOCT']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente{year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]["Isc0_NOCT"]],
                                        y=[df.loc[id_NOCT]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc y ISC"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]['Imax_NOCT']],
                                        y=[df.loc[id_NOCT]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Potencia Max NOCT:<br>{pot_NOCT}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    print("Returning Figure  NOCT")

                                if Seleccion == [1, 3]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    id_NOCT = df[
                                        'Pmax_NOCT'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idF = df[
                                        'Pmax_F'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    # Se obteiene la potencia maxima en el voltaje maximo.

                                    pot_NOCT = df.loc[id_NOCT]['Pmax_NOCT']
                                    pot_F = df.loc[idF]['Pmax_F']

                                    # para esta seleccion se debe de cambiar sandia por NOCT

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente{year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]["Isc0_NOCT"]],
                                        y=[df.loc[id_NOCT]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_NOCT y ISC_NOCT"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]["Isc0_F"]],
                                        y=[df.loc[idF]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_F y ISC_F"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]['Imax_NOCT']],
                                        y=[df.loc[id_NOCT]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max NOCT:<br>{pot_NOCT}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]['Imax_F']],
                                        y=[df.loc[idF]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Feinmann:<br>{pot_F}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                print("Returning figure NOCT and Feynman")

                                if Seleccion == [2, 3]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    idS = df[
                                        'Pmax_S'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    id_NOCT = df[
                                        'Pmax_NOCT'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    # Se obteiene la potencia maxima en el voltaje maximo.
                                    pot_S = df.loc[idS]['Pmax_S']
                                    pot_NOCT = df.loc[id_NOCT]['Pmax_NOCT']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_S',
                                        y='Voc_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente{year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[idS]["Isc0_S"]],
                                        y=[df.loc[idS]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_S y ISC_S"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]["Isc0_NOCT"]],
                                        y=[df.loc[id_NOCT]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_NOCT y ISC_NOCT"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idS]['Imax_S']],
                                        y=[df.loc[idS]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max Sandia:<br>{pot_S}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]['Imax_NOCT']],
                                        y=[df.loc[id_NOCT]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max NOCT:<br>{pot_NOCT}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                print("Returning figure 2")
                                if Seleccion == [1, 2, 3]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    idS = df[
                                        'Pmax_S'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    id_NOCT = df[
                                        'Pmax_NOCT'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    idF = df['Pmax_F'].idxmax()
                                    # Se obteiene la potencia maxima en el voltaje maximo.
                                    pot_S = df.loc[idS]['Pmax_S']
                                    pot_NOCT = df.loc[id_NOCT]['Pmax_NOCT']
                                    pot_F = df.loc[idF]['Pmax_F']

                                    # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    # Se obteiene la potencia maxima en el voltaje maximo.

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_S',
                                        y='Voc_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente{year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[idS]["Isc0_S"]],
                                        y=[df.loc[idS]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_S y ISC_S"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idS]["Isc0_F"]],
                                        y=[df.loc[idS]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_F y ISC_F"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]["Isc0_NOCT"]],
                                        y=[df.loc[id_NOCT]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_NOCT y ISC_NOCT"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idS]['Imax_S']],
                                        y=[df.loc[idS]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max Sandia:<br>{pot_S}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]['Imax_F']],
                                        y=[df.loc[idF]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max Feinman:<br>{pot_F}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]['Imax_NOCT']],
                                        y=[df.loc[id_NOCT]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max NOCT:<br>{pot_NOCT}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                print("Returning figure Feynamn,Sandia,NOCT")

                                return fig2, {'display': 'none'}, fig3

        if len(t) > 0 and len(t1) > 0:
            for df, df2 in zip(t, t1):
                year_str1 = f"Year {df.index.year.unique()[0]} [Hours: {len(df)}]"
                year_str2 = f"Year {df2.index.year.unique()[0]} [Hours: {len(df2)}]"
                for year in Yt_h:
                    if any(str(y) in year_str1 or str(y) in year_str2 for y in year):
                        for column in Cp:
                            if column in df.columns:
                                print("good job")

                                if Seleccion == [
                                    1]:  ## Tienes que modificar este para que sea solo para el metodo Feinman

                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    idF = df['Pmax_F'].idxmax()
                                    pot_F = df.loc[idF]['Pmax_F']

                                    df2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    idF2 = df2['Pmax_F'].idxmax()
                                    pot_F2 = df2.loc[idF2]['Pmax_F']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_F',
                                        y='Voc_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 1: {year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[idF]["Isc0_F"]],
                                        y=[df.loc[idF]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc y ISC"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]['Imax_F']],
                                        y=[df.loc[idF]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Potencia Max Modulo 1:<br>{pot_F}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    #############################################################

                                    fig3 = px.scatter(
                                        df2,
                                        x='Isc0_F',
                                        y='Voc_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 2 :{year}",
                                        marginal_x="box"
                                    )

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig3.add_scatter(
                                        x=[df2.loc[idF2]["Isc0_F"]],
                                        y=[df2.loc[idF2]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc y ISC"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idF2]['Imax_F']],
                                        y=[df2.loc[idF2]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Potencia Max Modulo 2:<br>{pot_F2}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                if Seleccion == [2]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    id_S = df['Pmax_S'].idxmax()
                                    pot_S = df.loc[id_S]['Pmax_S']

                                    df2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    id_S2 = df2['Pmax_S'].idxmax()
                                    pot_S2 = df2.loc[id_S2]['Pmax_S']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_S',
                                        y='Voc_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 1: {year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[id_S]["Isc0_S"]],
                                        y=[df.loc[id_S]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc y ISC"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_S]['Imax_S']],
                                        y=[df.loc[id_S]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Potencia Max:<br>{pot_S}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    ########################################################

                                    fig3 = px.scatter(
                                        df2,
                                        x='Isc0_S',
                                        y='Voc_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 2: {year}",
                                        marginal_x="box"
                                    )

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig3.add_scatter(
                                        x=[df2.loc[id_S2]["Isc0_S"]],
                                        y=[df2.loc[id_S2]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc y ISC"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[id_S2]['Imax_S']],
                                        y=[df2.loc[id_S2]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Potencia Max Modulo 2:<br>{pot_S2}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                if Seleccion == [1, 2]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    idS = df[
                                        'Pmax_S'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idF = df[
                                        'Pmax_F'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    # Se obteiene la potencia maxima en el voltaje maximo.
                                    pot_S = df.loc[idS]['Pmax_S']
                                    pot_F = df.loc[idF]['Pmax_F']

                                    df2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    idS2 = df2[
                                        'Pmax_S'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idF2 = df2[
                                        'Pmax_F'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    # Se obteiene la potencia maxima en el voltaje maximo.
                                    pot_S2 = df2.loc[idS2]['Pmax_S']
                                    pot_F2 = df2.loc[idF2]['Pmax_F']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_S',
                                        y='Voc_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 1: {year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[idS]["Isc0_S"]],
                                        y=[df.loc[idS]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_S y ISC_S"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]["Isc0_F"]],
                                        y=[df.loc[idF]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_F y ISC_F"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idS]['Imax_S']],
                                        y=[df.loc[idS]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max Sandia:<br>{pot_S}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]['Imax_F']],
                                        y=[df.loc[idF]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Feinmann:<br>{pot_F}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    #################################################################

                                    fig3 = px.scatter(
                                        df2,
                                        x='Isc0_S',
                                        y='Voc_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 2: {year}",
                                        marginal_x="box"
                                    )

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig3.add_scatter(
                                        x=[df2.loc[idS2]["Isc0_S"]],
                                        y=[df2.loc[idS2]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_S y ISC_S"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idF2]["Isc0_F"]],
                                        y=[df2.loc[idF2]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_F y ISC_F"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idS2]['Imax_S']],
                                        y=[df2.loc[idS2]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max Sandia Modulo 2:<br>{pot_S2}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idF2]['Imax_F']],
                                        y=[df2.loc[idF2]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Feinmann Modulo 2:<br>{pot_F2}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                print("Returning figure 2")

                                if Seleccion == [3]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    id_NOCT = df['Pmax_NOCT'].idxmax()
                                    pot_NOCT = df.loc[id_NOCT]['Pmax_NOCT']

                                    df2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    id_NOCT2 = df2['Pmax_NOCT'].idxmax()
                                    pot_NOCT2 = df2.loc[id_NOCT2]['Pmax_NOCT']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 1: {year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]["Isc0_NOCT"]],
                                        y=[df.loc[id_NOCT]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc y ISC"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]['Imax_NOCT']],
                                        y=[df.loc[id_NOCT]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Potencia Max:<br>{pot_NOCT}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    ########################################################

                                    fig3 = px.scatter(
                                        df2,
                                        x='Isc0_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 2: {year}",
                                        marginal_x="box"
                                    )

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig3.add_scatter(
                                        x=[df2.loc[id_NOCT2]["Isc0_NOCT"]],
                                        y=[df2.loc[id_NOCT2]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc y ISC"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[id_NOCT2]['Imax_NOCT']],
                                        y=[df2.loc[id_NOCT2]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Potencia Max Modulo 2:<br>{pot_NOCT2}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                if Seleccion == [1, 3]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    id_NOCT = df[
                                        'Pmax_NOCT'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idF = df[
                                        'Pmax_F'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    # Se obteiene la potencia maxima en el voltaje maximo.
                                    pot_NOCT = df.loc[id_NOCT]['Pmax_NOCT']
                                    pot_F = df.loc[idF]['Pmax_F']

                                    df2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    id_NOCT2 = df2[
                                        'Pmax_NOCT'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idF2 = df2[
                                        'Pmax_F'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    # Se obteiene la potencia maxima en el voltaje maximo.
                                    pot_NOCT2 = df2.loc[id_NOCT2]['Pmax_NOCT']
                                    pot_F2 = df2.loc[idF2]['Pmax_F']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 1: {year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]["Isc0_NOCT"]],
                                        y=[df.loc[id_NOCT]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_NOCT y ISC_NOCT"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]["Isc0_F"]],
                                        y=[df.loc[idF]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_F y ISC_F"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]['Imax_NOCT']],
                                        y=[df.loc[id_NOCT]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max Sandia:<br>{pot_NOCT}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]['Imax_F']],
                                        y=[df.loc[idF]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Feinmann:<br>{pot_F}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    #################################################################

                                    fig3 = px.scatter(
                                        df2,
                                        x='Isc0_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 2: {year}",
                                        marginal_x="box"
                                    )

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig3.add_scatter(
                                        x=[df2.loc[id_NOCT2]["Isc0_NOCT"]],
                                        y=[df2.loc[id_NOCT2]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_NOCT y ISC_NOCT"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idF2]["Isc0_F"]],
                                        y=[df2.loc[idF2]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_F y ISC_F"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[id_NOCT2]['Imax_NOCT']],
                                        y=[df2.loc[id_NOCT2]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max NOCT Modulo 2:<br>{pot_NOCT2}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idF2]['Imax_F']],
                                        y=[df2.loc[idF2]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Feinmann Modulo 2:<br>{pot_F2}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                print("Returning figure Feynman NOCT")

                                if Seleccion == [2, 3]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    id_NOCT = df[
                                        'Pmax_NOCT'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idS = df[
                                        'Pmax_S'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no

                                    # Se obteiene la potencia maxima en el voltaje maximo.
                                    pot_NOCT = df.loc[id_NOCT]['Pmax_NOCT']
                                    pot_S = df.loc[idS]['Pmax_S']
                                    pot_F = df.loc[idF]['Pmax_F']

                                    df2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    id_NOCT2 = df2[
                                        'Pmax_NOCT'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idS2 = df2[
                                        'Pmax_S'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    # Se obteiene la potencia maxima en el voltaje maximo.
                                    pot_NOCT2 = df2.loc[id_NOCT2]['Pmax_NOCT']
                                    pot_S2 = df2.loc[idS2]['Pmax_S']

                                    fig2 = px.scatter(
                                        df,
                                        x='Isc0_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 1: {year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]["Isc0_NOCT"]],
                                        y=[df.loc[id_NOCT]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_NOCT y ISC_NOCT"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idS]["Isc0_S"]],
                                        y=[df.loc[idS]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_S y ISC_S"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]['Imax_NOCT']],
                                        y=[df.loc[id_NOCT]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max Sandia:<br>{pot_NOCT}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idS]['Imax_S']],
                                        y=[df.loc[idS]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Sandia:<br>{pot_S}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    #################################################################

                                    fig3 = px.scatter(
                                        df2,
                                        x='Isc0_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 2: {year}",
                                        marginal_x="box"
                                    )

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Imax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig3.add_scatter(
                                        x=[df2.loc[id_NOCT2]["Isc0_NOCT"]],
                                        y=[df2.loc[id_NOCT2]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_NOCT y ISC_NOCT"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idS2]["Isc0_S"]],
                                        y=[df2.loc[idS2]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_S y ISC_S"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[id_NOCT2]['Imax_NOCT']],
                                        y=[df2.loc[id_NOCT2]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max NOCT Modulo 2:<br>{pot_NOCT2}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idS2]['Imax_S']],
                                        y=[df2.loc[idS2]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Sandia Modulo 2:<br>{pot_S2}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                print("Returning figure Sandia NOCT")

                                if Seleccion == [1, 2, 3]:
                                    # Filtrar por meses seleccionados
                                    df = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    id_NOCT = df[
                                        'Pmax_NOCT'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idS = df[
                                        'Pmax_S'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    idF = df['Pmax_F'].idxmax()  # Se obteiene la potencia maxima en el voltaje maximo.

                                    pot_NOCT = df.loc[id_NOCT]['Pmax_NOCT']
                                    pot_S = df.loc[idS]['Pmax_S']
                                    pot_F = df.loc[idF]['Pmax_F']

                                    ##############################

                                    df2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(
                                        how='any')  ## con esto se hace un filtrodo de meses
                                    id_NOCT2 = df2[
                                        'Pmax_NOCT'].idxmax()  # El id nos permite identificar el indice de la pontencia maxima en este caso
                                    idS2 = df2[
                                        'Pmax_S'].idxmax()  # En este caso el voltaje maximo, no correpsonde necesariamente a la corriente maxima, esto lo que hace es que no
                                    idF2 = df2[
                                        'Pmax_F'].idxmax()  # Se obteiene la potencia maxima en el voltaje maximo.

                                    pot_NOCT2 = df2.loc[id_NOCT2]['Pmax_NOCT']
                                    pot_S2 = df2.loc[idS2]['Pmax_S']
                                    pot_F2 = df2.loc[idF]['Pmax_F']

                                    fig2 = px.scatter(
                                        df,
                                        x='Pmax_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 1: {year}",
                                        marginal_x="box"
                                    )

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Pmax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Pmax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig2.add_trace(px.scatter(
                                        df,
                                        x='Pmax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]["Isc0_NOCT"]],
                                        y=[df.loc[id_NOCT]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_NOCT y ISC_NOCT"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idS]["Isc0_S"]],
                                        y=[df.loc[idS]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_S y ISC_S"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]["Isc0_F"]],
                                        y=[df.loc[idF]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_F y ISC_F"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[id_NOCT]['Imax_NOCT']],
                                        y=[df.loc[id_NOCT]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max NOCT:<br>{pot_NOCT}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idS]['Imax_S']],
                                        y=[df.loc[idS]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Sandia:<br>{pot_S}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.add_scatter(
                                        x=[df.loc[idF]['Imax_F']],
                                        y=[df.loc[idF]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Feinman:<br>{pot_F}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    #################################################################

                                    fig3 = px.scatter(
                                        df2,
                                        x='Pmax_NOCT',
                                        y='Voc_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_continuous_scale=px.colors.sequential.BuGn,
                                        title=f"Voltaje vs Corriente Modulo 2: {year}",
                                        marginal_x="box"
                                    )

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Pmax_S',
                                        y='Vmax_S',
                                        size='Pmax_S',
                                        color='Poa_global',
                                        color_discrete_sequence=["green"]
                                    ).data[0])

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Pmax_NOCT',
                                        y='Vmax_NOCT',
                                        size='Pmax_NOCT',
                                        color='Poa_global',
                                        color_discrete_sequence=["blue"]
                                    ).data[0])

                                    fig3.add_trace(px.scatter(
                                        df2,
                                        x='Pmax_F',
                                        y='Vmax_F',
                                        size='Pmax_F',
                                        color='Poa_global',
                                        color_discrete_sequence=["red"]
                                    ).data[0])

                                    fig3.add_scatter(
                                        x=[df2.loc[id_NOCT2]["Isc0_NOCT"]],
                                        y=[df2.loc[id_NOCT2]['Voc_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_NOCT y ISC_NOCT"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idS2]["Isc0_S"]],
                                        y=[df2.loc[idS2]['Voc_S']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_S y ISC_S"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idF2]["Isc0_F"]],
                                        y=[df2.loc[idF2]['Voc_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Relacion <br> Voc_F y ISC_F"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[id_NOCT2]['Imax_NOCT']],
                                        y=[df2.loc[id_NOCT2]['Vmax_NOCT']],
                                        mode='markers+text',
                                        marker=dict(color='blue', size=15, symbol='circle'),
                                        text=[f"Potencia Max NOCT Modulo 2:<br>{pot_NOCT2}"],
                                        textposition='bottom right',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idS2]['Imax_S']],
                                        y=[df2.loc[idS2]['Vmax_S']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Sandia Modulo 2:<br>{pot_S2}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig3.add_scatter(
                                        x=[df2.loc[idF2]['Imax_F']],
                                        y=[df2.loc[idF2]['Vmax_F']],
                                        mode='markers+text',
                                        marker=dict(color='red', size=20, symbol='circle'),
                                        text=[f"Potencia Max Feinman Modulo 2:<br>{pot_F2}"],
                                        textposition='bottom left',
                                        showlegend=False
                                    )

                                    fig2.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                    fig3.update_layout(
                                        xaxis_tickangle=30,
                                        title=dict(x=0.5),
                                        xaxis_tickfont=dict(size=9),
                                        yaxis_tickfont=dict(size=9),
                                        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
                                        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
                                        font=dict(color='white')  # Color del texto
                                    )

                                print("Returning figure Sandia NOCT")

                                return fig2, {'display': 'block'}, fig3

    print("Returning empty figure")
    return fig2, {'display': 'none'}, fig3


# Con la siguiente funcion, se va a obtener la lista para saber que año es el que se grafica.
# Ahora solo tienes que agregar la tabla final, con eso ya tendrias todoooo.
# meter la opcionn de cuando es una base de datos, osea puede ser uno o dos modulos.
@app.callback(
    Output('Year-Time-IV', "options")
    ## Esto es para la comparacion IV, pero no curva IV.
    ,
    [
        Input("Datos_PE", "data"),
        Input("Datos_PE2", "data"),
        Input('selection-dropdown', 'value')
    ]
)
def Graph_filter_IV(nombres_Pe, nombres_Pe2, selected_value):
    opciones = []
    opciones2 = []

    if selected_value == 'SELEC' or selected_value == 'INSERT' or selected_value == 'CEC':
        if len(nombres_Pe) > 0 and len(nombres_Pe2) == 0:
            t = input.df_creator_1(nombres_Pe, [1])  # feynman method 1 module [1]

            for i in range(len(t)):
                nombre = f"Año {t[i].index.year.unique()[0]} [Horas: {len(t[i])}]"
                opciones.append(nombre)
            return opciones

    if len(nombres_Pe) > 0 and len(nombres_Pe2) > 0: #dos modulos

        t = input.df_creator_1(nombres_Pe, [1])    # feynman method 1 module [1]
        t2 = input.df_creator_1(nombres_Pe2, [1])  # feynman method 1 module [1]

        for i in range(len(t)):
            nombre = f"Año {t[i].index.year.unique()[0]} [Horas: {len(t[i])}]"
            nombre2 = f"Año {t[i].index.year.unique()[0]} [Horas: {len(t[i])}]"
            opciones.append(nombre)
            opciones2.append(nombre2)
        else:
            return opciones
    else:
        return opciones


### has lo que querias hacer pero en un nuevo app calback no el de abajo
# @app.callback()
# Esta funcion se tiene que activar, con el boton de , correcion. En este appa callback vamos a desplegar  tanto los valores de forma total como de manera promedio.
## Tambien Dependiendo de la cantidad de datos que se metieron sera el tipo de for que se hara.
# Estas son las tablas para el resumen final.
# En eset caso hay dos porque, hay veces, que son dos tablas, por la seleccion de modulos.
### has lo que querias hacer pero en un nuevo app calback no el de abajo
# @app.callback()
# Esta funcion se tiene que activar, con el boton de , correcion. En este appa callback vamos a desplegar  tanto los valores de forma total como de manera promedio.
## Tambien Dependiendo de la cantidad de datos que se metieron sera el tipo de for que se hara.
# Estas son las tablas para el resumen final.
# En eset caso hay dos porque, hay veces, que son dos tablas, por la seleccion de modulos.
@app.callback(
          [
           Output("TdM", "style"),
           Output("IV-G0C", 'style'), #Curva 1 estilo
           Output("IV-G0C", 'figure'),  #Curva 1 figura
           Output("IV_CI_TableC", "style"), #Tabla 1 estilo
           Output('IV_CI_TableC', "children"), #Tabla 1
           Output('Table_Type',"style"), #seleccionador de estilo
           Output("Tabla_Info","data"),
           Output("Tabla_Info_m","data"),
           Output("Tabla_Info_s","data"),
           Output("Tablarm","data"),
           Output("Tablars","data"),
           Output("Real_Average_s","style")

                ]
            # div style, for dropdown
    ,
    [
        Input("correction", "value"),
        Input('selection-dropdown', 'value'),
        Input("Datos_PE", "data"),
        Input("Datos_PE2", "data"),
        Input('Pm', 'value'),
        Input('Vm', 'value'),
        Input('Im', 'value'),
        Input('Voc', 'value'),
        Input('Isc', 'value'),
        Input('Alpha', 'value'),
        Input('Beta', 'value'),
        Input('Gamma', 'value'),  ## Este valor realmente es delta, aunque diga gamma.
        Input('CS', 'value'),
        Input('T', 'value'),
        Input('monosi', 'value'),
        Input('Database1', 'data'),
        Input('Database2', 'data'),
        Input("Irradiancia_IV", 'value'),
        Input("Temperatura_IV", 'value'),
        Input('IV-Method', 'value'),
        Input("Tipo_d_Metodo", 'value'),
        Input("Tipo_d_Medicion", 'value'),
        Input("Tipo_d_Analisis", 'value'),


    ]
)

#### Ya arregle las graficas y controladores, por  lo que ya lo que te  falta es que aqui se haga el display de los datos corregidos.
#### Para eso tendras que crear nuevas figuras. Pero  con diferentes outputs e inputs. Ademas tiene que agregar los if , para los controladores.
#### Es para que se pueda elegir entre datos promedio, simulados, reales, etc.

def IV_Corrct(correct, Method, nombres_Pe, nombres_Pe2,Pmax0,Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series, temp_ref, celltype, D1, D2,i,to,Metodo,T_Metodo,T_Medicion,Tipo_Analisis):
    style = {"display": "none"}
    tableC1 = []
    T = Tm = Ts = 0
    Trm, Trs = 0,0
    style_com = {"display": "none"}

    if correct==[1]:
        if not all([T_Metodo, T_Medicion, Tipo_Analisis]):
            print("⚠ Warning: Missing required variables! Returning default values.")

            return (
                {"display": "block"}, {"display": "none"}, {}, {"display": "none"}, tableC1, style_com, T, Tm, Ts,Trm, Trs,{"display": "none"}
                    )



    if Metodo == "CI":
        df = pd.DataFrame(pd.read_excel("Uploaded_.xlsx"))
        df.columns = ["V", "I", "P"]
        if correct == [1]:
            if len(nombres_Pe) > 0 and len(nombres_Pe2) == 0:
                if Method == 'SELEC':  # Datos de modulo de ejemplo
                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                               27.5, "monoSi") # con esto describimos sobre que tipo de modulo resolvemos.
                    if i is not None and to is not None:
                        if i and to:
                            if len(df) > 0:
                                if T_Metodo=="M2": # Metodo dos antiguo
                                    if T_Medicion == 'Promedio':
                                        results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                                  T_Medicion)
                                        fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[2]
                                        T, Tm, Ts = results[1].to_dict(), results[3].to_dict(), results[4].to_dict()
                                        Trm,Trs   = results[5], results[6]
                                        style = {"display": "block"}
                                        return style, {"display": "block"}, fig, {"display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}

                                    if T_Medicion == 'Completos':
                                        results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                                  T_Medicion)
                                        fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[
                                            2]
                                        T, Tm, Ts = results[1].to_dict(),results[3].to_dict(), results[4].to_dict()
                                        Trm, Trs = results[5], results[6]
                                        style = {"display": "block"}

                                        return style, {"display": "block"}, fig, {
                                            "display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}


                                if T_Metodo == "M2N": ## Metodo dos actulizado
                                    if T_Medicion == 'Promedio':
                                        results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                                  T_Medicion)
                                        fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[2]
                                        T, Tm, Ts = results[1].to_dict(), results[3].to_dict(), results[4].to_dict()
                                        Trm, Trs = results[5], results[6]
                                        style = {"display": "block"}
                                        return style, {"display": "block"}, fig, {"display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}

                                    else:
                                        results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                                  T_Medicion)
                                        fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[
                                            2]
                                        T, Tm, Ts = results[1].to_dict(), results[3].to_dict(), results[4].to_dict()
                                        Trm, Trs = results[5], results[6]
                                        style = {"display": "block"}
                                        return style, {"display": "block"}, fig, {
                                            "display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}



                                return style, {"display": "none"}, {}, {
                                    "display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}

                if Method == 'INSERT':  # Datos propios
                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                               cells_in_series, temp_ref, celltype)

                    if i is not None and to is not None:
                        if i and to:
                            if len(df) > 0:

                                if T_Metodo == "M2":  # Metodo dos antiguo
                                    if T_Medicion == 'Promedio':
                                        results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                                  T_Medicion)
                                        fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[
                                            2]
                                        T, Tm, Ts = results[1].to_dict(), results[3].to_dict(), results[4].to_dict()
                                        Trm, Trs = results[5], results[6]
                                        style = {"display": "block"}
                                        return style, {"display": "block"}, fig, {
                                            "display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}

                                    else:
                                        results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                                  T_Medicion)
                                        fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[
                                            2]
                                        T, Tm, Ts = results[1].to_dict(), results[3].to_dict(), results[4].to_dict()
                                        Trm, Trs = results[5], results[6]
                                        style = {"display": "block"}
                                        return style, {"display": "block"}, fig, {
                                            "display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}

                                if T_Metodo == "M2N":  ## Metodo dos actulizado
                                    if T_Medicion == 'Promedio':
                                        results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                                  T_Medicion)
                                        fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[
                                            2]
                                        T, Tm, Ts = results[1].to_dict(), results[3].to_dict(), results[4].to_dict()
                                        Trm, Trs = results[5], results[6]
                                        style = {"display": "block"}
                                        return style, {"display": "block"}, fig, {
                                            "display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}

                                    else:
                                        results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                                  T_Medicion)
                                        fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[
                                            2]
                                        T, Tm, Ts = results[1].to_dict(), results[3].to_dict(), results[4].to_dict()
                                        Trm, Trs = results[5], results[6]

                                        style = {"display": "block"}
                                        return style, {"display": "block"}, fig, {
                                            "display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}



                                return style, {"display": "block"}, {}, {"display": "block"}, tableC1,style_com,T,Tm,Ts,Trm,Trs,{"display": "block"}



                if Method == "CEC":  # Base de datos
                    Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                           D1[8], D1[9], D1[10])

                    if i is not None and to is not None:
                        if i and to:
                            if len(df) > 0:
                                results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                          T_Medicion)
                                fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[2]
                                T, Tm, Ts = results[1].to_dict(), results[3].to_dict(), results[4].to_dict()
                                Trm, Trs = results[5], results[6]
                                style = {"display": "block"}
                                return style, {"display": "block"}, fig, {
                                    "display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}

            # Esta parte es para los modulos medidos.

            if  len(nombres_Pe) > 0 and len(nombres_Pe2) > 0:

                    if Method == "CEC":  # Base de datos
                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                               D1[8], D1[9], D1[10])

                        results = input.IV_CI_cor(Placa, float(i), float(to), T_Metodo, Tipo_Analisis,
                                                  T_Medicion)
                        fig, tableC1, style_com = results[0], input.table_final_IV(results[1]), results[2]
                        T, Tm, Ts = results[1].to_dict(), results[3].to_dict(), results[4].to_dict()
                        Trm, Trs = results[5], results[6]
                        style = {"display": "block"}
                        return style, {"display": "block"}, fig, {"display": "block"}, tableC1, style_com, T, Tm, Ts,Trm,Trs,{"display": "block"}

        return {"display": "none"}, {"display": "none"}, {}, {"display": "none"}, tableC1,style_com,T,Tm,Ts,Trm,Trs,{"display": "none"}

    return {"display": "none"}, {"display": "none"},{},{"display": "none"},tableC1,style_com,T,Tm,Ts,Trm,Trs,{"display": "none"}


## Con este call back se crean las tablas  el slider de tablas promedio y todo eso.
@app.callback(

            [Output('IV_CI_Table2C',"style"),
                    Output('IV_CI_Table2C', "children")],

            [Input("Table_Selection",'value'),
            Input("Tipo_d_Analisis", 'value'),
            Input("Tabla_Info", "data"),
            Input("Tabla_Info_m", "data"),
            Input("Tabla_Info_s", "data")
             ]

            )

def Tabla_select(valor,TA,t,tm,ts):

    Tabla = []

    if TA=='Simu_Med':

        if valor=='Med_i':
            Tabla=input.table_final_IV(pd.DataFrame(tm))
            return {"display": "block"},Tabla

        if valor == 'Sim_u':
            Tabla=input.table_final_IV(pd.DataFrame(ts))
            return {"display": "block"},Tabla

        if valor == 'Med_i/Sim_u':
            Tabla=input.table_final_IV(pd.DataFrame(t))
            return {"display": "block"},Tabla

        return {"display": "none"}, Tabla

    return {"display": "none"}, Tabla


### Resumen final tabla De mediciones extras: # esto solo es para Ejemplo y subir datos propios.
### Aqui es donde meto todo al final
@app.callback(
                 [
                 Output('IV_CI_TableRm', "style"), #Tabla 1 estilo
                 Output('IV_CI_TableRm', "children"),
                 Output("IV_CI_TableRs","style"),
                 Output("IV_CI_TableRs","children"),
                 Output("IV-RP", 'style'), #Curva 1 estilo -- Esta es la curva final, se muestra pero no quiero que se muestre
                 Output("IV-RP", 'figure'),
                 Output("contenedor-grafica-rp","style"),
                 Output("IV-RP2", 'style'), #Curva 1 estilo -- Esta es la curva final, se muestra pero no quiero que se muestre
                 Output("IV-RP2", 'figure'),
                 Output("contenedor-grafica-rp2","style")
                        ],



                [Input("Tablarm","data"),
                 Input("Tablars","data"),
                 Input('IV-Method', 'value'), # Metodo de comparacion CI para que esto solo se muestre en
                 Input('selection-dropdown', 'value'), # Tipo de datos Seleccion de datos, Base de datos, Ejemplo modulo
                 Input('Pm', 'value'),
                 Input('Vm', 'value'),
                 Input('Im', 'value'),
                 Input('Voc', 'value'),
                 Input('Isc', 'value'),
                 Input('Alpha', 'value'),
                 Input('Beta', 'value'),
                 Input('Gamma', 'value'),  ## Este valor realmente es delta, aunque diga gamma.
                 Input('CS', 'value'),
                 Input('T', 'value'),
                 Input('monosi', 'value'),
                 Input('Database1', 'data'),
                 Input('Database2', 'data'),
                 Input("Tipo_d_Analisis", 'value'),
                 Input("Real_Average","value"),
                 Input("correction", "value")
                 ]

              )
def Tabla_R_Boots(Trm, Trs, Metodo, Method, Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                  temp_ref, celltype, D1, D2, TdA, Rl, corr):
    # --- Condición principal para MOSTRAR la gráfica ---
    # Solo si Rl es [1], intentamos generar y mostrar una figura.

    tabla = []
    tabla2 = []

    if 2 in Rl:
        # Crear figura completamente vacía
        empty_fig = go.Figure()
        empty_fig.update_layout(
            xaxis={'visible': False, 'showgrid': False},
            yaxis={'visible': False, 'showgrid': False},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0}
                                )

        return [
            {"display": "none"}, [],  # IV_CI_TableRm
            {"display": "none"}, [],  # IV_CI_TableRs
            {"display": "none"}, empty_fig,  # IV-RP
            {"display": "none"},  # contenedor-grafica-rp
            {"display": "none"}, empty_fig,  # IV-RP2
            {"display": "none"}  # contenedor-grafica-rp2
        ]

    if 1 in Rl:
        # Crear figura completamente vacía
        empty_fig = go.Figure()
        empty_fig.update_layout(
            xaxis={'visible': False, 'showgrid': False},
            yaxis={'visible': False, 'showgrid': False},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0}
        )
        if Metodo == "CI":
            if Method == 'SELEC':
                if TdA == 'Medidos':
                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
                    results = input.Bootstrap(Trm, Placa,Rl)
                    tabla = input.table_final_IVM(input.Comprobacion(results[0], Placa))
                    fig = results[2]

                    # Este es un caso válido, retornamos la figura.
                    return {"style": "block"}, tabla, {"style": "none"}, tabla2, {"style": "block"}, fig,{"style": "block"},{"style": "none"},empty_fig,{"display": "none", "height": "0px"}

                elif TdA == 'Simulados':  # Usar elif para más claridad
                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
                    results_ = input.Bootstrap(Trs, Placa,Rl)
                    tabla = input.table_final_IVS(input.Comprobacion(results_[0], Placa))
                    fig = results_[2]
                    # Este es un caso válido, retornamos la figura.
                    return {"style": "block"}, tabla, {"style": "none"}, tabla2, {"style": "block"}, fig,{"style": "block"},{"style": "none"},empty_fig,{"display": "none", "height": "0px"}

                elif TdA == 'Simu_Med':
                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66, 27.5, "monoSi")
                    results = input.Bootstrap(Trm, Placa,Rl)
                    results_ = input.Bootstrap2(Trs, Placa)
                    tabla, tabla2 = input.table_final_IVM(input.Comprobacion(results[0], Placa)), input.table_final_IVS(
                        input.Comprobacion(results_[0], Placa))
                    fig,fig2 = results[2], results_[2]
                    # Este es un caso válido, retornamos la figura.
                    return {"style": "block"}, tabla, {"style": "block"}, tabla2, {"style": "block"}, fig,{"style": "block"},{"style": "block"}, fig2,{"display": "block", "height": "auto", "padding": "0px", "margin": "0px"}



            elif Method == 'INSERT':  # Usar elif
                Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series,
                                           temp_ref, celltype)
                # aquí tu lógica para generar la figura ...
                # Este es un caso válido, retornamos la figura.
                return {"style": "block"}, tabla, {"style": "none"}, tabla2, {"style": "block"},{},{"style": "block"},{"style": "none"},{},{"style": "none"}



    # --- RETORNO DE SEGURIDAD ---
    # Si la función llega hasta aquí, significa que Rl no era [1] o que ninguna de
    # las combinaciones de Metodo/Method/TdA resultó en un 'return'.
    # En cualquier otro caso, ocultamos todo.
    return {"style": "none"}, [], {"style": "none"}, [], {"style": "none"}, {},{"style": "none"},{"style": "none"},{},{"style": "none"}


    ### Esta funcion crea la tabla final para el resumen de los datos.
    ### Agragar Rs.

@app.callback(
    [
        Output("IV-G0", 'style'),
        Output('PE-IV', "children"),
        Output("PE-IV2", "children"),
        Output("IV-Tab2", "style"),
        Output("IV-G0", 'figure'),
        Output("IV_Tabla_Selector", "style"),  # tabla creador#
        Output("IV_BASE", "style"),
        Output("IV-G02", "style"),
        Output("IV-G02", "figure"),
        Output("IV_CI_Table", "style"),  # Estas son las tablas para el resumen final.
        Output("IV_CI_Table2", "style"),
        # En eset caso hay dos porque, hay veces, que son dos tablas, por la seleccion de modulos.
        Output('IV_CI_Table', "children"),
        Output("IV_CI_Table2", "children")
    ]
    ,
    [
        Input("Datos_PE", "data"),  ##Estos valores me dan el nombre del CSV
        Input('Datos_PE2', "data"),

        Input("checklist-input", 'value'),
        Input('store-ndh', 'data'),
        Input('IV-Method', 'value'),
        Input('Year-Time-IV', 'value'),
        Input('my-range-slider-IV', 'value'),
        Input('loading-states-table', 'data'),
        Input("Irradiancia_IV", 'value'),
        Input("Temperatura_IV", 'value'),
        Input('selection-dropdown', 'value'),
        Input('Pm', 'value'),
        Input('Vm', 'value'),
        Input('Im', 'value'),
        Input('Voc', 'value'),
        Input('Isc', 'value'),
        Input('Alpha', 'value'),
        Input('Beta', 'value'),
        Input('Gamma', 'value'),  ## Este valor realmente es delta, aunque diga gamma.
        Input('CS', 'value'),
        Input('T', 'value'),
        Input('monosi', 'value'),
        Input('Database1', 'data'),
        Input('Database2', 'data'),
        Input('Table_modulos_base', "derived_virtual_selected_rows"),
        Input("correction", "value")

    ]
)
def electric_parameters(nombres_Pe, nombres_Pe2, Seleccion, nombre, Metodo, Yt_h, Meses, datos, i, to, Method, Pmax0,
                        Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series, temp_ref, celltype, D1, D2,
                        rows, correct):
    t = []
    t1 = []
    Bases = []



    d = {}
    tables1 = []
    tables2 = []
    fig = go.Figure()
    fig2 = go.Figure()

    fig.update_layout(
        title='Curva-IV',
        xaxis_title="Module voltage [V]"
        ,
        yaxis_title="Module current [A]",
        xaxis=dict(type='date'),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    fig2.update_layout(
        title='Curva-IV Modulo 2',
        xaxis_title="Module voltage [V]"
        ,
        yaxis_title="Module current [A]",
        xaxis=dict(type='date'),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )

    tableC1 = []  # tables for the final resume.
    tableC2 = []

    # lo que hacen los ifs, es descargar los datos que existen para ocuparlos.
    meses = list(range(Meses[0], Meses[1] + 1))

    if len(nombres_Pe2) > 0 and len(nombres_Pe) > 0:
        t = input.df_creator_1(nombres_Pe, [1])
        t1 = input.df_creator_1(nombres_Pe2, [1])
    if len(nombres_Pe) > 0 and len(nombres_Pe2) == 0:
        t = input.df_creator_1(nombres_Pe, [1])
        t1 = []
    if len(nombres_Pe2) > 0 and len(nombres_Pe) == 0:
        t = []
        t1 = input.df_creator_1(nombres_Pe2, [1])

    Yt_h = [Yt_h]


    if len(Yt_h) > 0:
        if len(t) > 0 and len(t1) == 0:
            print("DataFrames created:")
            for df in t:
                print("Processing DataFrame:")
                for year in Yt_h:
                    print("Processing year0000000:", year)
                    if year == f"Año {df.index.year.unique()[0]} [Horas: {len(df)}]":

                        if Method == 'SELEC':

                            if Seleccion == [1, 2]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)  # Falta agregar el NOCT
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion,
                                                             lt)  # Tabla para restar, YA tiene el NOCT , LISTOOOO
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    fig = input.IV_R(Placa, resume)[0]  # agrega las opciones para noct
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)

                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ( {'display': 'block'},
                                    tables1, [], {'display': 'none'}, fig, {'display': 'block'}, {'display': 'none'},
                                    {'display': 'none'}, fig2,
                                    {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi") ## recuerda modificar esto.

                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_excel("Uploaded_.xlsx"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {
                                                        'display': 'block'}, {'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                        'display': 'none'}, {'display': 'block'}, {
                                        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [1]:
                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ( {'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5,
                                                               "monoSi")

                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                        return  {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                            'display': 'block'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                            'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [2]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return  {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ( {'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5,
                                                               "monoSi")
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'}, tables1, [], {'display': 'none'}, fig, {
                                                        'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {
                                                        'display': 'block'}, {
                                                        'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []



                            if Seleccion == [3]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return  {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5,
                                                               "monoSi")
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'}, tables1, [], {'display': 'none'}, fig, {
                                                        'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {
                                                        'display': 'block'}, {
                                                        'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [2, 3]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5,
                                                               "monoSi")
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                                        'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [1, 2, 3]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d) ## con esta parte se hace el resumen general de l infomacinor
                                                            ## en la que se ocupo el la trasalacion de eacuaciones.
                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5,
                                                               "monoSi")
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                    input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'}, tables1, [], {'display': 'none'}, fig, {
                                                        'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {
                                                        'display': 'block'}, {
                                                        'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [1, 3]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5, "monoSi")
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34, 66,
                                                               27.5,
                                                               "monoSi")
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                                        'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                        'display': 'none'}, {'display': 'block'}, {
                                        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                        if Method == 'INSERT':

                            if Seleccion == [1, 2]:
                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return{'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])
                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                                        'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [1]:
                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return{'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                                        'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [2]:
                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return ({'display': 'block'},
                                                            tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                                            {'display': 'none'},
                                                            {'display': 'none'}, fig2,
                                                            {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [3]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                                        'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [2, 3]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return{'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                            'display': 'block'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                            'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                            if Seleccion == [1, 2, 3]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                                    'display': 'block'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                                    'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []


                            if Seleccion == [1, 3]:

                                lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                d = input.resume_df(Seleccion, lt)
                                tables1 = input.table_IV(d)

                                if Metodo == 'PE':
                                    resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    fig = input.IV_R(Placa, resume)[0]
                                    tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                    return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                        'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                        'display': 'none'}, tableC1, []

                                if Metodo == 'VE':
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    df = pd.DataFrame(datos)
                                    df.columns = ['Geff', 'Tcell']
                                    df = df.astype(float)
                                    print(df)
                                    fig = input.IV_R_VE(Placa, df)[0]  ## Debes poner esto en todos los demas de VE.
                                    tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                    return ({'display': 'block'},
                                        tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                        {'display': 'none'},
                                        {'display': 'none'}, fig2,
                                        {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                if Metodo == "CI":
                                    Placa = input.Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha,
                                                               cells_in_series, temp_ref, celltype)
                                    if correct != [1]:
                                        if i is not None and to is not None:
                                            if i and to:
                                                df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                df.columns = ["V", "I", "P"]
                                                if len(df) > 0:
                                                    fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                    tableC1 = input.table_final_IV(
                                                        input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                    return {'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                                        'display': 'block'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                                        'display': 'none'}, tableC1, []

                                return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                    'display': 'none'}, {'display': 'block'}, {
                                    'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                        if Method == "CEC":

                            if len(rows) == 1:

                                if Seleccion == [1, 2]:
                                    lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    d = input.resume_df(Seleccion, lt)
                                    tables1 = input.table_IV(d)

                                    if Metodo == 'PE':
                                        resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        fig = input.IV_R(Placa, resume)[0]
                                        tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                        return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                            'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                            'display': 'none'}, tableC1, []

                                    if Metodo == 'VE':
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        df = pd.DataFrame(datos)
                                        df.columns = ['Geff', 'Tcell']
                                        df = df.astype(float)
                                        print(df)
                                        fig = input.IV_R_VE(Placa, df)[
                                            0]  ## Debes poner esto en todos los demas de VE.
                                        tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                        return ({'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                                {'display': 'none'}, {'display': 'none'}, fig2,
                                                {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                    if Metodo == "CI":
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        if correct != [1]:
                                            if i is not None and to is not None:
                                                if i and to:
                                                    df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                    df.columns = ["V", "I", "P"]
                                                    if len(df) > 0:
                                                        fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                        tableC1 = input.table_final_IV(
                                                            input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                        return {'display': 'block'}, tables1, [], {
                                                            'display': 'none'}, fig, {'display': 'none'}, {
                                                            'display': 'block'}, {'display': 'none'}, fig2, {
                                                            'display': 'block'}, {
                                                            'display': 'none'}, tableC1, []

                                    return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                        'display': 'none'}, {'display': 'block'}, {
                                        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []



                                if Seleccion == [1]:
                                    lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    d = input.resume_df(Seleccion, lt)
                                    tables1 = input.table_IV(d)

                                    if Metodo == 'PE':
                                        resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        fig = input.IV_R(Placa, resume)[0]
                                        tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                        return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                            'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                            'display': 'none'}, tableC1, []

                                    if Metodo == 'VE':
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        df = pd.DataFrame(datos)
                                        df.columns = ['Geff', 'Tcell']
                                        df = df.astype(float)
                                        print(df)
                                        fig = input.IV_R_VE(Placa, df)[
                                            0]  ## Debes poner esto en todos los demas de VE.
                                        tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                        return ({'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                                {'display': 'none'}, {'display': 'none'}, fig2,
                                                {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                    if Metodo == "CI":
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        if correct != [1]:
                                            if i is not None and to is not None:
                                                if i and to:
                                                    df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                    df.columns = ["V", "I", "P"]
                                                    if len(df) > 0:
                                                        fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                        tableC1 = input.table_final_IV(
                                                            input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                        return {'display': 'block'}, tables1, [], {
                                                            'display': 'none'}, fig, {'display': 'none'}, {
                                                            'display': 'block'}, {'display': 'none'}, fig2, {
                                                            'display': 'block'}, {
                                                            'display': 'none'}, tableC1, []

                                    return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                        'display': 'none'}, {'display': 'block'}, {
                                        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []



                                if Seleccion == [2]:
                                    lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    d = input.resume_df(Seleccion, lt)
                                    tables1 = input.table_IV(d)

                                    if Metodo == 'PE':
                                        resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        fig = input.IV_R(Placa, resume)[0]
                                        tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                        return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                            'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                            'display': 'none'}, tableC1, []
                                        # El display que esta abierto aqui, es el que nos da la tabla resumen.
                                        # La figura uno , no tiene ninguna condicion de display, ya que en toda condicion aparece.
                                    if Metodo == 'VE':
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        df = pd.DataFrame(datos)
                                        df.columns = ['Geff', 'Tcell']
                                        df = df.astype(float)
                                        print(df)
                                        fig = input.IV_R_VE(Placa, df)[
                                            0]  ## Debes poner esto en todos los demas de VE.
                                        tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                        return ({'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                                {'display': 'none'}, {'display': 'none'}, fig2,
                                                {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                    if Metodo == "CI":
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        if correct != [1]:
                                            if i is not None and to is not None:
                                                if i and to:
                                                    df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                    df.columns = ["V", "I", "P"]
                                                    if len(df) > 0:
                                                        fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                        tableC1 = input.table_final_IV(
                                                            input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                        return {'display': 'block'}, tables1, [], {
                                                            'display': 'none'}, fig, {'display': 'none'}, {
                                                            'display': 'block'}, {'display': 'none'}, fig2, {
                                                            'display': 'block'}, {
                                                            'display': 'none'}, tableC1, []

                                    return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                        'display': 'none'}, {'display': 'block'}, {
                                        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []


                                if Seleccion == [3]:

                                    lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    d = input.resume_df(Seleccion, lt)
                                    tables1 = input.table_IV(d)

                                    if Metodo == 'PE':
                                        resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        fig = input.IV_R(Placa, resume)[0]
                                        tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                        return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                            'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                            'display': 'none'}, tableC1, []

                                    if Metodo == 'VE':
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        df = pd.DataFrame(datos)
                                        df.columns = ['Geff', 'Tcell']
                                        df = df.astype(float)
                                        print(df)
                                        fig = input.IV_R_VE(Placa, df)[
                                            0]  ## Debes poner esto en todos los demas de VE.
                                        tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                        return ({'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                                {'display': 'none'}, {'display': 'none'}, fig2,
                                                {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                    if Metodo == "CI":
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        if correct != [1]:
                                            if i is not None and to is not None:
                                                if i and to:
                                                    df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                    df.columns = ["V", "I", "P"]
                                                    if len(df) > 0:
                                                        fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                        tableC1 = input.table_final_IV(
                                                            input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                        return {'display': 'block'}, tables1, [], {
                                                            'display': 'none'}, fig, {'display': 'none'}, {
                                                            'display': 'block'}, {'display': 'none'}, fig2, {
                                                            'display': 'block'}, {
                                                            'display': 'none'}, tableC1, []

                                    return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                        'display': 'none'}, {'display': 'block'}, {
                                        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []



                                if Seleccion == [2, 3]:

                                    lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    d = input.resume_df(Seleccion, lt)
                                    tables1 = input.table_IV(d)

                                    if Metodo == 'PE':
                                        resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        fig = input.IV_R(Placa, resume)[0]
                                        tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                        return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                            'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                            'display': 'none'}, tableC1, []

                                    if Metodo == 'VE':
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        df = pd.DataFrame(datos)
                                        df.columns = ['Geff', 'Tcell']
                                        df = df.astype(float)
                                        print(df)
                                        fig = input.IV_R_VE(Placa, df)[
                                            0]  ## Debes poner esto en todos los demas de VE.
                                        tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                        return ({'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                                {'display': 'none'}, {'display': 'none'}, fig2,
                                                {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                    if Metodo == "CI":
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        if correct != [1]:
                                            if i is not None and to is not None:
                                                if i and to:
                                                    df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                    df.columns = ["V", "I", "P"]
                                                    if len(df) > 0:
                                                        fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                        tableC1 = input.table_final_IV(
                                                            input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                        return {'display': 'block'}, tables1, [], {
                                                            'display': 'none'}, fig, {'display': 'none'}, {
                                                            'display': 'block'}, {'display': 'none'}, fig2, {
                                                            'display': 'block'}, {
                                                            'display': 'none'}, tableC1, []

                                    return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                        'display': 'none'}, {'display': 'block'}, {
                                        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []



                                if Seleccion == [1, 2, 3]:

                                    lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    d = input.resume_df(Seleccion, lt)
                                    tables1 = input.table_IV(d)

                                    if Metodo == 'PE':
                                        resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        fig = input.IV_R(Placa, resume)[0]
                                        tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                        return {'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                            'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                            'display': 'none'}, tableC1, []

                                    if Metodo == 'VE':
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        df = pd.DataFrame(datos)
                                        df.columns = ['Geff', 'Tcell']
                                        df = df.astype(float)
                                        print(df)
                                        fig = input.IV_R_VE(Placa, df)[
                                            0]  ## Debes poner esto en todos los demas de VE.
                                        tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                        return ({'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                                {'display': 'none'}, {'display': 'none'}, fig2,
                                                {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                    if Metodo == "CI":
                                        Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7],
                                                               D1[8], D1[9], D1[10])
                                        if correct != [1]:
                                            if i is not None and to is not None:
                                                if i and to:
                                                    df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                    df.columns = ["V", "I", "P"]
                                                    if len(df) > 0:
                                                        fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                        tableC1 = input.table_final_IV(
                                                            input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                        return {'display': 'block'}, tables1, [], {
                                                'display': 'none'}, fig, {'display': 'none'}, {
                                                'display': 'block'}, {'display': 'none'}, fig2, {
                                                'display': 'block'}, {
                                                'display': 'none'}, tableC1, []

                                    return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                        'display': 'none'}, {'display': 'block'}, {
                                        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []

                                if Seleccion == [1, 3]:

                                    lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                                    d = input.resume_df(Seleccion, lt)
                                    tables1 = input.table_IV(d)

                                    if Metodo == 'PE':
                                        resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                        Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34,
                                                                   66,
                                                                   27.5, "monoSi")
                                        fig = input.IV_R(Placa, resume)[0]
                                        tableC1 = input.table_final_IV(input.IV_R(Placa, resume)[1])

                                        return{'display': 'block'}, tables1, [], {'display': 'none'}, fig, {'display': 'none'}, {
                                            'display': 'none'}, {'display': 'none'}, fig2, {'display': 'block'}, {
                                            'display': 'none'}, tableC1, []

                                    if Metodo == 'VE':
                                        Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34,
                                                                   66,
                                                                   27.5, "monoSi")
                                        df = pd.DataFrame(datos)
                                        df.columns = ['Geff', 'Tcell']
                                        df = df.astype(float)
                                        print(df)
                                        fig = input.IV_R_VE(Placa, df)[
                                            0]  ## Debes poner esto en todos los demas de VE.
                                        tableC1 = input.table_final_IV(input.IV_R_VE(Placa, df)[1])

                                        return ({'display': 'block'},tables1, [], {'display': 'none'}, fig, {'display': 'block'},
                                                {'display': 'none'}, {'display': 'none'}, fig2,
                                                {'display': 'block'}, {'display': 'none'}, tableC1, [])

                                    if Metodo == "CI":
                                        Placa = input.Placa_Prueba(570, 38.5, 14.79, 45.8, 15.85, 0.04, -0.25, -0.34,
                                                                   66,
                                                                   27.5,
                                                                   "monoSi")
                                        if correct != [1]:

                                            if i is not None and to is not None:
                                                if i and to:
                                                    df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                                    df.columns = ["V", "I", "P"]
                                                    if len(df) > 0:
                                                        fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                        tableC1 = input.table_final_IV(
                                                            input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])

                                                        return {'display': 'block'}, tables1, [], {
                                                            'display': 'none'}, fig, {'display': 'none'}, {
                                                            'display': 'block'}, {'display': 'none'}, fig2, {
                                                            'display': 'block'}, {
                                                            'display': 'none'}, tableC1, []

                                    return {'display': 'none'}, tables1, [], {'display': 'none'}, fig, {
                                        'display': 'none'}, {'display': 'block'}, {
                                        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, [], []



                                # Los ultimos dos pares de corchetes no osn necesarios, porque ya defini arriba que son listas vacias.

        if len(t) > 0 and len(t1) > 0:
            for df, df2 in zip(t, t1):
                year_str1 = f"Year {df.index.year.unique()[0]} [Hours: {len(df)}]"
                year_str2 = f"Year {df2.index.year.unique()[0]} [Hours: {len(df2)}]"
                for year in Yt_h:
                    if any(str(y) in year_str1 or str(y) in year_str2 for y in year):
                        print("good job perro del mal")

                        if Seleccion == [1, 2]:
                            # modulo uno
                            lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                            d = input.resume_df(Seleccion, lt)
                            tables1 = input.table_IV(d)
                            # modulo dos
                            lt2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                            d2 = input.resume_df(Seleccion, lt2)
                            tables2 = input.table_IV2(d2)

                            if Metodo == 'PE':
                                resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                       D1[9], D1[10])

                                resume2 = input.resume_IV(Seleccion, lt2)
                                Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                        D2[9], D2[10])

                                fig = input.IV_R1(Placa, resume)[0]
                                tableC1 = input.table_final_IV(input.IV_R1(Placa, resume)[1])
                                fig2 = input.IV_R2(Placa2, resume2)[0]
                                tableC2 = input.table_final_IV(input.IV_R2(Placa, resume)[1])

                                return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                    'display': 'none'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                    'display': 'block'}, tableC1, tableC2

                            if Metodo == 'VE':
                                Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                       D1[9], D1[10])

                                Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                        D2[9], D2[10])

                                df = pd.DataFrame(datos)
                                df.columns = ['Geff', 'Tcell']
                                df = df.astype(float)

                                fig = input.IV_R_VE(Placa, df)  # Esta funcion te da la figura
                                fig2 = input.IV_R_VE(Placa2, df)

                                return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                    'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                    'display': 'none'}, tableC1, tableC2

                            if Metodo == "CI":
                                Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                       D1[9], D1[10])
                                Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                        D2[9], D2[10])
                                if correct != [1]:
                                    if i is not None and to is not None:
                                        if i and to:
                                            df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                            df.columns = ["V", "I", "P"]
                                            df2 = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                            df2.columns = ["V", "I", "P"]
                                            if len(df) > 0:
                                                fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                fig2 = input.IV_CI2(Placa2, lt2, float(i), float(to), df2, Seleccion)[0]
                                                tableC1 = input.table_final_IV(
                                                    input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])
                                                tableC2 = input.table_final_IV(
                                                    input.IV_CI2(Placa2, lt2, float(i), float(to), df, Seleccion)[1])

                                    return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                        'display': 'block'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                        'display': 'block'}, tableC1, tableC2

                            return {'display': 'none'},tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                'display': 'none'}, tableC1, tableC2

                        if Seleccion == [1]:

                            # modulo uno

                            lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                            d = input.resume_df(Seleccion,
                                                lt)  # Esto se hizo, porque adentro de cada funcion se separa, dependiendo del metodo.
                            tables1 = input.table_IV(d)

                            # modulo dos

                            lt2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                            d2 = input.resume_df(Seleccion, lt2)
                            tables2 = input.table_IV2(d2)

                            if Metodo == 'PE':
                                resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                       D1[9], D1[10])

                                resume2 = input.resume_IV(Seleccion, lt2)
                                Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                        D2[9], D2[10])

                                fig = input.IV_R1(Placa, resume)[0]
                                tableC1 = input.table_final_IV(input.IV_R1(Placa, resume)[1])
                                fig2 = input.IV_R2(Placa2, resume2)[0]
                                tableC2 = input.table_final_IV(input.IV_R2(Placa, resume)[1])

                                return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                    'display': 'none'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                    'display': 'block'}, tableC1, tableC2

                            if Metodo == 'VE':
                                Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                       D1[9], D1[10])

                                Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                        D2[9], D2[10])

                                df = pd.DataFrame(datos)
                                df.columns = ['Geff', 'Tcell']
                                df = df.astype(float)

                                fig = input.IV_R_VE(Placa, df)
                                fig2 = input.IV_R_VE(Placa2, df)

                                return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                    'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                    'display': 'none'}, tableC1, tableC2

                            if Metodo == "CI":
                                Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                       D1[9], D1[10])
                                Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                        D2[9], D2[10])
                                if correct != [1]:
                                    if i is not None and to is not None:
                                        if i and to:
                                            df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                            df.columns = ["V", "I", "P"]
                                            if len(df) > 0:
                                                fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                fig2 = input.IV_CI2(Placa2, lt2, float(i), float(to), df, Seleccion)[0]
                                                tableC1 = input.table_final_IV(
                                                    input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])
                                                tableC2 = input.table_final_IV(
                                                    input.IV_CI2(Placa2, lt2, float(i), float(to), df, Seleccion)[1])

                                    return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                        'display': 'block'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                        'display': 'block'}, tableC1, tableC2

                            return {'display': 'none'},tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                'display': 'none'}, tableC1, tableC2

                        if Seleccion == [2]:

                            # modulo uno

                            lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                            d = input.resume_df(Seleccion, lt)
                            tables1 = input.table_IV(d)

                            # modulo dos

                            lt2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                            d2 = input.resume_df(Seleccion, lt2)
                            tables2 = input.table_IV2(d2)

                            if Metodo == 'PE':
                                resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                                Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                       D1[9], D1[10])

                                resume2 = input.resume_IV(Seleccion, lt2)
                                Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                        D2[9], D2[10])

                                fig = input.IV_R1(Placa, resume)[0]
                                tableC1 = input.table_final_IV(input.IV_R1(Placa, resume)[1])
                                fig2 = input.IV_R2(Placa2, resume2)[0]
                                tableC2 = input.table_final_IV(input.IV_R2(Placa, resume)[1])

                                return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                    'display': 'none'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                    'display': 'block'}, tableC1, tableC2

                            if Metodo == 'VE':
                                Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                       D1[9], D1[10])

                                Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                        D2[9], D2[10])

                                df = pd.DataFrame(datos)
                                df.columns = ['Geff', 'Tcell']
                                df = df.astype(float)

                                fig = input.IV_R_VE(Placa, df)
                                fig2 = input.IV_R_VE(Placa2, df)

                                return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                    'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                    'display': 'none'}, tableC1, tableC2

                            if Metodo == "CI":
                                Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                       D1[9], D1[10])

                                Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                        D2[9], D2[10])
                                if correct != [1]:
                                    if i is not None and to is not None:
                                        if i and to:
                                            df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                            df.columns = ["V", "I", "P"]
                                            if len(df) > 0:
                                                fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                                fig2 = input.IV_CI2(Placa2, lt2, float(i), float(to), df, Seleccion)[0]
                                                tableC1 = input.table_final_IV(
                                                    input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])
                                                tableC2 = input.table_final_IV(
                                                    input.IV_CI2(Placa2, lt2, float(i), float(to), df, Seleccion)[1])

                                    return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                        'display': 'block'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                        'display': 'block'}, tableC1, tableC2

                            return{'display': 'none'}, tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                'display': 'none'}, tableC1, tableC2

                    if Seleccion == [3]:
                        # modulo uno
                        lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                        d = input.resume_df(Seleccion, lt)
                        tables1 = input.table_IV(d)
                        # modulo dos
                        lt2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                        d2 = input.resume_df(Seleccion, lt2)
                        tables2 = input.table_IV2(d2)

                        if Metodo == 'PE':
                            resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])

                            resume2 = input.resume_IV(Seleccion, lt2)
                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])

                            fig = input.IV_R1(Placa, resume)[0]
                            tableC1 = input.table_final_IV(input.IV_R1(Placa, resume)[1])
                            fig2 = input.IV_R2(Placa2, resume2)[0]
                            tableC2 = input.table_final_IV(input.IV_R2(Placa, resume)[1])

                            return{'display': 'block'}, tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                'display': 'block'}, tableC1, tableC2

                        if Metodo == 'VE':
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])

                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])

                            df = pd.DataFrame(datos)
                            df.columns = ['Geff', 'Tcell']
                            df = df.astype(float)

                            fig = input.IV_R_VE(Placa, df)  # Esta funcion te da la figura
                            fig2 = input.IV_R_VE(Placa2, df)

                            return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                'display': 'none'}, tableC1, tableC2

                        if Metodo == "CI":
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])
                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])
                            if correct != [1]:
                                if i is not None and to is not None:
                                    if i and to:
                                        df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                        df.columns = ["V", "I", "P"]
                                        df2 = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                        df2.columns = ["V", "I", "P"]
                                        if len(df) > 0:
                                            fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                            fig2 = input.IV_CI2(Placa2, lt2, float(i), float(to), df2, Seleccion)[0]
                                            tableC1 = input.table_final_IV(
                                                input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])
                                            tableC2 = input.table_final_IV(
                                                input.IV_CI2(Placa2, lt2, float(i), float(to), df, Seleccion)[1])

                                return{'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                    'display': 'block'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                    'display': 'block'}, tableC1, tableC2

                        return{'display': 'none'}, tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {'display': 'none'}, {
                            'display': 'block'}, fig2, {'display': 'none'}, {'display': 'none'}, tableC1, tableC2

                    if Seleccion == [1, 3]:
                        # modulo uno
                        lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                        d = input.resume_df(Seleccion, lt)
                        tables1 = input.table_IV(d)
                        # modulo dos
                        lt2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                        d2 = input.resume_df(Seleccion, lt2)
                        tables2 = input.table_IV2(d2)

                        if Metodo == 'PE':
                            resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])

                            resume2 = input.resume_IV(Seleccion, lt2)
                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])

                            fig = input.IV_R1(Placa, resume)[0]
                            tableC1 = input.table_final_IV(input.IV_R1(Placa, resume)[1])
                            fig2 = input.IV_R2(Placa2, resume2)[0]
                            tableC2 = input.table_final_IV(input.IV_R2(Placa, resume)[1])

                            return{'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                'display': 'block'}, tableC1, tableC2

                        if Metodo == 'VE':
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])

                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])

                            df = pd.DataFrame(datos)
                            df.columns = ['Geff', 'Tcell']
                            df = df.astype(float)

                            fig = input.IV_R_VE(Placa, df)  # Esta funcion te da la figura
                            fig2 = input.IV_R_VE(Placa2, df)

                            return{'display': 'block'}, tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                'display': 'none'}, tableC1, tableC2

                        if Metodo == "CI":
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])
                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])
                            if correct != [1]:
                                if i is not None and to is not None:
                                    if i and to:
                                        df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                        df.columns = ["V", "I", "P"]
                                        df2 = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                        df2.columns = ["V", "I", "P"]
                                        if len(df) > 0:
                                            fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                            fig2 = input.IV_CI2(Placa2, lt2, float(i), float(to), df2, Seleccion)[0]
                                            tableC1 = input.table_final_IV(
                                                input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])
                                            tableC2 = input.table_final_IV(
                                                input.IV_CI2(Placa2, lt2, float(i), float(to), df, Seleccion)[1])

                                return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                    'display': 'block'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                    'display': 'block'}, tableC1, tableC2

                        return{'display': 'none'}, tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {'display': 'none'}, {
                            'display': 'block'}, fig2, {'display': 'none'}, {'display': 'none'}, tableC1, tableC2

                    if Seleccion == [2, 3]:
                        # modulo uno
                        lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                        d = input.resume_df(Seleccion, lt)
                        tables1 = input.table_IV(d)
                        # modulo dos
                        lt2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                        d2 = input.resume_df(Seleccion, lt2)
                        tables2 = input.table_IV2(d2)

                        if Metodo == 'PE':
                            resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])

                            resume2 = input.resume_IV(Seleccion, lt2)
                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])

                            fig = input.IV_R1(Placa, resume)[0]
                            tableC1 = input.table_final_IV(input.IV_R1(Placa, resume)[1])
                            fig2 = input.IV_R2(Placa2, resume2)[0]
                            tableC2 = input.table_final_IV(input.IV_R2(Placa, resume)[1])

                            return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                'display': 'block'}, tableC1, tableC2

                        if Metodo == 'VE':
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])

                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])

                            df = pd.DataFrame(datos)
                            df.columns = ['Geff', 'Tcell']
                            df = df.astype(float)

                            fig = input.IV_R_VE(Placa, df)  # Esta funcion te da la figura
                            fig2 = input.IV_R_VE(Placa2, df)

                            return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                'display': 'none'}, tableC1, tableC2

                        if Metodo == "CI":
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])
                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])
                            if correct != [1]:
                                if i is not None and to is not None:
                                    if i and to:
                                        df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                        df.columns = ["V", "I", "P"]
                                        df2 = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                        df2.columns = ["V", "I", "P"]
                                        if len(df) > 0:
                                            fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                            fig2 = input.IV_CI2(Placa2, lt2, float(i), float(to), df2, Seleccion)[0]
                                            tableC1 = input.table_final_IV(
                                                input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])
                                            tableC2 = input.table_final_IV(
                                                input.IV_CI2(Placa2, lt2, float(i), float(to), df, Seleccion)[1])

                                return{'display': 'block'}, tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                    'display': 'block'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                    'display': 'block'}, tableC1, tableC2

                        return {'display': 'none'},tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {'display': 'none'}, {
                            'display': 'block'}, fig2, {'display': 'none'}, {'display': 'none'}, tableC1, tableC2

                    if Seleccion == [1, 2, 3]:
                        # modulo uno
                        lt = (df[df["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                        d = input.resume_df(Seleccion, lt)
                        tables1 = input.table_IV(d)
                        # modulo dos
                        lt2 = (df2[df2["Month"].isin(meses)]).replace(0, np.nan).dropna(how='any')
                        d2 = input.resume_df(Seleccion, lt2)
                        tables2 = input.table_IV2(d2)

                        if Metodo == 'PE':
                            resume = input.resume_IV(Seleccion, lt)  # Tabla par restar
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])

                            resume2 = input.resume_IV(Seleccion, lt2)
                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])

                            fig = input.IV_R1(Placa, resume)[0]
                            tableC1 = input.table_final_IV(input.IV_R1(Placa, resume)[1])
                            fig2 = input.IV_R2(Placa2, resume2)[0]
                            tableC2 = input.table_final_IV(input.IV_R2(Placa, resume)[1])

                            return{'display': 'block'}, tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                'display': 'block'}, tableC1, tableC2

                        if Metodo == 'VE':
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])

                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])

                            df = pd.DataFrame(datos)
                            df.columns = ['Geff', 'Tcell']
                            df = df.astype(float)

                            fig = input.IV_R_VE(Placa, df)  # Esta funcion te da la figura
                            fig2 = input.IV_R_VE(Placa2, df)

                            return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {
                                'display': 'none'}, {'display': 'block'}, fig2, {'display': 'none'}, {
                                'display': 'none'}, tableC1, tableC2

                        if Metodo == "CI":
                            Placa = input.Placa_D1(D1[0], D1[1], D1[2], D1[3], D1[4], D1[5], D1[6], D1[7], D1[8],
                                                   D1[9], D1[10])
                            Placa2 = input.Placa_D1(D2[0], D2[1], D2[2], D2[3], D2[4], D2[5], D2[6], D2[7], D2[8],
                                                    D2[9], D2[10])
                            if correct != [1]:
                                if i is not None and to is not None:
                                    if i and to:
                                        df = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                        df.columns = ["V", "I", "P"]
                                        df2 = pd.DataFrame(pd.read_csv("Uploaded_.csv"))
                                        df2.columns = ["V", "I", "P"]
                                        if len(df) > 0:
                                            fig = input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[0]
                                            fig2 = input.IV_CI2(Placa2, lt2, float(i), float(to), df2, Seleccion)[0]
                                            tableC1 = input.table_final_IV(
                                                input.IV_CI(Placa, lt, float(i), float(to), df, Seleccion)[1])
                                            tableC2 = input.table_final_IV(
                                                input.IV_CI2(Placa2, lt2, float(i), float(to), df, Seleccion)[1])

                                return {'display': 'block'},tables1, tables2, {'display': 'block'}, fig, {'display': 'none'}, {
                                    'display': 'block'}, {'display': 'block'}, fig2, {'display': 'block'}, {
                                'display': 'block'}, tableC1, tableC2

                        return{'display': 'none'}, tables1, tables2, {'display': 'block'}, fig, {'display': 'block'}, {'display': 'none'}, {
                            'display': 'block'}, fig2, {'display': 'none'}, {'display': 'none'}, tableC1, tableC2

    return {'display': 'none'},tables1, tables2, {'display': 'none'}, fig, {'display': 'none'}, {'display': 'none'}, {
        'display': 'none'}, fig2, {'display': 'none'}, {'display': 'none'}, tableC1, tableC2


@app.callback(
    Output('loading-states-table', 'data'),  # Actualiza las filas (data)
    Input('add-column-button', 'n_clicks'),  # Escucha clics en el botón de agregar fila
    State('loading-states-table', 'data'),  # Obtiene las filas actuales de la tabla
    State('loading-states-table', 'columns')  # Obtiene las columnas actuales de la tabla
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        # Crear una nueva fila con valores None (o cualquier valor predeterminado que desees)
        new_row = {c['id']: None for c in columns}
        # Agregar la nueva fila a las filas existentes
        rows.append(new_row)
    return rows


# aqui se hace la tabla que se sube al input file.
# Función para eliminar cualquier archivo previo llamado "Uploaded_.xlsx"
# Función para procesar el contenido y mostrar las tablas
def parse_contents(contents, filename):
    # Guardar el archivo subido y obtener las hojas
    input.eliminar_archivo_anterior()
    sheets, xls = input.guardar_archivo(contents)

    # Crear un contenedor para las tablas de cada hoja
    tables = []
    for sheet in sheets:
        df = pd.read_excel(xls, sheet_name=sheet)

        # Añadir título de la hoja
        tables.append(html.H5(f'Hoja: {sheet} - {filename}'))

        # Crear la tabla para la hoja actual
        table = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_data={
                'color': 'black',
                'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold'
            },
            page_action="native",
            page_current=0,
            page_size=10,
            style_table={'width': '100%', 'overflowX': 'auto', 'maxHeight': '500px',
                         'overflowY': 'auto'},
            style_cell={
                'minWidth': '100px', 'maxWidth': '200px',
                'whiteSpace': 'normal',
                'textAlign': 'center'
            },
            css=[{
                'selector': '.dash-spreadsheet-container .pagination',
                'rule': 'text-align: center;'
            }]
        )

        tables.append(table)  # Añadir la tabla de la hoja actual al contenedor de tablas

    return html.Div(tables)


# Callback para manejar la subida del archivo y mostrar las tablas
@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        children = parse_contents(contents, filename)
        return children


if __name__ == '__main__':
   app.run(debug=True)

