from operator import index

import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import html, dcc
from dash import html, dcc
from dash.dash_table.Format import Group
from dash.dash_table import DataTable
from dash.dash_table.Format import Group
from dash import dash_table
from dash.dash_table import DataTable
import pvlib
import pandas as pd
import os
import glob

from fontTools.ttLib.tables.otTables import VarIdxMap
from jinja2.nodes import Import
from scipy import special, constants
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os
import base64
import io

def table(B, C, ID, Val):
    dd1 = dbc.InputGroup(
        [dbc.InputGroupText(B,style={'background-color': '#007bff', 'color': 'white'}), dbc.Input(id=ID, placeholder=C, value=Val)],size="sm",
        className="mb-3", style={

             'margin-right': '150px', 'width': '150px'
                                 })
    # Pmax0
    return dd1

####Datos de moduloooooo

def table_module(q,w,e,r,t,y,u,i,p,a,s):

    module=html.Div(id='inputs-container', children=[

        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(table("Pmax", "W", "Pm", q), width=3 ),
                    dbc.Col(table("Vmax", "Volts", "Vm", w), width=3),
                    dbc.Col(table("Imax", "Amperes", "Im", e), width=3),
                    dbc.Col(table("Voc", "Volts", "Voc", r), width=3)
                ]),
                dbc.Row([
                    dbc.Col(table("Isc", "Amperes", "Isc", t), width=3),
                    dbc.Col(table("Alpha", "%/C°", "Alpha", y), width=3),
                    dbc.Col(table("Beta", "%/C°", "Beta", u), width=3),
                    dbc.Col(table("Deltha", "%/C°", "Gamma",i), width=3)
                ]),
                dbc.Row([
                    dbc.Col(table("Cells in series", "Number", "CS", p), width=3),
                    dbc.Col(table("Temp_ref", "°C", "T", a), width=3),
                    dbc.Col(table("Cell type", "", "monosi", s), width=3)
                ])
            ])
        )
    ],
             style={'display': 'block'}
             )
    return module

### Tabla para base de datos:

def table_module_b(q,w,e,r,t,y,u,i,p,a,s): #modificar entradas de variable 11

    module=html.Div(id='input_data_base', children=[
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(table("Pmax", f"{q}", "Pm", q), width=3),
                    dbc.Col(table("Vmax", f"{w}", "Vm", w), width=3),
                    dbc.Col(table("Imax", f"{e}", "Im", e), width=3),
                    dbc.Col(table("Voc", f"{r}", "Voc", r), width=3)
                ]),
                dbc.Row([
                    dbc.Col(table("Isc", f"{t}", "Isc", t), width=3),
                    dbc.Col(table("Alpha", f"{y}", "Alpha", y), width=3),
                    dbc.Col(table("Beta", f"{u}", "Beta", u), width=3),
                    dbc.Col(table("Deltha", f"{i}", "Gamma", i), width=3)
                ]),
                dbc.Row([
                    dbc.Col(table("Cells in series", f"{p}", "CS", p), width=3),
                    dbc.Col(table("Temp_ref", f"{a}", "T", a), width=3),
                    dbc.Col(table("Cell type",f"{s}" , "monosi", s), width=3)
                ])
            ])
        )
    ],
             style={'display': 'block'}
             )
    return module

def table_module_b2(q,w,e,r,t,y,u,i,p,a,s): #modificar entradas de variable
    t
    module=html.Div(id='input_data_base2', children=[
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(table("Pmax", f"{q}", "Pm", q), width=3),
                    dbc.Col(table("Vmax", f"{w}", "Vm", w), width=3),
                    dbc.Col(table("Imax", f"{e}", "Im", e), width=3),
                    dbc.Col(table("Voc", f"{r}", "Voc", r), width=3)
                ]),
                dbc.Row([
                    dbc.Col(table("Isc", f"{t}", "Isc", t), width=3),
                    dbc.Col(table("Alpha", f"{y}", "Alpha", y), width=3),
                    dbc.Col(table("Beta", f"{u}", "Beta", u), width=3),
                    dbc.Col(table("Deltha", f"{i}", "Gamma", i), width=3)
                ]),
                dbc.Row([
                    dbc.Col(table("Cells in series", f"{p}", "CS", p), width=3),
                    dbc.Col(table("Temp_ref", f"{a}", "T", a), width=3),
                    dbc.Col(table("Cell type", f"{s}", "monosi", s), width=3)
                ])
            ])
        )
    ],
             style={'display': 'block'}
             )
    return module


