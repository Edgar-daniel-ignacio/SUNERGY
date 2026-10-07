import pvlib
import numpy as np
from scipy import special, constants
import pandas as pd

def temperaturas(NDH):
        Tmod=np.array([15,25,35,45,55,75]) # Russel calculation

        a,b=np.array([-3.47,-2.98,-3.56,-2.81,-3.58,-3.23]),np.array([-.0594,-.0471,-.0750,-.0455,-.113,-.130]) # Sandia Calculation Factores que se utilizan dependiendo la forma de la
        # forma de instlacion
        deltaT=[3,1,3,0]
        TypeModuleSandia=int(input("Tipo de Modulo que ocupas \n 1) glass\glass open-rack \n 2) glass\glass close-roof \n 3)glass\polymer open/rack \n 4) glas\polymer insulated back \n Introduzca el numero de posicinador: \t",))
        New_r=TypeModuleSandia
        temp_df=[]
        for horas, datos in NDH.items():
            for lista in datos:
                for size in [8760, 17520, 35040, 105120]:  # Different sizes

                    if len(lista) == size:
                        E=lista.Poa_global # Irradiancia global horizontal
                        WS=lista.wind_speed # Velocidad del viento
                        Ta=lista.temp_air
                        Eo=1000
                        #Calculo dela temperatura Sandia
                        T=E*(np.exp(a[TypeModuleSandia-1]+(b[TypeModuleSandia-1]*WS)))+Ta # calculo de modelo sandia con temperatura de modulo
                        Ts=pvlib.temperature.sapm_cell_from_module(T,E,deltaT[TypeModuleSandia-1],irrad_ref=Eo) # calculo de modelo sandia temperatura de celda
                        lista["Tsandia"]=Ts
                        #Calculo de la temperatura Feinman
                        TFeinman=pvlib.temperature.faiman(poa_global=E, temp_air=Ta,wind_speed=WS, u0=25.0, u1=6.84) #u0=29.432, u1=4.468
                        lista["TFeinman"]=TFeinman



def Placa(Pmax0, Vmax60, Imax0, Voc0, Isc0, alpha, beta, deltha, cells_in_series, temp_ref, celltype):
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
        'cell_type': celltype,
        'A': 1.33,
        'Boltzmann': constants.Boltzmann,
        'Elementary_charge': constants.elementary_charge

    }
    # Retornar el diccionario
    return datos_placa

def PE(
        Placa_r,NDH): #PLaca es una libreria que contiene valores
    irr = {}
    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=Placa_r["Vmax60"],
        i_mp=Placa_r["Imax"],
        v_oc=Placa_r["Voc"],
        i_sc=Placa_r["Isc"],
        alpha_sc=float(Placa_r["alpha"] / 100) * (Placa_r["Isc"]),
        beta_voc=float(Placa_r["beta"] / 100) * (Placa_r["Voc"]),
        gamma_pmp=float(Placa_r["deltha"]) ,
        cells_in_series=float(Placa_r["cells_in_series"]),
        temp_ref=float(Placa_r["temp_ref"])
    )

    for hora, lista in NDH.items():
        for datos in lista:
            print("hola")
            if "TFeinman" in datos:
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

            if 'Tsandia' in datos and "TFeinman" in datos:
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

    for hora, lista in NDH.items():
        for datos in lista:
            for t in [8760, 17520, 35040, 105120]:
                if t == len(datos):
                    A = Placa_r["A"]
                    K =Placa_r["Boltzmann"]
                    q = Placa_r["Elementary_charge"]
                    Pmax0 = Placa_r["Pmax"]
                    Imax0 = Placa_r["Imax"]
                    Vmax0 = Placa_r["Vmax60"]
                    Voc0 = Placa_r["Voc"]
                    Isc0c = Placa_r["Isc"]  # Aquí se corrigió el nombre de la variable
                    betha = Placa_r["beta"]/ 100  # Aquí se corrigió el nombre de la variable para mantener la consistencia
                    alpha = Placa_r["alpha"]/ 100  # Recuerda este valor es importante dividir entre 100
                    deltha = Placa_r["deltha"]/100 ## esto realmente es gamma
                    ## GaMMA  es el coeficiente de temperatura de la potencia
                    ## DElta es difernte.



                    nombre_df = f"{t}_{datos.index.year.unique()[0]}"
                    df = pd.DataFrame(datos.Poa_global)

                    #parametros electricos: Aqui tienes que meter los parametros electricos pero ahora calculados con las nuevas irradiancias una ves teniendo eso , puedes resolver la ecuacion del diodo. Ademas de poder hacer las curvas IV.
                    df["Year"] = datos.Year
                    df["Month"] = datos.Month
                    gamma = (datos.AF * K * ((datos.TFeinman + 273.15))) / q
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

                    Pmax = ((Pmax0 * (1 + (deltha * (datos.TFeinman - 25)))) * (
                            1 + (df.Gamma_F * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)

                    #Pmax = Imax60*Vmax60

                    Pmax[np.isnan(Pmax)] = 0
                    df["Pmax_F"] = Pmax
                    df["T_Feinman"] = datos.TFeinman


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

                    Imax60 = Imax0 * (1 + (alpha * (datos.Tsandia - 25))) * (datos.Poa_global / 1000)
                    df["Imax_S"] = Imax60

                    Vmax60 = Vmax0 * (1 + (deltha * (datos.Tsandia - 25))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))
                    Vmax60[np.isinf(Vmax60)] = 0
                    df["Vmax_S"] = Vmax60

                    Pmax60 = ((Pmax0 * (1 + (deltha * (datos.Tsandia - 25)))) * (
                            1 + (df.Gamma_S * (np.log(datos.Poa_global / 1000))))) / (1000 / datos.Poa_global)

                    Pmax60[np.isnan(Pmax60)] = 0
                    df["Pmax_S"] = Pmax60
                    df["T_Sandia"] = datos.Tsandia

                    df["AF"] = nNsVth
                    df["AS"] = nNsVthS



                    irr[nombre_df] = df
    return irr








