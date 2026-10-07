import pytz
from timezonefinder import TimezoneFinder
from datetime import datetime
import pvlib
from pvlib._deprecation import pvlibDeprecationWarning
import warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
warnings.filterwarnings(action='ignore', category=pvlibDeprecationWarning)
import pandas as pd


def obtener_utc_de_coordenadas(lat, lon):


    # Encontrar el nombre de la zona horaria con timezonefinder
    tf = TimezoneFinder()
    nombre_zona_horaria = tf.timezone_at(lat=lat, lng=lon)

    if nombre_zona_horaria is None:
        return "Zona horaria no encontrada"

    # Obtener el objeto de zona horaria con pytz
    zona_horaria = pytz.timezone(nombre_zona_horaria)

    # Obtener la diferencia UTC actual
    # Nota: La diferencia UTC puede variar si la zona horaria tiene horario de verano
    ahora_utc = datetime.now(pytz.utc)
    ahora_zona_horaria = ahora_utc.astimezone(zona_horaria)
    diferencia_utc = ahora_zona_horaria.utcoffset().total_seconds() / 3600

    return diferencia_utc


def Clima(lat, lon, A, tiempos, intervalos):
    NDH = None
    key = 'hUjeTpNxpUpyKV4tOGRYFsnCFqkmnM3eboSlUssq'
    email = 'edidzing@gmail.com'

    # 1. TMY logic using the TMY PSM4 function
    if A == "TMY":
        # Note: year='tmy' is the default for this function
        df, metadata = pvlib.iotools.get_nsrdb_psm4_tmy(
            lat, lon, key, email,
            year='tmy',
            map_variables=True,
            timeout=60
        )
        NDH = {8760.0: []}
        if len(df) == 8760:
            NDH[8760.0].append(df)
            print(f"Año típico (PSM4) de {len(df)} horas agregado.")
        return NDH

    # 2. Specific Year (SY) logic using the Aggregated PSM4 function
    elif A == "SY":
        NDH = {8760.0: [], 17520.0: [], 35040.0: [], 105120.0: []}
        for year in tiempos:
            for dt in intervalos:
                # Use the aggregated function for specific year requests
                df, metadata = pvlib.iotools.get_nsrdb_psm4_aggregated(
                    lat, lon, key, email,
                    year=year,
                    time_step=dt,
                    map_variables=True,
                    timeout=600
                )
                longitud_df = len(df)
                if longitud_df in NDH:
                    NDH[longitud_df].append(df)
                    print(f"Año específico {year} (PSM4) agregado.")
        return NDH