def lat(lat):
    lati = html.Div([  # Entrada de la latitud #####
        html.Label('Latitud          :', style={
            'font-size': '20px', 'margin-right': '10px', 'display': 'inline-block', 'width': '80px'}),
        dcc.Input(
            id='Latitude',
            placeholder='Enter Latitud',
            type='number',
            value=lat,
            style={'width': '20%'}
        )
    ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-bottom': '10px'})

    return lati


def lon(lon):
    longi = html.Div([  # Entrada de la latitud #####
        html.Label('Longitud:', style={
            'font-size': '20px', 'margin-right': '10px', 'display': 'inline-block', 'width': '80px'}),
        dcc.Input(
            id='Longitude',
            placeholder='Enter Longitude',
            type='number',
            value=lon,
            style={'width': '20%','marginRight':'10px'}
        )
    ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'margin-bottom': '10px'})

    return longi


from dash import dash_table, html


def table_e(NDH):
    global tables
    dataframes = []
    for hora, lista in NDH.items():
        for datos in lista:
            for t in [8760, 17520, 35040, 105120]:
                if t == len(datos):
                    columns = [{'name': i, 'id': i} for i in datos.columns]
                    data = datos.to_dict('records')
                    dataframes.append((data, columns))

                    tables = [
                        html.Div([
                            html.H3(f"Año específico"),
                            html.Div(
                                dash_table.DataTable(
                                    id=f"Tabla-{i + 1}",
                                    data=data,
                                    columns=columns,
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
                                ),
                                style={'width': '100%', 'overflowX': 'auto'}  # Ensures the div takes the full width
                            )
                        ], style={'width': '100%'}) for i, (data, columns) in enumerate(dataframes)
                    ]
    return tables


def TMY(NDH):
    global tables
    dataframes = []
    for hora, lista in NDH.items():
        for datos in lista:
            for t in [8760, 17520, 35040, 105120]:
                if t == len(datos):
                    columns = [{'name': i, 'id': i} for i in datos.columns]
                    data = datos.to_dict('records')
                    dataframes.append((data, columns))

                    tables = [
                        html.Div([
                            html.H3(f"Año típico Metereológico "),
                            html.Div(
                                dash_table.DataTable(
                                    id=f"Tabla-{i + 1}",
                                    data=data,
                                    columns=columns,
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
                                ),
                                style={'width': '100%', 'overflowX': 'auto'}  # Ensures the div takes the full width
                            )
                        ], style={'width': '100%'}) for i, (data, columns) in enumerate(dataframes)
                    ]
    return tables
def type_year(t):
    tpy=html.Div(children=[html.Label("Selección de tipo de año   :",
                                           style={'font-weight': 'bold'
                                                  }),dcc.Dropdown(
        id='Tipo_A',
        options=[
            {'label':  html.Span(['Año especifico 1998-2023'], style={'color': 'Black', 'font-size': 15}), 'value': 'SY'},

            {'label': html.Span(['Año tipico Meteoreologico'], style={'color': 'Black', 'font-size': 15}), 'value': 'TMY'}
        ],
        value=t,
        style={
            'margin-bottom': '10px',
            'margin-right': '10x'
        }
    )])

    return tpy

def year_time(t):
    years = ['1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
             '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
    t
    y_t=html.Div(id="CY", children=[html.Label("Selección de Años    :",
                                           style={'font-weight': 'bold'
                                                  }),
                                dcc.Dropdown(
                                    id='Years_Selected',
                                    options=[{'label': html.Span(i,style={'color': 'Black', 'font-size': 15}), 'value': i} for i in years],
                                    value="",
                                    style={
                                        'margin-bottom': '1px',
                                        'margin-right': '20px'
                                    }
                                    ,
                                    multi=True,
                                )], style={'display': 'none'})
    return y_t

def Pos_modulo(t):

    Ps = html.Div(id="PosM", children=[html.Label("Posicion del Modulo    :",
                                                 style={'font-weight': 'bold'
                                                        }),
                                      dcc.Dropdown(
                                          id='Posicion_Mod',
                                          options=[

                                              {'label': html.Span(['Posicion ideal (Respecto a latitud)'],
                                                                  style={'color': 'Black', 'font-size': 15}),
                                               'value': 'Pos_i'},

                                              {'label': html.Span(["Posicion Especifica"],
                                                                  style={'color': 'Black', 'font-size': 15}),
                                                'value': 'Pos_e'}


                                          ],
                                          value="",
                                          style={
                                              'margin-bottom': '1px',
                                              'margin-right': '20px'
                                          }
                                          ,
                                          multi=False,
                                      )], style={'display': 'block'})
    return Ps

def tilt(lat):
    lati =dbc.InputGroup(
        [dbc.InputGroupText("Inclinación",style={'background-color': '#007bff', 'color': 'white'}), dbc.Input(id="tilt", placeholder=" Inclinación °", value=0)],size="sm",
        className="mb-3", style={

             'margin-right': '150px', 'width': '150px'
                                 })

    return lati


def Azimuth(lon):
    longi =dbc.InputGroup(
        [dbc.InputGroupText("Orientación",style={'background-color': '#007bff', 'color': 'white'}), dbc.Input(id="azimuth", placeholder="Azimuth °", value=0)],size="sm",
        className="mb-3", style={

             'margin-right': '150px', 'width': '150px'
                                 })

    return longi


def time_range(t):
    t
    t_r=html.Div(id="Time", children=[html.Label('Rango de medición  :  ', style={
        'font-weight': 'bold'  }),
                                  dcc.Dropdown(
                                      options=[{'label': html.Span(str(i), style={'color': 'Black', 'font-size': 15}), 'value': i} for i in [60, 30, 15, 5]],
                                      value="",
                                      style={
                                          'margin-bottom': '1px',
                                          'margin-right': '20px'
                                      }
                                      ,

                                      id='Diferencial de tiempo',
                                      multi=True,
                                  )], style={'display': 'none'})
    return t_r

#### Estos siguientes dropdown son los que te daran la manera correcta para acomodar el filtro de la base de datos.

def Dropdown_1():
    d1=html.Div(id="D1", children=[html.Label("","Etiqueta", style={
        'font-weight': 'bold'  }),
                                  dcc.Dropdown(
                                      options=[],
                                      value= [],
                                      style={
                                          'margin-bottom': '10px',
                                          'margin-right': '10px',
                                          'width': '100%',
                                          'color': '#000000',
                                          'font-size': 15
                                      }
                                      ,

                                      id='Drop_1',
                                      multi=True,
                                  )], style={'display': 'block'})
    return d1

def Dropdown_2():

    t_r=html.Div(id="D2", children=[html.Label("","Etiqueta2", style={
        'font-weight': 'bold'  }),
                                  dcc.Dropdown(
                                      options=[],
                                      value="",
                                      style={'margin-bottom': '10px',
                                            'margin-right': '10px',
                                            'width': '100%',
                                            'color': '#000000',
                                            'font-size': 15
                                      }
                                      ,

                                      id='Drop_2',
                                      multi=True,
                                  )], style={'display': 'none'})
    return t_r

def Dropdown_3():

    t_r=html.Div(id="D3", children=[html.Label("","Etiqueta3", style={
        'font-weight': 'bold'  }),
                                  dcc.Dropdown(
                                      options=[],
                                      value="",
                                      style={
                                          'margin-bottom': '10px',
                                          'margin-right': '10px',
                                          'width': '100%',
                                          'color': '#000000',
                                          'font-size': 15
                                      }
                                      ,

                                      id='Drop_3',
                                      multi=True,
                                  )], style={'display': 'none'})
    return t_r

def Dropdown_4():

    t_r=html.Div(id="D4", children=[html.Label("","Etiqueta4", style={
        'font-weight': 'bold'  }),
                                  dcc.Dropdown(
                                      options=[],
                                      value="",
                                      style={
                                          'margin-bottom': '10px',
                                          'margin-right': '10px',
                                          'width': '100%',
                                          'color': '#000000',
                                          'font-size': 15
                                      }
                                      ,

                                      id='Drop_4',
                                      multi=True,
                                  )], style={'display': 'none'})
    return t_r






def Data_filter(S, A, B, C):
    # Get user inputs
    # Esta representa cuando quieres ver todos los datos tal y como estan, esto por si no quieren filtrar los datos.
    # Example: "Potencia Modulo"
    # Example: "Modelo"
    # Example: "Marca"
    # Perform actions based on the conditions
    global l
    if S == "Ninguno":
        l = pd.read_excel("Libro1.xlsx")
        return l

    if A == "Potencia Modulo" and S == 0 and B == 0 and C == 0:
        # dependiendo la potencia
        l = pd.read_excel("Libro1.xlsx")
        s = l["Nameplate Pmax"].unique()
        return s

    if B == "Modelo" and S == 0 and A == 0 and C == 0:
        # dpendiendo el modelo
        l = pd.read_excel("Libro1.xlsx")
        s = l["Model Number"].unique()
        return s

    if C == "Marca" and S == 0 and A == 0 and B == 0:
        # dependiendo la marca
        l = pd.read_excel("Libro1.xlsx")
        s = l["Manufacturer"].unique()
        return s

    if A == "Potencia Modulo" and B == "Modelo" and S == 0 and C == 0 :
        l = pd.read_excel("Libro1.xlsx")
        s = l["Nameplate Pmax"].unique()
        s1 = l["Model Number"].unique()
        return s,s1

    if A == "Potencia Modulo" and C == "Marca" and S == 0 and B == 0:
        l  = pd.read_excel("Libro1.xlsx")
        s  = l["Nameplate Pmax"].unique()
        s1 = l["Manufacturer"].unique()
        return s,s1

    if B == "Modelo" and C == "Marca" and A == 0 and B == 0:
        l = pd.read_excel("Libro1.xlsx")
        s = l["Model Number"].unique()
        s1 = l["Manufacturer"].unique()
        return s,s1

    if A == "Potencia Modulo" and B == "Modelo" and C == "Marca" and S==0:
        l = pd.read_excel("Libro1.xlsx")
        s = list(l["Nameplate Pmax"].unique())
        s1 =list( l["Model Number"].unique())
        s2 = list( l["Manufacturer"].unique())
        return s,s1,s2




def filter_selector(t):
    filter_s = html.Div(id='filter_selector',children=[html.Label("Tipo de filtro  :",
                                        style={'font-weight': 'bold'
                                               }), dcc.Dropdown(id='filter_selector_',

        options=[


            {'label': html.Span(["Potencia Modulo"], style={'color': 'Black', 'font-size': 15}),
             'value':'Pm'},

            {'label': html.Span(["Modelo"], style={'color': 'Black', 'font-size': 15}),
             'value': 'M'},

            {'label': html.Span(["Marca"], style={'color': 'Black', 'font-size': 15}),
             'value': 'Mar'}


        ],
        value=t,
        style={
            'margin-bottom': '10px',
            'margin-right': '10x',
            'width': '100%'
        }
        ,
        multi=True
        ,
    )], style={'display': 'block'}

                        )


    return filter_s


def creador_de_filtros(data_bases):

    global name
    if not data_bases:
        # Return default style and empty options if no selection
        return [], {'display': 'none'}, [], "", {'display': 'none'}, [], "", {
            'display': 'none'}, [], "", {'display': 'none'}, [], ""

    # Example to handle multiple selections
    options_list = []

    if len(data_bases) == 1:
        for data_base in data_bases:
            if data_base == 'Pm':  # Make sure the value matches exactly with dropdown option value
                options_list.extend(
                    [{'label': str(num), 'value': num} for num in Data_filter(0, "Potencia Modulo", 0, 0)])
                name = "Potencia Modulo"
            if data_base == 'M':  # Make sure the value matches exactly with dropdown option value
                options_list.extend([{'label': str(num), 'value': num} for num in Data_filter(0, 0, "Modelo", 0)])
                name = "Modelo"
            if data_base == 'Mar':  # Make sure the value matches exactly with dropdown option value
                options_list.extend([{'label': str(num), 'value': num} for num in Data_filter(0, 0, 0, "Marca")])
                name = "Marca"

    if len(data_bases) == 2:
        options_list1 = []
        options_list2 = []
        options_list3 = []

        if data_bases == ['Pm', 'M'] or data_bases == ['M','Pm']:  # Make sure the value matches exactly with dropdown option value
            options_list1.extend(
                [{'label': str(num), 'value': num} for num in Data_filter(0, "Potencia Modulo", 0, 0)])
            options_list2.extend(
                [{'label': str(num), 'value': num} for num in Data_filter(0, 0, "Modelo", 0)])
            name1 = "Potencia Modulo"
            name2 = "Modelo"
            print(data_bases)
            return dcc.Loading([html.Div(id="loading")]), {'display': 'none'}, [], "", {
                'display': 'block'}, options_list1, name1, {'display': 'block'}, options_list2, name2, {
                'display': 'none'}, [], ""

        if data_bases == ['Mar', 'M'] or data_bases == ['M','Mar']:  # Make sure the value matches exactly with dropdown option value
            options_list3.extend(
                [{'label': str(num), 'value': num} for num in Data_filter(0, 0, 0, "Marca")])
            options_list2.extend(
                [{'label': str(num), 'value': num} for num in Data_filter(0, 0, "Modelo", 0)])
            name3 = "Marca"
            name2 = "Modelo"
            print(data_bases)
            return dcc.Loading([html.Div(id="loading")]), {'display': 'none'}, [], "", {
                'display': 'none'}, [],"", {'display': 'block'}, options_list2, name2, {
                'display': 'block'}, options_list3, name3

        if data_bases == ['Mar', 'Pm'] or data_bases == ['Pm','Mar']:  # Make sure the value matches exactly with dropdown option value
            options_list3.extend(
                [{'label': str(num), 'value': num} for num in Data_filter(0, 0, 0, "Marca")])
            options_list1.extend(
                [{'label': str(num), 'value': num} for num in Data_filter(0, "Potencia Modulo", 0, 0)])
            name3 = "Marca"
            name1 = "Potencia Modulo"
            print(data_bases)
            return dcc.Loading([html.Div(id="loading")]), {'display': 'none'}, [], "", {
                'display': 'block'}, options_list1,name1, {'display': 'none'}, [], "", {
                'display': 'block'}, options_list3, name3

    if len(data_bases) == 3:
        options_list1 = []
        options_list2 = []
        options_list3 = []

        if data_bases == ['Pm', 'M', 'Mar'] or data_bases == ['Pm', 'Mar', 'M'] or data_bases == ['M', 'Pm',
                                                                                                  'Mar'] or data_bases == [
            'M', 'Mar', 'Pm'] or data_bases == ['Mar', 'Pm', 'M'] or data_bases == ['Mar', 'M', 'Pm']:
            options_list1.extend(
                [{'label': str(num), 'value': num} for num in Data_filter(0, "Potencia Modulo", 0, 0)])
            options_list2.extend(
                [{'label': str(num), 'value': num} for num in Data_filter(0, 0, "Modelo", 0)]),
            options_list3.extend(
                [{'label': str(num), 'value': num} for num in Data_filter(0, 0, 0, "Marca")])

            name1 = "Potencia Modulo"
            name2 = "Modelo"
            name3 = "Marca"
            print(data_bases)
            return dcc.Loading([html.Div(id="loading")]), {'display': 'none'}, [], "", {
                'display': 'block'}, options_list1, name1, {'display': 'block'}, options_list2, name2, {
                'display': 'block'}, options_list3, name3

    if options_list:
        return dcc.Loading([html.Div(id="loading")]), {'display': 'block'}, options_list, name, {
            'display': 'none'}, [], "", {'display': 'none'}, [], "", {'display': 'none'}, [], ""
    else:
        return dcc.Loading([html.Div(id="loading")]), {'display': 'none'}, [], "", {'display': 'none'}, [], "", {
            'display': 'none'}, [], "", {'display': 'none'}, [], ""

def tabla_modulos_base():

        final_one= dash_table.DataTable(
        id='Table_modulos_base',
        columns=[],
        data=[],
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
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
        page_size=4,
        style_table={'overflowX': 'auto', 'maxHeight': '500px', 'overflowY': 'auto'},
            style_cell={
                'minWidth': '100px', 'maxWidth': '200px',
                'whiteSpace': 'normal',
                'textAlign': 'left'
            }
        )


        return final_one

def temperature_items():
    t= html.Div([
                dbc.Label("Selecciona el metodo de analisis para la temperatura del Modulo"),
                dbc.Checklist(
                    options=[
                        {"label": "Feinman", "value": 1},
                        {"label": "Sandia", "value": 2},
                        {"label": "NOCT", "value": 3},
                    ],
                    value=[],
                    id="checklist-input",
                ),
            ])

    return t

def Feinman_options():
        feinman_div = html.Div(
            id="feinman",
            children=[
                dbc.Row([
                    dbc.Col(dbc.Label("Opciones para Feinman:"), width=12),
                    dbc.Col(
                        table("U0", "", "U_0", 25.0),
                        width=6
                    ),
                    dbc.Col(
                        table("U1", "", "U_1", 6.84),
                        width=6
                    )
                ])
            ],
            style={'display': 'none',"width": "100px"}
        )

        return feinman_div


def NOCT_In():
    NOCT_div = html.Div(
        id="NOCT",
        children=[
            dbc.Row([
                dbc.Col(dbc.Label("Temperatura:"), width=12),
                dbc.Col(
                    table("NOCT", "", "noct", 43),
                    width=3
                )
            ])
        ],
        style={'display': 'none',"width": "10px"}
    )

    return NOCT_div

def Sandia_options():
    t =html.Div(
        id="sandia", #Con este id , se muestra el div que contiene las temps
        children=[
            dbc.Row([
                dbc.Col(dbc.Label("Opciones para Sandia:"), width=12),
                dbc.Col(
                    dbc.RadioItems(
                        options=[
                            {"label": "glass/glass open-rack", "value": 1},
                            {"label": "glass/glass close-roof", "value": 2},
                            {"label": "glass/polymer open/rack", "value": 3},
                            {"label": "glass/polymer insulated back", "value": 4},
                        ],
                        id="radio-sandia", #este div contien
                    ), width=12
                )
            ])
        ],style={'display': 'none'}
)

    return t

def Temperature_sandia( Sandia,NDH ):
            a, b = np.array([-3.47, -2.98, -3.56, -2.81, -3.58, -3.23]), np.array([-.0594, -.0471, -.0750, -.0455, -.113, -.130])
            deltaT = [3, 1, 3, 0]

            for horas, datos in NDH.items():
                for lista in datos:
                    for size in [8760, 17520, 35040, 105120]:
                        if len(lista) == size:
                            E = lista.Poa_global  # Irradiancia global horizontal
                            WS = lista.wind_speed  # Velocidad del viento
                            Ta = lista.temp_air
                            Eo = 1000
                            # Calculo dela temperatura Sandia
                            T = E * (np.exp(a[Sandia - 1] + (b[Sandia - 1] * WS))) + Ta  # calculo de modelo sandia con temperatura de modulo
                            Ts = pvlib.temperature.sapm_cell_from_module(T, E, deltaT[Sandia - 1],irrad_ref=Eo)  # calculo de modelo sandia temperatura de celda
                            lista["Tsandia"] = Ts




def Temperature_feinman( U0,U1,NDH ):
    for horas, datos in NDH.items():
        for lista in datos:
            for size in [8760, 17520, 35040, 105120]:
                E = lista.Poa_global  # Irradiancia global horizontal
                WS = lista.wind_speed  # Velocidad del viento
                Ta = lista.temp_air
                TFeinman = pvlib.temperature.faiman(poa_global=E, temp_air=Ta, wind_speed=WS, u0=U0,
                                                    u1=U1)  # u0=29.432, u1=4.468
                lista["TFeinman"] = TFeinman


def Temperature_NOCT( TNMOT,NDH ):
    for horas, datos in NDH.items():
        for lista in datos:
            for size in [8760, 17520, 35040, 105120]:
                E = lista.Poa_global  # Irradiancia global horizontal
                WS = lista.wind_speed  # Velocidad del viento
                Ta = lista.temp_air
                TNOCT = Ta +((((TNMOT)-20)/800)*E) # TNMOT: Es la temperatura del modullo
                lista["NOCT"] = TNOCT


def creador_csv_clima(NDH):
    # Eliminar todos los archivos CSV generados por esta función en el pasado
    nombres = []
    csv_files = glob.glob("g_*.csv")
    for file in csv_files:
        try:
            os.remove(file)
            print(f"Archivo {file} eliminado.")
        except Exception as e:
            print(f"Error eliminando archivo {file}: {e}")

    for hora, lista in NDH.items():
        for datos in lista:
            print(f"Procesando datos para hora: {hora}")
            for t in [8760, 17520, 35040, 105120]:
                if t == len(datos):
                    try:
                        # Crear el nombre del archivo sin basarse en el año

                        nombre = f"g_{datos.Year.unique()[0]}_{t}.csv"
                        nombres.append(nombre)
                        datos.to_csv(nombre, index=True)
                        print(f"Archivo {nombre} generado exitosamente.")
                    except PermissionError:
                        print(f"Error de permiso al procesar {hora} con {t} datos: no se pudo acceder a {nombre}.")
                    except Exception as e:
                        print(f"Error procesando {hora} con {t} datos: {e}")
    return nombres

#ahora tenemos que generar los CSV de los parametros electricos.

def creador_csv_PE(PE1):
    nombres_1 = []
    csv_files = glob.glob("PE_*.csv")

    for file in csv_files:
        try:
            os.remove(file)
            print(f"Archivo {file} eliminado.")
        except Exception as e:
            print(f"Error eliminando archivo {file}: {e}")

    for hora, lista in PE1.items():
        print(f"Procesando datos para hora: {hora}")
        for t in [8760, 17520, 35040, 105120]:
            if t == len(lista):
                try:
                    nombre = f"PE_{lista['Year'].unique()[0]}_{t}.csv"
                    nombres_1.append(nombre)
                    lista.to_csv(nombre, index=True)
                    print(f"Archivo {nombre} generado exitosamente.")
                except PermissionError:
                    print(f"Error de permiso al procesar {hora} con {t} datos: no se pudo acceder a {nombre}.")
                except Exception as e:
                    print(f"Error procesando {hora} con {t} datos: {e}")

    return nombres_1

def creador_csv_PE2(PE2):
    nombres_2 = []
    csv_files = glob.glob("PE2_*.csv")

    for file in csv_files:
        try:
            os.remove(file)
            print(f"Archivo {file} eliminado.")
        except Exception as e:
            print(f"Error eliminando archivo {file}: {e}")

    for hora, lista in PE2.items():
        print(f"Procesando datos para hora: {hora}")
        for t in [8760, 17520, 35040, 105120]:
            if t == len(lista):
                try:
                    nombre = f"PE2_{lista['Year'].unique()[0]}_{t}.csv"
                    nombres_2.append(nombre)
                    lista.to_csv(nombre, index=True)
                    print(f"Archivo {nombre} generado exitosamente.")
                except PermissionError:
                    print(f"Error de permiso al procesar {hora} con {t} datos: no se pudo acceder a {nombre}.")
                except Exception as e:
                    print(f"Error procesando {hora} con {t} datos: {e}")

    return nombres_2

#def creador_uplouded(PE2):
    #nombres_2 = []
    #csv_files = glob.glob("Uploaded_.csv")

    #for file in csv_files:
        #try:
            #os.remove(file)
            #print(f"Archivo {file} eliminado.")
        #except Exception as e:
            #print(f"Error eliminando archivo {file}: {e}")


    #nombre = f"Uploaded_.csv"
    #nombres_2.append(nombre)
    #PE2.to_csv(nombre, index=False)


    #return nombres_2

#def creador_uplouded(PE2):
#    nombres_2 = []

    # Buscar archivos existentes con extensión .xlsx
 #   xlsx_files = glob.glob("Uploaded_.xlsx")

    # Eliminar archivos previos si existen
  #  for file in xlsx_files:
   #     try:
    #        os.remove(file)
            #print(f"Archivo {file} eliminado.")
#        except Exception as e:

 #           print(f"Error eliminando archivo {file}: {e}")

    # Guardar el nuevo archivo en formato Excel
    #nombre = f"Uploaded_.xlsx"
    #nombres_2.append(nombre)
    #PE2.to_excel(nombre, index=False, engine='openpyxl')  # Especifica el motor de escritura
    #print(f"Archivo {nombre} creado exitosamente.")

    #return nombres_2

def eliminar_archivo_anterior():
    if os.path.exists("Uploaded_.xlsx"):
        os.remove("Uploaded_.xlsx")
        print("Archivo 'Uploaded_.xlsx' eliminado.")


# Función para procesar el archivo subido y renombrarlo
def guardar_archivo(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Leer todas las hojas del archivo Excel subido
    xls = pd.ExcelFile(io.BytesIO(decoded), engine='openpyxl')
    sheets = xls.sheet_names

    # Eliminar el archivo anterior si existe
    eliminar_archivo_anterior()

    # Guardar el archivo subido como "Uploaded_.xlsx"
    with pd.ExcelWriter("Uploaded_.xlsx", engine='openpyxl') as writer:
        for sheet in sheets:
            df = pd.read_excel(xls, sheet_name=sheet)
            df.to_excel(writer, sheet_name=sheet, index=False)

    print("Archivo subido y guardado como 'Uploaded_.xlsx'.")
    return sheets, xls  # Retorna las hojas y el archivo Excel para mostrar las tablas

def Placa_Prueba(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series, temp_ref, celltype):

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
    Tc = "monoSi"


    # Crear un diccionario con los valores recibidos
    datos_placa = {
        'Pmax': float(Pot),
        'Vmax60': float(Vm),
        'Imax': float(Im),
        'Voc': float(Voc),
        'Isc': float(Isc),
        'alpha': float(alpha),
        'beta': float(beta),
        'deltha': float(gamma), ### Este antes era Gamma.
        'cells_in_series': float(Numero_celda),
        'temp_ref': float(Tempref),
        'cell_type': str(Tc),
        'A': 1.33,
        'Boltzmann': constants.Boltzmann,
        'Elementary_charge': constants.elementary_charge
    }
    # Retornar el diccionario
    return datos_placa

def Placa_D1(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series, temp_ref, celltype):
    # Crear un diccionario con los valores recibidos
    datos_placa = {
        'Pmax': Pmax0,
        'Vmax60': Vmax60,
        'Imax': Imax0,
        'Voc': Voc0,
        'Isc': Isc0,
        'alpha': alpha,
        'beta': beta,
        'deltha': deltha,
        'cells_in_series': cells_in_series,
        'temp_ref': temp_ref,
        'cell_type': str(celltype),
        'A': 1.33,
        'Boltzmann': constants.Boltzmann,
        'Elementary_charge': constants.elementary_charge
    }
    # Retornar el diccionario
    return datos_placa

def Placa_D2(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series, temp_ref, celltype):
    # Crear un diccionario con los valores recibidos
    datos_placa = {
        'Pmax': Pmax0,
        'Vmax60': Vmax60,
        'Imax': Imax0,
        'Voc': Voc0,
        'Isc': Isc0,
        'alpha': alpha,
        'beta': beta,
        'deltha': deltha,
        'cells_in_series': cells_in_series,
        'temp_ref': temp_ref,
        'cell_type': str(celltype),
        'A': 1.33,
        'Boltzmann': constants.Boltzmann,
        'Elementary_charge': constants.elementary_charge
    }
    # Retornar el diccionario
    return datos_placa

def df_creator(nombre,Seleccion):
    datos = []
    if Seleccion == [1]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)
    if Seleccion == [1,2]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)
    if Seleccion == [2]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

    if Seleccion == [3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

    if Seleccion == [1,3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

    if Seleccion == [2,3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

    if Seleccion == [1,2,3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

    return datos

def df_creator_PE(nombre,Seleccion):
    datos = []
    if Seleccion == [1]:
        for i in nombre:
            print(i)
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Time"])
            l = l.set_index(time)
            l.drop(columns=['Time'], inplace=True)
            datos.append(l)
            print("Feynmann")
    if Seleccion == [1,2]:
        for i in nombre:
            print(i)
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Time"])
            l = l.set_index(time)
            l.drop(columns=['Time'], inplace=True)
            datos.append(l)
            print("Feynmann/Sandia")

    if Seleccion == [2]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)
            print("Sandia")

    if Seleccion == [3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

    if Seleccion == [1, 3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

    if Seleccion == [2, 3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

    if Seleccion == [1, 2, 3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

    return datos

def df_creator_1(nombre,Seleccion):
    datos = []
    if Seleccion == [1]:

        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Time"])
            l = l.set_index(time)
            l.drop(columns=['Time'], inplace=True)
            datos.append(l)
            print("Feynmann")

    if Seleccion == [1,2]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Time"])
            l = l.set_index(time)
            l.drop(columns=['Time'], inplace=True)
            datos.append(l)
            print("Feynmann/Sandia")

    if Seleccion == [2]:

        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)
            print("Sandia")

    if Seleccion == [3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)
            print("NOCT")

    if Seleccion == [1, 3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)
            print("Feynmann/NOCT")

    if Seleccion == [2, 3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)
            print("Sandia/NOCT")

    if Seleccion == [1, 2, 3]:
        for i in nombre:
            d = pd.read_csv(i)
            l = pd.DataFrame(d)
            time = pd.to_datetime(l["Unnamed: 0"])
            l = l.set_index(time)
            l.index.names = ['Time']
            l.drop(columns=["Unnamed: 0"], inplace=True)
            datos.append(l)

            print("Sandia/NOCTFeinman")

    return datos

### Tienes que obtener el factor de idealidad para cada situacion, esto permitira ser mas precisos

def Factor_Idealidad(Placa_r, Ndh):
    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=Placa_r["Vmax60"],
        i_mp=Placa_r["Imax"],
        v_oc=Placa_r["Voc"],
        i_sc=Placa_r["Isc"],
        alpha_sc=float(Placa_r["alpha"] / 100) * (Placa_r["Isc"]),
        beta_voc=float(Placa_r["beta"] / 100) * (Placa_r["Voc"]),
        gamma_pmp=float(Placa_r["deltha"]),
        cells_in_series=float(Placa_r["cells_in_series"]),
        temp_ref=float(Placa_r["temp_ref"])
    )

    for datos in Ndh:
        if 'TFeinman' in datos:
            temp = datos['TFeinman']
            rad = datos['Poa_global']
            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AF"] = nNsVth
            return nNsVth

        if 'Tsandia' in datos:
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AS"] = nNsVthS
            return nNsVthS

        if 'Tsandia' in datos and 'TFeinman' in datos:
            temp = datos['TFeinman']
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["AS"] = nNsVthS
            return nNsVth, nNsVthS

def PE(Placa_r,Ndh): #PLaca es una libreria que contiene valores
    irr={}
    x= -1

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=Placa_r["Vmax60"],
        i_mp=Placa_r["Imax"],
        v_oc=Placa_r["Voc"],
        i_sc=Placa_r["Isc"],
        alpha_sc=float(Placa_r["alpha"] / 100) * (Placa_r["Isc"]),
        beta_voc=float(Placa_r["beta"] / 100) * (Placa_r["Voc"]),
        gamma_pmp=float(Placa_r["deltha"]),
        cells_in_series=float(Placa_r["cells_in_series"]),
        temp_ref=float(Placa_r["temp_ref"])
    )

    for datos in Ndh:
        if 'TFeinman' in datos:
            temp = datos['TFeinman']
            rad = datos['Poa_global']
            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AF"] = nNsVth

        if 'Tsandia' in datos:
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AS"] = nNsVthS


        if 'Tsandia' in datos and 'TFeinman' in datos:
            temp = datos['TFeinman']
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["AS"] = nNsVthS



    for datos in Ndh:



                    x = x + 1
                    A= 1.2928
                    K =Placa_r["Boltzmann"]
                    q = Placa_r["Elementary_charge"]
                    Pmax0 = Placa_r["Pmax"]
                    Imax0 = Placa_r["Imax"]
                    Vmax0 = Placa_r["Vmax60"]
                    Voc0 = Placa_r["Voc"]
                    Isc0c = Placa_r["Isc"]  # Aquí se corrigió el nombre de la variable
                    deltha = Placa_r["deltha"]/100 # Esto de aqui es realmente gamma.
                    betha = Placa_r["beta"] / 100  # Aquí se corrigió el nombre de la variable para mantener la consistencia
                    alpha = Placa_r["alpha"] / 100  # Recuerda este valor es importante dividir entre 100


                    nombre_df = f"{len(datos)}_{pd.to_datetime(Ndh[x].index).year.unique()[0]}"
                    df = pd.DataFrame(datos.Poa_global)

                    # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                    df["Year"] = datos.Year
                    df["Month"] = datos.Month
                    gamma = (datos.AF * K * (datos.TFeinman + 273.15)) / q ## Esto es deltha y no gamma.

                    df["Gamma_F"] = gamma # este deberia de ser deltha y no gamma.
                    Isc0 = Isc0c * (1 + (alpha * (datos.TFeinman - 25))) * ((datos.Poa_global) / 1000)
                    df["Isc0_F"] = Isc0
                    Voc60 = Voc0 * (1 + (betha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                    Voc60[np.isinf(Voc60)] = 0
                    df["Voc_F"] = Voc60

                    Imax60 = Imax0 * (1 + alpha * (datos.TFeinman - 25)) * (datos.Poa_global / 1000)
                    df["Imax_F"] = Imax60

                    Vmax60 = Vmax0 * (1 + (deltha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                    Vmax60[np.isinf(Vmax60)] = 0
                    df["Vmax_F"] = Vmax60

                    #Pmax = ((Pmax0 * (1 + deltha * (datos.TFeinman - 25))) * (
                                #1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                    Pmax = df["Vmax_F"]*df["Imax_F"]
                    Pmax[np.isnan(Pmax)] = 0
                    df["Pmax_F"] = Pmax

                    df["T_Feinman"]=datos.TFeinman

                    df["AF"]=datos.AF



                    irr[nombre_df] = df
    return irr


#NOCT Funcion

def PE_NOCT(Placa_r,Ndh,Seleccion): #PLaca es una libreria que contiene valores
    irr={}
    x= -1

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=Placa_r["Vmax60"],
        i_mp=Placa_r["Imax"],
        v_oc=Placa_r["Voc"],
        i_sc=Placa_r["Isc"],
        alpha_sc=float(Placa_r["alpha"] / 100) * (Placa_r["Isc"]),
        beta_voc=float(Placa_r["beta"] / 100) * (Placa_r["Voc"]),
        gamma_pmp=float(Placa_r["deltha"]),
        cells_in_series=float(Placa_r["cells_in_series"]),
        temp_ref=float(Placa_r["temp_ref"])
    )

    for datos in Ndh:
        if 'TFeinman' in datos:
            temp = datos['TFeinman']
            rad = datos['Poa_global']
            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AF"] = nNsVth

        if 'Tsandia' in datos:
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AS"] = nNsVthS

        if 'NOCT' in datos:
            temps = datos['NOCT']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthn = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["ANOCT"] = nNsVthn

        if 'NOCT' in datos and 'TFeinman' in datos:
            tempn = datos['NOCT']
            temp = datos['TFeinman']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthn = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=tempn,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["ANOCT"] = nNsVthn


        if 'NOCT' in datos and 'Tsandia' in datos:
            tempn = datos['NOCT']
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthn = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=tempn,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVths = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AS"] = nNsVths
            datos["ANOCT"] = nNsVthn




        if 'Tsandia' in datos and 'TFeinman' in datos and 'NOCT':
            temp = datos['TFeinman']
            temps = datos['Tsandia']
            tempn = datos['NOCT']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            ILS, I0S, RsS, RshS, nNsVthn = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=tempn,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["AS"] = nNsVthS
            datos["ANOCT"] = nNsVthn

        if 'Tsandia' in datos and 'TFeinman' in datos:
            temp = datos['TFeinman']
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["AS"] = nNsVthS



    for datos in Ndh:



                    x = x + 1
                    A= 1.2928
                    K =Placa_r["Boltzmann"]
                    q = Placa_r["Elementary_charge"]
                    Pmax0 = Placa_r["Pmax"]
                    Imax0 = Placa_r["Imax"]
                    Vmax0 = Placa_r["Vmax60"]
                    Voc0 = Placa_r["Voc"]
                    Isc0c = Placa_r["Isc"]  # Aquí se corrigió el nombre de la variable
                    deltha = Placa_r["deltha"]/100 # Esto de aqui es realmente gamma.
                    betha = Placa_r["beta"] / 100  # Aquí se corrigió el nombre de la variable para mantener la consistencia
                    alpha = Placa_r["alpha"] / 100  # Recuerda este valor es importante dividir entre 100


                    nombre_df = f"{len(datos)}_{pd.to_datetime(Ndh[x].index).year.unique()[0]}"
                    df = pd.DataFrame(datos.Poa_global)

                    if Seleccion==[3]:

                        # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                        df["Year"] = datos.Year
                        df["Month"] = datos.Month
                        gamma = (datos.ANOCT * K * (datos.NOCT + 273.15)) / q ## Esto es deltha y no gamma.

                        df["Gamma_NOCT"] = gamma # este deberia de ser deltha y no gamma.
                        Isc0 = Isc0c * (1 + (alpha * (datos.NOCT - 25))) * ((datos.Poa_global) / 1000)
                        df["Isc0_NOCT"] = Isc0
                        Voc60 = Voc0 * (1 + (betha * (datos.NOCT - 25))) * (
                                    1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))
                        Voc60[np.isinf(Voc60)] = 0
                        df["Voc_NOCT"] = Voc60

                        Imax60 = Imax0 * (1 + alpha * (datos.NOCT - 25)) * (datos.Poa_global / 1000)
                        df["Imax_NOCT"] = Imax60

                        Vmax60 = Vmax0 * (1 + (deltha * (datos.NOCT - 25))) * (
                                    1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))
                        Vmax60[np.isinf(Vmax60)] = 0
                        df["Vmax_NOCT"] = Vmax60

                       # Pmax = #((Pmax0 * (1 + deltha * (datos.NOCT - 25))) * (
                                #    1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                        Pmax = df.Imax_NOCT*df.Vmax_NOCT
                        Pmax[np.isnan(Pmax)] = 0
                        df["Pmax_NOCT"] = Pmax

                        df["T_NOCT"]=datos.NOCT

                        df["ANOCT"]=datos.ANOCT

                        irr[nombre_df] = df

                    if Seleccion==[1,3]:

                        # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                        df["Year"] = datos.Year
                        df["Month"] = datos.Month
                        gamma = (datos.ANOCT * K * (datos.NOCT + 273.15)) / q ## Esto es deltha y no gamma.

                        df["Gamma_NOCT"] = gamma # este deberia de ser deltha y no gamma.
                        Isc0 = Isc0c * (1 + (alpha * (datos.NOCT - 25))) * ((datos.Poa_global) / 1000)
                        df["Isc0_NOCT"] = Isc0
                        Voc60 = Voc0 * (1 + (betha * (datos.NOCT - 25))) * (
                                    1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))
                        Voc60[np.isinf(Voc60)] = 0
                        df["Voc_NOCT"] = Voc60

                        Imax60 = Imax0 * (1 + alpha * (datos.NOCT - 25)) * (datos.Poa_global / 1000)
                        df["Imax_NOCT"] = Imax60

                        Vmax60 = Vmax0 * (1 + (deltha * (datos.NOCT - 25))) * (
                                    1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))
                        Vmax60[np.isinf(Vmax60)] = 0
                        df["Vmax_NOCT"] = Vmax60

                        #Pmax = ((Pmax0 * (1 + deltha * (datos.NOCT - 25))) * (
                         #           1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                        Pmax =df.Imax_NOCT*df.Vmax_NOCT
                        Pmax[np.isnan(Pmax)] = 0
                        df["Pmax_NOCT"] = Pmax

                        df["T_NOCT"]=datos.NOCT

                        df["ANOCT"]=datos.ANOCT

                        gamma = (datos.AF * K * (datos.TFeinman + 273.15)) / q
                        df["Gamma_F"] = gamma
                        Isc0 = Isc0c * (1 + (alpha * (datos.TFeinman - 25))) * ((datos.Poa_global) / 1000)
                        df["Isc0_F"] = Isc0
                        Voc60 = Voc0 * (1 + (betha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                        Voc60[np.isinf(Voc60)] = 0
                        df["Voc_F"] = Voc60

                        Imax60 = Imax0 * (1 + (alpha * (datos.TFeinman - 25))) * (datos.Poa_global / 1000)
                        df["Imax_F"] = Imax60

                        Vmax60 = Vmax0 * (1 + (deltha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                        Vmax60[np.isinf(Vmax60)] = 0
                        df["Vmax_F"] = Vmax60

                        #Pmax = ((Pmax0 * (1 + (deltha * (datos.TFeinman - 25)))) * (
                         #       1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                        Pmax = df.Imax_F*df.Vmax_F
                        Pmax[np.isnan(Pmax)] = 0
                        df["Pmax_F"] = Pmax
                        df["T_Feinman"] = datos.TFeinman
                        df["AF"] = datos.AF

                        irr[nombre_df] = df

                    if Seleccion==[2,3]:

                        # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                        df["Year"] = datos.Year
                        df["Month"] = datos.Month
                        gamma = (datos.ANOCT * K * (datos.NOCT + 273.15)) / q ## Esto es deltha y no gamma.

                        df["Gamma_NOCT"] = gamma # este deberia de ser deltha y no gamma.
                        Isc0 = Isc0c * (1 + (alpha * (datos.NOCT - 25))) * ((datos.Poa_global) / 1000)
                        df["Isc0_NOCT"] = Isc0
                        Voc60 = Voc0 * (1 + (betha * (datos.NOCT - 25))) * (
                                    1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))
                        Voc60[np.isinf(Voc60)] = 0
                        df["Voc_NOCT"] = Voc60

                        Imax60 = Imax0 * (1 + alpha * (datos.NOCT - 25)) * (datos.Poa_global / 1000)
                        df["Imax_NOCT"] = Imax60

                        Vmax60 = Vmax0 * (1 + (deltha * (datos.NOCT - 25))) * (
                                    1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))
                        Vmax60[np.isinf(Vmax60)] = 0
                        df["Vmax_NOCT"] = Vmax60

                        #Pmax = ((Pmax0 * (1 + deltha * (datos.NOCT - 25))) * (
                         #           1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                        Pmax=df.Imax_NOCT*df.Vmax_NOCT
                        Pmax[np.isnan(Pmax)] = 0
                        df["Pmax_NOCT"] = Pmax

                        df["T_NOCT"]=datos.NOCT

                        df["ANOCT"]=datos.ANOCT

                        gamma = (datos.AS * K * (datos.Tsandia + 273.15)) / q
                        df["Gamma_S"] = gamma
                        Isc0 = Isc0c * (1 + (alpha * (datos.Tsandia - 25))) * (datos.Poa_global / 1000)
                        df["Isc0_S"] = Isc0

                        # Modificando las ecuaciones para usar 'datos.Tsandia' y agregando "_S" a los nombres de las columnas
                        Voc60 = Voc0 * (1 + (betha * (datos.Tsandia - 25))) * (
                                1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                        Voc60[np.isinf(Voc60)] = 0
                        df["Voc_S"] = Voc60

                        Imax60 = Imax0 * (1 + alpha * (datos.Tsandia - 25)) * (datos.Poa_global / 1000)
                        df["Imax_S"] = Imax60

                        Vmax60 = Vmax0 * (1 + (deltha * (datos.Tsandia - 25))) * (
                                1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                        Vmax60[np.isinf(Vmax60)] = 0
                        df["Vmax_S"] = Vmax60

                        #Pmax60 = ((Pmax0 * (1 + deltha * (datos.Tsandia - 25))) * (
                                #1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                        Pmax60 = df.Imax_S*df.Vmax_S
                        Pmax60[np.isnan(Pmax60)] = 0
                        df["Pmax_S"] = Pmax60
                        df["T_Sandia"] = datos.Tsandia
                        df["AS"] = datos.AS

                        irr[nombre_df] = df

                    if Seleccion == [1,2, 3]:
                        # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                        df["Year"] = datos.Year
                        df["Month"] = datos.Month
                        gamma = (datos.ANOCT * K * (datos.NOCT + 273.15)) / q  ## Esto es deltha y no gamma.

                        df["Gamma_NOCT"] = gamma  # este deberia de ser deltha y no gamma.
                        Isc0 = Isc0c * (1 + (alpha * (datos.NOCT - 25))) * ((datos.Poa_global) / 1000)
                        df["Isc0_NOCT"] = Isc0
                        Voc60 = Voc0 * (1 + (betha * (datos.NOCT - 25))) * (
                                1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))
                        Voc60[np.isinf(Voc60)] = 0
                        df["Voc_NOCT"] = Voc60

                        Imax60 = Imax0 * (1 + alpha * (datos.NOCT - 25)) * (datos.Poa_global / 1000)
                        df["Imax_NOCT"] = Imax60

                        Vmax60 = Vmax0 * (1 + (deltha * (datos.NOCT - 25))) * (
                                1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))
                        Vmax60[np.isinf(Vmax60)] = 0
                        df["Vmax_NOCT"] = Vmax60

                        #Pmax = ((Pmax0 * (1 + deltha * (datos.NOCT - 25))) * (
                         #       1 + (df.Gamma_NOCT * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)

                        Pmax= df.Imax_NOCT*df.Vmax_NOCT
                        Pmax[np.isnan(Pmax)] = 0
                        df["Pmax_NOCT"] = Pmax

                        df["T_NOCT"] = datos.NOCT

                        df["ANOCT"] = datos.ANOCT

                        gamma = (datos.AF * K * (datos.TFeinman + 273.15)) / q
                        df["Gamma_F"] = gamma
                        Isc0 = Isc0c * (1 + (alpha * (datos.TFeinman - 25))) * ((datos.Poa_global) / 1000)
                        df["Isc0_F"] = Isc0
                        Voc60 = Voc0 * (1 + (betha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                        Voc60[np.isinf(Voc60)] = 0
                        df["Voc_F"] = Voc60

                        Imax60 = Imax0 * (1 + (alpha * (datos.TFeinman - 25))) * (datos.Poa_global / 1000)
                        df["Imax_F"] = Imax60

                        Vmax60 = Vmax0 * (1 + (deltha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                        Vmax60[np.isinf(Vmax60)] = 0
                        df["Vmax_F"] = Vmax60

                        #Pmax = ((Pmax0 * (1 + (deltha * (datos.TFeinman - 25)))) * (
                         #       1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                        Pmax = df.Imax_F*df.Vmax_F
                        Pmax[np.isnan(Pmax)] = 0
                        df["Pmax_F"] = Pmax
                        df["T_Feinman"] = datos.TFeinman
                        df["AF"] = datos.AF

                        gamma = (datos.AS * K * (datos.Tsandia + 273.15)) / q
                        df["Gamma_S"] = gamma
                        Isc0 = Isc0c * (1 + (alpha * (datos.Tsandia - 25))) * (datos.Poa_global / 1000)
                        df["Isc0_S"] = Isc0

                        # Modificando las ecuaciones para usar 'datos.Tsandia' y agregando "_S" a los nombres de las columnas
                        Voc60 = Voc0 * (1 + (betha * (datos.Tsandia - 25))) * (
                                1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                        Voc60[np.isinf(Voc60)] = 0
                        df["Voc_S"] = Voc60

                        Imax60 = Imax0 * (1 + alpha * (datos.Tsandia - 25)) * (datos.Poa_global / 1000)
                        df["Imax_S"] = Imax60

                        Vmax60 = Vmax0 * (1 + (deltha * (datos.Tsandia - 25))) * (
                                1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                        Vmax60[np.isinf(Vmax60)] = 0
                        df["Vmax_S"] = Vmax60

                        #Pmax60 = ((Pmax0 * (1 + deltha * (datos.Tsandia - 25))) * (
                         #       1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                        Pmax60= df.Imax_S*df.Vmax_S
                        Pmax60[np.isnan(Pmax60)] = 0
                        df["Pmax_S"] = Pmax60
                        df["T_Sandia"] = datos.Tsandia
                        df["AS"] = datos.AS

                        irr[nombre_df] = df

    return irr

def PE_t(Placa_r,Ndh): #PLaca es una libreria que contiene valores
    irr={}
    x = -1
    FA = Factor_Idealidad(Placa_r, Ndh)

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=Placa_r["Vmax60"],
        i_mp=Placa_r["Imax"],
        v_oc=Placa_r["Voc"],
        i_sc=Placa_r["Isc"],
        alpha_sc=float(Placa_r["alpha"] / 100) * (Placa_r["Isc"]),
        beta_voc=float(Placa_r["beta"] / 100) * (Placa_r["Voc"]),
        gamma_pmp=float(Placa_r["deltha"]),
        cells_in_series=float(Placa_r["cells_in_series"]),
        temp_ref=float(Placa_r["temp_ref"])
    )

    for datos in Ndh:
        if 'TFeinman' in datos:
            temp = datos['TFeinman']
            rad = datos['Poa_global']
            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AF"] = nNsVth

        if 'Tsandia' in datos:
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AS"] = nNsVthS

        if 'Tsandia' in datos and 'TFeinman' in datos:
            temp = datos['TFeinman']
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["AS"] = nNsVthS

    for datos in Ndh:
                    x = x + 1
                    A = FA
                    K =Placa_r["Boltzmann"]
                    q = Placa_r["Elementary_charge"]
                    Pmax0 = Placa_r["Pmax"]
                    Imax0 = Placa_r["Imax"]
                    Vmax0 = Placa_r["Vmax60"]
                    Voc0 = Placa_r["Voc"]
                    Isc0c = Placa_r["Isc"]  # Aquí se corrigió el nombre de la variable
                    deltha= Placa_r["deltha"]/100
                    betha = Placa_r["beta"]/100  # Aquí se corrigió el nombre de la variable para mantener la consistencia
                    alpha = Placa_r["alpha"]/ 100  # Recuerda este valor es importante dividir entre 100


                    nombre_df = f"{len(datos)}_{pd.to_datetime(Ndh[x].index).year.unique()[0]}"
                    df = pd.DataFrame(datos.Poa_global)

                    # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                    df["Year"] = datos.Year
                    df["Month"] = datos.Month
                    gamma = (datos.AF * K * (datos.TFeinman + 273.15)) / q
                    df["Gamma_F"] = gamma
                    Isc0 = Isc0c * (1 + (alpha * (datos.TFeinman - 25))) * ((datos.Poa_global) / 1000)
                    df["Isc0_F"] = Isc0
                    Voc60 = Voc0 * (1 + (betha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                    Voc60[np.isinf(Voc60)] = 0
                    df["Voc_F"] = Voc60

                    Imax60 = Imax0 * (1 + (alpha * (datos.TFeinman - 25))) * (datos.Poa_global / 1000)
                    df["Imax_F"] = Imax60

                    Vmax60 = Vmax0 * (1 + (deltha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                    Vmax60[np.isinf(Vmax60)] = 0
                    df["Vmax_F"] = Vmax60

                    #Pmax = ((Pmax0 * (1 + (deltha * (datos.TFeinman - 25)))) * (
                     #           1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                    Pmax=df.Imax_F*df.Vmax_F
                    Pmax[np.isnan(Pmax)] = 0
                    df["Pmax_F"] = Pmax
                    df["T_Feinman"] = datos.TFeinman
                    df["AF"]=datos.AF

                    ### Sandia

                    # obetencion de Parametros con el modelo Sandia:

                    gamma = (datos.AS * K * (datos.Tsandia + 273.15)) / q
                    df["Gamma_S"] = gamma
                    Isc0 = Isc0c * (1 + (alpha * (datos.Tsandia - 25))) * (datos.Poa_global / 1000)
                    df["Isc0_S"] = Isc0

                    # Modificando las ecuaciones para usar 'datos.Tsandia' y agregando "_S" a los nombres de las columnas
                    Voc60 = Voc0 * (1 + (betha * (datos.Tsandia - 25))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                    Voc60[np.isinf(Voc60)] = 0
                    df["Voc_S"] = Voc60


                    Imax60 = Imax0 * (1 + alpha * (datos.Tsandia - 25)) * (datos.Poa_global / 1000)
                    df["Imax_S"] = Imax60

                    Vmax60 = Vmax0 * (1 + (deltha * (datos.Tsandia - 25))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                    Vmax60[np.isinf(Vmax60)] = 0
                    df["Vmax_S"] = Vmax60

                    #Pmax60 = ((Pmax0 * (1 + deltha * (datos.Tsandia - 25))) * (
                     #           1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                    Pmax60= df.Imax_S*df.Vmax_S
                    Pmax60[np.isnan(Pmax60)] = 0
                    df["Pmax_S"] = Pmax60
                    df["T_Sandia"] = datos.Tsandia
                    df["AS"] = datos.AS

                    irr[nombre_df] = df
    return irr

def PE_t_S(Placa_r,Ndh): #PLaca es una libreria que contiene valores
    irr={}
    x = -1

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=Placa_r["Vmax60"],
        i_mp=Placa_r["Imax"],
        v_oc=Placa_r["Voc"],
        i_sc=Placa_r["Isc"],
        alpha_sc=float(Placa_r["alpha"] / 100) * (Placa_r["Isc"]),
        beta_voc=float(Placa_r["beta"] / 100) * (Placa_r["Voc"]),
        gamma_pmp=float(Placa_r["deltha"]),
        cells_in_series=float(Placa_r["cells_in_series"]),
        temp_ref=float(Placa_r["temp_ref"])
    )

    for datos in Ndh:
        if 'TFeinman' in datos:
            temp = datos['TFeinman']
            rad = datos['Poa_global']
            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AF"] = nNsVth

        if 'Tsandia' in datos:
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AS"] = nNsVthS

        if 'Tsandia' in datos and 'TFeinman' in datos:
            temp = datos['TFeinman']
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["AS"] = nNsVthS


    for datos in Ndh:
                    x = x + 1

                    K =Placa_r["Boltzmann"]
                    q = Placa_r["Elementary_charge"]
                    Pmax0 = Placa_r["Pmax"]
                    Imax0 = Placa_r["Imax"]
                    Vmax0 = Placa_r["Vmax60"]
                    Voc0 = Placa_r["Voc"]
                    Isc0c = Placa_r["Isc"]  # Aquí se corrigió el nombre de la variable
                    deltha = Placa_r["deltha"] / 100
                    betha = Placa_r["beta"]/100  # Aquí se corrigió el nombre de la variable para mantener la consistencia
                    alpha = Placa_r["alpha"]/ 100  # Recuerda este valor es importante dividir entre 100


                    nombre_df = f"{len(datos)}_{pd.to_datetime(Ndh[x].index).year.unique()[0]}"
                    df = pd.DataFrame(datos.Poa_global)

                    # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                    df["Year"] = datos.Year
                    df["Month"] = datos.Month
                    ### Sandia, obetencion de Parametros con el modelo Sandia:

                    gamma = (datos.AS * K * (datos.Tsandia + 273.15)) / q
                    df["Gamma_S"] = gamma
                    Isc0 = Isc0c * (1 + (alpha * (datos.Tsandia - 25))) * (datos.Poa_global / 1000)
                    df["Isc0_S"] = Isc0

                    # Modificando las ecuaciones para usar 'datos.Tsandia' y agregando "_S" a los nombres de las columnas
                    Voc60 = Voc0 * (1 + (betha * (datos.Tsandia - 25))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                    Voc60[np.isinf(Voc60)] = 0

                    df["Voc_S"] = Voc60

                    Imax60 = Imax0 * (1 + alpha * (datos.Tsandia - 25)) * (datos.Poa_global / 1000)
                    df["Imax_S"] = Imax60

                    Vmax60 = Vmax0 * (1 + (deltha * (datos.Tsandia - 25))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                    Vmax60[np.isinf(Vmax60)] = 0
                    df["Vmax_S"] = Vmax60

                    #Pmax60 = ((Pmax0 * (1 + deltha * (datos.Tsandia - 25))) * (1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                    Pmax60 = df.Imax_S * df.Vmax_S
                    Pmax60[np.isnan(Pmax60)] = 0
                    df["Pmax_S"] = Pmax60
                    df["T_Sandia"] = datos.Tsandia

                    df["AS"]=datos.AS

                    irr[nombre_df] = df
    return irr

def PE_t_S1(Placa_r,Ndh): #PLaca es una libreria que contiene valores
    irr={}
    x = -1

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=Placa_r["Vmax60"],
        i_mp=Placa_r["Imax"],
        v_oc=Placa_r["Voc"],
        i_sc=Placa_r["Isc"],
        alpha_sc=float(Placa_r["alpha"] / 100) * (Placa_r["Isc"]),
        beta_voc=float(Placa_r["beta"] / 100) * (Placa_r["Voc"]),
        gamma_pmp=float(Placa_r["deltha"]),
        cells_in_series=float(Placa_r["cells_in_series"]),
        temp_ref=float(Placa_r["temp_ref"])
    )

    for datos in Ndh:
        if 'TFeinman' in datos:
            temp = datos['TFeinman']
            rad = datos['Poa_global']
            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AF"] = nNsVth

        if 'Tsandia' in datos:
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AS"] = nNsVthS

        if 'Tsandia' in datos and 'TFeinman' in datos:
            temp = datos['TFeinman']
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["AS"] = nNsVthS

    for datos in Ndh:
                    x = x + 1

                    K =Placa_r["Boltzmann"]
                    q = Placa_r["Elementary_charge"]
                    Pmax0 = Placa_r["Pmax"]
                    Imax0 = Placa_r["Imax"]
                    Vmax0 = Placa_r["Vmax60"]
                    Voc0 = Placa_r["Voc"]
                    Isc0c = Placa_r["Isc"]  # Aquí se corrigió el nombre de la variable
                    deltha = Placa_r["deltha"] / 100
                    betha = Placa_r["beta"]/100  # Aquí se corrigió el nombre de la variable para mantener la consistencia
                    alpha = Placa_r["alpha"]/ 100  # Recuerda este valor es importante dividir entre 100


                    nombre_df = f"{len(datos)}_{pd.to_datetime(Ndh[x].index).year.unique()[0]}"
                    df = pd.DataFrame(datos.Poa_global)

                    # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                    df["Year"] = datos.Year
                    df["Month"] = datos.Month
                    ### Sandia, obetencion de Parametros con el modelo Sandia:

                    gamma = (datos.AS * K * (datos.Tsandia + 273.15)) / q
                    df["Gamma_S"] = gamma
                    Isc0 = Isc0c * (1 + (alpha * (datos.Tsandia - 25))) * (datos.Poa_global / 1000)
                    df["Isc0_S"] = Isc0

                    # Modificando las ecuaciones para usar 'datos.Tsandia' y agregando "_S" a los nombres de las columnas
                    Voc60 = Voc0 * (1 + (betha * (datos.Tsandia - 25))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                    Voc60[np.isinf(Voc60)] = 0

                    df["Voc_S"] = Voc60

                    Imax60 = Imax0 * (1 + alpha * (datos.Tsandia - 25)) * (datos.Poa_global / 1000)
                    df["Imax_S"] = Imax60

                    Vmax60 = Vmax0 * (1 + (deltha * (datos.Tsandia - 25))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                    Vmax60[np.isinf(Vmax60)] = 0
                    df["Vmax_S"] = Vmax60

                    #Pmax60 = ((Pmax0 * (1 + deltha * (datos.Tsandia - 25))) * (1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)

                    Pmax60 = df.Imax_S * df.Vmax_S

                    Pmax60[np.isnan(Pmax60)] = 0
                    df["Pmax_S"] = Pmax60
                    df["T_Sandia"] = datos.Tsandia
                    df["AS"]= datos.AS
                    irr[nombre_df] = df
    return irr

def PE_1(Placa_r,Ndh): #PLaca es una libreria que contiene valores
    irr={}
    x= -1

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=Placa_r["Vmax60"],
        i_mp=Placa_r["Imax"],
        v_oc=Placa_r["Voc"],
        i_sc=Placa_r["Isc"],
        alpha_sc=float(Placa_r["alpha"] / 100) * (Placa_r["Isc"]),
        beta_voc=float(Placa_r["beta"] / 100) * (Placa_r["Voc"]),
        gamma_pmp=float(Placa_r["deltha"]),
        cells_in_series=float(Placa_r["cells_in_series"]),
        temp_ref=float(Placa_r["temp_ref"])
    )

    for datos in Ndh:
        if 'TFeinman' in datos:
            temp = datos['TFeinman']
            rad = datos['Poa_global']
            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AF"] = nNsVth

        if 'Tsandia' in datos:
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AS"] = nNsVthS

        if 'Tsandia' in datos and 'TFeinman' in datos:
            temp = datos['TFeinman']
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["AS"] = nNsVthS

    for datos in Ndh:
                    x = x + 1

                    K =Placa_r["Boltzmann"]
                    q = Placa_r["Elementary_charge"]
                    Pmax0 = Placa_r["Pmax"]
                    Imax0 = Placa_r["Imax"]
                    Vmax0 = Placa_r["Vmax60"]
                    Voc0 = Placa_r["Voc"]
                    Isc0c = Placa_r["Isc"]  # Aquí se corrigió el nombre de la variable
                    deltha = Placa_r["deltha"] / 100
                    betha = Placa_r["beta"] / 100  # Aquí se corrigió el nombre de la variable para mantener la consistencia
                    alpha = Placa_r["alpha"] / 100  # Recuerda este valor es importante dividir entre 100


                    nombre_df = f"{len(datos)}_{pd.to_datetime(Ndh[x].index).year.unique()[0]}"
                    df = pd.DataFrame(datos.Poa_global)

                    # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                    df["Year"] = datos.Year
                    df["Month"] = datos.Month
                    gamma = (datos.AF * K * (datos.TFeinman + 273.15)) / q
                    df["Gamma_F"] = gamma
                    Isc0 = Isc0c * (1 + (alpha * (datos.TFeinman - 25))) * ((datos.Poa_global) / 1000)
                    df["Isc0_F"] = Isc0
                    Voc60 = Voc0 * (1 + (betha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                    Voc60[np.isinf(Voc60)] = 0
                    df["Voc_F"] = Voc60

                    Imax60 = Imax0 * (1 + alpha * (datos.TFeinman - 25)) * (datos.Poa_global / 1000)
                    df["Imax_F"] = Imax60

                    Vmax60 = Vmax0 * (1 + (deltha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                    Vmax60[np.isinf(Vmax60)] = 0
                    df["Vmax_F"] = Vmax60

                    #Pmax = ((Pmax0 * (1 + deltha * (datos.TFeinman - 25))) * (
                     #           1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                    Pmax= df.Imax_F* df.Vmax_F
                    Pmax[np.isnan(Pmax)] = 0
                    df["Pmax_F"] = Pmax
                    df["T_Feinman"] = datos.TFeinman
                    df["AF"]=datos.AF



                    irr[nombre_df] = df
    return irr

def PE_t1(Placa_r,Ndh): #PLaca es una libreria que contiene valores
    irr={}
    x = -1
    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=Placa_r["Vmax60"],
        i_mp=Placa_r["Imax"],
        v_oc=Placa_r["Voc"],
        i_sc=Placa_r["Isc"],
        alpha_sc=float(Placa_r["alpha"] / 100) * (Placa_r["Isc"]),
        beta_voc=float(Placa_r["beta"] / 100) * (Placa_r["Voc"]),
        gamma_pmp=float(Placa_r["deltha"]),
        cells_in_series=float(Placa_r["cells_in_series"]),
        temp_ref=float(Placa_r["temp_ref"])
    )

    for datos in Ndh:
        if 'TFeinman' in datos:
            temp = datos['TFeinman']
            rad = datos['Poa_global']
            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AF"] = nNsVth

        if 'Tsandia' in datos:
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )
            datos["AS"] = nNsVthS

        if 'Tsandia' in datos and 'TFeinman' in datos:
            temp = datos['TFeinman']
            temps = datos['Tsandia']
            rad = datos['Poa_global']
            ILS, I0S, RsS, RshS, nNsVthS = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temps,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=rad,
                temp_cell=temp,
                alpha_sc=Placa_r["alpha"],
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            datos["AF"] = nNsVth
            datos["AS"] = nNsVthS

    for datos in Ndh:
                    x = x + 1

                    K =Placa_r["Boltzmann"]
                    q = Placa_r["Elementary_charge"]
                    Pmax0 = Placa_r["Pmax"]
                    Imax0 = Placa_r["Imax"]
                    Vmax0 = Placa_r["Vmax60"]
                    Voc0 = Placa_r["Voc"]
                    Isc0c = Placa_r["Isc"]  # Aquí se corrigió el nombre de la variable
                    deltha = Placa_r["deltha"] / 100
                    betha = Placa_r["beta"]/100  # Aquí se corrigió el nombre de la variable para mantener la consistencia
                    alpha = Placa_r["alpha"]/ 100  # Recuerda este valor es importante dividir entre 100


                    nombre_df = f"{len(datos)}_{pd.to_datetime(Ndh[x].index).year.unique()[0]}"
                    df = pd.DataFrame(datos.Poa_global)

                    # parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                    df["Year"] = datos.Year
                    df["Month"] = datos.Month
                    gamma = (datos.AF * K * (datos.TFeinman + 273.15)) / q
                    df["Gamma_F"] = gamma
                    Isc0 = Isc0c * (1 + (alpha * (datos.TFeinman - 25))) * ((datos.Poa_global) / 1000)
                    df["Isc0_F"] = Isc0
                    Voc60 = Voc0 * (1 + (betha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                    Voc60[np.isinf(Voc60)] = 0
                    df["Voc_F"] = Voc60

                    Imax60 = Imax0 * (1 + alpha * (datos.TFeinman - 25)) * (datos.Poa_global / 1000)
                    df["Imax_F"] = Imax60

                    Vmax60 = Vmax0 * (1 + (deltha * (datos.TFeinman - 25))) * (
                                1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))
                    Vmax60[np.isinf(Vmax60)] = 0
                    df["Vmax_F"] = Vmax60

                    #Pmax = ((Pmax0 * (1 + deltha * (datos.TFeinman - 25))) * (
                     #           1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                    Pmax = df.Imax_F* df.Vmax_F
                    Pmax[np.isnan(Pmax)] = 0
                    df["Pmax_F"] = Pmax
                    df["T_Feinman"] = datos.TFeinman
                    df["AF"]=datos.AF

                    ### Sandia

                    # obetencion de Parametros con el modelo Sandia:

                    gamma = (datos.AS * K * (datos.Tsandia + 273.15)) / q
                    df["Gamma_S"] = gamma
                    Isc0 = Isc0c * (1 + (alpha * (datos.Tsandia - 25))) * (datos.Poa_global / 1000)
                    df["Isc0_S"] = Isc0

                    # Modificando las ecuaciones para usar 'datos.Tsandia' y agregando "_S" a los nombres de las columnas
                    Voc60 = Voc0 * (1 + (betha * (datos.Tsandia - 25))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                    Voc60[np.isinf(Voc60)] = 0
                    df["Voc_S"] = Voc60
                    'Tsandia'

                    Imax60 = Imax0 * (1 + alpha * (datos.Tsandia - 25)) * (datos.Poa_global / 1000)
                    df["Imax_S"] = Imax60

                    Vmax60 = Vmax0 * (1 + (deltha * (datos.Tsandia - 25))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                    Vmax60[np.isinf(Vmax60)] = 0
                    df["Vmax_S"] = Vmax60

                    #Pmax60 = ((Pmax0 * (1 + deltha * (datos.Tsandia - 25))) * (
                               # 1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)
                    Pmax60 = df.Imax_S* df.Vmax_S

                    Pmax60[np.isnan(Pmax60)] = 0
                    df["Pmax_S"] = Pmax60
                    df["T_Sandia"] = datos.Tsandia
                    df["AS"]=datos.AS



                    irr[nombre_df] = df
    return irr

## Parametros electricos tablas:
def table_PE1(d, nombre):

    nombre
    global tablespe
    dataframes = []

    for tiempo, datos in d.items():
            for t in [8760, 17520, 35040, 105120]:
                if t == len(datos):
                    columns = [{'name': i, 'id': i} for i in datos.columns]
                    data = datos.to_dict('records')

                    dataframes.append((nombre,data, columns))

    tablespe = [
        html.Div([
            html.H3(f"Parametros Electricos del Modulo 1"),
            html.Div(
                dash_table.DataTable(
                    id=f"Modulo-{i + 1}",
                    data=data,
                    columns=columns,
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
                ),
                style={'width': '100%', 'overflowX': 'auto'}
            )
        ], style={'width': '100%'}) for i, ( nombre ,data, columns) in enumerate(dataframes)
    ]

    return tablespe

def table_PE2(d, nombre):
    nombre
    global tablespe
    dataframes = []

    for tiempo, datos in d.items():
        for t in [8760, 17520, 35040, 105120]:
            if t == len(datos):
                columns = [{'name': i, 'id': i} for i in datos.columns]
                data = datos.to_dict('records')
                dataframes.append((data, columns))

    tablespe = [
        html.Div([
            html.H3(f"Parametros Electricos del Modulo 2"),
            html.Div(
                dash_table.DataTable(
                    id=f"Modulo-{i + 1}",
                    data=data,
                    columns=columns,
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
                ),
                style={'width': '100%', 'overflowX': 'auto'}
            )
        ], style={'width': '100%'}) for i, (data, columns) in enumerate(dataframes)
    ]

    return tablespe

def Year_tabla():

    tabla=dcc.Dropdown(
        id='Year-Time',
        options=["No se ha seleccionado ningun año"],
        value='',
        multi=True,
        style={
            'margin-bottom': '10px',
            'margin-right': '10px',
            'width': '100%',
            'color': '#000000',
            'font-size': 15
        }
    )

    return tabla

def column_Pe():

    tabla =  (html.Div(
            [   html.H4("Componentes del Grafico"),
                dbc.Label("Año"),
                dcc.Dropdown(
                    id='Year-Time',
                    options=[],
                    value=[],
                    multi=True,
                    style={
                        'margin-bottom': '10px',
                        'margin-right': '10px',
                        'width': '100%',
                        'color': '#000000',
                        'font-size': 15
                    }
                ),
            ]
        ),
            html.Div(
            [
                dbc.Label("Parametros Electricos"),
                dcc.Dropdown(
                    id='Column_Pe',
                    options=[],
                    value=[],
                    multi=True,
                    style={
                        'margin-bottom': '10px',
                        'margin-right': '10px',
                        'width': '100%',
                        'color': '#000000',
                        'font-size': 15
                    }
                ),
            ]
        ))



    return tabla


def column_Pe_CEC(l):



    if len(l) == 2 :

        tabla =  (

            html.Div(
                [   html.H4("Componentes del Grafico"),
                    dbc.Label("Año"),
                    dcc.Dropdown(
                        id='Year-Time',
                        options=[],
                        value=[],
                        multi=True,
                        style={
                            'margin-bottom': '10px',
                            'margin-right': '10px',
                            'width': '100%',
                            'color': '#000000',
                            'font-size': 15
                        }
                    ),
                ]
            ),
                html.Div(
                [
                    dbc.Label("Parametros Electricos"),
                    dcc.Dropdown(
                        id='Column_Pe',
                        options=[],
                        value=[],
                        multi=True,
                        style={
                            'margin-bottom': '10px',
                            'margin-right': '10px',
                            'width': '100%',
                            'color': '#000000',
                            'font-size': 15
                             }
                    ),
                ]
            )
        )

    if len(l) == 1:

        tabla = (

            html.Div(
            [html.H4("Componentes del Grafico"),
             dbc.Label("Año"),
             dcc.Dropdown(
                 id='Year-Time',
                 options=[],
                 value=[],
                 multi=True,
                 style={
                     'margin-bottom': '10px',
                     'margin-right': '10px',
                     'width': '100%',
                     'color': '#000000',
                     'font-size': 15
                 }
             ),
             ])
            ,
                 html.Div(
                     [
                         dbc.Label("Parametros Electricos"),
                         dcc.Dropdown(
                             id='Column_Pe',
                             options=[],
                             value=[],
                             multi=True,
                             style={
                                 'margin-bottom': '10px',
                                 'margin-right': '10px',
                                 'width': '100%',
                                 'color': '#000000',
                                 'font-size': 15

                             }
                         ),
                     ]
                 ))


    return tabla

def M_IV():

    l=(
        html.Div(
            [html.H4("Componentes del Grafico"),
             dbc.Label("Metodo"),
             dcc.Dropdown(
                 id='IV-Method',
                 options=[

                     {'label': 'Prueba Estandar', 'value': 'PE'},

                     {'label': 'Valores Especificos', 'value': 'VE'},

                     {'label': 'Comparacion de IV', 'value': 'CI'}
                 ],
                 value=[],
                 style={
                     'margin-bottom': '10px',
                     'margin-right': '10px',
                     'width': '100%',
                     'color': '#000000',
                     'font-size': 15
                 }
             )
                ,
             ])
        ,

        (
            html.Div(
                [
                    dbc.Label("Año"),
                    dcc.Dropdown(
                        id='Year-Time-IV',
                        options=[],
                        value=[],
                        multi=False,
                        style={
                            'margin-bottom': '10px',
                            'margin-right': '10px',
                            'width': '100%',
                            'color': '#000000',
                            'font-size': 15
                        }
                    ),
                ])
        )

        )


    return l





                                                                        ##################### Agregar NOCT ###############################

### Aqui se hace la ultima tabla donde se resumen toda la informacion ###
### Con esta tabla se podra comparar los resultados de la curva IV ###
### Las opciones que se deben de dar, es hacerlo respecto al clima que seleccionaste buscando las condiciones caracteristicas de ese clima###
### Hacerlo con condiciones estandares, las que se usan en la tabla de franhoffer###
### Con un Excel o tu introduciendo valores###
### Lo del excel es mas que nada para  comparar resultados con mediciones ###

def resume_df(Seleccion, lt):
    lista = []
    lista1 = []

    if Seleccion == [1]:
        #### Aquí es donde se hace la tabla final
        ## Estas son fechas
        Potmax_id_F = lt["Pmax_F"].idxmax()  #
        Potmin_id_F = lt["Pmax_F"].idxmin()  #
        Imax_id_F = lt["Imax_F"].idxmax()  #
        Imin_id_F = lt["Imax_F"].idxmin()  #
        Vmax_id_F = lt["Vmax_F"].idxmax()  #
        Vmin_id_F = lt["Vmax_F"].idxmin()  #
        ### Circuito abierto fechas ###
        Iscmax_id_F = lt["Isc0_F"].idxmax()
        Iscmin_id_F = lt["Isc0_F"].idxmin()
        Vocmax_id_F = lt["Voc_F"].idxmax()
        Vocmin_id_F = lt["Voc_F"].idxmin()
        ### Valores en funcionamiento ###
        PotmaxF = lt["Pmax_F"].loc[Potmax_id_F]
        PotminF = lt["Pmax_F"].loc[Potmin_id_F]
        ImaxF = lt["Imax_F"].loc[Imax_id_F]
        IminF = lt["Imax_F"].loc[Imin_id_F]
        VmaxF = lt["Vmax_F"].loc[Vmax_id_F]
        VminF = lt["Vmax_F"].loc[Vmin_id_F]
        #### Valores en circuito ####
        IscMaxF = lt["Isc0_F"].loc[Iscmax_id_F]
        IscMinF = lt["Isc0_F"].loc[Iscmin_id_F]
        VocMaxF = lt["Vmax_F"].loc[Vocmax_id_F]
        VocMinF = lt["Vmax_F"].loc[Vocmin_id_F]
        #### Temperarutas ###
        TpmaxF = lt["T_Feinman"].loc[Potmax_id_F]
        TpminF = lt["T_Feinman"].loc[Potmin_id_F]
        TImaxF = lt["T_Feinman"].loc[Imax_id_F]
        TIminF = lt["T_Feinman"].loc[Imin_id_F]
        TVmaxF = lt["T_Feinman"].loc[Vmax_id_F]
        TVminF = lt["T_Feinman"].loc[Vmin_id_F]
        #### Valores en circuito ####
        TIscMaxF = lt["T_Feinman"].loc[Iscmax_id_F]
        TIscMinF = lt["T_Feinman"].loc[Iscmin_id_F]
        TVocMaxF = lt["T_Feinman"].loc[Vocmax_id_F]
        TVocMinF = lt["T_Feinman"].loc[Vocmin_id_F]
        #### Irradancia_Efectiva ####
        PoamaxF = lt["Poa_global"].loc[Potmax_id_F]
        PoaminF = lt["Poa_global"].loc[Potmin_id_F]
        PoaImaxF = lt["Poa_global"].loc[Imax_id_F]
        PoaIminF = lt["Poa_global"].loc[Imin_id_F]
        PoaVmaxF = lt["Poa_global"].loc[Vmax_id_F]
        PoaVminF = lt["Poa_global"].loc[Vmin_id_F]
        #### Irradiancia_Efectiva Valores en circuito ####
        PoaIscMaxF = lt["Poa_global"].loc[Iscmax_id_F]
        PoaIscMinF = lt["Poa_global"].loc[Iscmin_id_F]
        PoaVocMaxF = lt["Poa_global"].loc[Vocmax_id_F]
        PoaVocMinF = lt["Poa_global"].loc[Vocmin_id_F]
        ### Diccionario ###

        d = {
            'Valores': [PotmaxF, PotminF, ImaxF, IminF, VmaxF, VminF, IscMaxF, IscMinF, VocMaxF, VocMinF],

            "Valores_operacionales": [
                f"I={lt.Imax_F.loc[Potmax_id_F]:.2f},V={lt.Vmax_F.loc[Potmax_id_F]:.2f}",  # PotmaxF
                f"I={lt.Imax_F.loc[Potmin_id_F]:.2f},V={lt.Vmax_F.loc[Potmin_id_F]:.2f}",  # PotminF
                f"V={lt.Vmax_F.loc[Imax_id_F]:.2f},P={lt.Pmax_F.loc[Imax_id_F]:.2f}",  # ImaxF
                f"V={lt.Vmax_F.loc[Imin_id_F]:.2f},P={lt.Pmax_F.loc[Imin_id_F]:.2f}",  # IminF
                f"I={lt.Imax_F.loc[Vmax_id_F]:.2f},P={lt.Pmax_F.loc[Vmax_id_F]:.2f}",  # VmaxF
                f"I={lt.Imax_F.loc[Vmin_id_F]:.2f},P={lt.Pmax_F.loc[Vmin_id_F]:.2f}",  # VminF
                f"Voc={lt.Voc_F.loc[Iscmax_id_F]:.2f}",  # IscMaxF
                f"Voc={lt.Voc_F.loc[Iscmin_id_F]:.2f}",  # IscMinF
                f"Isc={lt.Isc0_F.loc[Vocmax_id_F]:.2f}",  # VocMaxF
                f"Isc={lt.Isc0_F.loc[Vocmin_id_F]:.2f}"  # VocMinF
            ]
            ,
            'Temperaturas Feinman [C°]': [TpmaxF, TpminF, TImaxF, TIminF, TVmaxF, TVminF, TIscMaxF, TIscMinF, TVocMaxF,
                                          TVocMinF],
            'Irradiancia_Efectiva': [PoamaxF, PoaminF, PoaImaxF, PoaIminF, PoaVmaxF, PoaVminF, PoaIscMaxF, PoaIscMinF,
                                     PoaVocMaxF, PoaVocMinF],
            'Fechas': [Potmax_id_F, Potmin_id_F, Imax_id_F, Imin_id_F, Vmax_id_F, Vmin_id_F, Iscmax_id_F, Iscmin_id_F,
                       Vocmax_id_F, Vocmin_id_F]
        }

        df = pd.DataFrame(data=d,
                          index=["Potencia _maxima F", "Potencia_minima F", "Corriente Maxima F", "Corriente Minima F",
                                 "Voltaje Maximo F", "Voltaje Minimo F", "Corriente maxima de Corto Circuito F",
                                 "Corriente minima de Corto Circuito F", "Voltaje maximo de Corto Circuito F",
                                 "Voltaje minimo de Corto Circuito F"])

        m = df.reset_index().round(2)
        m.columns = ["Parametros Electricos", 'Valores', "Valor_Operacional", 'Temperaturas[C°]',
                     'Irradiancia_Efectiva', 'Fechas']

        return m

    if Seleccion == [2]:
        #### Aquí es donde se hace la tabla final para Sandia
        Potmax_id_S = lt["Pmax_S"].idxmax()
        Potmin_id_S = lt["Pmax_S"].idxmin()
        Imax_id_S = lt["Imax_S"].idxmax()
        Imin_id_S = lt["Imax_S"].idxmin()
        Vmax_id_S = lt["Vmax_S"].idxmax()
        Vmin_id_S = lt["Vmax_S"].idxmin()
        ### Circuito abierto fechas ###
        Iscmax_id_S = lt["Isc0_S"].idxmax()
        Iscmin_id_S = lt["Isc0_S"].idxmin()
        Vocmax_id_S = lt["Voc_S"].idxmax()
        Vocmin_id_S = lt["Voc_S"].idxmin()
        ### Valores en funcionamiento ###
        PotmaxS = lt["Pmax_S"].loc[Potmax_id_S]
        PotminS = lt["Pmax_S"].loc[Potmin_id_S]
        ImaxS = lt["Imax_S"].loc[Imax_id_S]
        IminS = lt["Imax_S"].loc[Imin_id_S]
        VmaxS = lt["Vmax_S"].loc[Vmax_id_S]
        VminS = lt["Vmax_S"].loc[Vmin_id_S]
        #### Valores en circuito ####
        IscMaxS = lt["Isc0_S"].loc[Iscmax_id_S]
        IscMinS = lt["Isc0_S"].loc[Iscmin_id_S]
        VocMaxS = lt["Voc_S"].loc[Vocmax_id_S]
        VocMinS = lt["Voc_S"].loc[Vocmin_id_S]
        #### Temperaturas ###
        TpmaxS = lt["T_Sandia"].loc[Potmax_id_S]
        TpminS = lt["T_Sandia"].loc[Potmin_id_S]
        TImaxS = lt["T_Sandia"].loc[Imax_id_S]
        TIminS = lt["T_Sandia"].loc[Imin_id_S]
        TVmaxS = lt["T_Sandia"].loc[Vmax_id_S]
        TVminS = lt["T_Sandia"].loc[Vmin_id_S]
        #### Valores en circuito ####
        TIscMaxS = lt["T_Sandia"].loc[Iscmax_id_S]
        TIscMinS = lt["T_Sandia"].loc[Iscmin_id_S]
        TVocMaxS = lt["T_Sandia"].loc[Vocmax_id_S]
        TVocMinS = lt["T_Sandia"].loc[Vocmin_id_S]
        #### Irradiancia_Efectiva ####
        PoamaxS = lt["Poa_global"].loc[Potmax_id_S]
        PoaminS = lt["Poa_global"].loc[Potmin_id_S]
        PoaImaxS = lt["Poa_global"].loc[Imax_id_S]
        PoaIminS = lt["Poa_global"].loc[Imin_id_S]
        PoaVmaxS = lt["Poa_global"].loc[Vmax_id_S]
        PoaVminS = lt["Poa_global"].loc[Vmin_id_S]
        #### Irradiancia_Efectiva Valores en circuito ####
        PoaIscMaxS = lt["Poa_global"].loc[Iscmax_id_S]
        PoaIscMinS = lt["Poa_global"].loc[Iscmin_id_S]
        PoaVocMaxS = lt["Poa_global"].loc[Vocmax_id_S]
        PoaVocMinS = lt["Poa_global"].loc[Vocmin_id_S]
        ### Diccionario ###

        d = {
            'Valores': [PotmaxS, PotminS, ImaxS, IminS, VmaxS, VminS, IscMaxS, IscMinS, VocMaxS, VocMinS],
            "Valores_operacionales": [
                f"I={lt.Imax_S.loc[Potmax_id_S]:.2f},V={lt.Vmax_S.loc[Potmax_id_S]:.2f}",  # PotmaxS
                f"I={lt.Imax_S.loc[Potmin_id_S]:.2f},V={lt.Vmax_S.loc[Potmin_id_S]:.2f}",  # PotminS
                f"V={lt.Vmax_S.loc[Imax_id_S]:.2f},P={lt.Pmax_S.loc[Imax_id_S]:.2f}",  # ImaxS
                f"V={lt.Vmax_S.loc[Imin_id_S]:.2f},P={lt.Pmax_S.loc[Imin_id_S]:.2f}",  # IminS
                f"I={lt.Imax_S.loc[Vmax_id_S]:.2f},P={lt.Pmax_S.loc[Vmax_id_S]:.2f}",  # VmaxS
                f"I={lt.Imax_S.loc[Vmin_id_S]:.2f},P={lt.Pmax_S.loc[Vmin_id_S]:.2f}",  # VminS
                f"Voc={lt.Voc_S.loc[Iscmax_id_S]:.2f}",  # IscMaxS
                f"Voc={lt.Voc_S.loc[Iscmin_id_S]:.2f}",  # IscMinS
                f"Isc={lt.Isc0_S.loc[Vocmax_id_S]:.2f}",  # VocMaxS
                f"Isc={lt.Isc0_S.loc[Vocmin_id_S]:.2f}"  # VocMinS
            ]
            ,

            'Temperaturas Sandia [C°]': [TpmaxS, TpminS, TImaxS, TIminS, TVmaxS, TVminS, TIscMaxS, TIscMinS, TVocMaxS,
                                         TVocMinS],
            'Irradiancia_Efectiva': [PoamaxS, PoaminS, PoaImaxS, PoaIminS, PoaVmaxS, PoaVminS, PoaIscMaxS, PoaIscMinS,
                                     PoaVocMaxS, PoaVocMinS],
            'Fechas': [Potmax_id_S, Potmin_id_S, Imax_id_S, Imin_id_S, Vmax_id_S, Vmin_id_S, Iscmax_id_S, Iscmin_id_S,
                       Vocmax_id_S, Vocmin_id_S]
        }

        df = pd.DataFrame(data=round(d,2),
                          index=["Potencia _maximaS", "Potencia_minima S", "Corriente Maxima S", "Corriente Minima S",
                                 "Voltaje Maximo S", "Voltaje Minimo S", "Corriente maxima de Corto Circuito S",
                                 "Corriente minima de Corto Circuito S", "Voltaje maximo de Corto Circuito S",
                                 "Voltaje minimo de Corto Circuito S"])

        m = df.reset_index()
        m.columns = ["Parametros Electricos", 'Valores', "Valores_operacionales", 'Temperaturas[C°]',
                     'Irradiancia_Efectiva', 'Fechas']

        return m

    if Seleccion == [1, 2]:
        #### Aquí es donde se hace la tabla final combinando Feinman y Sandia
        #### Feinman
        Potmax_id_F = lt["Pmax_F"].idxmax()
        Potmin_id_F = lt["Pmax_F"].idxmin()
        Imax_id_F = lt["Imax_F"].idxmax()
        Imin_id_F = lt["Imax_F"].idxmin()
        Vmax_id_F = lt["Vmax_F"].idxmax()
        Vmin_id_F = lt["Vmax_F"].idxmin()
        Iscmax_id_F = lt["Isc0_F"].idxmax()
        Iscmin_id_F = lt["Isc0_F"].idxmin()
        Vocmax_id_F = lt["Voc_F"].idxmax()
        Vocmin_id_F = lt["Voc_F"].idxmin()

        PotmaxF = lt["Pmax_F"].loc[Potmax_id_F]
        PotminF = lt["Pmax_F"].loc[Potmin_id_F]
        ImaxF = lt["Imax_F"].loc[Imax_id_F]
        IminF = lt["Imax_F"].loc[Imin_id_F]
        VmaxF = lt["Vmax_F"].loc[Vmax_id_F]
        VminF = lt["Vmax_F"].loc[Vmin_id_F]
        IscMaxF = lt["Isc0_F"].loc[Iscmax_id_F]
        IscMinF = lt["Isc0_F"].loc[Iscmin_id_F]
        VocMaxF = lt["Vmax_F"].loc[Vocmax_id_F]
        VocMinF = lt["Vmax_F"].loc[Vocmin_id_F]

        TpmaxF = lt["T_Feinman"].loc[Potmax_id_F]
        TpminF = lt["T_Feinman"].loc[Potmin_id_F]
        TImaxF = lt["T_Feinman"].loc[Imax_id_F]
        TIminF = lt["T_Feinman"].loc[Imin_id_F]
        TVmaxF = lt["T_Feinman"].loc[Vmax_id_F]
        TVminF = lt["T_Feinman"].loc[Vmin_id_F]
        TIscMaxF = lt["T_Feinman"].loc[Iscmax_id_F]
        TIscMinF = lt["T_Feinman"].loc[Iscmin_id_F]
        TVocMaxF = lt["T_Feinman"].loc[Vocmax_id_F]
        TVocMinF = lt["T_Feinman"].loc[Vocmin_id_F]

        PoamaxF = lt["Poa_global"].loc[Potmax_id_F]
        PoaminF = lt["Poa_global"].loc[Potmin_id_F]
        PoaImaxF = lt["Poa_global"].loc[Imax_id_F]
        PoaIminF = lt["Poa_global"].loc[Imin_id_F]
        PoaVmaxF = lt["Poa_global"].loc[Vmax_id_F]
        PoaVminF = lt["Poa_global"].loc[Vmin_id_F]
        PoaIscMaxF = lt["Poa_global"].loc[Iscmax_id_F]
        PoaIscMinF = lt["Poa_global"].loc[Iscmin_id_F]
        PoaVocMaxF = lt["Poa_global"].loc[Vocmax_id_F]
        PoaVocMinF = lt["Poa_global"].loc[Vocmin_id_F]

        #### Sandia
        Potmax_id_S = lt["Pmax_S"].idxmax()
        Potmin_id_S = lt["Pmax_S"].idxmin()
        Imax_id_S = lt["Imax_S"].idxmax()
        Imin_id_S = lt["Imax_S"].idxmin()
        Vmax_id_S = lt["Vmax_S"].idxmax()
        Vmin_id_S = lt["Vmax_S"].idxmin()
        Iscmax_id_S = lt["Isc0_S"].idxmax()
        Iscmin_id_S = lt["Isc0_S"].idxmin()
        Vocmax_id_S = lt["Voc_S"].idxmax()
        Vocmin_id_S = lt["Voc_S"].idxmin()

        PotmaxS = lt["Pmax_S"].loc[Potmax_id_S]
        PotminS = lt["Pmax_S"].loc[Potmin_id_S]
        ImaxS = lt["Imax_S"].loc[Imax_id_S]
        IminS = lt["Imax_S"].loc[Imin_id_S]
        VmaxS = lt["Vmax_S"].loc[Vmax_id_S]
        VminS = lt["Vmax_S"].loc[Vmin_id_S]
        IscMaxS = lt["Isc0_S"].loc[Iscmax_id_S]
        IscMinS = lt["Isc0_S"].loc[Iscmin_id_S]
        VocMaxS = lt["Voc_S"].loc[Vocmax_id_S]
        VocMinS = lt["Voc_S"].loc[Vocmin_id_S]

        TpmaxS = lt["T_Sandia"].loc[Potmax_id_S]
        TpminS = lt["T_Sandia"].loc[Potmin_id_S]
        TImaxS = lt["T_Sandia"].loc[Imax_id_S]
        TIminS = lt["T_Sandia"].loc[Imin_id_S]
        TVmaxS = lt["T_Sandia"].loc[Vmax_id_S]
        TVminS = lt["T_Sandia"].loc[Vmin_id_S]
        TIscMaxS = lt["T_Sandia"].loc[Iscmax_id_S]
        TIscMinS = lt["T_Sandia"].loc[Iscmin_id_S]
        TVocMaxS = lt["T_Sandia"].loc[Vocmax_id_S]
        TVocMinS = lt["T_Sandia"].loc[Vocmin_id_S]

        PoamaxS = lt["Poa_global"].loc[Potmax_id_S]
        PoaminS = lt["Poa_global"].loc[Potmin_id_S]
        PoaImaxS = lt["Poa_global"].loc[Imax_id_S]
        PoaIminS = lt["Poa_global"].loc[Imin_id_S]
        PoaVmaxS = lt["Poa_global"].loc[Vmax_id_S]
        PoaVminS = lt["Poa_global"].loc[Vmin_id_S]
        PoaIscMaxS = lt["Poa_global"].loc[Iscmax_id_S]
        PoaIscMinS = lt["Poa_global"].loc[Iscmin_id_S]
        PoaVocMaxS = lt["Poa_global"].loc[Vocmax_id_S]
        PoaVocMinS = lt["Poa_global"].loc[Vocmin_id_S]

        ### Diccionario ###

        d = {
            'Valores': [PotmaxF, PotminF, ImaxF, IminF, VmaxF, VminF, IscMaxF, IscMinF, VocMaxF, VocMinF],

            "Valores_operacionales": [
                f"I={lt.Imax_F.loc[Potmax_id_F]:.2f},V={lt.Vmax_F.loc[Potmax_id_F]:.2f}",  # PotmaxF
                f"I={lt.Imax_F.loc[Potmin_id_F]:.2f},V={lt.Vmax_F.loc[Potmin_id_F]:.2f}",  # PotminF
                f"V={lt.Vmax_F.loc[Imax_id_F]:.2f},P={lt.Pmax_F.loc[Imax_id_F]:.2f}",  # ImaxF
                f"V={lt.Vmax_F.loc[Imin_id_F]:.2f},P={lt.Pmax_F.loc[Imin_id_F]:.2f}",  # IminF
                f"I={lt.Imax_F.loc[Vmax_id_F]:.2f},P={lt.Pmax_F.loc[Vmax_id_F]:.2f}",  # VmaxF
                f"I={lt.Imax_F.loc[Vmin_id_F]:.2f},P={lt.Pmax_F.loc[Vmin_id_F]:.2f}",  # VminF
                f"Voc={lt.Voc_F.loc[Iscmax_id_F]:.2f}",  # IscMaxF
                f"Voc={lt.Voc_F.loc[Iscmin_id_F]:.2f}",  # IscMinF
                f"Isc={lt.Isc0_F.loc[Vocmax_id_F]:.2f}",  # VocMaxF
                f"Isc={lt.Isc0_F.loc[Vocmin_id_F]:.2f}"  # VocMinF
            ]
            ,

            'Temperaturas[C°]': [TpmaxF, TpminF, TImaxF, TIminF, TVmaxF, TVminF, TIscMaxF, TIscMinF, TVocMaxF,
                                 TVocMinF],
            'Irradiancia_Efectiva': [PoamaxF, PoaminF, PoaImaxF, PoaIminF, PoaVmaxF, PoaVminF, PoaIscMaxF, PoaIscMinF,
                                     PoaVocMaxF, PoaVocMinF],
            'Fechas': [Potmax_id_F, Potmin_id_F, Imax_id_F, Imin_id_F, Vmax_id_F, Vmin_id_F, Iscmax_id_F, Iscmin_id_F,
                       Vocmax_id_F, Vocmin_id_F]
        }

        d1 = {
            'Valores': [PotmaxS, PotminS, ImaxS, IminS, VmaxS, VminS, IscMaxS, IscMinS, VocMaxS, VocMinS],
            "Valores_operacionales": [

                f"I={lt.Imax_S.loc[Potmax_id_S]:.2f},V={lt.Vmax_S.loc[Potmax_id_S]:.2f}",  # PotmaxS
                f"I={lt.Imax_S.loc[Potmin_id_S]:.2f},V={lt.Vmax_S.loc[Potmin_id_S]:.2f}",  # PotminS
                f"V={lt.Vmax_S.loc[Imax_id_S]:.2f},P={lt.Pmax_S.loc[Imax_id_S]:.2f}",  # ImaxS
                f"V={lt.Vmax_S.loc[Imin_id_S]:.2f},P={lt.Pmax_S.loc[Imin_id_S]:.2f}",  # IminS
                f"I={lt.Imax_S.loc[Vmax_id_S]:.2f},P={lt.Pmax_S.loc[Vmax_id_S]:.2f}",  # VmaxS
                f"I={lt.Imax_S.loc[Vmin_id_S]:.2f},P={lt.Pmax_S.loc[Vmin_id_S]:.2f}",  # VminS
                f"Voc={lt.Voc_S.loc[Iscmax_id_S]:.2f}",  # IscMaxS
                f"Voc={lt.Voc_S.loc[Iscmin_id_S]:.2f}",  # IscMinS
                f"Isc={lt.Isc0_S.loc[Vocmax_id_S]:.2f}",  # VocMaxS
                f"Isc={lt.Isc0_S.loc[Vocmin_id_S]:.2f}"  # VocMinS

                 ]
            ,

            'Temperaturas[C°]': [TpmaxS, TpminS, TImaxS, TIminS, TVmaxS, TVminS, TIscMaxS, TIscMinS, TVocMaxS,
                                 TVocMinS],
            'Irradiancia_Efectiva': [PoamaxS, PoaminS, PoaImaxS, PoaIminS, PoaVmaxS, PoaVminS, PoaIscMaxS, PoaIscMinS,
                                     PoaVocMaxS, PoaVocMinS],
            'Fechas': [Potmax_id_S, Potmin_id_S, Imax_id_S, Imin_id_S, Vmax_id_S, Vmin_id_S, Iscmax_id_S, Iscmin_id_S,
                       Vocmax_id_S, Vocmin_id_S]
        }



        df = pd.DataFrame(data=d,
                          index=["Potencia _maxima F", "Potencia_minima F", "Corriente Maxima F", "Corriente Minima F",
                                 "Voltaje Maximo F", "Voltaje Minimo F", "Corriente maxima de Corto Circuito F",
                                 "Corriente minima de Corto Circuito F", "Voltaje maximo de Corto Circuito F",
                                 "Voltaje minimo de Corto Circuito F"])


        # Estas son para si en el futuro se ocupa. 

        df2 = pd.DataFrame(data=d1,
                           index=["Potencia _maximaS", "Potencia_minima S", "Corriente Maxima S", "Corriente Minima S",
                                  "Voltaje Maximo S", "Voltaje Minimo S", "Corriente maxima de Corto Circuito S",
                                  "Corriente minima de Corto Circuito S", "Voltaje maximo de Corto Circuito S",
                                  "Voltaje minimo de Corto Circuito S"])

        m = pd.concat([round(df,2), round(df2,2)], axis=0, join="outer").reset_index()

        m.columns = ["Parametros Electricos", 'Valores', "Valores_operacionales", 'Temperaturas[C°]',
                     'Irradiancia_Efectiva', 'Fechas']

        return m

    ##NOCT##

    if Seleccion == [3]:
        #### Aquí es donde se hace la tabla final para Sandia
        Potmax_id_NOCT = lt["Pmax_NOCT"].idxmax()
        Potmin_id_NOCT = lt["Pmax_NOCT"].idxmin()
        Imax_id_NOCT = lt["Imax_NOCT"].idxmax()
        Imin_id_NOCT = lt["Imax_NOCT"].idxmin()
        Vmax_id_NOCT = lt["Vmax_NOCT"].idxmax()
        Vmin_id_NOCT = lt["Vmax_NOCT"].idxmin()
        ### Circuito abierto fechas ###
        Iscmax_id_NOCT = lt["Isc0_NOCT"].idxmax()
        Iscmin_id_NOCT = lt["Isc0_NOCT"].idxmin()
        Vocmax_id_NOCT = lt["Voc_NOCT"].idxmax()
        Vocmin_id_NOCT = lt["Voc_NOCT"].idxmin()
        ### Valores en funcionamiento ###
        PotmaxNOCT = lt["Pmax_NOCT"].loc[Potmax_id_NOCT]
        PotminNOCT = lt["Pmax_NOCT"].loc[Potmin_id_NOCT]
        ImaxNOCT = lt["Imax_NOCT"].loc[Imax_id_NOCT]
        IminNOCT = lt["Imax_NOCT"].loc[Imin_id_NOCT]
        VmaxNOCT = lt["Vmax_NOCT"].loc[Vmax_id_NOCT]
        VminNOCT = lt["Vmax_NOCT"].loc[Vmin_id_NOCT]
        #### Valores en circuito ####
        IscMaxNOCT = lt["Isc0_NOCT"].loc[Iscmax_id_NOCT]
        IscMinNOCT = lt["Isc0_NOCT"].loc[Iscmin_id_NOCT]
        VocMaxNOCT = lt["Voc_NOCT"].loc[Vocmax_id_NOCT]
        VocMinNOCT = lt["Voc_NOCT"].loc[Vocmin_id_NOCT]
        #### Temperaturas ###
        TpmaxNOCT = lt["T_NOCT"].loc[Potmax_id_NOCT]
        TpminNOCT = lt["T_NOCT"].loc[Potmin_id_NOCT]
        TImaxNOCT = lt["T_NOCT"].loc[Imax_id_NOCT]
        TIminNOCT = lt["T_NOCT"].loc[Imin_id_NOCT]
        TVmaxNOCT = lt["T_NOCT"].loc[Vmax_id_NOCT]
        TVminNOCT = lt["T_NOCT"].loc[Vmin_id_NOCT]
        #### Valores en circuito ####
        TIscMaxNOCT = lt["T_NOCT"].loc[Iscmax_id_NOCT]
        TIscMinNOCT = lt["T_NOCT"].loc[Iscmin_id_NOCT]
        TVocMaxNOCT = lt["T_NOCT"].loc[Vocmax_id_NOCT]
        TVocMinNOCT = lt["T_NOCT"].loc[Vocmin_id_NOCT]
        #### Irradiancia_Efectiva ####
        PoamaxNOCT = lt["Poa_global"].loc[Potmax_id_NOCT]
        PoaminNOCT = lt["Poa_global"].loc[Potmin_id_NOCT]
        PoaImaxNOCT = lt["Poa_global"].loc[Imax_id_NOCT]
        PoaIminNOCT = lt["Poa_global"].loc[Imin_id_NOCT]
        PoaVmaxNOCT = lt["Poa_global"].loc[Vmax_id_NOCT]
        PoaVminNOCT = lt["Poa_global"].loc[Vmin_id_NOCT]
        #### Irradiancia_Efectiva Valores en circuito ####
        PoaIscMaxNOCT = lt["Poa_global"].loc[Iscmax_id_NOCT]
        PoaIscMinNOCT = lt["Poa_global"].loc[Iscmin_id_NOCT]
        PoaVocMaxNOCT = lt["Poa_global"].loc[Vocmax_id_NOCT]
        PoaVocMinNOCT = lt["Poa_global"].loc[Vocmin_id_NOCT]
        ### Diccionario ###NOCT
        d = {
            'Valores': [PotmaxNOCT, PotminNOCT, ImaxNOCT, IminNOCT, VmaxNOCT, VminNOCT, IscMaxNOCT, IscMinNOCT, VocMaxNOCT, VocMinNOCT],
            "Valores_operacionales": [
                f"I={lt.Imax_NOCT.loc[Potmax_id_NOCT]:.2f},V={lt.Vmax_NOCT.loc[Potmax_id_NOCT]:.2f}",  # PotmaxNOCT
                f"I={lt.Imax_NOCT.loc[Potmin_id_NOCT]:.2f},V={lt.Vmax_NOCT.loc[Potmin_id_NOCT]:.2f}",  # PotminNOCT
                f"V={lt.Vmax_NOCT.loc[Imax_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Imax_id_NOCT]:.2f}",  # ImaxNOCT
                f"V={lt.Vmax_NOCT.loc[Imin_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Imin_id_NOCT]:.2f}",  # IminNOCT
                f"I={lt.Imax_NOCT.loc[Vmax_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Vmax_id_NOCT]:.2f}",  # VmaxNOCT
                f"I={lt.Imax_NOCT.loc[Vmin_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Vmin_id_NOCT]:.2f}",  # VminNOCT
                f"Voc={lt.Voc_NOCT.loc[Iscmax_id_NOCT]:.2f}",  # IscMaxNOCT
                f"Voc={lt.Voc_NOCT.loc[Iscmin_id_NOCT]:.2f}",  # IscMinNOCT
                f"Isc={lt.Isc0_NOCT.loc[Vocmax_id_NOCT]:.2f}",  # VocMaxNOCT
                f"Isc={lt.Isc0_NOCT.loc[Vocmin_id_NOCT]:.2f}"  # VocMinNOCT
            ]
            ,

            'Temperaturas NOCT [C°]': [TpmaxNOCT, TpminNOCT, TImaxNOCT, TIminNOCT, TVmaxNOCT, TVminNOCT, TIscMaxNOCT, TIscMinNOCT, TVocMaxNOCT,
                                         TVocMinNOCT],
            'Irradiancia_Efectiva': [PoamaxNOCT, PoaminNOCT, PoaImaxNOCT, PoaIminNOCT, PoaVmaxNOCT, PoaVminNOCT, PoaIscMaxNOCT, PoaIscMinNOCT,
                                     PoaVocMaxNOCT, PoaVocMinNOCT],
            'Fechas': [Potmax_id_NOCT, Potmin_id_NOCT, Imax_id_NOCT, Imin_id_NOCT, Vmax_id_NOCT, Vmin_id_NOCT, Iscmax_id_NOCT, Iscmin_id_NOCT,
                       Vocmax_id_NOCT, Vocmin_id_NOCT]
        }

        df = pd.DataFrame(data=round(d,2),
                          index=["Potencia _maximaNOCT", "Potencia_minima NOCT", "Corriente Maxima NOCT", "Corriente Minima NOCT",
                                 "Voltaje Maximo NOCT", "Voltaje Minimo NOCT", "Corriente maxima de Corto Circuito NOCT",
                                 "Corriente minima de Corto Circuito NOCT", "Voltaje maximo de Corto Circuito NOCT",
                                 "Voltaje minimo de Corto Circuito NOCT"])

        m = df.reset_index()
        m.columns = ["Parametros Electricos", 'Valores', "Valores_operacionales", 'Temperaturas[C°]',
                     'Irradiancia_Efectiva', 'Fechas']

        return m

    if Seleccion == [1, 3]:
        #### Aquí es donde se hace la tabla final combinando Feinman y Sandia
        #### Feinman
        Potmax_id_F = lt["Pmax_F"].idxmax()
        Potmin_id_F = lt["Pmax_F"].idxmin()
        Imax_id_F = lt["Imax_F"].idxmax()
        Imin_id_F = lt["Imax_F"].idxmin()
        Vmax_id_F = lt["Vmax_F"].idxmax()
        Vmin_id_F = lt["Vmax_F"].idxmin()
        Iscmax_id_F = lt["Isc0_F"].idxmax()
        Iscmin_id_F = lt["Isc0_F"].idxmin()
        Vocmax_id_F = lt["Voc_F"].idxmax()
        Vocmin_id_F = lt["Voc_F"].idxmin()

        PotmaxF = lt["Pmax_F"].loc[Potmax_id_F]
        PotminF = lt["Pmax_F"].loc[Potmin_id_F]
        ImaxF = lt["Imax_F"].loc[Imax_id_F]
        IminF = lt["Imax_F"].loc[Imin_id_F]
        VmaxF = lt["Vmax_F"].loc[Vmax_id_F]
        VminF = lt["Vmax_F"].loc[Vmin_id_F]
        IscMaxF = lt["Isc0_F"].loc[Iscmax_id_F]
        IscMinF = lt["Isc0_F"].loc[Iscmin_id_F]
        VocMaxF = lt["Vmax_F"].loc[Vocmax_id_F]
        VocMinF = lt["Vmax_F"].loc[Vocmin_id_F]

        TpmaxF = lt["T_Feinman"].loc[Potmax_id_F]
        TpminF = lt["T_Feinman"].loc[Potmin_id_F]
        TImaxF = lt["T_Feinman"].loc[Imax_id_F]
        TIminF = lt["T_Feinman"].loc[Imin_id_F]
        TVmaxF = lt["T_Feinman"].loc[Vmax_id_F]
        TVminF = lt["T_Feinman"].loc[Vmin_id_F]
        TIscMaxF = lt["T_Feinman"].loc[Iscmax_id_F]
        TIscMinF = lt["T_Feinman"].loc[Iscmin_id_F]
        TVocMaxF = lt["T_Feinman"].loc[Vocmax_id_F]
        TVocMinF = lt["T_Feinman"].loc[Vocmin_id_F]

        PoamaxF = lt["Poa_global"].loc[Potmax_id_F]
        PoaminF = lt["Poa_global"].loc[Potmin_id_F]
        PoaImaxF = lt["Poa_global"].loc[Imax_id_F]
        PoaIminF = lt["Poa_global"].loc[Imin_id_F]
        PoaVmaxF = lt["Poa_global"].loc[Vmax_id_F]
        PoaVminF = lt["Poa_global"].loc[Vmin_id_F]
        PoaIscMaxF = lt["Poa_global"].loc[Iscmax_id_F]
        PoaIscMinF = lt["Poa_global"].loc[Iscmin_id_F]
        PoaVocMaxF = lt["Poa_global"].loc[Vocmax_id_F]
        PoaVocMinF = lt["Poa_global"].loc[Vocmin_id_F]

                    #### NOCT ######

        #### Aquí es donde se hace la tabla final para Sandia
        Potmax_id_NOCT = lt["Pmax_NOCT"].idxmax()
        Potmin_id_NOCT = lt["Pmax_NOCT"].idxmin()
        Imax_id_NOCT = lt["Imax_NOCT"].idxmax()
        Imin_id_NOCT = lt["Imax_NOCT"].idxmin()
        Vmax_id_NOCT = lt["Vmax_NOCT"].idxmax()
        Vmin_id_NOCT = lt["Vmax_NOCT"].idxmin()
        ### Circuito abierto fechas ###
        Iscmax_id_NOCT = lt["Isc0_NOCT"].idxmax()
        Iscmin_id_NOCT = lt["Isc0_NOCT"].idxmin()
        Vocmax_id_NOCT = lt["Voc_NOCT"].idxmax()
        Vocmin_id_NOCT = lt["Voc_NOCT"].idxmin()
        ### Valores en funcionamiento ###
        PotmaxNOCT = lt["Pmax_NOCT"].loc[Potmax_id_NOCT]
        PotminNOCT = lt["Pmax_NOCT"].loc[Potmin_id_NOCT]
        ImaxNOCT = lt["Imax_NOCT"].loc[Imax_id_NOCT]
        IminNOCT = lt["Imax_NOCT"].loc[Imin_id_NOCT]
        VmaxNOCT = lt["Vmax_NOCT"].loc[Vmax_id_NOCT]
        VminNOCT = lt["Vmax_NOCT"].loc[Vmin_id_NOCT]
        #### Valores en circuito ####
        IscMaxNOCT = lt["Isc0_NOCT"].loc[Iscmax_id_NOCT]
        IscMinNOCT = lt["Isc0_NOCT"].loc[Iscmin_id_NOCT]
        VocMaxNOCT = lt["Voc_NOCT"].loc[Vocmax_id_NOCT]
        VocMinNOCT = lt["Voc_NOCT"].loc[Vocmin_id_NOCT]
        #### Temperaturas ###
        TpmaxNOCT = lt["T_NOCT"].loc[Potmax_id_NOCT]
        TpminNOCT = lt["T_NOCT"].loc[Potmin_id_NOCT]
        TImaxNOCT = lt["T_NOCT"].loc[Imax_id_NOCT]
        TIminNOCT = lt["T_NOCT"].loc[Imin_id_NOCT]
        TVmaxNOCT = lt["T_NOCT"].loc[Vmax_id_NOCT]
        TVminNOCT = lt["T_NOCT"].loc[Vmin_id_NOCT]
        #### Valores en circuito ####
        TIscMaxNOCT = lt["T_NOCT"].loc[Iscmax_id_NOCT]
        TIscMinNOCT = lt["T_NOCT"].loc[Iscmin_id_NOCT]
        TVocMaxNOCT = lt["T_NOCT"].loc[Vocmax_id_NOCT]
        TVocMinNOCT = lt["T_NOCT"].loc[Vocmin_id_NOCT]
        #### Irradiancia_Efectiva ####
        PoamaxNOCT = lt["Poa_global"].loc[Potmax_id_NOCT]
        PoaminNOCT = lt["Poa_global"].loc[Potmin_id_NOCT]
        PoaImaxNOCT = lt["Poa_global"].loc[Imax_id_NOCT]
        PoaIminNOCT = lt["Poa_global"].loc[Imin_id_NOCT]
        PoaVmaxNOCT = lt["Poa_global"].loc[Vmax_id_NOCT]
        PoaVminNOCT = lt["Poa_global"].loc[Vmin_id_NOCT]
        #### Irradiancia_Efectiva Valores en circuito ####
        PoaIscMaxNOCT = lt["Poa_global"].loc[Iscmax_id_NOCT]
        PoaIscMinNOCT = lt["Poa_global"].loc[Iscmin_id_NOCT]
        PoaVocMaxNOCT = lt["Poa_global"].loc[Vocmax_id_NOCT]
        PoaVocMinNOCT = lt["Poa_global"].loc[Vocmin_id_NOCT]

        ### Diccionario ###

        d = {
            'Valores': [PotmaxF, PotminF, ImaxF, IminF, VmaxF, VminF, IscMaxF, IscMinF, VocMaxF, VocMinF],

            "Valores_operacionales": [
                f"I={lt.Imax_F.loc[Potmax_id_F]:.2f},V={lt.Vmax_F.loc[Potmax_id_F]:.2f}",  # PotmaxF
                f"I={lt.Imax_F.loc[Potmin_id_F]:.2f},V={lt.Vmax_F.loc[Potmin_id_F]:.2f}",  # PotminF
                f"V={lt.Vmax_F.loc[Imax_id_F]:.2f},P={lt.Pmax_F.loc[Imax_id_F]:.2f}",  # ImaxF
                f"V={lt.Vmax_F.loc[Imin_id_F]:.2f},P={lt.Pmax_F.loc[Imin_id_F]:.2f}",  # IminF
                f"I={lt.Imax_F.loc[Vmax_id_F]:.2f},P={lt.Pmax_F.loc[Vmax_id_F]:.2f}",  # VmaxF
                f"I={lt.Imax_F.loc[Vmin_id_F]:.2f},P={lt.Pmax_F.loc[Vmin_id_F]:.2f}",  # VminF
                f"Voc={lt.Voc_F.loc[Iscmax_id_F]:.2f}",  # IscMaxF
                f"Voc={lt.Voc_F.loc[Iscmin_id_F]:.2f}",  # IscMinF
                f"Isc={lt.Isc0_F.loc[Vocmax_id_F]:.2f}",  # VocMaxF
                f"Isc={lt.Isc0_F.loc[Vocmin_id_F]:.2f}"  # VocMinF
            ]
            ,

            'Temperaturas[C°]': [TpmaxF, TpminF, TImaxF, TIminF, TVmaxF, TVminF, TIscMaxF, TIscMinF, TVocMaxF,
                                 TVocMinF],
            'Irradiancia_Efectiva': [PoamaxF, PoaminF, PoaImaxF, PoaIminF, PoaVmaxF, PoaVminF, PoaIscMaxF, PoaIscMinF,
                                     PoaVocMaxF, PoaVocMinF],
            'Fechas': [Potmax_id_F, Potmin_id_F, Imax_id_F, Imin_id_F, Vmax_id_F, Vmin_id_F, Iscmax_id_F, Iscmin_id_F,
                       Vocmax_id_F, Vocmin_id_F]
        }

        d1 = {
            'Valores': [PotmaxNOCT, PotminNOCT, ImaxNOCT, IminNOCT, VmaxNOCT, VminNOCT, IscMaxNOCT, IscMinNOCT,
                        VocMaxNOCT, VocMinNOCT],
            "Valores_operacionales": [
                f"I={lt.Imax_NOCT.loc[Potmax_id_NOCT]:.2f},V={lt.Vmax_NOCT.loc[Potmax_id_NOCT]:.2f}",  # PotmaxNOCT
                f"I={lt.Imax_NOCT.loc[Potmin_id_NOCT]:.2f},V={lt.Vmax_NOCT.loc[Potmin_id_NOCT]:.2f}",  # PotminNOCT
                f"V={lt.Vmax_NOCT.loc[Imax_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Imax_id_NOCT]:.2f}",  # ImaxNOCT
                f"V={lt.Vmax_NOCT.loc[Imin_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Imin_id_NOCT]:.2f}",  # IminNOCT
                f"I={lt.Imax_NOCT.loc[Vmax_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Vmax_id_NOCT]:.2f}",  # VmaxNOCT
                f"I={lt.Imax_NOCT.loc[Vmin_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Vmin_id_NOCT]:.2f}",  # VminNOCT
                f"Voc={lt.Voc_NOCT.loc[Iscmax_id_NOCT]:.2f}",  # IscMaxNOCT
                f"Voc={lt.Voc_NOCT.loc[Iscmin_id_NOCT]:.2f}",  # IscMinNOCT
                f"Isc={lt.Isc0_NOCT.loc[Vocmax_id_NOCT]:.2f}",  # VocMaxNOCT
                f"Isc={lt.Isc0_NOCT.loc[Vocmin_id_NOCT]:.2f}"  # VocMinNOCT
            ]
            ,

            'Temperaturas[C°]': [TpmaxNOCT, TpminNOCT, TImaxNOCT, TIminNOCT, TVmaxNOCT, TVminNOCT, TIscMaxNOCT,
                                       TIscMinNOCT, TVocMaxNOCT,
                                       TVocMinNOCT],
            'Irradiancia_Efectiva': [PoamaxNOCT, PoaminNOCT, PoaImaxNOCT, PoaIminNOCT, PoaVmaxNOCT, PoaVminNOCT,
                                     PoaIscMaxNOCT, PoaIscMinNOCT,
                                     PoaVocMaxNOCT, PoaVocMinNOCT],
            'Fechas': [Potmax_id_NOCT, Potmin_id_NOCT, Imax_id_NOCT, Imin_id_NOCT, Vmax_id_NOCT, Vmin_id_NOCT,
                       Iscmax_id_NOCT, Iscmin_id_NOCT,
                       Vocmax_id_NOCT, Vocmin_id_NOCT]
        }



        df = pd.DataFrame(data=d,
                          index=["Potencia _maxima F", "Potencia_minima F", "Corriente Maxima F", "Corriente Minima F",
                                 "Voltaje Maximo F", "Voltaje Minimo F", "Corriente maxima de Corto Circuito F",
                                 "Corriente minima de Corto Circuito F", "Voltaje maximo de Corto Circuito F",
                                 "Voltaje minimo de Corto Circuito F"])


        # Estas son para si en el futuro se ocupa.

        df2 = pd.DataFrame(data=d1,
                          index=["Potencia _maximaNOCT", "Potencia_minima NOCT", "Corriente Maxima NOCT",
                                 "Corriente Minima NOCT",
                                 "Voltaje Maximo NOCT", "Voltaje Minimo NOCT",
                                 "Corriente maxima de Corto Circuito NOCT",
                                 "Corriente minima de Corto Circuito NOCT", "Voltaje maximo de Corto Circuito NOCT",
                                 "Voltaje minimo de Corto Circuito NOCT"])

        m = pd.concat([round(df,2), round(df2,2)], axis=0, join="outer").reset_index()

        m.columns = ["Parametros Electricos", 'Valores', "Valores_operacionales", 'Temperaturas[C°]',
                     'Irradiancia_Efectiva', 'Fechas']

        return m

    if Seleccion == [2, 3]:

        #### Aquí es donde se hace la tabla final combinando Feinman y Sandia
        #### Feinman
        Potmax_id_S = lt["Pmax_S"].idxmax()
        Potmin_id_S = lt["Pmax_S"].idxmin()
        Imax_id_S = lt["Imax_S"].idxmax()
        Imin_id_S = lt["Imax_S"].idxmin()
        Vmax_id_S = lt["Vmax_S"].idxmax()
        Vmin_id_S = lt["Vmax_S"].idxmin()
        ### Circuito abierto fechas ###
        Iscmax_id_S = lt["Isc0_S"].idxmax()
        Iscmin_id_S = lt["Isc0_S"].idxmin()
        Vocmax_id_S = lt["Voc_S"].idxmax()
        Vocmin_id_S = lt["Voc_S"].idxmin()
        ### Valores en funcionamiento ###
        PotmaxS = lt["Pmax_S"].loc[Potmax_id_S]
        PotminS = lt["Pmax_S"].loc[Potmin_id_S]
        ImaxS = lt["Imax_S"].loc[Imax_id_S]
        IminS = lt["Imax_S"].loc[Imin_id_S]
        VmaxS = lt["Vmax_S"].loc[Vmax_id_S]
        VminS = lt["Vmax_S"].loc[Vmin_id_S]
        #### Valores en circuito ####
        IscMaxS = lt["Isc0_S"].loc[Iscmax_id_S]
        IscMinS = lt["Isc0_S"].loc[Iscmin_id_S]
        VocMaxS = lt["Voc_S"].loc[Vocmax_id_S]
        VocMinS = lt["Voc_S"].loc[Vocmin_id_S]
        #### Temperaturas ###
        TpmaxS = lt["T_Sandia"].loc[Potmax_id_S]
        TpminS = lt["T_Sandia"].loc[Potmin_id_S]
        TImaxS = lt["T_Sandia"].loc[Imax_id_S]
        TIminS = lt["T_Sandia"].loc[Imin_id_S]
        TVmaxS = lt["T_Sandia"].loc[Vmax_id_S]
        TVminS = lt["T_Sandia"].loc[Vmin_id_S]
        #### Valores en circuito ####
        TIscMaxS = lt["T_Sandia"].loc[Iscmax_id_S]
        TIscMinS = lt["T_Sandia"].loc[Iscmin_id_S]
        TVocMaxS = lt["T_Sandia"].loc[Vocmax_id_S]
        TVocMinS = lt["T_Sandia"].loc[Vocmin_id_S]
        #### Irradiancia_Efectiva ####
        PoamaxS = lt["Poa_global"].loc[Potmax_id_S]
        PoaminS = lt["Poa_global"].loc[Potmin_id_S]
        PoaImaxS = lt["Poa_global"].loc[Imax_id_S]
        PoaIminS = lt["Poa_global"].loc[Imin_id_S]
        PoaVmaxS = lt["Poa_global"].loc[Vmax_id_S]
        PoaVminS = lt["Poa_global"].loc[Vmin_id_S]
        #### Irradiancia_Efectiva Valores en circuito ####
        PoaIscMaxS = lt["Poa_global"].loc[Iscmax_id_S]
        PoaIscMinS = lt["Poa_global"].loc[Iscmin_id_S]
        PoaVocMaxS = lt["Poa_global"].loc[Vocmax_id_S]
        PoaVocMinS = lt["Poa_global"].loc[Vocmin_id_S]

        #### NOCT ######

        #### Aquí es donde se hace la tabla final para Sandia
        Potmax_id_NOCT = lt["Pmax_NOCT"].idxmax()
        Potmin_id_NOCT = lt["Pmax_NOCT"].idxmin()
        Imax_id_NOCT = lt["Imax_NOCT"].idxmax()
        Imin_id_NOCT = lt["Imax_NOCT"].idxmin()
        Vmax_id_NOCT = lt["Vmax_NOCT"].idxmax()
        Vmin_id_NOCT = lt["Vmax_NOCT"].idxmin()
        ### Circuito abierto fechas ###
        Iscmax_id_NOCT = lt["Isc0_NOCT"].idxmax()
        Iscmin_id_NOCT = lt["Isc0_NOCT"].idxmin()
        Vocmax_id_NOCT = lt["Voc_NOCT"].idxmax()
        Vocmin_id_NOCT = lt["Voc_NOCT"].idxmin()
        ### Valores en funcionamiento ###
        PotmaxNOCT = lt["Pmax_NOCT"].loc[Potmax_id_NOCT]
        PotminNOCT = lt["Pmax_NOCT"].loc[Potmin_id_NOCT]
        ImaxNOCT = lt["Imax_NOCT"].loc[Imax_id_NOCT]
        IminNOCT = lt["Imax_NOCT"].loc[Imin_id_NOCT]
        VmaxNOCT = lt["Vmax_NOCT"].loc[Vmax_id_NOCT]
        VminNOCT = lt["Vmax_NOCT"].loc[Vmin_id_NOCT]
        #### Valores en circuito ####
        IscMaxNOCT = lt["Isc0_NOCT"].loc[Iscmax_id_NOCT]
        IscMinNOCT = lt["Isc0_NOCT"].loc[Iscmin_id_NOCT]
        VocMaxNOCT = lt["Voc_NOCT"].loc[Vocmax_id_NOCT]
        VocMinNOCT = lt["Voc_NOCT"].loc[Vocmin_id_NOCT]
        #### Temperaturas ###
        TpmaxNOCT = lt["T_NOCT"].loc[Potmax_id_NOCT]
        TpminNOCT = lt["T_NOCT"].loc[Potmin_id_NOCT]
        TImaxNOCT = lt["T_NOCT"].loc[Imax_id_NOCT]
        TIminNOCT = lt["T_NOCT"].loc[Imin_id_NOCT]
        TVmaxNOCT = lt["T_NOCT"].loc[Vmax_id_NOCT]
        TVminNOCT = lt["T_NOCT"].loc[Vmin_id_NOCT]
        #### Valores en circuito ####
        TIscMaxNOCT = lt["T_NOCT"].loc[Iscmax_id_NOCT]
        TIscMinNOCT = lt["T_NOCT"].loc[Iscmin_id_NOCT]
        TVocMaxNOCT = lt["T_NOCT"].loc[Vocmax_id_NOCT]
        TVocMinNOCT = lt["T_NOCT"].loc[Vocmin_id_NOCT]
        #### Irradiancia_Efectiva ####
        PoamaxNOCT = lt["Poa_global"].loc[Potmax_id_NOCT]
        PoaminNOCT = lt["Poa_global"].loc[Potmin_id_NOCT]
        PoaImaxNOCT = lt["Poa_global"].loc[Imax_id_NOCT]
        PoaIminNOCT = lt["Poa_global"].loc[Imin_id_NOCT]
        PoaVmaxNOCT = lt["Poa_global"].loc[Vmax_id_NOCT]
        PoaVminNOCT = lt["Poa_global"].loc[Vmin_id_NOCT]
        #### Irradiancia_Efectiva Valores en circuito ####
        PoaIscMaxNOCT = lt["Poa_global"].loc[Iscmax_id_NOCT]
        PoaIscMinNOCT = lt["Poa_global"].loc[Iscmin_id_NOCT]
        PoaVocMaxNOCT = lt["Poa_global"].loc[Vocmax_id_NOCT]
        PoaVocMinNOCT = lt["Poa_global"].loc[Vocmin_id_NOCT]

        ### Diccionario ###

        d = {
            'Valores': [PotmaxS, PotminS, ImaxS, IminS, VmaxS, VminS, IscMaxS, IscMinS, VocMaxS, VocMinS],
            "Valores_operacionales": [
                f"I={lt.Imax_S.loc[Potmax_id_S]:.2f},V={lt.Vmax_S.loc[Potmax_id_S]:.2f}",  # PotmaxS
                f"I={lt.Imax_S.loc[Potmin_id_S]:.2f},V={lt.Vmax_S.loc[Potmin_id_S]:.2f}",  # PotminS
                f"V={lt.Vmax_S.loc[Imax_id_S]:.2f},P={lt.Pmax_S.loc[Imax_id_S]:.2f}",  # ImaxS
                f"V={lt.Vmax_S.loc[Imin_id_S]:.2f},P={lt.Pmax_S.loc[Imin_id_S]:.2f}",  # IminS
                f"I={lt.Imax_S.loc[Vmax_id_S]:.2f},P={lt.Pmax_S.loc[Vmax_id_S]:.2f}",  # VmaxS
                f"I={lt.Imax_S.loc[Vmin_id_S]:.2f},P={lt.Pmax_S.loc[Vmin_id_S]:.2f}",  # VminS
                f"Voc={lt.Voc_S.loc[Iscmax_id_S]:.2f}",  # IscMaxS
                f"Voc={lt.Voc_S.loc[Iscmin_id_S]:.2f}",  # IscMinS
                f"Isc={lt.Isc0_S.loc[Vocmax_id_S]:.2f}",  # VocMaxS
                f"Isc={lt.Isc0_S.loc[Vocmin_id_S]:.2f}"  # VocMinS
            ]
            ,

            'Temperaturas[C°]': [TpmaxS, TpminS, TImaxS, TIminS, TVmaxS, TVminS, TIscMaxS, TIscMinS, TVocMaxS,
                                         TVocMinS],
            'Irradiancia_Efectiva': [PoamaxS, PoaminS, PoaImaxS, PoaIminS, PoaVmaxS, PoaVminS, PoaIscMaxS, PoaIscMinS,
                                     PoaVocMaxS, PoaVocMinS],
            'Fechas': [Potmax_id_S, Potmin_id_S, Imax_id_S, Imin_id_S, Vmax_id_S, Vmin_id_S, Iscmax_id_S, Iscmin_id_S,
                       Vocmax_id_S, Vocmin_id_S]
        }

        d1 = {
            'Valores': [PotmaxNOCT, PotminNOCT, ImaxNOCT, IminNOCT, VmaxNOCT, VminNOCT, IscMaxNOCT, IscMinNOCT,
                        VocMaxNOCT, VocMinNOCT],
            "Valores_operacionales": [
                f"I={lt.Imax_NOCT.loc[Potmax_id_NOCT]:.2f},V={lt.Vmax_NOCT.loc[Potmax_id_NOCT]:.2f}",  # PotmaxNOCT
                f"I={lt.Imax_NOCT.loc[Potmin_id_NOCT]:.2f},V={lt.Vmax_NOCT.loc[Potmin_id_NOCT]:.2f}",  # PotminNOCT
                f"V={lt.Vmax_NOCT.loc[Imax_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Imax_id_NOCT]:.2f}",  # ImaxNOCT
                f"V={lt.Vmax_NOCT.loc[Imin_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Imin_id_NOCT]:.2f}",  # IminNOCT
                f"I={lt.Imax_NOCT.loc[Vmax_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Vmax_id_NOCT]:.2f}",  # VmaxNOCT
                f"I={lt.Imax_NOCT.loc[Vmin_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Vmin_id_NOCT]:.2f}",  # VminNOCT
                f"Voc={lt.Voc_NOCT.loc[Iscmax_id_NOCT]:.2f}",  # IscMaxNOCT
                f"Voc={lt.Voc_NOCT.loc[Iscmin_id_NOCT]:.2f}",  # IscMinNOCT
                f"Isc={lt.Isc0_NOCT.loc[Vocmax_id_NOCT]:.2f}",  # VocMaxNOCT
                f"Isc={lt.Isc0_NOCT.loc[Vocmin_id_NOCT]:.2f}"  # VocMinNOCT
            ]
            ,

            'Temperaturas[C°]': [TpmaxNOCT, TpminNOCT, TImaxNOCT, TIminNOCT, TVmaxNOCT, TVminNOCT, TIscMaxNOCT,
                                       TIscMinNOCT, TVocMaxNOCT,
                                       TVocMinNOCT],
            'Irradiancia_Efectiva': [PoamaxNOCT, PoaminNOCT, PoaImaxNOCT, PoaIminNOCT, PoaVmaxNOCT, PoaVminNOCT,
                                     PoaIscMaxNOCT, PoaIscMinNOCT,
                                     PoaVocMaxNOCT, PoaVocMinNOCT],
            'Fechas': [Potmax_id_NOCT, Potmin_id_NOCT, Imax_id_NOCT, Imin_id_NOCT, Vmax_id_NOCT, Vmin_id_NOCT,
                       Iscmax_id_NOCT, Iscmin_id_NOCT,
                       Vocmax_id_NOCT, Vocmin_id_NOCT]
        }

        df = pd.DataFrame(data=d,
                          index=["Potencia _maximaS", "Potencia_minima S", "Corriente Maxima S", "Corriente Minima S",
                                 "Voltaje Maximo S", "Voltaje Minimo S", "Corriente maxima de Corto Circuito S",
                                 "Corriente minima de Corto Circuito S", "Voltaje maximo de Corto Circuito S",
                                 "Voltaje minimo de Corto Circuito S"])

        # Estas son para si en el futuro se ocupa.

        df2 = pd.DataFrame(data=d1,
                           index=["Potencia _maximaNOCT", "Potencia_minima NOCT", "Corriente Maxima NOCT",
                                  "Corriente Minima NOCT",
                                  "Voltaje Maximo NOCT", "Voltaje Minimo NOCT",
                                  "Corriente maxima de Corto Circuito NOCT",
                                  "Corriente minima de Corto Circuito NOCT", "Voltaje maximo de Corto Circuito NOCT",
                                  "Voltaje minimo de Corto Circuito NOCT"])

        m = pd.concat([round(df,2), round(df2,2)], axis=0, join="outer").reset_index()

        m.columns = ["Parametros Electricos", 'Valores', "Valores_operacionales", 'Temperaturas[C°]',
                     'Irradiancia_Efectiva', 'Fechas']

        return m

    if Seleccion == [1, 2, 3]:
        #### Aquí es donde se hace la tabla final combinando Feinman y Sandia
        #### Feinman ####

        #### Feinman
        Potmax_id_F = lt["Pmax_F"].idxmax()
        Potmin_id_F = lt["Pmax_F"].idxmin()
        Imax_id_F = lt["Imax_F"].idxmax()
        Imin_id_F = lt["Imax_F"].idxmin()
        Vmax_id_F = lt["Vmax_F"].idxmax()
        Vmin_id_F = lt["Vmax_F"].idxmin()
        Iscmax_id_F = lt["Isc0_F"].idxmax()
        Iscmin_id_F = lt["Isc0_F"].idxmin()
        Vocmax_id_F = lt["Voc_F"].idxmax()
        Vocmin_id_F = lt["Voc_F"].idxmin()

        PotmaxF = lt["Pmax_F"].loc[Potmax_id_F]
        PotminF = lt["Pmax_F"].loc[Potmin_id_F]
        ImaxF = lt["Imax_F"].loc[Imax_id_F]
        IminF = lt["Imax_F"].loc[Imin_id_F]
        VmaxF = lt["Vmax_F"].loc[Vmax_id_F]
        VminF = lt["Vmax_F"].loc[Vmin_id_F]
        IscMaxF = lt["Isc0_F"].loc[Iscmax_id_F]
        IscMinF = lt["Isc0_F"].loc[Iscmin_id_F]
        VocMaxF = lt["Vmax_F"].loc[Vocmax_id_F]
        VocMinF = lt["Vmax_F"].loc[Vocmin_id_F]

        TpmaxF = lt["T_Feinman"].loc[Potmax_id_F]
        TpminF = lt["T_Feinman"].loc[Potmin_id_F]
        TImaxF = lt["T_Feinman"].loc[Imax_id_F]
        TIminF = lt["T_Feinman"].loc[Imin_id_F]
        TVmaxF = lt["T_Feinman"].loc[Vmax_id_F]
        TVminF = lt["T_Feinman"].loc[Vmin_id_F]
        TIscMaxF = lt["T_Feinman"].loc[Iscmax_id_F]
        TIscMinF = lt["T_Feinman"].loc[Iscmin_id_F]
        TVocMaxF = lt["T_Feinman"].loc[Vocmax_id_F]
        TVocMinF = lt["T_Feinman"].loc[Vocmin_id_F]

        PoamaxF = lt["Poa_global"].loc[Potmax_id_F]
        PoaminF = lt["Poa_global"].loc[Potmin_id_F]
        PoaImaxF = lt["Poa_global"].loc[Imax_id_F]
        PoaIminF = lt["Poa_global"].loc[Imin_id_F]
        PoaVmaxF = lt["Poa_global"].loc[Vmax_id_F]
        PoaVminF = lt["Poa_global"].loc[Vmin_id_F]
        PoaIscMaxF = lt["Poa_global"].loc[Iscmax_id_F]
        PoaIscMinF = lt["Poa_global"].loc[Iscmin_id_F]
        PoaVocMaxF = lt["Poa_global"].loc[Vocmax_id_F]
        PoaVocMinF = lt["Poa_global"].loc[Vocmin_id_F]

        #### Sandia ####
        Potmax_id_S = lt["Pmax_S"].idxmax()
        Potmin_id_S = lt["Pmax_S"].idxmin()
        Imax_id_S = lt["Imax_S"].idxmax()
        Imin_id_S = lt["Imax_S"].idxmin()
        Vmax_id_S = lt["Vmax_S"].idxmax()
        Vmin_id_S = lt["Vmax_S"].idxmin()
        ### Circuito abierto fechas ###
        Iscmax_id_S = lt["Isc0_S"].idxmax()
        Iscmin_id_S = lt["Isc0_S"].idxmin()
        Vocmax_id_S = lt["Voc_S"].idxmax()
        Vocmin_id_S = lt["Voc_S"].idxmin()
        ### Valores en funcionamiento ###
        PotmaxS = lt["Pmax_S"].loc[Potmax_id_S]
        PotminS = lt["Pmax_S"].loc[Potmin_id_S]
        ImaxS = lt["Imax_S"].loc[Imax_id_S]
        IminS = lt["Imax_S"].loc[Imin_id_S]
        VmaxS = lt["Vmax_S"].loc[Vmax_id_S]
        VminS = lt["Vmax_S"].loc[Vmin_id_S]
        #### Valores en circuito ####
        IscMaxS = lt["Isc0_S"].loc[Iscmax_id_S]
        IscMinS = lt["Isc0_S"].loc[Iscmin_id_S]
        VocMaxS = lt["Voc_S"].loc[Vocmax_id_S]
        VocMinS = lt["Voc_S"].loc[Vocmin_id_S]
        #### Temperaturas ###
        TpmaxS = lt["T_Sandia"].loc[Potmax_id_S]
        TpminS = lt["T_Sandia"].loc[Potmin_id_S]
        TImaxS = lt["T_Sandia"].loc[Imax_id_S]
        TIminS = lt["T_Sandia"].loc[Imin_id_S]
        TVmaxS = lt["T_Sandia"].loc[Vmax_id_S]
        TVminS = lt["T_Sandia"].loc[Vmin_id_S]
        #### Valores en circuito ####
        TIscMaxS = lt["T_Sandia"].loc[Iscmax_id_S]
        TIscMinS = lt["T_Sandia"].loc[Iscmin_id_S]
        TVocMaxS = lt["T_Sandia"].loc[Vocmax_id_S]
        TVocMinS = lt["T_Sandia"].loc[Vocmin_id_S]
        #### Irradiancia_Efectiva ####
        PoamaxS = lt["Poa_global"].loc[Potmax_id_S]
        PoaminS = lt["Poa_global"].loc[Potmin_id_S]
        PoaImaxS = lt["Poa_global"].loc[Imax_id_S]
        PoaIminS = lt["Poa_global"].loc[Imin_id_S]
        PoaVmaxS = lt["Poa_global"].loc[Vmax_id_S]
        PoaVminS = lt["Poa_global"].loc[Vmin_id_S]
        #### Irradiancia_Efectiva Valores en circuito ####
        PoaIscMaxS = lt["Poa_global"].loc[Iscmax_id_S]
        PoaIscMinS = lt["Poa_global"].loc[Iscmin_id_S]
        PoaVocMaxS = lt["Poa_global"].loc[Vocmax_id_S]
        PoaVocMinS = lt["Poa_global"].loc[Vocmin_id_S]

        #### NOCT ######

        #### Aquí es donde se hace la tabla final para Sandia
        Potmax_id_NOCT = lt["Pmax_NOCT"].idxmax()
        Potmin_id_NOCT = lt["Pmax_NOCT"].idxmin()
        Imax_id_NOCT = lt["Imax_NOCT"].idxmax()
        Imin_id_NOCT = lt["Imax_NOCT"].idxmin()
        Vmax_id_NOCT = lt["Vmax_NOCT"].idxmax()
        Vmin_id_NOCT = lt["Vmax_NOCT"].idxmin()
        ### Circuito abierto fechas ###
        Iscmax_id_NOCT = lt["Isc0_NOCT"].idxmax()
        Iscmin_id_NOCT = lt["Isc0_NOCT"].idxmin()
        Vocmax_id_NOCT = lt["Voc_NOCT"].idxmax()
        Vocmin_id_NOCT = lt["Voc_NOCT"].idxmin()
        ### Valores en funcionamiento ###
        PotmaxNOCT = lt["Pmax_NOCT"].loc[Potmax_id_NOCT]
        PotminNOCT = lt["Pmax_NOCT"].loc[Potmin_id_NOCT]
        ImaxNOCT = lt["Imax_NOCT"].loc[Imax_id_NOCT]
        IminNOCT = lt["Imax_NOCT"].loc[Imin_id_NOCT]
        VmaxNOCT = lt["Vmax_NOCT"].loc[Vmax_id_NOCT]
        VminNOCT = lt["Vmax_NOCT"].loc[Vmin_id_NOCT]
        #### Valores en circuito ####
        IscMaxNOCT = lt["Isc0_NOCT"].loc[Iscmax_id_NOCT]
        IscMinNOCT = lt["Isc0_NOCT"].loc[Iscmin_id_NOCT]
        VocMaxNOCT = lt["Voc_NOCT"].loc[Vocmax_id_NOCT]
        VocMinNOCT = lt["Voc_NOCT"].loc[Vocmin_id_NOCT]
        #### Temperaturas ###
        TpmaxNOCT = lt["T_NOCT"].loc[Potmax_id_NOCT]
        TpminNOCT = lt["T_NOCT"].loc[Potmin_id_NOCT]
        TImaxNOCT = lt["T_NOCT"].loc[Imax_id_NOCT]
        TIminNOCT = lt["T_NOCT"].loc[Imin_id_NOCT]
        TVmaxNOCT = lt["T_NOCT"].loc[Vmax_id_NOCT]
        TVminNOCT = lt["T_NOCT"].loc[Vmin_id_NOCT]
        #### Valores en circuito ####
        TIscMaxNOCT = lt["T_NOCT"].loc[Iscmax_id_NOCT]
        TIscMinNOCT = lt["T_NOCT"].loc[Iscmin_id_NOCT]
        TVocMaxNOCT = lt["T_NOCT"].loc[Vocmax_id_NOCT]
        TVocMinNOCT = lt["T_NOCT"].loc[Vocmin_id_NOCT]
        #### Irradiancia_Efectiva ####
        PoamaxNOCT = lt["Poa_global"].loc[Potmax_id_NOCT]
        PoaminNOCT = lt["Poa_global"].loc[Potmin_id_NOCT]
        PoaImaxNOCT = lt["Poa_global"].loc[Imax_id_NOCT]
        PoaIminNOCT = lt["Poa_global"].loc[Imin_id_NOCT]
        PoaVmaxNOCT = lt["Poa_global"].loc[Vmax_id_NOCT]
        PoaVminNOCT = lt["Poa_global"].loc[Vmin_id_NOCT]
        #### Irradiancia_Efectiva Valores en circuito ####
        PoaIscMaxNOCT = lt["Poa_global"].loc[Iscmax_id_NOCT]
        PoaIscMinNOCT = lt["Poa_global"].loc[Iscmin_id_NOCT]
        PoaVocMaxNOCT = lt["Poa_global"].loc[Vocmax_id_NOCT]
        PoaVocMinNOCT = lt["Poa_global"].loc[Vocmin_id_NOCT]

        ### Diccionario ###

        d = {
            'Valores': [PotmaxF, PotminF, ImaxF, IminF, VmaxF, VminF, IscMaxF, IscMinF, VocMaxF, VocMinF],

            "Valores_operacionales": [
                f"I={lt.Imax_F.loc[Potmax_id_F]:.2f},V={lt.Vmax_F.loc[Potmax_id_F]:.2f}",  # PotmaxF
                f"I={lt.Imax_F.loc[Potmin_id_F]:.2f},V={lt.Vmax_F.loc[Potmin_id_F]:.2f}",  # PotminF
                f"V={lt.Vmax_F.loc[Imax_id_F]:.2f},P={lt.Pmax_F.loc[Imax_id_F]:.2f}",  # ImaxF
                f"V={lt.Vmax_F.loc[Imin_id_F]:.2f},P={lt.Pmax_F.loc[Imin_id_F]:.2f}",  # IminF
                f"I={lt.Imax_F.loc[Vmax_id_F]:.2f},P={lt.Pmax_F.loc[Vmax_id_F]:.2f}",  # VmaxF
                f"I={lt.Imax_F.loc[Vmin_id_F]:.2f},P={lt.Pmax_F.loc[Vmin_id_F]:.2f}",  # VminF
                f"Voc={lt.Voc_F.loc[Iscmax_id_F]:.2f}",  # IscMaxF
                f"Voc={lt.Voc_F.loc[Iscmin_id_F]:.2f}",  # IscMinF
                f"Isc={lt.Isc0_F.loc[Vocmax_id_F]:.2f}",  # VocMaxF
                f"Isc={lt.Isc0_F.loc[Vocmin_id_F]:.2f}"  # VocMinF
            ]
            ,

            'Temperaturas[C°]': [TpmaxF, TpminF, TImaxF, TIminF, TVmaxF, TVminF, TIscMaxF, TIscMinF, TVocMaxF,
                                 TVocMinF],
            'Irradiancia_Efectiva': [PoamaxF, PoaminF, PoaImaxF, PoaIminF, PoaVmaxF, PoaVminF, PoaIscMaxF, PoaIscMinF,
                                     PoaVocMaxF, PoaVocMinF],
            'Fechas': [Potmax_id_F, Potmin_id_F, Imax_id_F, Imin_id_F, Vmax_id_F, Vmin_id_F, Iscmax_id_F, Iscmin_id_F,
                       Vocmax_id_F, Vocmin_id_F]
        }

        d1 = {
            'Valores': [PotmaxS, PotminS, ImaxS, IminS, VmaxS, VminS, IscMaxS, IscMinS, VocMaxS, VocMinS],
            "Valores_operacionales": [
                f"I={lt.Imax_S.loc[Potmax_id_S]:.2f},V={lt.Vmax_S.loc[Potmax_id_S]:.2f}",  # PotmaxS
                f"I={lt.Imax_S.loc[Potmin_id_S]:.2f},V={lt.Vmax_S.loc[Potmin_id_S]:.2f}",  # PotminS
                f"V={lt.Vmax_S.loc[Imax_id_S]:.2f},P={lt.Pmax_S.loc[Imax_id_S]:.2f}",  # ImaxS
                f"V={lt.Vmax_S.loc[Imin_id_S]:.2f},P={lt.Pmax_S.loc[Imin_id_S]:.2f}",  # IminS
                f"I={lt.Imax_S.loc[Vmax_id_S]:.2f},P={lt.Pmax_S.loc[Vmax_id_S]:.2f}",  # VmaxS
                f"I={lt.Imax_S.loc[Vmin_id_S]:.2f},P={lt.Pmax_S.loc[Vmin_id_S]:.2f}",  # VminS
                f"Voc={lt.Voc_S.loc[Iscmax_id_S]:.2f}",  # IscMaxS
                f"Voc={lt.Voc_S.loc[Iscmin_id_S]:.2f}",  # IscMinS
                f"Isc={lt.Isc0_S.loc[Vocmax_id_S]:.2f}",  # VocMaxS
                f"Isc={lt.Isc0_S.loc[Vocmin_id_S]:.2f}"  # VocMinS
            ]
            ,

            'Temperaturas[C°]': [TpmaxS, TpminS, TImaxS, TIminS, TVmaxS, TVminS, TIscMaxS, TIscMinS, TVocMaxS,
                                         TVocMinS],
            'Irradiancia_Efectiva': [PoamaxS, PoaminS, PoaImaxS, PoaIminS, PoaVmaxS, PoaVminS, PoaIscMaxS, PoaIscMinS,
                                     PoaVocMaxS, PoaVocMinS],
            'Fechas': [Potmax_id_S, Potmin_id_S, Imax_id_S, Imin_id_S, Vmax_id_S, Vmin_id_S, Iscmax_id_S, Iscmin_id_S,
                       Vocmax_id_S, Vocmin_id_S]
        }

        d2 = {
            'Valores': [PotmaxNOCT, PotminNOCT, ImaxNOCT, IminNOCT, VmaxNOCT, VminNOCT, IscMaxNOCT, IscMinNOCT,
                        VocMaxNOCT, VocMinNOCT],
            "Valores_operacionales": [
                f"I={lt.Imax_NOCT.loc[Potmax_id_NOCT]:.2f},V={lt.Vmax_NOCT.loc[Potmax_id_NOCT]:.2f}",  # PotmaxNOCT
                f"I={lt.Imax_NOCT.loc[Potmin_id_NOCT]:.2f},V={lt.Vmax_NOCT.loc[Potmin_id_NOCT]:.2f}",  # PotminNOCT
                f"V={lt.Vmax_NOCT.loc[Imax_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Imax_id_NOCT]:.2f}",  # ImaxNOCT
                f"V={lt.Vmax_NOCT.loc[Imin_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Imin_id_NOCT]:.2f}",  # IminNOCT
                f"I={lt.Imax_NOCT.loc[Vmax_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Vmax_id_NOCT]:.2f}",  # VmaxNOCT
                f"I={lt.Imax_NOCT.loc[Vmin_id_NOCT]:.2f},P={lt.Pmax_NOCT.loc[Vmin_id_NOCT]:.2f}",  # VminNOCT
                f"Voc={lt.Voc_NOCT.loc[Iscmax_id_NOCT]:.2f}",  # IscMaxNOCT
                f"Voc={lt.Voc_NOCT.loc[Iscmin_id_NOCT]:.2f}",  # IscMinNOCT
                f"Isc={lt.Isc0_NOCT.loc[Vocmax_id_NOCT]:.2f}",  # VocMaxNOCT
                f"Isc={lt.Isc0_NOCT.loc[Vocmin_id_NOCT]:.2f}"  # VocMinNOCT
            ]
            ,

            'Temperaturas[C°]': [TpmaxNOCT, TpminNOCT, TImaxNOCT, TIminNOCT, TVmaxNOCT, TVminNOCT, TIscMaxNOCT,
                                       TIscMinNOCT, TVocMaxNOCT,
                                       TVocMinNOCT],
            'Irradiancia_Efectiva': [PoamaxNOCT, PoaminNOCT, PoaImaxNOCT, PoaIminNOCT, PoaVmaxNOCT, PoaVminNOCT,
                                     PoaIscMaxNOCT, PoaIscMinNOCT,
                                     PoaVocMaxNOCT, PoaVocMinNOCT],
            'Fechas': [Potmax_id_NOCT, Potmin_id_NOCT, Imax_id_NOCT, Imin_id_NOCT, Vmax_id_NOCT, Vmin_id_NOCT,
                       Iscmax_id_NOCT, Iscmin_id_NOCT,
                       Vocmax_id_NOCT, Vocmin_id_NOCT]
        }

        df = pd.DataFrame(data=d,
                          index=["Potencia _maxima F", "Potencia_minima F", "Corriente Maxima F", "Corriente Minima F",
                                 "Voltaje Maximo F", "Voltaje Minimo F", "Corriente maxima de Corto Circuito F",
                                 "Corriente minima de Corto Circuito F", "Voltaje maximo de Corto Circuito F",
                                 "Voltaje minimo de Corto Circuito F"])

        df2 = pd.DataFrame(data=d1,
                          index=["Potencia _maximaS", "Potencia_minima S", "Corriente Maxima S", "Corriente Minima S",
                                 "Voltaje Maximo S", "Voltaje Minimo S", "Corriente maxima de Corto Circuito S",
                                 "Corriente minima de Corto Circuito S", "Voltaje maximo de Corto Circuito S",
                                 "Voltaje minimo de Corto Circuito S"])

        # Estas son para si en el futuro se ocupa.

        df3 = pd.DataFrame(data=d2,
                           index=["Potencia _maximaNOCT", "Potencia_minima NOCT", "Corriente Maxima NOCT",
                                  "Corriente Minima NOCT",
                                  "Voltaje Maximo NOCT", "Voltaje Minimo NOCT",
                                  "Corriente maxima de Corto Circuito NOCT",
                                  "Corriente minima de Corto Circuito NOCT", "Voltaje maximo de Corto Circuito NOCT",
                                  "Voltaje minimo de Corto Circuito NOCT"])

        m = pd.concat([round(df,2), round(df2,2),round(df3,2)], axis=0, join="outer").reset_index()

        m.columns = ["Parametros Electricos", 'Valores', "Valores_operacionales", 'Temperaturas[C°]','Irradiancia_Efectiva', 'Fechas']

        return m











def table_IV(d):

    global tablespe
    dataframes = []
    columns = [{'name': i, 'id': i} for i in d.columns]
    data = d.to_dict('records')
    dataframes.append((data, columns))

    tablespe = [
        html.Div([html.H1(f"Condiciones limite"),
            html.H3(f"Simulacion del modulo en el año seleccionado"),
            html.Div(
                dash_table.DataTable(
                    id=f"Modulo-IV-{i + 1}",
                    data=data,
                    columns=columns,
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
                ),
                style={'width': '100%', 'overflowX': 'auto'}
            )
        ], style={'width': '100%'}) for i, (data, columns) in enumerate(dataframes)
    ]

    return tablespe

def table_IV2(d):

    global tablespe
    dataframes = []
    columns = [{'name': i, 'id': i} for i in d.columns]
    data = d.to_dict('records')
    dataframes.append((data, columns))

    tablespe = [
        html.Div([
            html.H3(f"Comportamiento del modulo 2"),
            html.Div(
                dash_table.DataTable(
                    id=f"Modulo-IV-{i + 1}",
                    data=data,
                    columns=columns,
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
                ),
                style={'width': '100%', 'overflowX': 'auto'}
            )
        ], style={'width': '100%'}) for i, (data, columns) in enumerate(dataframes)
    ]

    return tablespe

# estas 'PE'
def IV_R(Placa, ds):
    valores = [valor for parametro, valor in Placa.items()]

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=float(valores[7]),  # deltha is gamma, but the proffesor commeted an error
        cells_in_series=float(valores[8]),
        temp_ref=25
    )

    conditions = ds

    i_sc = []
    v_oc = []
    i_mpi = []
    v_mpv = []
    p_mp = []

    fig = go.Figure()

    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=Placa["alpha"],
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)
        i_b = np.linspace(15.948434, 0., 100)
        v_b = pvlib.pvsystem.v_from_i(current=i_b, method='lambertw', **SDE_params)

        fig.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f"{case.Condiciones}"))

        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']
        fig.add_trace(go.Scatter(
            x=[v_mp],
            y=[i_mp],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp {idx + 1}",
            customdata=[v_mp * i_mp]
        ))

        i_sc.append(curve_info['i_sc'])
        v_oc.append(curve_info['v_oc'])
        i_mpi.append(curve_info['i_mp'])
        v_mpv.append(curve_info['v_mp'])
        p_mp.append(curve_info['p_mp'])

        fig.update_layout(
            title="Curva IV",
            xaxis_title="Module voltage [V]",
            yaxis_title="Module current [A]",
            legend_title="Conditions",
            xaxis_tickangle=30,
            xaxis_tickfont=dict(size=10),
            yaxis_tickfont=dict(size=10),
            plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
            paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
            font=dict(color='white'))

    d = {"ISC (Error %)": round((abs(i_sc - ds.Isc) / i_sc) * 100, 2),
         "VOC (Error %)": round((abs(v_oc - ds.Voc) / v_oc) * 100, 2),
         "IM (Error %)": round((abs(i_mpi - ds.Im) / i_mpi) * 100, 2),
         "VM (Error %)": round((abs(v_mpv - ds.Vm) / v_mpv) * 100, 2),
         "POT (Error %)": round((abs(p_mp - ds.Potencia) / p_mp) * 100, 2), "Irradiancia": round(ds.Geff, 2),
         "T_cell": round(ds.Tcell, 2)}

                 #   Tabla para la obtencion de parametros electricos.   #



    data_frame = pd.DataFrame(data=d).set_index(ds.Condiciones)
    data_frame=data_frame.reset_index()

    return fig, data_frame

## IV_R1

def IV_R1(Placa, ds):
    valores = [valor for parametro, valor in Placa.items()]

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=float(valores[7]),  # deltha is gamma, but the proffesor commeted an error
        cells_in_series=float(valores[8]),
        temp_ref=25
    )

    conditions = ds

    i_sc = []
    v_oc = []
    i_mpi = []
    v_mpv = []
    p_mp = []

    fig = go.Figure()

    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=Placa["alpha"],
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)
        i_b = np.linspace(15.948434, 0., 100)
        v_b = pvlib.pvsystem.v_from_i(current=i_b, method='lambertw', **SDE_params)

        fig.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f"{case.Condiciones}"))

        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']
        fig.add_trace(go.Scatter(
            x=[v_mp],
            y=[i_mp],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp {idx + 1}",
            customdata=[v_mp * i_mp]
        ))

        i_sc.append(curve_info['i_sc'])
        v_oc.append(curve_info['v_oc'])
        i_mpi.append(curve_info['i_mp'])
        v_mpv.append(curve_info['v_mp'])
        p_mp.append(curve_info['p_mp'])

        fig.update_layout(
            title="Curva IV",
            xaxis_title="Module voltage [V]",
            yaxis_title="Module current [A]",
            legend_title="Conditions",
            xaxis_tickangle=30,
            xaxis_tickfont=dict(size=10),
            yaxis_tickfont=dict(size=10),
            plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
            paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
            font=dict(color='white'))

    d = {"ISC (Error %)": round((abs(i_sc - ds.Isc) / i_sc) * 100, 2),
         "VOC (Error %)": round((abs(v_oc - ds.Voc) / v_oc) * 100, 2),
         "IM (Error %)": round((abs(i_mpi - ds.Im) / i_mpi) * 100, 2),
         "VM (Error %)": round((abs(v_mpv - ds.Vm) / v_mpv) * 100, 2),
         "POT (Error %)": round((abs(p_mp - ds.Potencia) / p_mp) * 100, 2), "Irradiancia": round(ds.Geff, 2),
         "T_cell": round(ds.Tcell, 2)}

    data_frame = pd.DataFrame(data=d).set_index(ds.Condiciones)
    data_frame=data_frame.reset_index()

    return fig, data_frame

## IV_R2
def IV_R2(Placa, ds):
    valores = [valor for parametro, valor in Placa.items()]

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=float(valores[7]),  # deltha is gamma, but the proffesor commeted an error
        cells_in_series=float(valores[8]),
        temp_ref=25
    )

    conditions = ds

    i_sc = []
    v_oc = []
    i_mpi = []
    v_mpv = []
    p_mp = []

    fig = go.Figure()

    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=Placa["alpha"],
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)
        i_b = np.linspace(15.948434, 0., 100)
        v_b = pvlib.pvsystem.v_from_i(current=i_b, method='lambertw', **SDE_params)

        fig.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f"{case.Condiciones}"))

        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']
        fig.add_trace(go.Scatter(
            x=[v_mp],
            y=[i_mp],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp {idx + 1}",
            customdata=[v_mp * i_mp]
        ))

        i_sc.append(curve_info['i_sc'])
        v_oc.append(curve_info['v_oc'])
        i_mpi.append(curve_info['i_mp'])
        v_mpv.append(curve_info['v_mp'])
        p_mp.append(curve_info['p_mp'])

        fig.update_layout(
            title="Curva IV",
            xaxis_title="Module voltage [V]",
            yaxis_title="Module current [A]",
            legend_title="Conditions",
            xaxis_tickangle=30,
            xaxis_tickfont=dict(size=10),
            yaxis_tickfont=dict(size=10),
            plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
            paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
            font=dict(color='white'))

    d = {"ISC (Error %)": round((abs(i_sc - ds.Isc) / i_sc) * 100,2), "VOC (Error %)": round((abs(v_oc - ds.Voc) / v_oc) * 100,2),
         "IM (Error %)": round((abs(i_mpi - ds.Im) / i_mpi) * 100,2), "VM (Error %)": round((abs(v_mpv - ds.Vm) / v_mpv) * 100,2),
         "POT (Error %)": round((abs(p_mp - ds.Potencia) / p_mp) * 100,2), "Irradiancia": round(ds.Geff,2), "T_cell": round(ds.Tcell,2)}

    data_frame = pd.DataFrame(data=d).set_index(ds.Condiciones)
    data_frame=data_frame.reset_index()

    return fig, data_frame

def IV_R_VE(Placa, ds):

    valores = [valor for parametro, valor in Placa.items()]

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=-0.36, #deltha is gamma, but the proffesor commeted an error
        cells_in_series=float(valores[8]),
        temp_ref=25
    )

    conditions = ds

    fig = go.Figure()

    ILo=[]
    I0o=[]
    Rso=[]
    Rsho=[]
    nNsVth0=[]

    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=Placa["alpha"],
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        ILo.append(IL)
        I0o.append(I0)
        Rso.append(Rs)
        Rsho.append(Rsh)
        nNsVth0.append(nNsVth)

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)


        fig.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f"T :{case.Tcell}, I :{case.Geff}"))
        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']

        fig.add_trace(go.Scatter(
            x=[v_mp],
            y=[i_mp],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp {idx + 1}",
            customdata=[v_mp * i_mp]
        ))



        fig.update_layout(
            title="Curva IV",
            xaxis_title="Module voltage [V]",
            yaxis_title="Module current [A]",
            legend_title="Conditions",
            xaxis_tickangle=30,
            xaxis_tickfont=dict(size=10),
            yaxis_tickfont=dict(size=10),
            plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
            paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
            font=dict(color='white')
        )

    Params = {
            'photocurrent': ILo,  # Light Generated current Il
            'saturation_current': I0o,  # Dark saturation current
            'resistance_series': Rso,
            'resistance_shunt': Rsho,
            'nNsVth': nNsVth0
             }

    Parametros= pd.DataFrame(data=Params)


    print(Parametros)




    return fig,Parametros



def resume_IV(Seleccion, lt):
    lista = []
    lista1 = []

    if Seleccion == [1]:
        #### Aquí es donde se hace la tabla final
        ## Estas son fechas
        Potmax_id_F = lt["Pmax_F"].idxmax()  #
        Vmax_id_F = lt["Vmax_F"].idxmax()  #
        Imax_id_F = lt["Imax_F"].idxmax()  #
        Tmax_id_F = lt["T_Feinman"].idxmax()  #
        Poa_id_F = lt["Poa_global"].idxmax()  #
        Gamma_F = lt["Gamma_F"].idxmax()  #

        ### Valores en funcionamiento en potencia maxima ###
        PotmaxF = lt["Pmax_F"].loc[Potmax_id_F]  #
        IscMaxF = lt["Isc0_F"].loc[Potmax_id_F]  #
        VocMaxF = lt["Voc_F"].loc[Potmax_id_F]  #
        TpmaxF = lt["T_Feinman"].loc[Potmax_id_F]  #
        PoamaxF = lt["Poa_global"].loc[Potmax_id_F]  #
        PVm = lt["Vmax_F"].loc[Potmax_id_F]
        PIm = lt["Imax_F"].loc[Potmax_id_F]
        PGF = lt["Gamma_F"].loc[Potmax_id_F]
        ### Valores de voltaje maximo ##

        VPotmaxF = lt["Pmax_F"].loc[Vmax_id_F]  #
        VIscMaxF = lt["Isc0_F"].loc[Vmax_id_F]  #
        VVocMaxF = lt["Voc_F"].loc[Vmax_id_F]  #
        VTpmaxF = lt["T_Feinman"].loc[Vmax_id_F]  #
        VPoamaxF = lt["Poa_global"].loc[Vmax_id_F]  #
        VVm = lt["Vmax_F"].loc[Vmax_id_F]
        VIm = lt["Imax_F"].loc[Vmax_id_F]
        VPGF = lt["Gamma_F"].loc[Vmax_id_F]
        ### VALORES DE CORRIENTE MAXIMO ###

        iPotmaxF = lt["Pmax_F"].loc[Imax_id_F]  #
        iIscMaxF = lt["Isc0_F"].loc[Imax_id_F]  #
        iVocMaxF = lt["Voc_F"].loc[Imax_id_F]  #
        iTpmaxF = lt["T_Feinman"].loc[Imax_id_F]  #
        iPoamaxF = lt["Poa_global"].loc[Imax_id_F]  #
        IVm = lt["Vmax_F"].loc[Imax_id_F]
        IIm = lt["Imax_F"].loc[Imax_id_F]
        IPGF = lt["Gamma_F"].loc[Imax_id_F]

        #### Valores en Temperatura maxima ####
        TPotmaxF = lt["Pmax_F"].loc[Tmax_id_F]  #
        TIscMaxF = lt["Isc0_F"].loc[Tmax_id_F]  #
        TVocMaxF = lt["Voc_F"].loc[Tmax_id_F]  #
        TTpmaxF = lt["T_Feinman"].loc[Tmax_id_F]  #
        TPoamaxF = lt["Poa_global"].loc[Tmax_id_F]  #
        TVm = lt["Vmax_F"].loc[Tmax_id_F]
        TIm = lt["Imax_F"].loc[Tmax_id_F]
        TPGF = lt["Gamma_F"].loc[Tmax_id_F]

        #### Irradancia_Efectiva ####

        PPotmaxF = lt["Pmax_F"].loc[Poa_id_F]
        PIscMaxF = lt["Isc0_F"].loc[Poa_id_F]
        PVocMaxF = lt["Voc_F"].loc[Poa_id_F]
        PTpmaxF = lt["T_Feinman"].loc[Poa_id_F]
        PPoamaxF = lt["Poa_global"].loc[Poa_id_F]
        POVm = lt["Vmax_F"].loc[Poa_id_F]
        POIm = lt["Imax_F"].loc[Poa_id_F]
        POPGF = lt["Gamma_F"].loc[Poa_id_F]
        ### Diccionario ###

        # Potencia Maxima **
        # Voltaje maximo**
        # Corriente maxima**
        # Temperatura maxima**
        # Irradiancia maxima**

        d = {
            "Geff": [PoamaxF, VPoamaxF, iPoamaxF, TPoamaxF, PPoamaxF],
            # Orden( Irradiancia de la pot maxima ,Voc,ISC,Temperatura, Irradiancia)
            "Tcell": [TpmaxF, VTpmaxF, iTpmaxF, TTpmaxF, PTpmaxF],
            "Voltajes": [VocMaxF, VVocMaxF, iVocMaxF, TVocMaxF, PVocMaxF],
            "Corrientes": [IscMaxF, VIscMaxF, iIscMaxF, TIscMaxF, PIscMaxF],
            "Potencia": [PotmaxF, VPotmaxF, iPotmaxF, TPotmaxF, PPotmaxF],
            "Vm": [PVm, VVm, IVm, TVm, POVm],
            "Im": [PIm, VIm, IIm, TIm, POIm]
        }

        df = pd.DataFrame(data=d,
                          index=["Potencia Maxima", "Temperatura Minima", "Corriente maxima", "Temperatura maxima",
                                 "Irradiancia maxima"])

        m = df.reset_index()
        m.columns = ["Condiciones", "Geff", "Tcell", "Voc", "Isc", "Potencia", "Vm", "Im"]

        return m

    if Seleccion == [2]:
        #### Aquí es donde se hace la tabla final para Sandia
        ## Estas son fechas
        Potmax_id_S = lt["Pmax_S"].idxmax()
        Vmax_id_S = lt["Vmax_S"].idxmax()
        Imax_id_S = lt["Imax_S"].idxmax()
        Tmax_id_S = lt["T_Sandia"].idxmax()
        Poa_id_S = lt["Poa_global"].idxmax()

        ### Valores en funcionamiento en potencia maxima ###
        PotmaxS = lt["Pmax_S"].loc[Potmax_id_S]
        IscMaxS = lt["Isc0_S"].loc[Potmax_id_S]
        VocMaxS = lt["Voc_S"].loc[Potmax_id_S]
        TpmaxS = lt["T_Sandia"].loc[Potmax_id_S]
        PoamaxS = lt["Poa_global"].loc[Potmax_id_S]
        PVmS = lt["Vmax_S"].loc[Potmax_id_S]
        PImS = lt["Imax_S"].loc[Potmax_id_S]

        ### Valores de voltaje maximo ##
        VPotmaxS = lt["Pmax_S"].loc[Vmax_id_S]
        VIscMaxS = lt["Isc0_S"].loc[Vmax_id_S]
        VVocMaxS = lt["Voc_S"].loc[Vmax_id_S]
        VTpmaxS = lt["T_Sandia"].loc[Vmax_id_S]
        VPoamaxS = lt["Poa_global"].loc[Vmax_id_S]
        VVmS = lt["Vmax_S"].loc[Vmax_id_S]
        VImS = lt["Imax_S"].loc[Vmax_id_S]

        ### VALORES DE CORRIENTE MAXIMO ###
        iPotmaxS = lt["Pmax_S"].loc[Imax_id_S]
        iIscMaxS = lt["Isc0_S"].loc[Imax_id_S]
        iVocMaxS = lt["Voc_S"].loc[Imax_id_S]
        iTpmaxS = lt["T_Sandia"].loc[Imax_id_S]
        iPoamaxS = lt["Poa_global"].loc[Imax_id_S]
        IVmS = lt["Vmax_S"].loc[Imax_id_S]
        IImS = lt["Imax_S"].loc[Imax_id_S]

        #### Valores en Temperatura maxima ####
        TPotmaxS = lt["Pmax_S"].loc[Tmax_id_S]
        TIscMaxS = lt["Isc0_S"].loc[Tmax_id_S]
        TVocMaxS = lt["Voc_S"].loc[Tmax_id_S]
        TTpmaxS = lt["T_Sandia"].loc[Tmax_id_S]
        TPoamaxS = lt["Poa_global"].loc[Tmax_id_S]
        TVmS = lt["Vmax_S"].loc[Tmax_id_S]
        TImS = lt["Imax_S"].loc[Tmax_id_S]

        #### Irradiancia_Efectiva ####
        PPotmaxS = lt["Pmax_S"].loc[Poa_id_S]
        PIscMaxS = lt["Isc0_S"].loc[Poa_id_S]
        PVocMaxS = lt["Voc_S"].loc[Poa_id_S]
        PTpmaxS = lt["T_Sandia"].loc[Poa_id_S]
        PPoamaxS = lt["Poa_global"].loc[Poa_id_S]
        POVmS = lt["Vmax_S"].loc[Poa_id_S]
        POImS = lt["Imax_S"].loc[Poa_id_S]

        ### Diccionario ###

        d = {
            "Geff": [PoamaxS, VPoamaxS, iPoamaxS, TPoamaxS, PPoamaxS],
            "Tcell": [TpmaxS, VTpmaxS, iTpmaxS, TTpmaxS, PTpmaxS],
            "Voltajes": [VocMaxS, VVocMaxS, iVocMaxS, TVocMaxS, PVocMaxS],
            "Corrientes": [IscMaxS, VIscMaxS, iIscMaxS, TIscMaxS, PIscMaxS],
            "Potencia": [PotmaxS, VPotmaxS, iPotmaxS, TPotmaxS, PPotmaxS],
            "Vm": [PVmS, VVmS, IVmS, TVmS, POVmS],
            "Im": [PImS, VImS, IImS, TImS, POImS]
            }

        df = pd.DataFrame(data=d,
                          index=["Potencia Maxima", "Temperatura Minima", "Corriente maxima", "Temperatura maxima",
                                 "Irradiancia maxima"])

        m = df.reset_index()
        m.columns = ["Condiciones", "Geff", "Tcell", "Voc", "Isc", "Potencia", "Vm", "Im"]

        return m

    if Seleccion == [1, 2]:
        #### Aquí es donde se hace la tabla final combinando Feinman y Sandia

        ## Feinman ID
        Potmax_id_F = lt["Pmax_F"].idxmax()  #
        Vmax_id_F = lt["Vmax_F"].idxmax()  #
        Imax_id_F = lt["Imax_F"].idxmax()  #
        Tmax_id_F = lt["T_Feinman"].idxmax()  #
        Poa_id_F = lt["Poa_global"].idxmax()  #

        ## Sandia ID
        Potmax_id_S = lt["Pmax_S"].idxmax()
        Vmax_id_S = lt["Vmax_S"].idxmax()
        Imax_id_S = lt["Imax_S"].idxmax()
        Tmax_id_S = lt["T_Sandia"].idxmax()
        Poa_id_S = lt["Poa_global"].idxmax()

        ### Valores en funcionamiento en potencia maxima ###
        ### Categoria de potencia maxima

        PotmaxF = lt["Pmax_F"].loc[Potmax_id_F]  #
        IscMaxF = lt["Isc0_F"].loc[Potmax_id_F]  #
        VocMaxF = lt["Voc_F"].loc[Potmax_id_F]  #
        TpmaxF = lt["T_Feinman"].loc[Potmax_id_F]  #
        PoamaxF = lt["Poa_global"].loc[Potmax_id_F]  #

        PVm = lt["Vmax_F"].loc[Potmax_id_F]

        PIm = lt["Imax_F"].loc[Potmax_id_F]

        ### Valores de voltaje maximo NO VOC ##

        VPotmaxF = lt["Pmax_F"].loc[Vmax_id_F]  # Potencia.
        VIscMaxF = lt["Isc0_F"].loc[Vmax_id_F]  #
        VVocMaxF = lt["Voc_F"].loc[Vmax_id_F]  #
        VTpmaxF = lt["T_Feinman"].loc[Vmax_id_F]  #
        VPoamaxF = lt["Poa_global"].loc[Vmax_id_F]  # Irradiancia Vmax.
        VVm = lt["Vmax_F"].loc[Vmax_id_F]
        VIm = lt["Imax_F"].loc[Vmax_id_F]

        ### VALORES DE CORRIENTE MAXIMO ###

        iPotmaxF = lt["Pmax_F"].loc[Imax_id_F]  #
        iIscMaxF = lt["Isc0_F"].loc[Imax_id_F]  #
        iVocMaxF = lt["Voc_F"].loc[Imax_id_F]  #
        iTpmaxF = lt["T_Feinman"].loc[Imax_id_F]  #
        iPoamaxF = lt["Poa_global"].loc[Imax_id_F]  #
        IVm = lt["Vmax_F"].loc[Imax_id_F]
        IIm = lt["Imax_F"].loc[Imax_id_F]

        #### Valores en Temperatura maxima ####
        TPotmaxF = lt["Pmax_F"].loc[Tmax_id_F]  #
        TIscMaxF = lt["Isc0_F"].loc[Tmax_id_F]  #
        TVocMaxF = lt["Voc_F"].loc[Tmax_id_F]  #
        TTpmaxF = lt["T_Feinman"].loc[Tmax_id_F]  #
        TPoamaxF = lt["Poa_global"].loc[Tmax_id_F]  #
        TVm = lt["Vmax_F"].loc[Tmax_id_F]
        TIm = lt["Imax_F"].loc[Tmax_id_F]

        #### Irradancia_Efectiva ####
        ####Primer columna ####

        PPotmaxF = lt["Pmax_F"].loc[Poa_id_F]

        PIscMaxF = lt["Isc0_F"].loc[Poa_id_F]

        PVocMaxF = lt["Voc_F"].loc[Poa_id_F]
        PTpmaxF = lt["T_Feinman"].loc[Poa_id_F]
        PPoamaxF = lt["Poa_global"].loc[Poa_id_F]
        POVm = lt["Vmax_F"].loc[Poa_id_F]
        POIm = lt["Imax_F"].loc[Poa_id_F]
        ### Diccionario ###

        # Potencia Maxima **
        # Voltaje maximo**
        # Corriente maxima**
        # Temperatura maxima**
        # Irradiancia maxima**

        ### Valores en funcionamiento en potencia maxima ###
        PotmaxS = lt["Pmax_S"].loc[Potmax_id_S]
        IscMaxS = lt["Isc0_S"].loc[Potmax_id_S]
        VocMaxS = lt["Voc_S"].loc[Potmax_id_S]
        TpmaxS = lt["T_Sandia"].loc[Potmax_id_S]
        PoamaxS = lt["Poa_global"].loc[Potmax_id_S]
        PVmS = lt["Vmax_S"].loc[Potmax_id_S]
        PImS = lt["Imax_S"].loc[Potmax_id_S]

        ### Valores de voltaje maximo ##
        VPotmaxS = lt["Pmax_S"].loc[Vmax_id_S]
        VIscMaxS = lt["Isc0_S"].loc[Vmax_id_S]
        VVocMaxS = lt["Voc_S"].loc[Vmax_id_S]
        VTpmaxS = lt["T_Sandia"].loc[Vmax_id_S]
        VPoamaxS = lt["Poa_global"].loc[Vmax_id_S]
        VVmS = lt["Vmax_S"].loc[Vmax_id_S]
        VImS = lt["Imax_S"].loc[Vmax_id_S]

        ### VALORES DE CORRIENTE MAXIMO ###
        iPotmaxS = lt["Pmax_S"].loc[Imax_id_S]
        iIscMaxS = lt["Isc0_S"].loc[Imax_id_S]
        iVocMaxS = lt["Voc_S"].loc[Imax_id_S]
        iTpmaxS = lt["T_Sandia"].loc[Imax_id_S]
        iPoamaxS = lt["Poa_global"].loc[Imax_id_S]
        IVmS = lt["Vmax_S"].loc[Imax_id_S]
        IImS = lt["Imax_S"].loc[Imax_id_S]

        #### Valores en Temperatura maxima ####
        TPotmaxS = lt["Pmax_S"].loc[Tmax_id_S]
        TIscMaxS = lt["Isc0_S"].loc[Tmax_id_S]
        TVocMaxS = lt["Voc_S"].loc[Tmax_id_S]
        TTpmaxS = lt["T_Sandia"].loc[Tmax_id_S]
        TPoamaxS = lt["Poa_global"].loc[Tmax_id_S]
        TVmS = lt["Vmax_S"].loc[Tmax_id_S]
        TImS = lt["Imax_S"].loc[Tmax_id_S]

        #### Irradiancia_Efectiva ####
        PPotmaxS = lt["Pmax_S"].loc[Poa_id_S]
        PIscMaxS = lt["Isc0_S"].loc[Poa_id_S]
        PVocMaxS = lt["Voc_S"].loc[Poa_id_S]
        PTpmaxS = lt["T_Sandia"].loc[Poa_id_S]
        PPoamaxS = lt["Poa_global"].loc[Poa_id_S]
        POVmS = lt["Vmax_S"].loc[Poa_id_S]
        POImS = lt["Imax_S"].loc[Poa_id_S]

        ### Diccionario ##

        d = {
            "Geff": [PoamaxF, VPoamaxF, TPoamaxF],
            # Orden( Irradiancia de la pot maxima ,Voc,ISC,Temperatura, Irradiancia)
            "Tcell": [TpmaxF, VTpmaxF, TTpmaxF],
            "Voltajes": [VocMaxF, VVocMaxF, TVocMaxF],
            "Corrientes": [IscMaxF, VIscMaxF, TIscMaxF],
            "Potencia": [PotmaxF, VPotmaxF, TPotmaxF],
            "Vm": [PVm, VVm, TVm],
            "Im": [PIm, VIm, TIm]
            }

        d1 = {
            "Geff": [PoamaxS, VPoamaxS, TPoamaxS],
            "Tcell": [TpmaxS, VTpmaxS, TTpmaxS],
            "Voltajes": [VocMaxS, VVocMaxS, TVocMaxS],
            "Corrientes": [IscMaxS, VIscMaxS, TIscMaxS],
            "Potencia": [PotmaxS, VPotmaxS, TPotmaxS],
            "Vm": [PVmS, VVmS, TVmS],
            "Im": [PImS, VImS, TImS]
            }

        # Create DataFrames
        df = pd.DataFrame(data=d, index=["Potencia Maxima Feinman", "Temperatura minima Feinman", "Temperatura maxima Feinman"])
        df2 = pd.DataFrame(data=d1, index=["Potencia Maxima Sandia", "Temperatura minima Sandia ", "Temperatura maxima Sandia"])

        # Concatenate DataFrames
        m = pd.concat([df, df2], axis=0, join="outer").reset_index()

        # Set the correct column names
        m.columns = ["Condiciones", "Geff", "Tcell", "Voc", "Isc", "Potencia", "Vm", "Im"]



        return m

    if Seleccion == [3]:
        #### Aquí es donde se hace la tabla final para Sandia
        ## Estas son fechas
        Potmax_id_NOCT = lt["Pmax_NOCT"].idxmax()
        Vmax_id_NOCT = lt["Vmax_NOCT"].idxmax()
        Imax_id_NOCT = lt["Imax_NOCT"].idxmax()
        Tmax_id_NOCT = lt["T_NOCT"].idxmax()
        Poa_id_NOCT = lt["Poa_global"].idxmax()

        ### Valores en funcionamiento en potencia maxima ###
        PotmaxNOCT = lt["Pmax_NOCT"].loc[Potmax_id_NOCT]
        IscMaxNOCT = lt["Isc0_NOCT"].loc[Potmax_id_NOCT]
        VocMaxNOCT = lt["Voc_NOCT"].loc[Potmax_id_NOCT]
        TpmaxNOCT = lt["T_NOCT"].loc[Potmax_id_NOCT]
        PoamaxNOCT = lt["Poa_global"].loc[Potmax_id_NOCT]
        PVmNOCT = lt["Vmax_NOCT"].loc[Potmax_id_NOCT]
        PImNOCT = lt["Imax_NOCT"].loc[Potmax_id_NOCT]

        ### Valores de voltaje maximo ##
        VPotmaxNOCT = lt["Pmax_NOCT"].loc[Vmax_id_NOCT]
        VIscMaxNOCT = lt["Isc0_NOCT"].loc[Vmax_id_NOCT]
        VVocMaxNOCT = lt["Voc_NOCT"].loc[Vmax_id_NOCT]
        VTpmaxNOCT = lt["T_NOCT"].loc[Vmax_id_NOCT]
        VPoamaxNOCT = lt["Poa_global"].loc[Vmax_id_NOCT]
        VVmNOCT = lt["Vmax_NOCT"].loc[Vmax_id_NOCT]
        VImNOCT = lt["Imax_NOCT"].loc[Vmax_id_NOCT]

        ### VALORES DE CORRIENTE MAXIMO ###
        iPotmaxNOCT = lt["Pmax_NOCT"].loc[Imax_id_NOCT]
        iIscMaxNOCT = lt["Isc0_NOCT"].loc[Imax_id_NOCT]
        iVocMaxNOCT = lt["Voc_NOCT"].loc[Imax_id_NOCT]
        iTpmaxNOCT = lt["T_NOCT"].loc[Imax_id_NOCT]
        iPoamaxNOCT = lt["Poa_global"].loc[Imax_id_NOCT]
        IVmNOCT = lt["Vmax_NOCT"].loc[Imax_id_NOCT]
        IImNOCT = lt["Imax_NOCT"].loc[Imax_id_NOCT]

        #### Valores en Temperatura maxima ####
        TPotmaxNOCT = lt["Pmax_NOCT"].loc[Tmax_id_NOCT]
        TIscMaxNOCT = lt["Isc0_NOCT"].loc[Tmax_id_NOCT]
        TVocMaxNOCT = lt["Voc_NOCT"].loc[Tmax_id_NOCT]
        TTpmaxNOCT = lt["T_NOCT"].loc[Tmax_id_NOCT]
        TPoamaxNOCT = lt["Poa_global"].loc[Tmax_id_NOCT]
        TVmNOCT = lt["Vmax_NOCT"].loc[Tmax_id_NOCT]
        TImNOCT = lt["Imax_NOCT"].loc[Tmax_id_NOCT]

        #### Irradiancia_Efectiva ####
        PPotmaxNOCT = lt["Pmax_NOCT"].loc[Poa_id_NOCT]
        PIscMaxNOCT = lt["Isc0_NOCT"].loc[Poa_id_NOCT]
        PVocMaxNOCT = lt["Voc_NOCT"].loc[Poa_id_NOCT]
        PTpmaxNOCT = lt["T_NOCT"].loc[Poa_id_NOCT]
        PPoamaxNOCT = lt["Poa_global"].loc[Poa_id_NOCT]
        POVmNOCT = lt["Vmax_NOCT"].loc[Poa_id_NOCT]
        POImNOCT = lt["Imax_NOCT"].loc[Poa_id_NOCT]

        ### Diccionario ###

        d = {
            "Geff": [PoamaxNOCT, VPoamaxNOCT, iPoamaxNOCT, TPoamaxNOCT, PPoamaxNOCT],
            "Tcell": [TpmaxNOCT, VTpmaxNOCT, iTpmaxNOCT, TTpmaxNOCT, PTpmaxNOCT],
            "Voltajes": [VocMaxNOCT, VVocMaxNOCT, iVocMaxNOCT, TVocMaxNOCT, PVocMaxNOCT],
            "Corrientes": [IscMaxNOCT, VIscMaxNOCT, iIscMaxNOCT, TIscMaxNOCT, PIscMaxNOCT],
            "Potencia": [PotmaxNOCT, VPotmaxNOCT, iPotmaxNOCT, TPotmaxNOCT, PPotmaxNOCT],
            "Vm": [PVmNOCT, VVmNOCT, IVmNOCT, TVmNOCT, POVmNOCT],
            "Im": [PImNOCT, VImNOCT, IImNOCT, TImNOCT, POImNOCT]
            }

        df = pd.DataFrame(data=d,
                          index=["Potencia Maxima", "Temperatura minima", "Corriente maxima", "Temperatura maxima",
                                 "Irradiancia maxima"])

        m = df.reset_index()
        m.columns = ["Condiciones", "Geff", "Tcell", "Voc", "Isc", "Potencia", "Vm", "Im"]

        return m

    if Seleccion == [1,3]:
        #### Aquí es donde se hace la tabla final para Sandia
        ## Estas son fechas
        Potmax_id_NOCT = lt["Pmax_NOCT"].idxmax()
        Vmax_id_NOCT = lt["Vmax_NOCT"].idxmax()
        Imax_id_NOCT = lt["Imax_NOCT"].idxmax()
        Tmax_id_NOCT = lt["T_NOCT"].idxmax()
        Poa_id_NOCT = lt["Poa_global"].idxmax()

        ### Valores en funcionamiento en potencia maxima ###
        PotmaxNOCT = lt["Pmax_NOCT"].loc[Potmax_id_NOCT]
        IscMaxNOCT = lt["Isc0_NOCT"].loc[Potmax_id_NOCT]
        VocMaxNOCT = lt["Voc_NOCT"].loc[Potmax_id_NOCT]
        TpmaxNOCT = lt["T_NOCT"].loc[Potmax_id_NOCT]
        PoamaxNOCT = lt["Poa_global"].loc[Potmax_id_NOCT]
        PVmNOCT = lt["Vmax_NOCT"].loc[Potmax_id_NOCT]
        PImNOCT = lt["Imax_NOCT"].loc[Potmax_id_NOCT]

        ### Valores de voltaje maximo ##
        VPotmaxNOCT = lt["Pmax_NOCT"].loc[Vmax_id_NOCT]
        VIscMaxNOCT = lt["Isc0_NOCT"].loc[Vmax_id_NOCT]
        VVocMaxNOCT = lt["Voc_NOCT"].loc[Vmax_id_NOCT]
        VTpmaxNOCT = lt["T_NOCT"].loc[Vmax_id_NOCT]
        VPoamaxNOCT = lt["Poa_global"].loc[Vmax_id_NOCT]
        VVmNOCT = lt["Vmax_NOCT"].loc[Vmax_id_NOCT]
        VImNOCT = lt["Imax_NOCT"].loc[Vmax_id_NOCT]

        ### VALORES DE CORRIENTE MAXIMO ###
        iPotmaxNOCT = lt["Pmax_NOCT"].loc[Imax_id_NOCT]
        iIscMaxNOCT = lt["Isc0_NOCT"].loc[Imax_id_NOCT]
        iVocMaxNOCT = lt["Voc_NOCT"].loc[Imax_id_NOCT]
        iTpmaxNOCT = lt["T_NOCT"].loc[Imax_id_NOCT]
        iPoamaxNOCT = lt["Poa_global"].loc[Imax_id_NOCT]
        IVmNOCT = lt["Vmax_NOCT"].loc[Imax_id_NOCT]
        IImNOCT = lt["Imax_NOCT"].loc[Imax_id_NOCT]

        #### Valores en Temperatura maxima ####
        TPotmaxNOCT = lt["Pmax_NOCT"].loc[Tmax_id_NOCT]
        TIscMaxNOCT = lt["Isc0_NOCT"].loc[Tmax_id_NOCT]
        TVocMaxNOCT = lt["Voc_NOCT"].loc[Tmax_id_NOCT]
        TTpmaxNOCT = lt["T_NOCT"].loc[Tmax_id_NOCT]
        TPoamaxNOCT = lt["Poa_global"].loc[Tmax_id_NOCT]
        TVmNOCT = lt["Vmax_NOCT"].loc[Tmax_id_NOCT]
        TImNOCT = lt["Imax_NOCT"].loc[Tmax_id_NOCT]

        #### Irradiancia_Efectiva ####
        PPotmaxNOCT = lt["Pmax_NOCT"].loc[Poa_id_NOCT]
        PIscMaxNOCT = lt["Isc0_NOCT"].loc[Poa_id_NOCT]
        PVocMaxNOCT = lt["Voc_NOCT"].loc[Poa_id_NOCT]
        PTpmaxNOCT = lt["T_NOCT"].loc[Poa_id_NOCT]
        PPoamaxNOCT = lt["Poa_global"].loc[Poa_id_NOCT]
        POVmNOCT = lt["Vmax_NOCT"].loc[Poa_id_NOCT]
        POImNOCT = lt["Imax_NOCT"].loc[Poa_id_NOCT]


        ############### FEINMAN ##############

        ### Valores en funcionamiento en potencia maxima ###
        ### Categoria de potencia maxima

        ## Feinman ID
        Potmax_id_F = lt["Pmax_F"].idxmax()  #
        Vmax_id_F = lt["Vmax_F"].idxmax()  #
        Imax_id_F = lt["Imax_F"].idxmax()  #
        Tmax_id_F = lt["T_Feinman"].idxmax()  #
        Poa_id_F = lt["Poa_global"].idxmax()  #

        PotmaxF = lt["Pmax_F"].loc[Potmax_id_F]  #
        IscMaxF = lt["Isc0_F"].loc[Potmax_id_F]  #
        VocMaxF = lt["Voc_F"].loc[Potmax_id_F]  #
        TpmaxF = lt["T_Feinman"].loc[Potmax_id_F]  #
        PoamaxF = lt["Poa_global"].loc[Potmax_id_F]  #

        PVm = lt["Vmax_F"].loc[Potmax_id_F]

        PIm = lt["Imax_F"].loc[Potmax_id_F]

        ### Valores de voltaje maximo NO VOC ##

        VPotmaxF = lt["Pmax_F"].loc[Vmax_id_F]  # Potencia.
        VIscMaxF = lt["Isc0_F"].loc[Vmax_id_F]  #
        VVocMaxF = lt["Voc_F"].loc[Vmax_id_F]  #
        VTpmaxF = lt["T_Feinman"].loc[Vmax_id_F]  #
        VPoamaxF = lt["Poa_global"].loc[Vmax_id_F]  # Irradiancia Vmax.
        VVm = lt["Vmax_F"].loc[Vmax_id_F]
        VIm = lt["Imax_F"].loc[Vmax_id_F]

        ### VALORES DE CORRIENTE MAXIMO ###

        iPotmaxF = lt["Pmax_F"].loc[Imax_id_F]  #
        iIscMaxF = lt["Isc0_F"].loc[Imax_id_F]  #
        iVocMaxF = lt["Voc_F"].loc[Imax_id_F]  #
        iTpmaxF = lt["T_Feinman"].loc[Imax_id_F]  #
        iPoamaxF = lt["Poa_global"].loc[Imax_id_F]  #
        IVm = lt["Vmax_F"].loc[Imax_id_F]
        IIm = lt["Imax_F"].loc[Imax_id_F]

        #### Valores en Temperatura maxima ####
        TPotmaxF = lt["Pmax_F"].loc[Tmax_id_F]  #
        TIscMaxF = lt["Isc0_F"].loc[Tmax_id_F]  #
        TVocMaxF = lt["Voc_F"].loc[Tmax_id_F]  #
        TTpmaxF = lt["T_Feinman"].loc[Tmax_id_F]  #
        TPoamaxF = lt["Poa_global"].loc[Tmax_id_F]  #
        TVm = lt["Vmax_F"].loc[Tmax_id_F]
        TIm = lt["Imax_F"].loc[Tmax_id_F]

        #### Irradancia_Efectiva ####
        ####Primer columna ####

        PPotmaxF = lt["Pmax_F"].loc[Poa_id_F]

        PIscMaxF = lt["Isc0_F"].loc[Poa_id_F]

        PVocMaxF = lt["Voc_F"].loc[Poa_id_F]
        PTpmaxF = lt["T_Feinman"].loc[Poa_id_F]
        PPoamaxF = lt["Poa_global"].loc[Poa_id_F]
        POVm = lt["Vmax_F"].loc[Poa_id_F]
        POIm = lt["Imax_F"].loc[Poa_id_F]
        ### Diccionario ###

        d = {
            "Geff": [PoamaxNOCT, VPoamaxNOCT, TPoamaxNOCT],
            "Tcell": [TpmaxNOCT, VTpmaxNOCT, TTpmaxNOCT],
            "Voltajes": [VocMaxNOCT, VVocMaxNOCT, TVocMaxNOCT],
            "Corrientes": [IscMaxNOCT, VIscMaxNOCT, TIscMaxNOCT],
            "Potencia": [PotmaxNOCT, VPotmaxNOCT, TPotmaxNOCT],
            "Vm": [PVmNOCT, VVmNOCT,  TVmNOCT],
            "Im": [PImNOCT, VImNOCT, TImNOCT]
            }

        d1 = {
            "Geff": [PoamaxF, VPoamaxF, TPoamaxF],
            # Orden( Irradiancia de la pot maxima ,Voc,ISC,Temperatura, Irradiancia)
            "Tcell": [TpmaxF, VTpmaxF, TTpmaxF],
            "Voltajes": [VocMaxF, VVocMaxF, TVocMaxF],
            "Corrientes": [IscMaxF, VIscMaxF, TIscMaxF],
            "Potencia": [PotmaxF, VPotmaxF, TPotmaxF],
            "Vm": [PVm, VVm, TVm],
            "Im": [PIm, VIm, TIm]
        }

        # Create DataFrames
        df = pd.DataFrame(data=d, index=["Potencia Maxima NOCT", "Temperatura minima NOCT", "Temperatura maxima NOCT"])
        df2 = pd.DataFrame(data=d1, index=["Potencia Maxima Feinman", "Temperatura minima Feinman", "Temperatura maxima Feinman"])

        # Concatenate DataFrames
        m = pd.concat([df, df2], axis=0, join="outer").reset_index()

        # Set the correct column names
        m.columns = ["Condiciones", "Geff", "Tcell", "Voc", "Isc", "Potencia", "Vm", "Im"]

        return m

    if Seleccion == [1,2,3]:
        #### Aquí es donde se hace la tabla final para Sandia
        ## Estas son fechas
        ## NOCT ID ###
        Potmax_id_NOCT = lt["Pmax_NOCT"].idxmax()
        Vmax_id_NOCT = lt["Vmax_NOCT"].idxmax()
        Imax_id_NOCT = lt["Imax_NOCT"].idxmax()
        Tmax_id_NOCT = lt["T_NOCT"].idxmax()
        Poa_id_NOCT = lt["Poa_global"].idxmax()

        ### Valores en funcionamiento en potencia maxima ###
        PotmaxNOCT = lt["Pmax_NOCT"].loc[Potmax_id_NOCT]
        IscMaxNOCT = lt["Isc0_NOCT"].loc[Potmax_id_NOCT]
        VocMaxNOCT = lt["Voc_NOCT"].loc[Potmax_id_NOCT]
        TpmaxNOCT = lt["T_NOCT"].loc[Potmax_id_NOCT]
        PoamaxNOCT = lt["Poa_global"].loc[Potmax_id_NOCT]
        PVmNOCT = lt["Vmax_NOCT"].loc[Potmax_id_NOCT]
        PImNOCT = lt["Imax_NOCT"].loc[Potmax_id_NOCT]

        ### Valores de voltaje maximo ##
        VPotmaxNOCT = lt["Pmax_NOCT"].loc[Vmax_id_NOCT]
        VIscMaxNOCT = lt["Isc0_NOCT"].loc[Vmax_id_NOCT]
        VVocMaxNOCT = lt["Voc_NOCT"].loc[Vmax_id_NOCT]
        VTpmaxNOCT = lt["T_NOCT"].loc[Vmax_id_NOCT]
        VPoamaxNOCT = lt["Poa_global"].loc[Vmax_id_NOCT]
        VVmNOCT = lt["Vmax_NOCT"].loc[Vmax_id_NOCT]
        VImNOCT = lt["Imax_NOCT"].loc[Vmax_id_NOCT]

        ### VALORES DE CORRIENTE MAXIMO ###
        iPotmaxNOCT = lt["Pmax_NOCT"].loc[Imax_id_NOCT]
        iIscMaxNOCT = lt["Isc0_NOCT"].loc[Imax_id_NOCT]
        iVocMaxNOCT = lt["Voc_NOCT"].loc[Imax_id_NOCT]
        iTpmaxNOCT = lt["T_NOCT"].loc[Imax_id_NOCT]
        iPoamaxNOCT = lt["Poa_global"].loc[Imax_id_NOCT]
        IVmNOCT = lt["Vmax_NOCT"].loc[Imax_id_NOCT]
        IImNOCT = lt["Imax_NOCT"].loc[Imax_id_NOCT]

        #### Valores en Temperatura maxima ####
        TPotmaxNOCT = lt["Pmax_NOCT"].loc[Tmax_id_NOCT]
        TIscMaxNOCT = lt["Isc0_NOCT"].loc[Tmax_id_NOCT]
        TVocMaxNOCT = lt["Voc_NOCT"].loc[Tmax_id_NOCT]
        TTpmaxNOCT = lt["T_NOCT"].loc[Tmax_id_NOCT]
        TPoamaxNOCT = lt["Poa_global"].loc[Tmax_id_NOCT]
        TVmNOCT = lt["Vmax_NOCT"].loc[Tmax_id_NOCT]
        TImNOCT = lt["Imax_NOCT"].loc[Tmax_id_NOCT]

        #### Irradiancia_Efectiva ####
        PPotmaxNOCT = lt["Pmax_NOCT"].loc[Poa_id_NOCT]
        PIscMaxNOCT = lt["Isc0_NOCT"].loc[Poa_id_NOCT]
        PVocMaxNOCT = lt["Voc_NOCT"].loc[Poa_id_NOCT]
        PTpmaxNOCT = lt["T_NOCT"].loc[Poa_id_NOCT]
        PPoamaxNOCT = lt["Poa_global"].loc[Poa_id_NOCT]
        POVmNOCT = lt["Vmax_NOCT"].loc[Poa_id_NOCT]
        POImNOCT = lt["Imax_NOCT"].loc[Poa_id_NOCT]


        ############### SANDIA ##############

        ### Valores en funcionamiento en potencia maxima ###
        ### Categoria de potencia maxima

        ## Sandia ID
        Potmax_id_S = lt["Pmax_S"].idxmax()
        Vmax_id_S = lt["Vmax_S"].idxmax()
        Imax_id_S = lt["Imax_S"].idxmax()
        Tmax_id_S = lt["T_Sandia"].idxmax()
        Poa_id_S = lt["Poa_global"].idxmax()

        ## Feinman ID
        ### Valores en funcionamiento en potencia maxima ###
        PotmaxS = lt["Pmax_S"].loc[Potmax_id_S]
        IscMaxS = lt["Isc0_S"].loc[Potmax_id_S]
        VocMaxS = lt["Voc_S"].loc[Potmax_id_S]
        TpmaxS = lt["T_Sandia"].loc[Potmax_id_S]
        PoamaxS = lt["Poa_global"].loc[Potmax_id_S]
        PVmS = lt["Vmax_S"].loc[Potmax_id_S]
        PImS = lt["Imax_S"].loc[Potmax_id_S]

        ### Valores de voltaje maximo ##
        VPotmaxS = lt["Pmax_S"].loc[Vmax_id_S]
        VIscMaxS = lt["Isc0_S"].loc[Vmax_id_S]
        VVocMaxS = lt["Voc_S"].loc[Vmax_id_S]
        VTpmaxS = lt["T_Sandia"].loc[Vmax_id_S]
        VPoamaxS = lt["Poa_global"].loc[Vmax_id_S]
        VVmS = lt["Vmax_S"].loc[Vmax_id_S]
        VImS = lt["Imax_S"].loc[Vmax_id_S]

        ### VALORES DE CORRIENTE MAXIMO ###
        iPotmaxS = lt["Pmax_S"].loc[Imax_id_S]
        iIscMaxS = lt["Isc0_S"].loc[Imax_id_S]
        iVocMaxS = lt["Voc_S"].loc[Imax_id_S]
        iTpmaxS = lt["T_Sandia"].loc[Imax_id_S]
        iPoamaxS = lt["Poa_global"].loc[Imax_id_S]
        IVmS = lt["Vmax_S"].loc[Imax_id_S]
        IImS = lt["Imax_S"].loc[Imax_id_S]

        #### Valores en Temperatura maxima ####
        TPotmaxS = lt["Pmax_S"].loc[Tmax_id_S]
        TIscMaxS = lt["Isc0_S"].loc[Tmax_id_S]
        TVocMaxS = lt["Voc_S"].loc[Tmax_id_S]
        TTpmaxS = lt["T_Sandia"].loc[Tmax_id_S]
        TPoamaxS = lt["Poa_global"].loc[Tmax_id_S]
        TVmS = lt["Vmax_S"].loc[Tmax_id_S]
        TImS = lt["Imax_S"].loc[Tmax_id_S]

        #### Irradiancia_Efectiva ####
        PPotmaxS = lt["Pmax_S"].loc[Poa_id_S]
        PIscMaxS = lt["Isc0_S"].loc[Poa_id_S]
        PVocMaxS = lt["Voc_S"].loc[Poa_id_S]
        PTpmaxS = lt["T_Sandia"].loc[Poa_id_S]
        PPoamaxS = lt["Poa_global"].loc[Poa_id_S]
        POVmS = lt["Vmax_S"].loc[Poa_id_S]
        POImS = lt["Imax_S"].loc[Poa_id_S]


        ##### Feinman ##########
        ############### FEINMAN ##############

        ### Valores en funcionamiento en potencia maxima ###
        ### Categoria de potencia maxima

        ## Feinman ID
        Potmax_id_F = lt["Pmax_F"].idxmax()  #
        Vmax_id_F = lt["Vmax_F"].idxmax()  #
        Imax_id_F = lt["Imax_F"].idxmax()  #
        Tmax_id_F = lt["T_Feinman"].idxmax()  #
        Poa_id_F = lt["Poa_global"].idxmax()  #

        PotmaxF = lt["Pmax_F"].loc[Potmax_id_F]  #
        IscMaxF = lt["Isc0_F"].loc[Potmax_id_F]  #
        VocMaxF = lt["Voc_F"].loc[Potmax_id_F]  #
        TpmaxF = lt["T_Feinman"].loc[Potmax_id_F]  #
        PoamaxF = lt["Poa_global"].loc[Potmax_id_F]  #

        PVm = lt["Vmax_F"].loc[Potmax_id_F]

        PIm = lt["Imax_F"].loc[Potmax_id_F]

        ### Valores de voltaje maximo NO VOC ##

        VPotmaxF = lt["Pmax_F"].loc[Vmax_id_F]  # Potencia.
        VIscMaxF = lt["Isc0_F"].loc[Vmax_id_F]  #
        VVocMaxF = lt["Voc_F"].loc[Vmax_id_F]  #
        VTpmaxF = lt["T_Feinman"].loc[Vmax_id_F]  #
        VPoamaxF = lt["Poa_global"].loc[Vmax_id_F]  # Irradiancia Vmax.
        VVm = lt["Vmax_F"].loc[Vmax_id_F]
        VIm = lt["Imax_F"].loc[Vmax_id_F]

        ### VALORES DE CORRIENTE MAXIMO ###

        iPotmaxF = lt["Pmax_F"].loc[Imax_id_F]  #
        iIscMaxF = lt["Isc0_F"].loc[Imax_id_F]  #
        iVocMaxF = lt["Voc_F"].loc[Imax_id_F]  #
        iTpmaxF = lt["T_Feinman"].loc[Imax_id_F]  #
        iPoamaxF = lt["Poa_global"].loc[Imax_id_F]  #
        IVm = lt["Vmax_F"].loc[Imax_id_F]
        IIm = lt["Imax_F"].loc[Imax_id_F]

        #### Valores en Temperatura maxima ####
        TPotmaxF = lt["Pmax_F"].loc[Tmax_id_F]  #
        TIscMaxF = lt["Isc0_F"].loc[Tmax_id_F]  #
        TVocMaxF = lt["Voc_F"].loc[Tmax_id_F]  #
        TTpmaxF = lt["T_Feinman"].loc[Tmax_id_F]  #
        TPoamaxF = lt["Poa_global"].loc[Tmax_id_F]  #
        TVm = lt["Vmax_F"].loc[Tmax_id_F]
        TIm = lt["Imax_F"].loc[Tmax_id_F]

        #### Irradancia_Efectiva ####
        ####Primer columna ####

        PPotmaxF = lt["Pmax_F"].loc[Poa_id_F]

        PIscMaxF = lt["Isc0_F"].loc[Poa_id_F]

        PVocMaxF = lt["Voc_F"].loc[Poa_id_F]
        PTpmaxF = lt["T_Feinman"].loc[Poa_id_F]
        PPoamaxF = lt["Poa_global"].loc[Poa_id_F]
        POVm = lt["Vmax_F"].loc[Poa_id_F]
        POIm = lt["Imax_F"].loc[Poa_id_F]
        ### Diccionario ###

        ### Diccionario ###

        d = {
            "Geff": [PoamaxNOCT, VPoamaxNOCT, TPoamaxNOCT],
            "Tcell": [TpmaxNOCT, VTpmaxNOCT, TTpmaxNOCT],
            "Voltajes": [VocMaxNOCT, VVocMaxNOCT, TVocMaxNOCT],
            "Corrientes": [IscMaxNOCT, VIscMaxNOCT, TIscMaxNOCT],
            "Potencia": [PotmaxNOCT, VPotmaxNOCT, TPotmaxNOCT],
            "Vm": [PVmNOCT, VVmNOCT,  TVmNOCT],
            "Im": [PImNOCT, VImNOCT, TImNOCT]
            }

        d1 = {
            "Geff": [PoamaxS, VPoamaxS, TPoamaxS],
            "Tcell": [TpmaxS, VTpmaxS, TTpmaxS],
            "Voltajes": [VocMaxS, VVocMaxS, TVocMaxS],
            "Corrientes": [IscMaxS, VIscMaxS, TIscMaxS],
            "Potencia": [PotmaxS, VPotmaxS, TPotmaxS],
            "Vm": [PVmS, VVmS, TVmS],
            "Im": [PImS, VImS, TImS]
        }

        d2 = {
            "Geff": [PoamaxF, VPoamaxF, TPoamaxF],
            # Orden( Irradiancia de la pot maxima ,Voc,ISC,Temperatura, Irradiancia)
            "Tcell": [TpmaxF, VTpmaxF, TTpmaxF],
            "Voltajes": [VocMaxF, VVocMaxF, TVocMaxF],
            "Corrientes": [IscMaxF, VIscMaxF, TIscMaxF],
            "Potencia": [PotmaxF, VPotmaxF, TPotmaxF],
            "Vm": [PVm, VVm, TVm],
            "Im": [PIm, VIm, TIm]
        }

        # Create DataFrames
        df = pd.DataFrame(data=d, index=["Potencia Maxima NOCT", "Temperatura minima NOCT", "Temperatura maxima NOCT"])
        df2 = pd.DataFrame(data=d1, index=["Potencia Maxima Sandia", "Temperatura minima Sandia", "Temperatura maxima Sandia"])
        df3=pd.DataFrame(data=d2, index=["Potencia Maxima Feinman", "Temperatura minima Feinman", "Temperatura maxima Feinman"])

        # Concatenate DataFrames
        m = pd.concat([df, df2,df3], axis=0, join="outer").reset_index()

        # Set the correct column names
        m.columns = ["Condiciones", "Geff", "Tcell", "Voc", "Isc", "Potencia", "Vm", "Im"]

        return m

    if Seleccion == [2,3]:
        #### Aquí es donde se hace la tabla final para Sandia
        ## Estas son fechas
        Potmax_id_NOCT = lt["Pmax_NOCT"].idxmax()
        Vmax_id_NOCT = lt["Vmax_NOCT"].idxmax()
        Imax_id_NOCT = lt["Imax_NOCT"].idxmax()
        Tmax_id_NOCT = lt["T_NOCT"].idxmax()
        Poa_id_NOCT = lt["Poa_global"].idxmax()

        ### Valores en funcionamiento en potencia maxima ###
        PotmaxNOCT = lt["Pmax_NOCT"].loc[Potmax_id_NOCT]
        IscMaxNOCT = lt["Isc0_NOCT"].loc[Potmax_id_NOCT]
        VocMaxNOCT = lt["Voc_NOCT"].loc[Potmax_id_NOCT]
        TpmaxNOCT = lt["T_NOCT"].loc[Potmax_id_NOCT]
        PoamaxNOCT = lt["Poa_global"].loc[Potmax_id_NOCT]
        PVmNOCT = lt["Vmax_NOCT"].loc[Potmax_id_NOCT]
        PImNOCT = lt["Imax_NOCT"].loc[Potmax_id_NOCT]

        ### Valores de voltaje maximo ##
        VPotmaxNOCT = lt["Pmax_NOCT"].loc[Vmax_id_NOCT]
        VIscMaxNOCT = lt["Isc0_NOCT"].loc[Vmax_id_NOCT]
        VVocMaxNOCT = lt["Voc_NOCT"].loc[Vmax_id_NOCT]
        VTpmaxNOCT = lt["T_NOCT"].loc[Vmax_id_NOCT]
        VPoamaxNOCT = lt["Poa_global"].loc[Vmax_id_NOCT]
        VVmNOCT = lt["Vmax_NOCT"].loc[Vmax_id_NOCT]
        VImNOCT = lt["Imax_NOCT"].loc[Vmax_id_NOCT]

        ### VALORES DE CORRIENTE MAXIMO ###
        iPotmaxNOCT = lt["Pmax_NOCT"].loc[Imax_id_NOCT]
        iIscMaxNOCT = lt["Isc0_NOCT"].loc[Imax_id_NOCT]
        iVocMaxNOCT = lt["Voc_NOCT"].loc[Imax_id_NOCT]
        iTpmaxNOCT = lt["T_NOCT"].loc[Imax_id_NOCT]
        iPoamaxNOCT = lt["Poa_global"].loc[Imax_id_NOCT]
        IVmNOCT = lt["Vmax_NOCT"].loc[Imax_id_NOCT]
        IImNOCT = lt["Imax_NOCT"].loc[Imax_id_NOCT]

        #### Valores en Temperatura maxima ####
        TPotmaxNOCT = lt["Pmax_NOCT"].loc[Tmax_id_NOCT]
        TIscMaxNOCT = lt["Isc0_NOCT"].loc[Tmax_id_NOCT]
        TVocMaxNOCT = lt["Voc_NOCT"].loc[Tmax_id_NOCT]
        TTpmaxNOCT = lt["T_NOCT"].loc[Tmax_id_NOCT]
        TPoamaxNOCT = lt["Poa_global"].loc[Tmax_id_NOCT]
        TVmNOCT = lt["Vmax_NOCT"].loc[Tmax_id_NOCT]
        TImNOCT = lt["Imax_NOCT"].loc[Tmax_id_NOCT]

        #### Irradiancia_Efectiva ####
        PPotmaxNOCT = lt["Pmax_NOCT"].loc[Poa_id_NOCT]
        PIscMaxNOCT = lt["Isc0_NOCT"].loc[Poa_id_NOCT]
        PVocMaxNOCT = lt["Voc_NOCT"].loc[Poa_id_NOCT]
        PTpmaxNOCT = lt["T_NOCT"].loc[Poa_id_NOCT]
        PPoamaxNOCT = lt["Poa_global"].loc[Poa_id_NOCT]
        POVmNOCT = lt["Vmax_NOCT"].loc[Poa_id_NOCT]
        POImNOCT = lt["Imax_NOCT"].loc[Poa_id_NOCT]


        ############### SANDIA ##############

        ### Valores en funcionamiento en potencia maxima ###
        ### Categoria de potencia maxima

        ## Sandia ID
        Potmax_id_S = lt["Pmax_S"].idxmax()
        Vmax_id_S = lt["Vmax_S"].idxmax()
        Imax_id_S = lt["Imax_S"].idxmax()
        Tmax_id_S = lt["T_Sandia"].idxmax()
        Poa_id_S = lt["Poa_global"].idxmax()

        ## Feinman ID
        ### Valores en funcionamiento en potencia maxima ###
        PotmaxS = lt["Pmax_S"].loc[Potmax_id_S]
        IscMaxS = lt["Isc0_S"].loc[Potmax_id_S]
        VocMaxS = lt["Voc_S"].loc[Potmax_id_S]
        TpmaxS = lt["T_Sandia"].loc[Potmax_id_S]
        PoamaxS = lt["Poa_global"].loc[Potmax_id_S]
        PVmS = lt["Vmax_S"].loc[Potmax_id_S]
        PImS = lt["Imax_S"].loc[Potmax_id_S]

        ### Valores de voltaje maximo ##
        VPotmaxS = lt["Pmax_S"].loc[Vmax_id_S]
        VIscMaxS = lt["Isc0_S"].loc[Vmax_id_S]
        VVocMaxS = lt["Voc_S"].loc[Vmax_id_S]
        VTpmaxS = lt["T_Sandia"].loc[Vmax_id_S]
        VPoamaxS = lt["Poa_global"].loc[Vmax_id_S]
        VVmS = lt["Vmax_S"].loc[Vmax_id_S]
        VImS = lt["Imax_S"].loc[Vmax_id_S]

        ### VALORES DE CORRIENTE MAXIMO ###
        iPotmaxS = lt["Pmax_S"].loc[Imax_id_S]
        iIscMaxS = lt["Isc0_S"].loc[Imax_id_S]
        iVocMaxS = lt["Voc_S"].loc[Imax_id_S]
        iTpmaxS = lt["T_Sandia"].loc[Imax_id_S]
        iPoamaxS = lt["Poa_global"].loc[Imax_id_S]
        IVmS = lt["Vmax_S"].loc[Imax_id_S]
        IImS = lt["Imax_S"].loc[Imax_id_S]

        #### Valores en Temperatura maxima ####
        TPotmaxS = lt["Pmax_S"].loc[Tmax_id_S]
        TIscMaxS = lt["Isc0_S"].loc[Tmax_id_S]
        TVocMaxS = lt["Voc_S"].loc[Tmax_id_S]
        TTpmaxS = lt["T_Sandia"].loc[Tmax_id_S]
        TPoamaxS = lt["Poa_global"].loc[Tmax_id_S]
        TVmS = lt["Vmax_S"].loc[Tmax_id_S]
        TImS = lt["Imax_S"].loc[Tmax_id_S]

        #### Irradiancia_Efectiva ####
        PPotmaxS = lt["Pmax_S"].loc[Poa_id_S]
        PIscMaxS = lt["Isc0_S"].loc[Poa_id_S]
        PVocMaxS = lt["Voc_S"].loc[Poa_id_S]
        PTpmaxS = lt["T_Sandia"].loc[Poa_id_S]
        PPoamaxS = lt["Poa_global"].loc[Poa_id_S]
        POVmS = lt["Vmax_S"].loc[Poa_id_S]
        POImS = lt["Imax_S"].loc[Poa_id_S]

        ### Diccionario ###

        d = {
            "Geff": [PoamaxNOCT, VPoamaxNOCT, TPoamaxNOCT],
            "Tcell": [TpmaxNOCT, VTpmaxNOCT, TTpmaxNOCT],
            "Voltajes": [VocMaxNOCT, VVocMaxNOCT, TVocMaxNOCT],
            "Corrientes": [IscMaxNOCT, VIscMaxNOCT, TIscMaxNOCT],
            "Potencia": [PotmaxNOCT, VPotmaxNOCT, TPotmaxNOCT],
            "Vm": [PVmNOCT, VVmNOCT,  TVmNOCT],
            "Im": [PImNOCT, VImNOCT, TImNOCT]
            }

        d1 = {
            "Geff": [PoamaxS, VPoamaxS, TPoamaxS],
            "Tcell": [TpmaxS, VTpmaxS, TTpmaxS],
            "Voltajes": [VocMaxS, VVocMaxS, TVocMaxS],
            "Corrientes": [IscMaxS, VIscMaxS, TIscMaxS],
            "Potencia": [PotmaxS, VPotmaxS, TPotmaxS],
            "Vm": [PVmS, VVmS, TVmS],
            "Im": [PImS, VImS, TImS]
        }

        # Create DataFrames
        df = pd.DataFrame(data=d, index=["Potencia Maxima NOCT", "Temperatura minima NOCT", "Temperatura maxima NOCT"])
        df2 = pd.DataFrame(data=d1, index=["Potencia Maxima Sandia", "Temperatura minima Sandia", "Temperatura maxima Sandia"])

        # Concatenate DataFrames
        m = pd.concat([df, df2], axis=0, join="outer").reset_index()

        # Set the correct column names
        m.columns = ["Condiciones", "Geff", "Tcell", "Voc", "Isc", "Potencia", "Vm", "Im"]

        return m


### Este analisis es para la parte de la comparacion de datos, con archivos subidos.
def IV_CI(Placa, df, io, to,m,Seleccion):

    valores = [valor for parametro, valor in Placa.items()]

    # Calculate parameters using pvlib's function
    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=float(valores[7]),
        cells_in_series=float(valores[8]),
        temp_ref=25
    )

    # Initialize the figure for plotting
    fig = go.Figure()


    i_sc = []
    v_oc = []
    i_mpi = []
    v_mpv = []
    p_mp = []

    # Dictionaries for effective irradiance and cell temperature
    d = {
        'Geff': [io],
        'Tcell': [to]
        }



    # Create DataFrame with conditions
    conditions = pd.DataFrame(data=d)

    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=Placa["alpha"],
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)

        fig.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f"Temp:{case['Tcell']:.2f}, Irr: {case['Geff']:.2f}"))
        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']
        fig.add_trace(go.Scatter(
            x=[v_mp],
            y=[i_mp],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp medido",
            customdata=[v_mp * i_mp]
        ))

        i_sc.append(curve_info['i_sc'])
        v_oc.append(curve_info['v_oc'])
        i_mpi.append(curve_info['i_mp'])
        v_mpv.append(curve_info['v_mp'])
        p_mp.append(curve_info['p_mp'])



        fig.update_layout(
            title="Curva IV Comparaciones",
            xaxis_title="Module voltage [V]",
            yaxis_title="Module current [A]",
            legend_title="Conditions"
        )

    lenght = len(pd.read_excel("Uploaded_.xlsx", sheet_name="Info"))

    Isc=[]
    Voc=[]
    Imp=[]
    Vmp=[]
    Pmp=[]
    Cond=[]

    for i in range(lenght):
        # Prepare the measured data
        m=pd.read_excel("Uploaded_.xlsx", sheet_name=i)
        m.columns = ["V", "I", "P"]
        id_max = m['P'].idxmax()
        ppm = m["P"].loc[id_max]



        fig.add_trace(go.Scatter(x=m.V, y=m.I, mode='lines', name=f"Caso medido"))

        v_mpm = m["V"].loc[id_max]
        i_mpm = m["I"].loc[id_max]
        p_mpm = m["P"].loc[id_max]
        MISC = m.I[0]
        MVOC = m.V[len(m) - 1]
        nombre= f"IV{i+1}"

        Isc.append(m.I.max())
        Voc.append(m.V.max())
        Imp.append(i_mpm)
        Vmp.append(v_mpm)
        Pmp.append(ppm)
        Cond.append(nombre)


        fig.add_trace(go.Scatter(
            x=[v_mpm],
            y=[i_mpm],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp measured",
            customdata=[v_mpm * i_mpm]
        ))



    data_frame = pd.DataFrame(
        data={"Condicion": Cond,
              "ISC":Isc,
              "VOC":Voc,
              "IMP":Imp,
              "VMP":Vmp,
              "PMP":Pmp})

    fig.update_layout(
        title="Curva IV",
        xaxis_title="Module voltage [V]",
        yaxis_title="Module current [A]",
        legend_title="Condiciones",
        xaxis_tickangle=30,
        xaxis_tickfont=dict(size=10),
        yaxis_tickfont=dict(size=10),
        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
        font=dict(color='white')
                    )

    return fig,data_frame.round(2)


def IV_sim(Placa, Gmed, Tmod, df):
    valores = [valor for parametro, valor in Placa.items()]

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=float(valores[7]),
        cells_in_series=float(valores[8]),
        temp_ref=float(valores[9])
    )

    IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
        effective_irradiance=Gmed,
        temp_cell=Tmod,
        alpha_sc=(Placa["alpha"] / 100) * float(valores[4]),
        a_ref=parameters[4],
        I_L_ref=parameters[0],
        I_o_ref=parameters[1],
        R_sh_ref=parameters[3],
        R_s=parameters[2],
        EgRef=1.121,
        dEgdT=-0.0002677
    )

    SDE_params = {
        'photocurrent': IL,
        'saturation_current': I0,
        'resistance_series': Rs,
        'resistance_shunt': Rsh,
        'nNsVth': nNsVth
    }

    curve_info = pvlib.pvsystem.singlediode(method="lambertw", **SDE_params)
    v = np.linspace(0., curve_info["v_oc"], len(df))
    df["V_sim"] = np.linspace(0., curve_info["v_oc"], len(df))
    i = pvlib.pvsystem.i_from_v(voltage=v, method="lambertw", **SDE_params)
    df["I_sim"] = pvlib.pvsystem.i_from_v(voltage=v, method="lambertw", **SDE_params)
    df["P_sim"] = v * i

    return []


### Este analisis es para la parte de la comparacion de datos, con archivos subidos.
def IV_CI_cor(Placa,io, to):
    fig1 = go.Figure()
    fig2 = go.Figure()
    valores = [valor for parametro, valor in Placa.items()]

    # Calculate parameters using pvlib's function
    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=float(valores[7]),
        cells_in_series=float(valores[8]),
        temp_ref=25
    )

    d = {
        'Geff': [io],
        'Tcell': [to]
    }

    # Create DataFrame with conditions
    conditions = pd.DataFrame(data=d)

    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=Placa["alpha"],
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)

        fig2.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f"Temp:{case['Tcell']:.2f}, Irr: {case['Geff']:.2f}"))
        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']
        fig2.add_trace(go.Scatter(
            x=[v_mp],
            y=[i_mp],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp medido",
            customdata=[v_mp * i_mp]
        ))

    ds = pd.read_excel("Uploaded_.xlsx", sheet_name="Info")

    lenght = len(ds)
    Irradiancia = []
    Temperatura = []
    Voltaje = []
    Corriente = []
    Potencia = []
    Error_Pot = []
    Error_Corriente = []
    Error_Voltaje = []
    ##Simulados
    Irradiancia_s = []
    Temperatura_s = []
    Voltaje_s = []
    Corriente_s = []
    Potencia_s = []
    Error_Pot_s = []
    Error_Corriente_s = []
    Error_Voltaje_s = []
    # tablas
    Nombres = []
    Tabla_corregidosm = {}
    Tabla_simuladas = {}


    for i in range(lenght):
        df = pd.read_excel("Uploaded_.xlsx", sheet_name=i)
        Voc_med = (ds.iloc[i]["Voc"])
        Gmed = (ds.iloc[i]["Irrad1"])
        T1 = (ds.iloc[i]["Temp1"])
        T2 = (ds.iloc[i]["Temp2"])

        Tmod = 25 + ((1 / (Placa['beta'] / 100)) * (
                    (Voc_med / Placa["Voc"]) - 1 - ((Placa['deltha'] / 100) * np.log(Gmed / 1000))))
        correction_IV(df, Placa['cell_type'], Placa["Vmax60"], Placa["Imax"], Placa["Voc"], Placa["Isc"],
                            Placa["Pmax"],
                            Placa['alpha'], Placa['beta'], Placa['deltha'], Placa['cells_in_series'], Tmod, Gmed,
                            Voc_med)
        IV_sim(Placa, Gmed, Tmod, df)
        dt = pd.DataFrame({"Volts": df["V_sim"], "Amps": df["I_sim"], "Watts": df["P_sim"]})
        correction_IV_s(dt, Placa['cell_type'], Placa["Vmax60"], Placa["Imax"], Placa["Voc"], Placa["Isc"],
                              Placa["Pmax"],
                              Placa['alpha'], Placa['beta'], Placa['deltha'], Placa['cells_in_series'], Tmod, Gmed,
                              Voc_med)

        # la siguiente funcion obtiene las curvas, bajo la misma
        # tabla.append([Gmed,(T1,T2),df.V3.max(),df.I3.max(),df.P3.max(),(abs((250-df.P3.max())/250*100)),abs(abs((250-df.P3.max())/250*100)),abs(( 37.85-df.V3.max())/ 37.85*100)])

        # Agregar valores a las listas

        # Datos de medicion:
        Irradiancia.append(Gmed)
        Temperatura.append((T1 + T2) / 2)
        Voltaje.append(df['V3'].max())
        Corriente.append(minimos(df, Placa["Isc"]))
        Potencia.append(df['P3'].max())
        Error_Pot.append(abs((Placa["Pmax"] - df.P3.max()) / Placa["Pmax"] * 100))
        Error_Corriente.append(abs((Placa["Isc"] - minimos(df, Placa["Isc"])) / Placa["Isc"] * 100))
        Error_Voltaje.append(abs((Placa["Voc"] - df.V3.max()) / Placa["Voc"] * 100))

        # Datos de simulacion:

        Irradiancia_s.append(Gmed)
        Temperatura_s.append((T1 + T2) / 2)
        Voltaje_s.append(dt['V3_s'].max())
        Corriente_s.append(minimos_s(dt, Placa["Isc"]))
        Potencia_s.append(dt['P3_s'].max())
        Error_Pot_s.append(abs((Placa["Pmax"] - dt.P3_s.max()) / Placa["Pmax"] * 100))
        Error_Corriente_s.append(abs((Placa["Isc"] - minimos_s(dt, Placa["Isc"])) / Placa["Isc"] * 100))
        Error_Voltaje_s.append(abs((Placa["Voc"] - dt.V3_s.max()) / Placa["Voc"] * 100))

        nombre = f"Df{i + 1}"
        Nombres.append(nombre)
        Tabla_corregidosm[nombre] = df.V3, df.I3, df.P3
        Tabla_simuladas[nombre] = df["V_sim"], df["I_sim"], df["P_sim"]
        df["V3"] = pd.concat([pd.Series(data=[0]), df.V3]).reset_index(drop=True)
        df["I3"] = pd.concat([pd.Series(data=[minimos_s(dt, Placa["Isc"])]), df.I3]).reset_index(drop=True)
        df["P3"] = pd.concat([pd.Series(data=[0]), df.P3]).reset_index(drop=True)

        # Crear el diccionario 'Tabla' después del bucle
        Tabla = pd.DataFrame({
            "Irradiancia_m": Irradiancia,
            "Temperatura_m": Temperatura,
            "VOC": Voltaje,
            "ISC": Corriente,
            "Potencia": Potencia,
            "Error % Voc": Error_Voltaje,
            "Error % Isc": Error_Corriente,
            "Error % Pot": Error_Pot
        })

        Tabla_s = pd.DataFrame({
            "Irradiancia_m": Irradiancia_s,
            "Temperatura_m": Temperatura_s,
            "VOC_s": Voltaje_s,
            "ISC_s": Corriente_s,
            "Potencia_s": Potencia_s,
            "Error % Voc_s": Error_Voltaje_s,
            "Error % Isc_s": Error_Corriente_s,
            "Error % Pot_s": Error_Pot_s
        })

        id_max = df['P3'].idxmax()
        v_mpm = df["V3"].loc[id_max]
        i_mpm = df["I3"].loc[id_max]

        #  va la figura de los datos corregidos
        fig2.add_trace(go.Scatter(x=df.V3, y=df.I3, mode='lines', name=f"Voc:{Voc_med:.2f}, Irr: {Gmed:.2f}"))


        fig2.add_trace(go.Scatter(
            x=[v_mpm],
            y=[i_mpm],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp measured",
            customdata=[v_mpm * i_mpm]
        ))


        fig2.update_layout(
            title='Correccion Mediciones',
            xaxis_title="Module voltage [V]",
            yaxis_title="Module current [A]",
            plot_bgcolor='black',
            paper_bgcolor='black',
            font=dict(color='white')
        )



    # Aqui va la figura de la medicion normal


    return fig2,Tabla


    # Calculate parameters using pvlib's function
    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=float(valores[7]),
        cells_in_series=float(valores[8]),
        temp_ref=25
                                            )

    # Initialize the figure for plotting
    fig = go.Figure()


    i_sc = []
    v_oc = []
    i_mpi = []
    v_mpv = []
    p_mp = []

    # Dictionaries for effective irradiance and cell temperature
    d = {
        'Geff': [io],
        'Tcell': [to]
        }



    # Create DataFrame with conditions
    conditions = pd.DataFrame(data=d)

    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=Placa["alpha"],
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)

        fig.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f"Temp:{case['Tcell']:.2f}, Irr: {case['Geff']:.2f}"))
        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']
        fig.add_trace(go.Scatter(
            x=[v_mp],
            y=[i_mp],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp medido",
            customdata=[v_mp * i_mp]
        ))

        i_sc.append(curve_info['i_sc'])
        v_oc.append(curve_info['v_oc'])
        i_mpi.append(curve_info['i_mp'])
        v_mpv.append(curve_info['v_mp'])
        p_mp.append(curve_info['p_mp'])



        fig.update_layout(
            title="Curva IV Comparaciones",
            xaxis_title="Module voltage [V]",
            yaxis_title="Module current [A]",
            legend_title="Conditions"
        )

    lenght = len(pd.read_excel("Uploaded_.xlsx", sheet_name="Info"))

    Isc=[]
    Voc=[]
    Imp=[]
    Vmp=[]
    Pmp=[]
    Cond=[]

    for i in range(lenght):
        # Prepare the measured data
        m=pd.read_excel("Uploaded_.xlsx", sheet_name=i)
        m.columns = ["V", "I", "P"]
        id_max = m['P'].idxmax()
        ppm = m["P"].loc[id_max]



        fig.add_trace(go.Scatter(x=m.V, y=m.I, mode='lines', name=f"Caso medido"))

        v_mpm = m["V"].loc[id_max]
        i_mpm = m["I"].loc[id_max]
        p_mpm = m["P"].loc[id_max]
        MISC = m.I[0]
        MVOC = m.V[len(m) - 1]
        nombre= f"IV{i+1}"

        Isc.append(m.I.max())
        Voc.append(m.V.max())
        Imp.append(i_mpm)
        Vmp.append(v_mpm)
        Pmp.append(ppm)
        Cond.append(nombre)


        fig.add_trace(go.Scatter(
            x=[v_mpm],
            y=[i_mpm],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp measured",
            customdata=[v_mpm * i_mpm]
        ))



    data_frame = pd.DataFrame(
        data={"Condicion": Cond,
              "ISC":Isc,
              "VOC":Voc,
              "IMP":Imp,
              "VMP":Vmp,
              "PMP":Pmp})

    fig.update_layout(
        title="Curva IV",
        xaxis_title="Module voltage [V]",
        yaxis_title="Module current [A]",
        legend_title="Condiciones",
        xaxis_tickangle=30,
        xaxis_tickfont=dict(size=10),
        yaxis_tickfont=dict(size=10),
        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
        font=dict(color='white')
                    )

    return fig,data_frame.round(2)


