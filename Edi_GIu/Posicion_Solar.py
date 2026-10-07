# Esta parte del codigo sirve para calcular la irradiancia efectiva.
# con esta parte del codigo se calcula  todos los angulos solares y posiciones del lugar.
# desoto, sirve para sacar la curva Iv, factor de idealidad, Rs
# hacer tabla de Franhoffer
# Determinar irradiancia efectiva.
# Location.get_solarposition
# Declinacion solar
# Determinar_todo sobre la radiacion desde posicion hasta
# AMi = Masa de aire ideal.
# AMr= Masa de aire real.
#Esta funcion es dependiente de Primer_Funcion_Clima
from timezonefinder import TimezoneFinder
import pvlib
from pvlib._deprecation import pvlibDeprecationWarning
import warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
warnings.filterwarnings(action='ignore', category=pvlibDeprecationWarning)
import numpy as np
import Primer_Funcion_Clima as pf
from pvlib.irradiance import get_total_irradiance
from pvlib import pvsystem


def get_time_zone(latitude, longitude):
    """
    Given latitude and longitude, return the time zone name.
    """
    tz_finder = TimezoneFinder()
    time_zone_str = tz_finder.timezone_at(lat=latitude, lng=longitude)  # Find the time zone
    if time_zone_str:
        return time_zone_str
    else:
        return "Time zone not found"


def Solar_pos(NDH,lat,lon):
    for hora, lista in NDH.items():
        for datos in lista:
            for t in [8760, 17520, 35040, 105120]:
                if len(datos) == t:
                    location = pvlib.location.Location(lat, lon, get_time_zone(lat, lon))
                    # definimos la libreria de PVlib para definir la localidad:
                    solar_position = location.get_solarposition(datos.index)

                    T = datos.Hour + (datos.Minute * (1 / 60))  # Tiempo en horas
                    H = 15 * (T - 12)
                    Ds = -23.45 * np.cos(np.radians((360 / 365) * (10 + datos.Day)))  # Declinacion Angular es correcta
                    # Local standard Meridian
                    diferencia_utc = pf.obtener_utc_de_coordenadas(lat, lon)
                    LSTM = 15 * diferencia_utc
                    # Ecuacion de tiempo para la correcion (EoT)
                    B = (360 / 365) * (datos.Day - 81)
                    EoT = (9.87 * np.sin(np.radians(2 * B))) - (7.53 * np.cos(np.radians(B))) - (
                                1.5 * np.sin(np.radians(B)))
                    # Time correction Factor (TC)
                    TC = (4 * (lon - LSTM)) + EoT
                    # Local Solar time
                    LST = T + (TC / 60)
                    # Hour Angle
                    HRA = 15 * (LST - 12)
                    HRA_Pvlib = pvlib.solarposition.hour_angle(datos.index, lon, EoT)  # Correcto

                    argumento_elevacion = (np.sin(np.radians(Ds)) * np.sin(np.radians(lat))) + (
                                np.cos(np.radians(Ds)) * np.cos(np.radians(lat)) * np.cos(np.radians(HRA)))
                    Elevation_angle = np.degrees(np.arcsin(argumento_elevacion))  # Correcto

                    # Regla de resta 360 Esta parte no sirvio de nada, en el futuro cuando hagas la funcion quitala.
                    Argumento_azimuth = ((np.sin(np.radians(Ds)) * np.cos(np.radians(lat))) - (
                                np.cos(np.radians(Ds)) * np.sin(np.radians(lat)) * np.cos(np.radians(HRA)))) / (
                                            np.cos(np.radians(Elevation_angle)))
                    Azimuth = np.degrees(np.arccos(Argumento_azimuth))
                    Azimuth = solar_position.azimuth

                    # Azimuth con PVlib

                    location = pvlib.location.Location(lat, lon, tz=get_time_zone(lat, lon))
                    solar_position = location.get_solarposition(datos.index)
                    solar_azimuth = solar_position.azimuth
                    solar_zenith = solar_position.zenith

                    ## Zenith
                    Zenithal = 90 - solar_position.elevation  # Corrrecto*

                    AMi = 1 / np.cos(np.radians(Zenithal))

                    AMr = 1 / ((np.cos(np.radians(Zenithal))) + (0.50572 * ((96.07995 - Zenithal) ** (-1.6364))))

                    AMr_p = (AMi + AMr) / 2

                    system_one_array = pvsystem.PVSystem(surface_tilt=lat, surface_azimuth=180)

                    # Angle of incidence

                    aoi = system_one_array.get_aoi(solar_zenith=solar_zenith, solar_azimuth=solar_azimuth)

                    # Irradiancia respecto al plano.

                    Plane_of_irrradiance = get_total_irradiance(surface_tilt=lat, surface_azimuth=180,
                                                                solar_zenith=solar_position.apparent_zenith,
                                                                solar_azimuth=solar_azimuth, dni=datos.dni, ghi=datos.ghi,
                                                                dhi=datos.dhi, airmass=AMi, albedo=datos.albedo)

                    ##surface_tilt (float, default 0) – Surface tilt angle. The tilt angle is defined as angle from horizontal
                    # (e.g. surface facing up = 0, surface facing horizon = 90) [degrees]
                    #surface_azimuth (float, default 180) – Azimuth angle of the module surface. North=0, East=90, South=180, West=270. [degrees]


                    datos["Poa_global"] = Plane_of_irrradiance.poa_global
                    datos["Poa_direct"] = Plane_of_irrradiance.poa_direct
                    datos["Poa_diffuse"] = Plane_of_irrradiance.poa_diffuse
                    datos["Poa_sky_diffuse"] = Plane_of_irrradiance.poa_sky_diffuse
                    datos["Poa_ground_diffuse"] = Plane_of_irrradiance.poa_ground_diffuse

                    #Estos datos se agregan solitos, al estar ocupando NDH como valor de entrada  este se modifica cuando entra a la funcion.

