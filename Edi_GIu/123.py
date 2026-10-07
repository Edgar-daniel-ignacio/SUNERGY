def electric_parameters(nombres_Pe, nombres_Pe2, selected_value, Seleccion, nombre, Metodo, Yt_h):
    t = []
    t1 = []
    # lo que hacen los ifs, es descargar los datos que existen para ocuparlos.

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
                    print("Processing year0000:", year)
                    if year == f"Año {df.index.year.unique()[0]} [Horas: {len(df)}]":
                        print(f"llllll{Seleccion}")
                        print(input.resume_df(Seleccion, df))

    # frames=input.resume_df(Seleccion,t)

    Prueba = input.Placa_Prueba(585, 43.3, 13.42, 51.52, 14.3, 0.045, -0.23, -0.28, 72, 25, "monoSi")
    Ndh = input.df_creator(nombre, Seleccion)  ## NDH es el dataframe, tambien uso el nombre t,df,datos
    PE1 = input.PE(Prueba, Ndh)
    Pe_CSV = input.creador_csv_PE(PE1)

    tables1 = input.table_IV(PE1, nombre)
    print(Pe_CSV)  ## Creador de los CSV y da los nombres
    print("Bien ahi compa")

    print("Bien ahi compadre 0000")
    print(Metodo)

    return tables1

@app.callback(
    Output('PE-IV', "children"),
    [
        Input("Datos_PE", "data"),
        Input("Datos_PE2", "data"),
        Input('selection-dropdown', 'value'),
        Input("checklist-input", 'value'),
        Input('store-ndh', 'data'),
        Input('IV-Method', 'value'),
        Input('Year-Time-IV', 'value')
    ]
)
def electric_parameters(nombres_Pe_Iv, nombres_Pe2_Iv, selected_value, Seleccion, nombre, Metodo, Yt_h_iv):
    t = []
    t1 = []
    Yt_h = [Yt_h_iv]

    if len(Yt_h) > 0:
        if len(nombres_Pe2_Iv) > 0 and len(nombres_Pe_Iv) > 0:
            t = input.df_creator_1(nombres_Pe_Iv, [1])
            t1 = input.df_creator_1(nombres_Pe2_Iv, [1])
        elif len(nombres_Pe_Iv) > 0 and len(nombres_Pe2_Iv) == 0:
            t = input.df_creator_1(nombres_Pe_Iv, [1])
            t1 = []
        elif len(nombres_Pe2_Iv) > 0 and len(nombres_Pe_Iv) == 0:
            t = []
            t1 = input.df_creator_1(nombres_Pe2_Iv, [1])

        if len(t) > 0 and len(t1) == 0:
            for df in t:
                for year in Yt_h:
                    if year == f"Año {df.index.year.unique()[0]} [Horas: {len(df)}]":
                        input.resume_df(Seleccion, df)

    Prueba = input.Placa_Prueba(585, 43.3, 13.42, 51.52, 14.3, 0.045, -0.23, -0.28, 72, 25, "monoSi")
    Ndh = input.df_creator(nombre, Seleccion)
    PE1 = input.PE(Prueba, Ndh)
    Pe_CSV = input.creador_csv_PE(PE1)
    tables1 = input.table_IV(PE1, nombre)

    if Metodo == "Sandia":
        # Add the specific processing logic for the Sandia model here
        # This could involve unique calculations, transformations, etc.
        pass

    if len(t) > 0 and len(t1) > 0:
        # Add comparison logic here between t and t1
        # This could involve combining the data, comparing metrics, etc.
        pass

    return tables1