def IV_CI2(Placa, df, io, to, m, Seleccion):
    valores = [valor for parametro, valor in Placa.items()]

    # Prepare the measured data
    m.columns = ["V", "I", "P"]
    id_max = m['P'].idxmax()
    ppm = m["P"].loc[id_max]

    # Calculate parameters using pvlib's function
    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=float(valores[7]),
        cells_in_series=float(valores[8]),
        temp_ref=25
    )

    # Initialize the figure for plotting
    fig2 = go.Figure()

    i_sc = []
    v_oc = []
    i_mpi = []
    v_mpv = []
    p_mp = []

    # Dictionaries for effective irradiance and cell temperature
    d = {
        'Geff': [io],
        'Tcell': [to]
    }

    # Process Seleccion
    if 1 in Seleccion:
        df['Diferencia_Temp_F'] = (df['Pmax_F'] - ppm).abs()
        idx_min_F = df['Diferencia_Temp_F'].idxmin()
        l = df.loc[idx_min_F]
        d['Geff'].append(l['Poa_global'])
        d['Tcell'].append(l['T_Feinman'])

    if 2 in Seleccion:
        df['Diferencia_Temp_S'] = (df['Pmax_S'] - ppm).abs()
        idx_min_S = df['Diferencia_Temp_S'].idxmin()
        l = df.loc[idx_min_S]

        d['Geff'].append(l['Poa_global'])
        d['Tcell'].append(l['T_Sandia'])

    if 3 in Seleccion:
        df['Diferencia_Temp_NOCT'] = (df['Pmax_NOCT'] - ppm).abs()
        idx_min_NOCT = df['Diferencia_Temp_NOCT'].idxmin()
        l = df.loc[idx_min_NOCT]

        d['Geff'].append(l['Poa_global'])
        d['Tcell'].append(l['T_NOCT'])



    # Create DataFrame with conditions
    conditions = pd.DataFrame(data=d)

    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=Placa["alpha"],
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)

        fig2.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f"Temp:{case['Tcell']:.2f}, Irr: {case['Geff']:.2f}"))
        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']
        fig2.add_trace(go.Scatter(
            x=[v_mp],
            y=[i_mp],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp medido",
            customdata=[v_mp * i_mp]
        )) #Esto actua como una lista, de append, por lo que cualquier cosa que pases por este, se quedara guardado.

        i_sc.append(curve_info['i_sc'])
        v_oc.append(curve_info['v_oc'])
        i_mpi.append(curve_info['i_mp'])
        v_mpv.append(curve_info['v_mp'])
        p_mp.append(curve_info['p_mp'])

        fig2.update_layout(
            title="Curva IV Comparaciones",
            xaxis_title="Module voltage [V]",
            yaxis_title="Module current [A]",
            legend_title="Conditions"
        )

    fig2.add_trace(go.Scatter(x=m.V, y=m.I, mode='lines', name=f"Caso medido"))

    v_mpm = m["V"].loc[id_max]
    i_mpm = m["I"].loc[id_max]
    p_mpm = m["P"].loc[id_max]
    MISC = m.I[0]
    MVOC = m.V[len(m) - 1]

    fig2.add_trace(go.Scatter(
        x=[v_mpm],
        y=[i_mpm],
        mode='markers',
        marker=dict(color='white'),
        hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
        name=f"Mpp measured",
        customdata=[v_mpm * i_mpm]
    ))

    if Seleccion == [1]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion", "Potencia Maxima Feynman"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [2]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion", "Potencia Maxima Sandia"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [1, 2]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion", "Potencia Maxima Feynman", "Potencia Maxima Sandia"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [3]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion", "Potencia Maxima NOCT"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [1,3]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion","Potencia Maxima Feynman" ,"Potencia Maxima NOCT"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [1,2,3]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion","Potencia Maxima Feynman","Potencia Maxima Sandia" ,"Potencia Maxima NOCT"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [2,3]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion","Potencia Maxima Sandia" ,"Potencia Maxima NOCT"],
                  "ISC(Error porcentual)": (abs(MISC - i_sc) / MISC) * 100,
                  "VOC(Error porcentual)": (abs(MVOC - v_oc) / MVOC) * 100,
                  "IMP(Error porcentual)": (abs(i_mpm - i_mpi) / i_mpm) * 100,
                  "VMP(Error porcentual)": (abs(v_mpm - v_mpv) / v_mpm) * 100,
                  "PMP(Error porcentual)": (abs(p_mpm - p_mp) / p_mpm) * 100
                })



    fig2.update_layout(
        title="Curva IV",
        xaxis_title="Module voltage [V]",
        yaxis_title="Module current [A]",
        legend_title="Condiciones",
        xaxis_tickangle=30,
        xaxis_tickfont=dict(size=10),
        yaxis_tickfont=dict(size=10),
        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
        font=dict(color='white')
    )

    return fig2, data_frame.round(2)

