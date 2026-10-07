import pandas as pd

def clc(NDH):

    datos60, datos30, datos15, datos5 = [], [], [], []
    DNmin = []
    DNmax = []
    for clave, valor in NDH.items():
        for year in valor:
            DNmin.append(pd.DataFrame(year[year.Hour.isin([6, 7, 8])]))
            DNmax.append(pd.DataFrame(year[year.Hour.isin([14, 16])]))
    CLCmin = []
    CLCmax = []
    clc = 0
    for climamin in DNmin:
        clc = 0
        clc = pd.DataFrame(climamin.temp_air)
        clc.columns = ['TempMin']
        clc['ghi_min'] = climamin.ghi
        clc['wspeed_min'] = climamin.wind_speed
        CLCmin.append(clc)

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
    CLC = []
    for i in range(len(CLCmax)):
        clc = CLCmax[i]
        clcmin = CLCmin[i]

        clc = pd.concat([clc, clcmin], axis=1)
        CLC.append(clc)
    return (CLC)