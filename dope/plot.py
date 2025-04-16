import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Times'
mpl.rcParams['font.size'] = '9'

width_pt = 246
width_in = width_pt/72.27
subplot_arg = (0.12, 0.17, 0.82, 0.75)

bulk_beam_path = 'D:/python_project/Nb-Cd3As2/data/beam/bulk.csv'
surf_beam_path = 'D:/python_project/Nb-Cd3As2/data/beam/surf.csv'

bulk_beam = np.genfromtxt(bulk_beam_path, delimiter = ',')
surf_beam = np.genfromtxt(surf_beam_path, delimiter = ',')

fig = plt.figure(figsize = (width_in, 3*width_in/4))
ax = fig.add_axes(subplot_arg)
ax.plot(surf_beam[:, 0], surf_beam[:, 1], '.', alpha = 0.8, label = '25 keV')
ax.plot(bulk_beam[:, 0], bulk_beam[:, 1], '.', alpha = 0.8, label = '200 keV')
ax.set_ylim(0, 5E20)
ax.set_xlim(0, 1000)
ax.set_xlabel('Sample Depth [$\AA$]')
ax.set_ylabel('Nb Concentration [atoms/cm$^3$]')
ax.legend(title = 'Ion Energy')
fig.savefig('ionrange_beam.pdf', dpi = 300)


bulk_srim = pd.read_csv(f'D:/python_project/Nb-Cd3As2/data/srim/RANGE_3D_200keV.txt', skiprows = 28, sep = '\s+', encoding = 'latin-1', names = ['Ion Number', 'X', 'Y_lateral', 'Z_lateral'])
surf_srim = pd.read_csv(f'D:/python_project/Nb-Cd3As2/data/srim/RANGE_3D_25keV.txt', skiprows = 28, sep = '\s+', encoding = 'latin-1', names = ['Ion Number', 'X', 'Y_lateral', 'Z_lateral'])

binwidth = 16
bins = np.arange(0, 1000 + binwidth, binwidth)
fig = plt.figure(figsize = (width_in, 3*width_in/4))
ax = fig.add_axes(subplot_arg)
ax.hist(surf_srim.X, bins = bins, weights = 10**5*np.ones_like(surf_srim.X), alpha = 0.8, label = '25 keV')
ax.hist(bulk_srim.X, bins = bins, weights = 10**5*np.ones_like(bulk_srim.X), alpha = 0.8, label = '200 keV')
ax.set_xlim(0, 1000)
ax.set_xlabel('Sample Depth [$\AA$]')
ax.set_ylabel('Nb Concentration [Arbitrary Unit]')
ax.get_yaxis().set_ticklabels([])
ax.legend(title = 'Ion Energy')
fig.savefig(f'ionrange_srim.pdf', dpi = 300)