def table_final_IV(d):

    global tablespe
    dataframes = []
    columns = [{'name': i, 'id': i} for i in d.columns]
    data = d.to_dict('records')
    dataframes.append((data, columns))

    tablespe = [
        html.Div([
            html.H3(f"Paramatros electricos del modulo"),
            html.Div(
                dash_table.DataTable(
                    id=f"Modulo-IV-{i + 1}",
                    data=data,
                    columns=columns,
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
                ),
                style={'width': '100%', 'overflowX': 'auto'}
            )
        ], style={'width': '100%'}) for i, (data, columns) in enumerate(dataframes)
    ]

    return tablespe

def correcion_IV():
    t= html.Div([
                dbc.Label("Si la medición no es del todo buena o fue realizada en condiciones diferentes a las estandar, seleccionar casilla."),
                dbc.Checklist(
                    options=[
                        {"label": "Corregir Medición", "value": 1}
                            ],
                    value= 0  ,
                    id="correction",
                ),
            ])

    return t


def Rs_e(df,rs_SDM):
    dif = df.Volts.max() * 0.03
    Volt_voc = df.Volts.max() - dif
    data_v = df.Volts - Volt_voc
    num = 0
    indice = []
    voltajes = []
    for value in data_v:
        num += 1
        if value < 1 and value > -1:
            if value < 0:
                value = abs(value)  # Usar abs() para simplificar la conversión a positivo
            indice.append(num - 1)
            voltajes.append(value)

            # Crear el DataFrame Minimo_voc
            found = {"indice": indice, "value": voltajes}
            Minimo_voc = pd.DataFrame(found).set_index("indice")

            # Usar iloc para acceder por posición
            i = Minimo_voc['value'].idxmin()  # No hace falta [0] ya que estamos usando el nombre de la columna
            X = df.iloc[i]['Volts']  # Cambiamos a iloc para evitar la advertencia
            Y = df.iloc[i]['Amps']  # Cambiamos a iloc también aquí

            # Continuar con el resto del código
            NR = df.iloc[i:]

    i = 0
    distancias = []
    voltajes = []
    corrientes = []
    for V, I in zip(NR.Volts, NR.Amps):
        Voltaje = np.array(NR.Volts)
        Corriente = np.array(NR.Amps)
        distancias.append([Voltaje[i] - Voltaje[i + 1], Corriente[i + 1] - Corriente[i], NR.index[i]])
        i = 1 + i
        if i == len(NR) - 1:
            break

    num = 0
    num2 = 0
    indices = []
    for value in distancias:
        if value[0] < 0:
            indices.append(value[2])
            num += 1
        if value[0] > 0:
            num2 += 1

    i = 0
    z = 0
    listas = {}
    nombres = []
    for ind in indices:

        nombre = f"Lista_{z}"
        if nombre not in listas:
            listas[nombre] = []

        if i == (len(indices) - 1):
            break

        if (indices[i + 1] - indices[i]) == 1:

            listas[nombre].append(ind)




        else:
            z = z + 1
            nombre = f"Lista_{z}"
        nombres.append(nombre)

        i += 1

    from re import M
    x = []
    nombres = []
    for i, l in listas.items():
        x.append(len(listas[i]))
        nombres.append(i)
        l = pd.DataFrame(x)
        l["listas"] = nombres
        l.columns = ["longitud", "listas"]
        l = l.set_index("listas")
        Mayor = l.longitud.idxmax()
        listas[Mayor]
        m = df
        y2 = listas[Mayor][-1] + 2
        y1 = listas[Mayor][0]
        rs_o = abs((df.iloc[y2].Volts - df.iloc[y1].Volts) / (df.iloc[y2].Amps - df.iloc[y1].Amps)) / 2
        ri = ((rs_SDM + rs_o) / 2)

    return rs_o,ri

