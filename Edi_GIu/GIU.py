import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.dash_table import DataTable
import pvlib
import pandas as pd
import dash_bootstrap_components as dbc

# Aquí puedes escribir el resto de tu programa


# Aquí puedes escribir el resto de tu programa

years = ['1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
         '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']


app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])



app.layout = dbc.Container([
    html.Div([  # Entrada de la latitud #####
        html.Label('Latitud          :', style={
                   'font-size': '20px', 'margin-right': '10px', 'display': 'inline-block', 'width': '80px'}),
        dcc.Input(
            id='latitude',
            placeholder='Enter Latitud',
            type='number',
            value=19.28786,
            style={'width': '20%'}
        )
    ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-bottom': '10px'}),

    html.Div([  # Entrada de la longitud#####
        html.Label('Longitud:    ', style={
                   'font-size': '20px', 'margin-right': '10px', 'display': 'inline-block', 'width': '80px'}),
        dcc.Input(
            id='Longitude',
            placeholder='Enter Longitude',
            type='number',
            value=-99.65324,
            style={'width': '20%'}
        )
    ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-bottom': '10px'}),

    dcc.Store(id='Tipo de año'),

    html.Label('Selecciona el tipo de año que quieres analizar) :  ',
               style={'font-weight': 'bold'}),

    dcc.RadioItems(['Typical metheorological year',
                   'Espececific year (1998-2020)'], value=0, id='my-store-input'),

    html.Br(),
    html.Div(id='current-store'),

    html.Br(),
    html.Label('Solo para año especifico(De 1998 a 2018 los datos estan disponibles en [60, 30] minutos, 2018 en adelante estan disponibles para [60, 30, 15, 5] minutos) :  ', style={
               'font-weight': 'bold'}),
    dcc.RadioItems(
        options=[{'label': str(i), 'value': i} for i in [60, 30, 15, 5]],
        value=0,
        id='Diferencial de tiempo',
        inline=True
    ),

    html.Br(),

    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in years],
        value=0,
        multi=True,
    ), dcc.Loading([html.Div(id="loading-demo")]),
    html.Div(id='tables-container'),
    dcc.Store(id='CLC'),  # Base de datos para el clima caracteristico
    dcc.Store(id='Base de datos')  # Base de  datos de los datos normales Aqui se guarda toda la informacion con la que esta jugando el programa.
    ,



    html.Div([html.Label('Year to graph:'),


    dcc.Dropdown(
        id='dropdown1',
        options=[],
        value=0,
        multi=True,

    )]),

    dcc.Graph(id='Grafico_de_clima')


], fluid=False)






#corchete cierra Div, parentesis cierra container#####################################################
#####################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

## Selector de TMY o  Especifico ######


@app.callback(
    Output('my-store', 'data'),
    Input('my-store-input', 'value')
)
# Creacion de la base de datos de los climas ######  De aqui lo que contiene los datos importantes son el Output('Base de datos','data')
def update_store(value):
    return value

    #### App callback para la creacion de los DATA FRAMES###
stored_dataframes = []
BaseDatos_Records = []


@app.callback([Output("tables-container", "children"), Output("loading-demo", "children"), Output('Base de datos', 'data')],
              [Input('latitude', 'value'), Input('Longitude', 'value'),
               Input('dropdown', 'value'), Input("my-store-input", "value"), Input('Diferencial de tiempo', 'value')])
def latitude_longitude(latitude, longitude, years, valor, Tiempo):
    dataframes = []
    dfnum = 0
    fecha = []
    informacion = []
    if valor == 'Espececific year (1998-2020)':
        for year in years:
            fecha.append(int(year))
            key = 'h1w3fybDCdpHdZVEDJa9nclDAbH4eJ29tDRs96YV'
            email = 'edidz@ier.unam.mx'
            df, metadata = pvlib.iotools.get_psm3(latitude, longitude, key, email, names=int(
                year), interval=Tiempo, timeout=60, map_variables=True, leap_day=False)
            columns = [{'name': i, 'id': i} for i in df.columns]
            data = df.head(5).to_dict('records')
            dataframes.append((data, columns))
            dfnum = dfnum + 1
            datos60 = []
            datos30 = []
            datos15 = []
            datos5 = []
            TMY = []
            BaseDatos = [datos60, datos30, datos15, datos5, TMY]
            if len(df) == 8760.0:
                datos60.append(df)
            if len(df) == 17520.0:
                datos30.append(df)
            if len(df) == 35040.0:
                datos15.append(df)
            if len(df) == 105120.0:
                datos5.append(df)
            DNmin = []
            DNmax = []
            Nmin = 0
            Nmax = 0
            s = 0
            NumArchivos = []

            for archivo in BaseDatos:
                s = 0
                Nmin = 0
                Nmax = 0
                if len(archivo) > 0:
                    for year in archivo:
                        Nmin = pd.DataFrame(year[year.Hour.isin([6, 7, 8])])
                        Nmax = pd.DataFrame(
                            year[year.Hour.isin([12, 13, 14, 15])])
                        s = s + 1

                        DNmin.append(Nmin)
                        DNmax.append(Nmax)
            CLCmin = []
            clc = 0
            for climamin in DNmin:
                clc = 0
                clc = pd.DataFrame(climamin.temp_air)
                clc.columns = ['TempMin']
                clc['ghi_min'] = climamin.ghi
                clc['wspeed_min'] = climamin.wind_speed
                CLCmin.append(clc)
            CLCmax = []
            clc = 0
            for climamax in DNmax:
                clc = 0
                clc = pd.DataFrame(climamax.temp_air)
                clc.columns = ['TempMax']
                clc['ghi_max'] = climamax.ghi
                clc['wspeed_max'] = climamax.wind_speed
                CLCmax.append(clc)
            i = 0
            z = 0
            Hs = []
            for documento in BaseDatos:
                for clima in documento:
                    HS = (BaseDatos[i][z].ghi.resample(
                        'D').sum().dropna()) / 1000
                    z = 1 + z
                    Hs.append((HS))
                i = 1 + i
                z = 0
            i = 0
            z = 0
            CLC = []
            for i in range(len(CLCmax)):
                clc = CLCmax[i].resample("D").mean().dropna()
                clcmin = CLCmin[i].resample("D").mean().dropna()

                clc = pd.concat([clc, clcmin, Hs[i]], axis=1).dropna()
            CLC.append(clc)
            d60 = []
            d30 = []
            d15 = []
            d5 = []
            i = 0

            for dato in BaseDatos:
                z = 0
                for year in dato:
                    if len(BaseDatos[i][z]) == 8760:
                        d60.append(BaseDatos[i][z].to_dict('records'))
                    if len(BaseDatos[i][z]) == 17520.0:
                        d30.append(BaseDatos[i][z].to_dict('records'))
                    if len(BaseDatos[i][z]) == 35040.0:
                        d15.append(BaseDatos[i][z].to_dict('records'))
                    if len(BaseDatos[i][z]) == 105120.0:
                        d5.append(BaseDatos[i][z].to_dict('records'))
                    z += 1
                i += 1

            BaseDatos_Records = [d60, d30, d15, d5]

    if valor == "Espececific year (1998-2020)":  # Tabla de years especificos##
        tables = [html.Div([html.H3(f"Año {fecha[i]}"),
                            DataTable(id=f"Tabla-{i+1}", data=data, columns=columns)]) for i, (data, columns) in enumerate(dataframes)]

    if valor == 'Typical metheorological year':
        TMY = []
        key = 'h1w3fybDCdpHdZVEDJa9nclDAbH4eJ29tDRs96YV'
        email = 'edidz@ier.unam.mx'
        df, metadata = pvlib.iotools.get_psm3(
            latitude, longitude, key, email, names='tmy', interval=60, timeout=70, map_variables=True, leap_day=False)
        # esta linea conserva los datos origninales para una futura descgar, etc.
        informacion.append(df)
        TMY.append(df)
        columns = [{'name': i, 'id': i} for i in df.columns]
        data = df.head(7).to_dict('records')
        dataframes.append((data, columns))
        dfnum = dfnum + 1
        BaseDatos = [TMY]
        DNmin = []
        DNmax = []
        Nmin = 0
        Nmax = 0
        s = 0
        NumArchivos = []

        for archivo in BaseDatos:
            s = 0
            Nmin = 0
            Nmax = 0
            if len(archivo) > 0:
                for year in archivo:
                    Nmin = pd.DataFrame(year[year.Hour.isin([6, 7, 8])])
                    Nmax = pd.DataFrame(year[year.Hour.isin([12, 13, 14, 15])])
                    s = s + 1

                    DNmin.append(Nmin)
                    DNmax.append(Nmax)
        CLCmin = []
        clc = 0
        for climamin in DNmin:
            clc = 0
            clc = pd.DataFrame(climamin.temp_air)
            clc.columns = ['TempMin']
            clc['ghi_min'] = climamin.ghi
            clc['wspeed_min'] = climamin.wind_speed
            CLCmin.append(clc)
        CLCmax = []
        clc = 0
        for climamax in DNmax:
            clc = 0
            clc = pd.DataFrame(climamax.temp_air)
            clc.columns = ['TempMax']
            clc['ghi_max'] = climamax.ghi
            clc['wspeed_max'] = climamax.wind_speed
            CLCmax.append(clc)
        i = 0
        z = 0
        Hs = []
        for documento in BaseDatos:
            for clima in documento:
                HS = (BaseDatos[i][z].ghi.resample('D').sum().dropna()) / 1000
                z = 1 + z
                Hs.append((HS))
            i = 1 + i
            z = 0
        i = 0
        z = 0
        CLC = []
        for i in range(len(CLCmax)):
            clc = CLCmax[i].resample("D").mean().dropna()
            clcmin = CLCmin[i].resample("D").mean().dropna()

            clc = pd.concat([clc, clcmin, Hs[i]], axis=1).dropna()
        CLC.append(clc)
        print(CLC)
        i = 0
        TM = []
        for dato in BaseDatos:
            z = 0
            for year in dato:
                if len(BaseDatos[i][z]) == 8760:
                    TM.append(BaseDatos[i][z].to_dict('records'))
                z += 1
            i += 1

        BaseDatos_Records = [TM]

    if valor == "Typical metheorological year":  # Tabla de years especificos##
        tables = [html.Div([html.H3(f"Año Tipico Meteorologico"),
                            DataTable(id=f"Tabla-{i+1}", data=data, columns=columns)]) for i, (data, columns) in enumerate(dataframes)]

    return tables, dcc.Loading([html.Div(id="loading-output")]), BaseDatos_Records


@app.callback(
    Output('dropdown1', 'options'),
    Input('dropdown', 'value')
)
# Creacion del segundo Dropdown###### Este dropdown ve que datos escogio el usuario
def update_dropdown2_options(selected_values):
    return [{'label': i, 'value': i} for i in selected_values]



