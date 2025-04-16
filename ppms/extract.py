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

data = dict()
for data_name in data_names:
    data_dir = os.path.join(base_dir, data_name)
    dimension = pd.read_csv(os.path.join(data_dir, 'dimension.csv'))

    Rho_data = dict()
    
    for exp in ['Hall', 'Para', 'Perp']:
        exp_dir = os.path.join(data_dir, exp)
        Rho_data[exp] = {'Ts': [], 'Rhos': []}

        for file_name in os.listdir(exp_dir):
            exp_data = pd.read_csv(os.path.join(exp_dir, file_name))
            exp_data.rename(columns = {'Temperature (K)': 'T', 
                                   'Field (Oe)': 'B', 
                                   f'Resistance Ch{ch} (Ohms)': 'R'},
                        inplace = True)
        
            exp_data['T'] = np.round(exp_data['T'], 0)
            exp_data['B'] = exp_data['B']/10000
            if exp != 'Hall':
                exp_data['Rho'] = exp_data['R'] * dimension['T'][0] * dimension['W'][0] / dimension['L'][0]
            else:
                exp_data['Rho'] = exp_data['R'] * dimension['T'][0]

            Rho_0 = np.mean(exp_data['Rho'][np.argsort(np.abs(exp_data['B']))][:10])

            Rho_pos = exp_data.loc[(exp_data['B'] > 0)].sort_values(by = 'B', ascending = True)
            Rho_pos = Rho_pos[pd.to_numeric(Rho_pos['Rho'], errors = 'coerce').notnull()]
            Rho_neg = exp_data.loc[(exp_data['B'] < 0)].sort_values(by = 'B', ascending = False)
            Rho_neg = Rho_neg[pd.to_numeric(Rho_neg['Rho'], errors = 'coerce').notnull()]

            pos_interp = PchipInterpolator(*resolve_monotone(np.concatenate([[B_min], Rho_pos['B']]), np.concatenate([[Rho_0], Rho_pos['Rho']])), extrapolate = False)
            Rho_pos_new = pos_interp(Bs)
            neg_interp = PchipInterpolator(*resolve_monotone(np.concatenate([[B_min], np.abs(Rho_neg['B'])]), np.concatenate([[Rho_0], Rho_neg['Rho']])), extrapolate = False)
            Rho_neg_new = neg_interp(Bs)

            Rho_data[exp]['Ts'].append(exp_data['T'][0])
            if exp != 'Hall':
                Rho_data[exp]['Rhos'].append((Rho_pos_new + Rho_neg_new) / 2)
            else:
                Rho_data[exp]['Rhos'].append((Rho_pos_new - Rho_neg_new) / 2)

        Rho_data[exp]['Ts'] = np.array(Rho_data[exp]['Ts'])
        Rho_data[exp]['Rhos'] = np.stack(Rho_data[exp]['Rhos'])

        idxs = np.argsort(Rho_data[exp]['Ts'])
        Rho_data[exp]['Ts'] = Rho_data[exp]['Ts'][idxs]
        Rho_data[exp]['Rhos'] = Rho_data[exp]['Rhos'][idxs]

    data[data_name] = Rho_data

with open('extracted.pkl', 'wb') as f:
    pkl.dump((data, Bs), f)