def Temperature_coeffs(Tipo_celda, Vm, Im, Voc_l, Isc, Pm, alpha_abs, beta_abs, gama, Nc, T):

        parameters = pvlib.ivtools.sdm.fit_cec_sam(Tipo_celda, Vm, Im, Voc_l, Isc, (alpha_abs/100)*Isc, (beta_abs/100)*Voc_l, gama, Nc,
                                                   temp_ref=T)

        d = {
            'Geff': [1000, 1000, 1000, 1000, 1000, 1000],
            'Tcell': [25, 30, 40, 50, 60, 70]
            }

        conditions = pd.DataFrame(data=d)
        IV = {}
        IV = pd.DataFrame(IV)
        nombres = []
        for idx, case in conditions.iterrows():
            IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
                effective_irradiance=case['Geff'],
                temp_cell=case['Tcell'],
                alpha_sc=(alpha_abs/ 100) * Isc,
                a_ref=parameters[4],
                I_L_ref=parameters[0],
                I_o_ref=parameters[1],
                R_sh_ref=parameters[3],
                R_s=parameters[2],
                EgRef=1.121,
                dEgdT=-0.0002677
            )

            nombre = f"V_{case['Tcell']}"
            nombre2 = f"I_{case['Tcell']}"

            SDE_params = {
                'photocurrent': IL,  # Light Generated current Il
                'saturation_current': I0,  # Dark saturation current
                'resistance_series': Rs,
                'resistance_shunt': Rsh,
                'nNsVth': nNsVth
            }

            curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
            v = np.linspace(0., curve_info["v_oc"], 100)
            i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)
            IV[nombre] = v
            IV[nombre2] = i
            nombres.append([nombre, nombre2])

        Voc_t = []
        Isc_t = []
        Pm_t = []
        for cond in nombres:
            x = cond[0]
            y = cond[1]
            Voc = IV[x].max()
            Isc = IV[y].max()
            PM = IV[x] * IV[y]
            Pmm = PM.max()
            Voc_t.append(Voc)
            Isc_t.append(Isc)
            Pm_t.append(Pmm)

        coeffs = pd.DataFrame({
            "Tcell": [25, 30, 40, 50, 60, 70],
            "Voc_t": Voc_t,
            "Isc_t": Isc_t,
            "Pm_t": Pm_t
        })

        # Ajuste para Voc
        slope_voc, intercept_voc, r2_voc, coeffs['y_fit_voc'] = linear_fit(coeffs["Tcell"], coeffs["Voc_t"])

        # Ajuste para Isc
        slope_isc, intercept_isc, r2_isc, coeffs['y_fit_isc'] = linear_fit(coeffs["Tcell"], coeffs["Isc_t"])

        # Ajuste para Pm
        slope_pm, intercept_pm, r2_pm, coeffs['y_fit_pm'] = linear_fit(coeffs["Tcell"], coeffs["Pm_t"])
        beta = (slope_voc / Voc_l) * 100
        alpha = (slope_isc / Isc) * 100
        gamma = (slope_pm / Pm) * 100
        return alpha, beta, gamma

