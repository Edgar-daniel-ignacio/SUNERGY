import os
from pathlib import Path
import pytz
from timezonefinder import TimezoneFinder
from datetime import datetime
import pvlib
from pvlib._deprecation import pvlibDeprecationWarning
import warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
warnings.filterwarnings(action='ignore', category=pvlibDeprecationWarning)
import pandas as pd

try:
    from dotenv import load_dotenv
    # Cargar archivo .env desde la raíz del proyecto o desde el directorio local
    _base_dir = Path(__file__).resolve().parent
    load_dotenv(dotenv_path=_base_dir.parent / '.env')
    load_dotenv(dotenv_path=_base_dir / '.env')
    load_dotenv()
except ImportError:
    pass


def obtener_utc_de_coordenadas(lat, lon):
    # Encontrar el nombre de la zona horaria con timezonefinder
    tf = TimezoneFinder()
    nombre_zona_horaria = tf.timezone_at(lat=lat, lng=lon)

    if nombre_zona_horaria is None:
        return "Zona horaria no encontrada"

    # Obtener el objeto de zona horaria con pytz
    zona_horaria = pytz.timezone(nombre_zona_horaria)

    # Obtener la diferencia UTC actual
    ahora_utc = datetime.now(pytz.utc)
    ahora_zona_horaria = ahora_utc.astimezone(zona_horaria)
    diferencia_utc = ahora_zona_horaria.utcoffset().total_seconds() / 3600

    return diferencia_utc


class SmartNDH(dict):
    """
    Estructura híbrida compatible con:
    1. El dashboard GIU_Final_Presetacion (usado como diccionario NDH con .items() y claves [8760.0, ...]).
    2. Scripts independientes o notebooks donde se desempaqueta directamente como: `df, metadata = Clima(...)`.
    """
    def __init__(self, ndh_dict, df=None, metadata=None):
        super().__init__(ndh_dict)
        self.df = df
        self.metadata = metadata

    def __iter__(self):
        yield self.df
        yield self.metadata


# Dominio oficial activo para NSRDB API (NREL migró de developer.nrel.gov a developer.nlr.gov)
URL_PSM4_TMY = "https://developer.nlr.gov/api/nsrdb/v2/solar/nsrdb-GOES-tmy-v4-0-0-download.csv"
URL_PSM4_AGG = "https://developer.nlr.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv"


def Clima(lat, lon, A, tiempos=None, intervalos=None, api_key=None, email=None):
    # Credenciales de NREL obtenidas desde variables de entorno (.env) o parámetros
    if not api_key:
        api_key = os.getenv('NREL_API_KEY')
    if not email:
        email = os.getenv('NREL_API_EMAIL')

    if not api_key or not email:
        raise ValueError(
            "Credenciales de NREL no configuradas. Por favor agrega NREL_API_KEY y NREL_API_EMAIL "
            "en tu archivo .env (ver .env.example) o establécelas como variables de entorno del sistema."
        )

    df = None
    metadata = {}
    NDH = {8760.0: [], 17520.0: [], 35040.0: [], 105120.0: []}

    # 1. Lógica para Año Típico Meteorológico (TMY)
    if str(A).upper() == "TMY":
        try:
            if hasattr(pvlib.iotools, 'get_nsrdb_psm4_tmy'):
                # pvlib moderno con soporte nativo de PSM v4 y endpoint activo de developer.nlr.gov
                df, metadata = pvlib.iotools.get_nsrdb_psm4_tmy(
                    latitude=lat,
                    longitude=lon,
                    api_key=api_key,
                    email=email,
                    year='tmy',
                    time_step=60,
                    leap_day=False,
                    map_variables=True,
                    url=URL_PSM4_TMY,
                    timeout=6000
                )
            elif hasattr(pvlib.iotools, 'get_psm3'):
                # Fallback para versiones previas de pvlib usando PSM3
                df, metadata = pvlib.iotools.get_psm3(
                    latitude=lat,
                    longitude=lon,
                    api_key=api_key,
                    email=email,
                    names="tmy",
                    leap_day=False,
                    map_variables=True,
                    timeout=6000
                )
            else:
                raise RuntimeError("Tu versión de pvlib no cuenta con funciones compatibles para NSRDB TMY.")
        except Exception as e:
            print(f"[ERROR NREL TMY]: {e}")
            raise RuntimeError(f"Error al descargar datos solares TMY de NREL: {e}")

        longitud_df = float(len(df))
        if longitud_df not in NDH:
            NDH[longitud_df] = []
        NDH[longitud_df].append(df)
        print(f"Año típico meteorológico (TMY) de {len(df)} horas agregado exitosamente a NDH.")

    # 2. Lógica para Años Específicos (SY / año individual)
    else:
        # Determinar si 'A' es el año directo (ej. A=2020) o si viene desde el selector 'SY' del GUI
        if str(A).upper() == "SY" and tiempos:
            years_to_fetch = tiempos if isinstance(tiempos, (list, tuple)) else [tiempos]
        else:
            years_to_fetch = [str(A)]

        # Determinar intervalos temporales (por defecto 60 min)
        if isinstance(intervalos, (list, tuple)) and len(intervalos) > 0:
            interval_list = intervalos
        elif isinstance(intervalos, (int, float)) and intervalos > 0:
            interval_list = [int(intervalos)]
        else:
            interval_list = [60]

        for year in years_to_fetch:
            for dt in interval_list:
                dt_int = int(dt)
                year_str = str(year)
                try:
                    if hasattr(pvlib.iotools, 'get_nsrdb_psm4_aggregated'):
                        # pvlib moderno PSM4 para series específicas con endpoint activo de developer.nlr.gov
                        df, metadata = pvlib.iotools.get_nsrdb_psm4_aggregated(
                            latitude=lat,
                            longitude=lon,
                            api_key=api_key,
                            email=email,
                            year=year_str,
                            time_step=dt_int,
                            leap_day=False,
                            map_variables=True,
                            url=URL_PSM4_AGG,
                            timeout=6000
                        )
                    elif hasattr(pvlib.iotools, 'get_psm3'):
                        # Fallback a PSM3 para versiones anteriores de pvlib
                        df, metadata = pvlib.iotools.get_psm3(
                            latitude=lat,
                            longitude=lon,
                            api_key=api_key,
                            email=email,
                            names=year_str,
                            interval=dt_int,
                            leap_day=False,
                            map_variables=True,
                            timeout=6000
                        )
                    else:
                        raise RuntimeError("Tu versión de pvlib no cuenta con get_nsrdb_psm4_aggregated ni get_psm3.")

                    longitud_df = float(len(df))
                    if longitud_df not in NDH:
                        NDH[longitud_df] = []
                    NDH[longitud_df].append(df)
                    print(f"Año específico {year_str} (intervalo {dt_int}m, {len(df)} registros) agregado exitosamente a NDH.")

                except Exception as e:
                    raise RuntimeError(f"Error al descargar datos solares de NREL para el año {year_str}: {e}")

    # Retorna SmartNDH: funciona como NDH (dict) en el dashboard, o se desempaqueta como (df, metadata) en scripts
    return SmartNDH(NDH, df=df, metadata=metadata)