def Solar_pos_e(NDH,lat,lon,tilt,azimuth):
    for hora, lista in NDH.items():
        for datos in lista:
            for t in [8760, 17520, 35040, 105120]:
                if len(datos) == t:
                    location = pvlib.location.Location(lat, lon, get_time_zone(lat, lon))
                    # definimos la libreria de PVlib para definir la localidad:
                    solar_position = location.get_solarposition(datos.index)

                    T = datos.Hour + (datos.Minute * (1 / 60))  # Tiempo en horas
                    H = 15 * (T - 12)
                    Ds = -23.45 * np.cos(np.radians((360 / 365) * (10 + datos.Day)))  # Declinacion Angular es correcta
                    # Local standard Meridian
                    diferencia_utc = pf.obtener_utc_de_coordenadas(lat, lon)
                    LSTM = 15 * diferencia_utc
                    # Ecuacion de tiempo para la correcion (EoT)
                    B = (360 / 365) * (datos.Day - 81)
                    EoT = (9.87 * np.sin(np.radians(2 * B))) - (7.53 * np.cos(np.radians(B))) - (
                                1.5 * np.sin(np.radians(B)))
                    # Time correction Factor (TC)
                    TC = (4 * (lon - LSTM)) + EoT
                    # Local Solar time
                    LST = T + (TC / 60)
                    # Hour Angle
                    HRA = 15 * (LST - 12)
                    HRA_Pvlib = pvlib.solarposition.hour_angle(datos.index, lon, EoT)  # Correcto

                    argumento_elevacion = (np.sin(np.radians(Ds)) * np.sin(np.radians(lat))) + (
                                np.cos(np.radians(Ds)) * np.cos(np.radians(lat)) * np.cos(np.radians(HRA)))
                    Elevation_angle = np.degrees(np.arcsin(argumento_elevacion))  # Correcto

                    # Regla de resta 360 Esta parte no sirvio de nada, en el futuro cuando hagas la funcion quitala.
                    Argumento_azimuth = ((np.sin(np.radians(Ds)) * np.cos(np.radians(lat))) - (
                                np.cos(np.radians(Ds)) * np.sin(np.radians(lat)) * np.cos(np.radians(HRA)))) / (
                                            np.cos(np.radians(Elevation_angle)))
                    Azimuth = np.degrees(np.arccos(Argumento_azimuth))
                    Azimuth = solar_position.azimuth

                    # Azimuth con PVlib

                    location = pvlib.location.Location(lat, lon, tz=get_time_zone(lat, lon))
                    solar_position = location.get_solarposition(datos.index)
                    solar_azimuth = solar_position.azimuth
                    solar_zenith = solar_position.zenith

                    ## Zenith
                    Zenithal = 90 - solar_position.elevation  # Corrrecto*

                    AMi = 1 / np.cos(np.radians(Zenithal))

                    AMr = 1 / ((np.cos(np.radians(Zenithal))) + (0.50572 * ((96.07995 - Zenithal) ** (-1.6364))))

                    AMr_p = (AMi + AMr) / 2

                    system_one_array = pvsystem.PVSystem(surface_tilt=lat, surface_azimuth=180)

                    # Angle of incidence

                    aoi = system_one_array.get_aoi(solar_zenith=solar_zenith, solar_azimuth=solar_azimuth)

                    # Irradiancia respecto al plano.

                    Plane_of_irrradiance = get_total_irradiance(surface_tilt=float(tilt), surface_azimuth=float(azimuth),
                                                                solar_zenith=solar_position.apparent_zenith,
                                                                solar_azimuth=solar_azimuth, dni=datos.dni, ghi=datos.ghi,
                                                                dhi=datos.dhi, airmass=AMi, albedo=datos.albedo)

                    ##surface_tilt (float, default 0) – Surface tilt angle. The tilt angle is defined as angle from horizontal
                    # (e.g. surface facing up = 0, surface facing horizon = 90) [degrees]
                    #surface_azimuth (float, default 180) – Azimuth angle of the module surface. North=0, East=90, South=180, West=270. [degrees]


                    datos["Poa_global"] = Plane_of_irrradiance.poa_global
                    datos["Poa_direct"] = Plane_of_irrradiance.poa_direct
                    datos["Poa_diffuse"] = Plane_of_irrradiance.poa_diffuse
                    datos["Poa_sky_diffuse"] = Plane_of_irrradiance.poa_sky_diffuse
                    datos["Poa_ground_diffuse"] = Plane_of_irrradiance.poa_ground_diffuse

                    #Estos datos se agregan solitos, al estar ocupando NDH como valor de entrada  este se modifica cuando entra a la funcion.