def linear_fit(x, y):
    adjust = np.polyfit(x, y, deg=1)
    slope, intercept = adjust
    y_fit = slope * x + intercept
    ss_res = np.sum((y - y_fit) ** 2)  # Suma de los residuos al cuadrado
    ss_tot = np.sum((y - y.mean()) ** 2)  # Suma total de cuadrados
    r2 = 1 - (ss_res / ss_tot)
    return slope, intercept, r2, y_fit


def correction_IV(df, Tipo_celda, Vm, Im, Voc, Isc, Pm, alpha, beta, gamma_m, Nc, Tmed, G_med, Vocmed):
    df.columns = ["Volts", "Amps", "Watts"]
    V = df["Volts"]
    I = df["Amps"]
    PPm = df.loc[df["Watts"].idxmax()]
    df["R"] = V / I
    n = Nc
    gamma = gamma_m
    Temp_medida = Tmed
    Gmed = G_med
    Voc_med = Vocmed
    rs_medido = pvlib.ivtools.sdm.fit_cec_sam(Tipo_celda, PPm.Volts, PPm.Amps, df["Volts"].max(), df["Amps"].max(),
                                              (alpha / 100) * Isc, (beta / 100) * Voc, gamma, n, temp_ref=Tmed)
    rs_stc = pvlib.ivtools.sdm.fit_cec_sam(Tipo_celda, Vm, Im, Voc, Isc,(alpha / 100) * Isc, (beta / 100) * Voc, gamma, Nc, temp_ref=25)
    rs = (rs_medido[2] + rs_stc[2]) / 2
    ri = Rs_e(df,rs)[0]
    ri_2 = (rs_medido[2] + rs_stc[2] + ri) / 3

    df["(V+IRs)/n"] = (df.Volts + df.Amps * ri_2) / n
    df["Ln(Isc-I)"] = np.log(df["Amps"].max() - df.Amps)
    df["(V+IRs)/n"] = df["(V+IRs)/n"]
    df["Ln(Isc-I)"] = df["Ln(Isc-I)"]
    x = []
    y = []
    num_c = 0
    for i in df["Ln(Isc-I)"]:
        num_c += 1
        if i >= 0:
            x.append(i)
            y.append(num_c - 1)

    c = y[-1] - 59
    dl = df[c:]
    #dl.plot(x="(V+IRs)/n", y="Ln(Isc-I)", kind="scatter")

    # Ajuste lineal
    adjust = np.polyfit(dl["(V+IRs)/n"], dl["Ln(Isc-I)"], deg=1)
    slope, intercept = adjust
    dl['y_fit'] = slope * dl["(V+IRs)/n"] + intercept
    y_real = dl["Ln(Isc-I)"]
    y_pred = dl['y_fit']
    ss_res = np.sum((y_real - y_pred) ** 2)  # Suma de los residuos al cuadrado
    ss_tot = np.sum((y_real - y_real.mean()) ** 2)  # Suma total de cuadrados
    r2 = 1 - (ss_res / ss_tot)

    # Generar la línea de ajuste
    x_line = np.linspace(dl["(V+IRs)/n"].min(), dl["(V+IRs)/n"].max(), 100)
    y_line = slope * x_line + intercept

    # Agregar la línea de ajuste al gráfico
    #plt.plot(x_line, y_line, color="red", label=f'Ajuste lineal: y = {slope:.2f}x + {intercept:.2f} , R^2={r2:1f}')
    #plt.legend()

    # Mostrar la gráfica con la línea de ajuste
    #plt.xlabel("(V+IRs)/n")
    #plt.ylabel("Ln(Isc-I)")
    #plt.title("Gráfico de dispersión con línea de ajuste lineal")
    #plt.show()



    ## Trasalacion de resultados Metodo 1

    alpha_rel = (alpha / 100)
    beta_rel = (beta / 100)
    a = (rs_stc[4] + rs_medido[4]) / 2
    r = Rs_e(df, rs)[0]

    df["I2"] = df["Amps"] * (1 + ((alpha_rel) * (25 - Temp_medida))) * (1000 / Gmed)

    df["V2"] = (
            df["Volts"]
            + (Voc_med * (((beta_rel) * (25 - Temp_medida))) + ((a * (1/((constants.elementary_charge)/((Temp_medida+273)*constants.Boltzmann))) * np.log(1000 / Gmed))))
            - (r * (df["I2"] - df["Amps"]))
            - ((r / 100) * df["I2"] * (25 - Temp_medida))
    )

    df["P2"] = df.V2 * df.I2
    df.iloc[df["P2"].idxmax()]

    # Metodo de correcion 2.



    alpha, beta, gamma = Temperature_coeffs(Tipo_celda, Vm, Im, Voc, Isc, Pm, alpha,
                                                  beta, gamma, Nc, 25)
    parameters = pvlib.ivtools.sdm.fit_cec_sam(Tipo_celda, Vm, Im, Voc, Isc, (alpha / 100) * Isc, (beta / 100) * Voc,
                                               gamma, Nc, temp_ref=25)

    d = {
        'Geff': [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100],
        'Tcell': [25, 25, 25, 25, 25, 25, 25, 25, 25, 25]
    }

    conditions = pd.DataFrame(data=d)
    IV = {}
    IV = pd.DataFrame(IV)
    nombres = []
    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=(alpha / 100) * Isc,
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        nombre = f"V_{case['Geff']}"
        nombre2 = f"I_{case['Geff']}"

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)
        IV[nombre] = v
        IV[nombre2] = i
        nombres.append([nombre, nombre2])

    Voc_t = []
    Isc_t = []
    Pm_t = []
    for cond in nombres:
        x = cond[0]
        y = cond[1]
        Voc = IV[x].max()
        Isc = IV[y].max()
        PM = IV[x] * IV[y]
        Pmm = PM.max()
        Voc_t.append(Voc)
        Isc_t.append(Isc)
        Pm_t.append(Pmm)

    coeffs = pd.DataFrame({
        "G": [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100],
        "Voc_t": Voc_t,
        "Isc_t": Isc_t,
        "Pm_t": Pm_t
    })

    # Voc de referencia a 1000 W/m²
    voc_ref = coeffs.loc[coeffs["G"] == 1000, "Voc_t"].values[0]  # Voltaje de referencia a condiciones normales.

    # Lista de Voc para cada nivel de irradiancia
    allvoc = coeffs["Voc_t"].tolist()  # estos ya son los de corto circuito

    # Calcular x e y para el ajuste
    G = coeffs["G"]
    x = np.log(1000 / G)
    y = voc_ref / np.array(allvoc)

    # Ajuste polinomial para obtener B1 y B2
    para = np.polyfit(x, y, 2)
    B1 = para[1]
    B2 = para[0]

    i = df["Amps"]
    v = df["Volts"]
    G = G_med
    T = Tmed
    alpha_rel = alpha / 100
    beta_rel = beta / 100
    B1 = para[1]
    B2 = para[0]

    i_corr = i * 1000 / G / (1 + alpha_rel * (T - 25))

    rs1 = ri_2 + (ri_2 / 100) * (T - 25)

    fG1 = B2 * (np.log(1000 / G) ** 2) + B1 * np.log(1000 / G) + 1

    v_corr = v - rs1 * (i_corr - i) - (ri_2/ 100) * i_corr * (25 - T) + voc_ref * (
                beta_rel * (25 - T) * fG1 + 1 - 1 / fG1)

    df["I3"] = i_corr
    df["V3"] = v_corr
    df["P3"] = i_corr * v_corr


    return df

