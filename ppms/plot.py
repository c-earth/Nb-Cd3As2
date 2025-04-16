import pickle as pkl

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Times'
mpl.rcParams['font.size'] = '9'

# base = 1000
# colors = mpl.colormaps['gnuplot'](np.log(np.linspace(base**(0.1), base**(0.9), 300))/np.log(base))
colors = mpl.colormaps['gnuplot'](np.linspace(0, 1, 380))
cmap = mpl.colors.LinearSegmentedColormap.from_list('custom_gnuplot', colors)

width_pt = 246
width_in = width_pt/72.27
subplot_arg = (0.2, 0.25, 0.72, 0.68)

with open('extracted.pkl', 'rb') as f:
    data, Bs = pkl.load(f)


for data_name in data:
    for exp, exp_data in data[data_name].items():
        fig = plt.figure(figsize = (2*width_in/3, width_in/2))
        ax = fig.add_axes(subplot_arg)
        
        for T, Rho in zip(np.flip(exp_data['Ts'], axis = 0), np.flip(exp_data['Rhos'], axis = 0)):
            ax.plot(Bs, Rho * 1E6, '-', color = colors[int(T)+30])
        ax.set_xlim(0, 9)
        ax.set_xlabel('B [T]')
        ax.set_ylabel('$\\rho$ [$\mu\Omega$ m]')

        # cb = fig.colorbar(plt.cm.ScalarMappable(cmap = cmap, norm = plt.Normalize(vmin = -30, vmax = 350)), cax = ax.inset_axes([0.5, 0.1, 0.05, 0.8]))
        # cb.ax.set_title(r'$T$ [K]', fontsize = 10)
        # cb.ax.tick_params(length = 5, width = 1.5, labelsize = 10, which = 'both', direction = 'out')
        # cb.ax.set_ylim(0, 300)
        # cb.ax.set_yscale('log')
        # cb.ax.set_yticks([10, 100])
        # cb.ax.set_yticklabels([10, 100])

        fig.savefig(f'Rho_{exp}_{data_name}.pdf', dpi = 300)

        if exp == 'Hall':
            continue

        MRs = (exp_data['Rhos'] / exp_data['Rhos'][:, :1] - 1) * 100

        fig = plt.figure(figsize = (2*width_in/3, width_in/2))
        ax = fig.add_axes(subplot_arg)
        
        for T, MR in zip(np.flip(exp_data['Ts'], axis = 0), np.flip(MRs, axis = 0)):
            ax.plot(Bs, MR, '-', color = colors[int(T)+30])
        ax.set_xlim(0, 9)
        # ax.set_ylim(-2, 2)
        ax.set_xlabel('B [T]')
        ax.set_ylabel('MR [\%]')

        # cb = fig.colorbar(plt.cm.ScalarMappable(cmap = cmap, norm = plt.Normalize(vmin = -30, vmax = 350)), cax = ax.inset_axes([0.5, 0.1, 0.05, 0.8]))
        # cb.ax.set_title(r'$T$ [K]', fontsize = 10)
        # cb.ax.tick_params(length = 5, width = 1.5, labelsize = 10, which = 'both', direction = 'out')
        # cb.ax.set_ylim(0, 300)
        # cb.ax.set_yscale('log')
        # cb.ax.set_yticks([10, 100])
        # cb.ax.set_yticklabels([10, 100])

        fig.savefig(f'MR_{exp}_{data_name}.pdf', dpi = 300)



