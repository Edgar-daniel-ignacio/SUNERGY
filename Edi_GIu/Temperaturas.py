import numpy as np
import pvlib


def temp(NDH):
    Tmod = np.array([15, 25, 35, 45, 55, 75])  # Russel calculation
    a, b = np.array([-3.47, -2.98, -3.56, -2.81, -3.58, -3.23]), np.array([-.0594, -.0471, -.0750, -.0455, -.113,
                                                                           -.130])  # Sandia Calculation Factores que se utilizan dependiendo la forma de la
    # forma de instalacion
    TemperaturaM = []
    ModuleTypeMount = ["glass\glass \t open rack", "glass\glass \t close roof", "glass\polymer \t open rack",
                       "glass polymer \t insulated back", "Polymer\thin-fiml\steel", "22X Linear Concetrator\tracker"]
    deltaT = [3, 1, 3, 0]

    a, b = np.array([-3.47, -2.98, -3.56, -2.81, -3.58, -3.23]), np.array([-.0594, -.0471, -.0750, -.0455, -.113,
                                                                           -.130])  # Sandia Calculation Factores que se utilizan dependiendo la forma de la
    # forma de instlacion
    deltaT = [3, 1, 3, 0]
    TypeModuleSandia = int(input(
        "Tipo de Modulo que ocupas \n 1) glass\glass open-rack \n 2) glass\glass close-roof \n 3)glass\polymer open/rack \n 4) glas\polymer insulated back \n Introduzca el numero de posicinador: \t", ))
    New_r = TypeModuleSandia
    temp_df = []
    for horas, datos in NDH.items():
        for lista in datos:
            for size in [8760, 17520, 35040, 105120]:  # Different sizes

                if len(lista) == size:
                    E = lista.Poa_global  # Irradiancia global horizontal
                    WS = lista.wind_speed  # Velocidad del viento
                    Ta = lista.temp_air
                    Eo = lista.ghi
                    # Calculo dela temperatura Sandia
                    T = E * (np.exp(a[TypeModuleSandia - 1] + (b[TypeModuleSandia - 1] * WS))) + Ta  # calculo de modelo sandia con temperatura de modulo
                    Ts = pvlib.temperature.sapm_cell_from_module(T, E, deltaT[TypeModuleSandia - 1],
                                                                 irrad_ref=Eo)  # calculo de modelo sandia temperatura de celda
                    lista["Tsandia"] = Ts
                    # Calculo de la temperatura Feinman
                    TFeinman = pvlib.temperature.faiman(poa_global=E, temp_air=Ta, wind_speed=WS, u0=29.432,
                                                        u1=4.468)  # u0=29.432, u1=4.468
                    lista["TFeinman"] = TFeinman