def correction_IV_s(dt, Tipo_celda, Vm, Im, Voc, Isc, Pm, alpha, beta, gamma_m, Nc, Tmed, G_med, Vocmed):
    dt.columns = ["Volts", "Amps", "Watts"]
    V = dt["Volts"]
    I = dt["Amps"]
    PPm = dt.loc[dt["Watts"].idxmax()]
    dt["R"] = V / I
    n = Nc
    gamma = gamma_m
    Temp_medida = Tmed
    Gmed = G_med
    Voc_med = Vocmed
    rs_medido = pvlib.ivtools.sdm.fit_cec_sam(Tipo_celda, PPm.Volts, PPm.Amps, dt["Volts"].max(), dt["Amps"].max(),
                                              (alpha / 100) * Isc, (beta / 100) * Voc, gamma, n, temp_ref=Tmed)
    rs_stc = pvlib.ivtools.sdm.fit_cec_sam(Tipo_celda, Vm, Im, Voc, Isc,(alpha / 100) * Isc, (beta / 100) * Voc, gamma, Nc, temp_ref=25)
    rs = (rs_medido[2] + rs_stc[2]) / 2
    ri = Rs_e(dt,rs)[0]
    ri_2 = (rs_medido[2] + rs_stc[2] + ri) / 3

    dt["(V+IRs)/n"] = (dt.Volts + dt.Amps * ri_2) / n
    dt["Ln(Isc-I)"] = np.log(dt["Amps"].max() - dt.Amps)
    dt["(V+IRs)/n"] = dt["(V+IRs)/n"]
    dt["Ln(Isc-I)"] = dt["Ln(Isc-I)"]
    x = []
    y = []
    num_c = 0
    for i in dt["Ln(Isc-I)"]:
        num_c += 1
        if i >= 0:
            x.append(i)
            y.append(num_c - 1)

    c = y[-1] - 59
    dl = dt[c:]
    #dl.plot(x="(V+IRs)/n", y="Ln(Isc-I)", kind="scatter")

    # Ajuste lineal
    adjust = np.polyfit(dl["(V+IRs)/n"], dl["Ln(Isc-I)"], deg=1)
    slope, intercept = adjust
    dl['y_fit'] = slope * dl["(V+IRs)/n"] + intercept
    y_real = dl["Ln(Isc-I)"]
    y_pred = dl['y_fit']
    ss_res = np.sum((y_real - y_pred) ** 2)  # Suma de los residuos al cuadrado
    ss_tot = np.sum((y_real - y_real.mean()) ** 2)  # Suma total de cuadrados
    r2 = 1 - (ss_res / ss_tot)

    # Generar la línea de ajuste
    x_line = np.linspace(dl["(V+IRs)/n"].min(), dl["(V+IRs)/n"].max(), 100)
    y_line = slope * x_line + intercept

    # Agregar la línea de ajuste al gráfico
    #plt.plot(x_line, y_line, color="red", label=f'Ajuste lineal: y = {slope:.2f}x + {intercept:.2f} , R^2={r2:1f}')
    #plt.legend()

    # Mostrar la gráfica con la línea de ajuste
    #plt.xlabel("(V+IRs)/n")
    #plt.ylabel("Ln(Isc-I)")
    #plt.title("Gráfico de dispersión con línea de ajuste lineal")
    #plt.show()



    ## Trasalacion de resultados Metodo 1

    alpha_rel = (alpha / 100)
    beta_rel = (beta / 100)
    a = (rs_stc[4] + rs_medido[4]) / 2
    r = Rs_e(dt, rs)[0]

    dt["I2_s"] = dt["Amps"] * (1 + ((alpha_rel) * (25 - Temp_medida))) * (1000 / Gmed)

    dt["V2_s"] = (
            dt["Volts"]
            + (Voc_med * (((beta_rel) * (25 - Temp_medida))) + ((a * (1/((constants.elementary_charge)/((Temp_medida+273)*constants.Boltzmann))) * np.log(1000 / Gmed))))
            - (r * (dt["I2_s"] - dt["Amps"]))
            - ((r / 100) * dt["I2_s"] * (25 - Temp_medida))
    )

    dt["P2_s"] = dt.V2_s * dt.I2_s
    dt.iloc[dt["P2_s"].idxmax()]

    # Metodo de correcion 2.



    #alpha, beta, gamma = Temperature_coeffs(Tipo_celda, Vm, Im, Voc, Isc, Pm, alpha,
     #                                            beta, gamma, Nc, 25)
    parameters = pvlib.ivtools.sdm.fit_cec_sam(Tipo_celda, Vm, Im, Voc, Isc, (alpha / 100) * Isc, (beta / 100) * Voc,
                                               gamma, Nc, temp_ref=25)

    d = {
        'Geff': [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100],
        'Tcell': [25, 25, 25, 25, 25, 25, 25, 25, 25, 25]
    }

    conditions = pd.DataFrame(data=d)
    IV = {}
    IV = pd.DataFrame(IV)
    nombres = []
    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=(alpha / 100) * Isc,
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        nombre = f"V_{case['Geff']}"
        nombre2 = f"I_{case['Geff']}"

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)
        IV[nombre] = v
        IV[nombre2] = i
        nombres.append([nombre, nombre2])

    Voc_t = []
    Isc_t = []
    Pm_t = []
    for cond in nombres:
        x = cond[0]
        y = cond[1]
        Voc = IV[x].max()
        Isc = IV[y].max()
        PM = IV[x] * IV[y]
        Pmm = PM.max()
        Voc_t.append(Voc)
        Isc_t.append(Isc)
        Pm_t.append(Pmm)

    coeffs = pd.DataFrame({
        "G": [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100],
        "Voc_t": Voc_t,
        "Isc_t": Isc_t,
        "Pm_t": Pm_t
    })

    # Voc de referencia a 1000 W/m²
    voc_ref = coeffs.loc[coeffs["G"] == 1000, "Voc_t"].values[0]  # Voltaje de referencia a condiciones normales.

    # Lista de Voc para cada nivel de irradiancia
    allvoc = coeffs["Voc_t"].tolist()  # estos ya son los de corto circuito

    # Calcular x e y para el ajuste
    G = coeffs["G"]
    x = np.log(1000 / G)
    y = voc_ref / np.array(allvoc)

    # Ajuste polinomial para obtener B1 y B2
    para = np.polyfit(x, y, 2)
    B1 = para[1]
    B2 = para[0]

    i = dt["Amps"]
    v = dt["Volts"]
    G = G_med
    T = Tmed
    alpha_rel = alpha / 100
    beta_rel = beta / 100
    B1 = para[1]
    B2 = para[0]

    i_corr = i * 1000 / G / (1 + alpha_rel * (T - 25))

    rs1 = ri_2 + (ri_2 / 100) * (T - 25)

    fG1 = B2 * (np.log(1000 / G) ** 2) + B1 * np.log(1000 / G) + 1

    v_corr = v - rs1 * (i_corr - i) - (ri_2/ 100) * i_corr * (25 - T) + voc_ref * (
                beta_rel * (25 - T) * fG1 + 1 - 1 / fG1)

    dt["I3_s"] = i_corr
    dt["V3_s"] = v_corr
    dt["P3_s"] = i_corr * v_corr


    return dt


