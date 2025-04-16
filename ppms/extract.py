import os
import pickle as pkl

import pandas as pd
import numpy as np
from scipy.interpolate import PchipInterpolator

from data import resolve_monotone


data_names = ['pris', 'surf', 'bulk']
base_dir = 'D:/python_project/Nb-Cd3As2/data/ppms'

ch = 1

B_min = 0.0
B_max = 9.0
B_res = 1000

Bs = np.linspace(B_min, B_max, B_res)

for data_name in data_names:
    data_dir = os.path.join(base_dir, data_name)
    dimension = pd.read_csv(os.path.join(data_dir, 'dimension.csv'))

    Ts = []
    Rho_hall = []
    Rho_para = []
    Rho_perp = []
    
    for file_name in os.listdir(data_dir):
        data = pd.read_csv(os.path.join(data_dir, file_name))
        data.rename(columns = {'Temperature (K)': 'Temperature', 
                            'Field (Oe)': 'Field', 
                            f'Resistance Ch{ch} (Ohms)': 'rho_xx'},
                    inplace = True)
        
        data['Temperature'] = np.round(data['Temperature'], 0)  # round temperature to integer
        data['Field'] = data['Field']/10000                     # convert field unit from Gauss to Tesla
        data['rho_xx'] = data['rho_xx'] * W * T / (L * 1000)    # calculate sample resistivity

        rho_xx_0 = np.min(data['rho_xx'])
        rho_xx_pos = data.loc[(data['Field'] > 0)].sort_values(by = 'Field', ascending = True)
        rho_xx_neg = data.loc[(data['Field'] < 0)].sort_values(by = 'Field', ascending = False)
        
        # interpolate data between corresponding positive and negative fields
        pos_interp = PchipInterpolator(*resolve_monotone(np.concatenate([[H_min], rho_xx_pos['Field']]), np.concatenate([[rho_xx_0], rho_xx_pos['rho_xx']])), extrapolate = False)
        rho_xx_pos_new = pos_interp(Hs)
        neg_interp = PchipInterpolator(*resolve_monotone(np.concatenate([[H_min], np.abs(rho_xx_neg['Field'])]), np.concatenate([[rho_xx_0], rho_xx_neg['rho_xx']])), extrapolate = False)
        rho_xx_neg_new = neg_interp(Hs)
        
        # get unbiased resistivity
        rho_xx = (rho_xx_pos_new + rho_xx_neg_new)/2

        Ts.append(data['Temperature'][0])
        rho_xxs.append(rho_xx)

    Ts = np.array(Ts)
    rho_xxs = np.stack(rho_xxs)


    # sort data by temperature
    idxs = np.argsort(Ts)
    Ts = Ts[idxs]
    rho_xxs = rho_xxs[idxs]


    # truncate all H of data at all temperatures to  be the same
    idx_min = 0
    idx_max = H_res - 1
    for rho_xx in rho_xxs:
        got_min = False
        got_max = False

        nans = np.isnan(rho_xx)

        for i, nan in enumerate(nans):
            if not got_min:
                if not nan:
                    idx_min = max(idx_min, i)
                    got_min = True
            else:
                if not got_max:
                    if nan:
                        idx_max = min(idx_max, i - 1)
                        got_max = True
                    elif i == len(nans) - 1:
                        idx_max = min(idx_max, i)

    Hs = Hs[idx_min: idx_max + 1]
    rho_xxs = rho_xxs[:, idx_min: idx_max + 1]


    # save data
    with open(resu_name, 'wb') as f:
        pkl.dump([Ts, Hs, rho_xxs], f)