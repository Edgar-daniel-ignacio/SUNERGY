import Parametros_Electricos as pe
import pvlib
from pvlib._deprecation import pvlibDeprecationWarning
import warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)
warnings.filterwarnings(action='ignore', category=pvlibDeprecationWarning)
import pandas as pd
from pvlib import pvsystem
import matplotlib.pyplot as plt
import  numpy as np
import plotly.graph_objects as go


def IV(Placa):
    valores = [valor for parametro, valor in Placa.items()]

    parameters = pvlib.ivtools.sdm.fit_cec_sam(
        celltype='monoSi',
        v_mp=float(valores[1]),
        i_mp=float(valores[2]),
        v_oc=float(valores[3]),
        i_sc=float(valores[4]),
        alpha_sc=float((valores[5] / 100) * valores[4]),
        beta_voc=float((valores[6] / 100) * valores[3]),
        gamma_pmp= float(valores[7]),
        cells_in_series=float(valores[8]),
        temp_ref=float(valores[9])
    )

    cases = [
        (1098.160944, 57.447914),
        (375.491531, 24.069324),
        (1098.160944, 57.447914),
        (1073.095209, 67.377506),
        (1098.160944, 57.447914),
        (1001,27.5)
    ]

    conditions = pd.DataFrame(cases, columns=['Geff', 'Tcell'])

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
            'photocurrent':IL,
            'saturation_current': I0,
            'resistance_series': Rs,
            'resistance_shunt': Rsh,
            'nNsVth': nNsVth
        }

        curve_info = pvlib.pvsystem.singlediode(method='newton', **SDE_params)
        v = np.linspace(0.,curve_info["v_oc"], 100)
        i = pvlib.pvsystem.i_from_v(voltage=v, method='newton', **SDE_params)

        label = (
            f"$G_{{eff}}$ {case['Geff']} $W/m^2$\n"
            f"$T_{{cell}}$ {case['Tcell']} $\\degree C$"
                )

        fig.add_trace(go.Scatter(x=v, y=i, mode='lines', name=label))
        v_mp = curve_info['v_mp']
        i_mp = curve_info['i_mp']
        fig.add_trace(go.Scatter(x=[v_mp], y=[i_mp], mode='markers', marker=dict(color='white'), name=f'MPP {label}'))

        print(pd.DataFrame({
            'i_sc': [curve_info['i_sc']],
            'v_oc': [curve_info['v_oc']],
            'i_mp': [curve_info['i_mp']],
            'v_mp': [curve_info['v_mp']],
            'p_mp': [curve_info['p_mp']],
                            }))

        print(IL, I0, Rs, Rsh, nNsVth)

    fig.update_layout(
        title="IV Curve",
        xaxis_title="Module voltage [V]",
        yaxis_title="Module current [A]",
        legend_title="Conditions"
                    )



    return fig