def minimos(df,Isco):
    minimos = []
    indice = []
    i=3
    for i in range(3, len(df)):
        y = df["I3"].iloc[:i]
        x = df["V3"].iloc[:i]
        m = abs(Isco - (np.polyfit(x, y, deg=1)[1]))
        indice.append(i)
        minimos.append(m)
        lista = pd.DataFrame({"min": minimos, "indice": indice})
        lista=lista.set_index("indice")

    i = lista["min"].idxmin()
    y = df["I3"].iloc[:i]
    x = df["V3"].iloc[:i]
    Isc = (np.polyfit(x, y, deg=1)[1])
    return Isc

def minimos_s(dt,Isco):
    minimos = []
    indice = []
    i=3
    for i in range(3, len(dt)):
        y = dt["I3_s"].iloc[:i]
        x = dt["V3_s"].iloc[:i]
        m = abs(Isco - (np.polyfit(x, y, deg=1)[1]))
        indice.append(i)
        minimos.append(m)
        lista = pd.DataFrame({"min": minimos, "indice": indice})
        lista=lista.set_index("indice")

    i = lista["min"].idxmin()
    y = dt["I3_s"].iloc[:i]
    x = dt["V3_s"].iloc[:i]
    Isc = (np.polyfit(x, y, deg=1)[1])
    return Isc



def IV_CI_Corr(Placa, df, io, to, m, Seleccion):
    valores = [valor for parametro, valor in Placa.items()]
    #["Volts", "Amps", "Watts"]
    # Prepare the measured data
    m.columns = ["Volts", "Amps", "Watts"]
    id_max = m['Watts'].idxmax()
    ppm = m['Watts'].loc[id_max]

    # Calculate parameters using pvlib's function
    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp=float(valores[7]),
        cells_in_series=float(valores[8]),
        temp_ref=25
    )

    # Initialize the figure for plotting
    fig2 = go.Figure()

    i_sc = []
    v_oc = []
    i_mpi = []
    v_mpv = []
    p_mp = []

    # Dictionaries for effective irradiance and cell temperature
    d = {
        'Geff': [io],
        'Tcell': [to]
    }

    # Process Seleccion
    if 1 in Seleccion:
        df['Diferencia_Temp_F'] = (df['Pmax_F'] - ppm).abs()
        idx_min_F = df['Diferencia_Temp_F'].idxmin()
        l = df.loc[idx_min_F]
        d['Geff'].append(l['Poa_global'])
        d['Tcell'].append(l['T_Feinman'])

    if 2 in Seleccion:
        df['Diferencia_Temp_S'] = (df['Pmax_S'] - ppm).abs()
        idx_min_S = df['Diferencia_Temp_S'].idxmin()
        l = df.loc[idx_min_S]

        d['Geff'].append(l['Poa_global'])
        d['Tcell'].append(l['T_Sandia'])

    if 3 in Seleccion:
        df['Diferencia_Temp_NOCT'] = (df['Pmax_NOCT'] - ppm).abs()
        idx_min_NOCT = df['Diferencia_Temp_NOCT'].idxmin()
        l = df.loc[idx_min_NOCT]

        d['Geff'].append(l['Poa_global'])
        d['Tcell'].append(l['T_NOCT'])



    # Create DataFrame with conditions
    conditions = pd.DataFrame(data=d)

    for idx, case in conditions.iterrows():
        IL, I0, Rs, Rsh, nNsVth = pvlib.pvsystem.calcparams_desoto(
            effective_irradiance=case['Geff'],
            temp_cell=case['Tcell'],
            alpha_sc=Placa["alpha"],
            a_ref=parameters[4],
            I_L_ref=parameters[0],
            I_o_ref=parameters[1],
            R_sh_ref=parameters[3],
            R_s=parameters[2],
            EgRef=1.121,
            dEgdT=-0.0002677
        )

        SDE_params = {
            'photocurrent': IL,  # Light Generated current Il
            'saturation_current': I0,  # Dark saturation current
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='lambertw', **SDE_params)
        v = np.linspace(0., curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='lambertw', **SDE_params)

        fig2.add_trace(go.Scatter(x=v, y=i, mode='lines', name=f"Temp:{case['Tcell']:.2f}, Irr: {case['Geff']:.2f}"))
        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']
        fig2.add_trace(go.Scatter(
            x=[v_mp],
            y=[i_mp],
            mode='markers',
            marker=dict(color='white'),
            hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
            name=f"Mpp medido",
            customdata=[v_mp * i_mp]
        ))

        i_sc.append(curve_info['i_sc'])
        v_oc.append(curve_info['v_oc'])
        i_mpi.append(curve_info['i_mp'])
        v_mpv.append(curve_info['v_mp'])
        p_mp.append(curve_info['p_mp'])

        fig2.update_layout(
            title="Curva IV Comparaciones",
            xaxis_title="Module voltage [V]",
            yaxis_title="Module current [A]",
            legend_title="Conditions"
        )

    fig2.add_trace(go.Scatter(x=m.Volts, y=m.Amps, mode='lines', name=f"Caso medido"))

    v_mpm = m["Volts"].loc[id_max]
    i_mpm = m["Amps"].loc[id_max]
    p_mpm = m["Watts"].loc[id_max]
    MISC = m.I[0]
    MVOC = m.V[len(m) - 1]

    fig2.add_trace(go.Scatter(
        x=[v_mpm],
        y=[i_mpm],
        mode='markers',
        marker=dict(color='white'),
        hovertemplate='Mpp: %{x} * %{y} = %{customdata} W/m2',
        name=f"Mpp measured",
        customdata=[v_mpm * i_mpm]
    ))

    if Seleccion == [1]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion", "Potencia Maxima Feynman"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [2]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion", "Potencia Maxima Sandia"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [1, 2]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion", "Potencia Maxima Feynman", "Potencia Maxima Sandia"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [3]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion", "Potencia Maxima NOCT"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [1,3]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion","Potencia Maxima Feynman" ,"Potencia Maxima NOCT"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [1,2,3]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion","Potencia Maxima Feynman","Potencia Maxima Sandia" ,"Potencia Maxima NOCT"],
                  "ISC(Error porcentual)": ((abs(MISC - i_sc)) / MISC) * 100,
                  "VOC(Error porcentual)": ((abs(MVOC - v_oc)) / MVOC) * 100,
                  "IMP(Error porcentual)": ((abs(i_mpm - i_mpi)) / i_mpm) * 100,
                  "VMP(Error porcentual)": ((abs(v_mpm - v_mpv)) / v_mpm) * 100,
                  "PMP(Error porcentual)": ((abs(p_mpm - p_mp)) / p_mpm) * 100})

    if Seleccion == [2,3]:
        data_frame = pd.DataFrame(
            data={"Condicion": ["Condicion de Medicion","Potencia Maxima Sandia" ,"Potencia Maxima NOCT"],
                  "ISC(Error porcentual)": (abs(MISC - i_sc) / MISC) * 100,
                  "VOC(Error porcentual)": (abs(MVOC - v_oc) / MVOC) * 100,
                  "IMP(Error porcentual)": (abs(i_mpm - i_mpi) / i_mpm) * 100,
                  "VMP(Error porcentual)": (abs(v_mpm - v_mpv) / v_mpm) * 100,
                  "PMP(Error porcentual)": (abs(p_mpm - p_mp) / p_mpm) * 100
                })



    fig2.update_layout(
        title="Curva IV",
        xaxis_title="Module voltage [V]",
        yaxis_title="Module current [A]",
        legend_title="Condiciones",
        xaxis_tickangle=30,
        xaxis_tickfont=dict(size=10),
        yaxis_tickfont=dict(size=10),
        plot_bgcolor="rgb(0,0,0)",  # Fondo del gráfico
        paper_bgcolor='black',  # Fondo del papel (entorno alrededor del gráfico)
        font=dict(color='white')
    )

    return fig2, data_frame.round(2)



