import pickle as pkl

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'cm'
mpl.rcParams['font.size'] = '9'

colors = mpl.colormaps['gnuplot'](np.linspace(0, 1, 26))
cmap = mpl.colors.LinearSegmentedColormap.from_list('custom_gnuplot', colors)

width_pt = 246
width_in = width_pt/72.27

def plot_arg(axis_size, width_in, axis_margin, have_label, have_tick_label, label_size, tick_label_size):
    fig_size = [(axis_size[i] + (2 + have_label[i] * (1 - have_tick_label[i])) * axis_margin[i] + label_size[i] * have_label[i] + tick_label_size[i] * have_tick_label[i]) * width_in for i in range(2)]
    ax_size = [((1 + have_label[i] * (1 - have_tick_label[i])) * axis_margin[i] + label_size[i] * have_label[i] + tick_label_size[i] * have_tick_label[i]) * width_in / fig_size[i] for i in range(2)] \
            + [axis_size[i] * width_in / fig_size[i] for i in range(2)]
    return fig_size, ax_size

with open('extracted.pkl', 'rb') as f:
    data, Bs = pkl.load(f)

fig_size, ax_size = plot_arg((1.78, 0.05), width_in, (0.03, 0.02), (1, 1), (1, 1), (0.05, 0.05), (0.08, 0.05))
fig = plt.figure(figsize = fig_size)
ax = fig.add_axes(ax_size)
ax.axis('off')
cb = fig.colorbar(plt.cm.ScalarMappable(cmap = cmap, norm = plt.Normalize(vmin = 0, vmax = 25)), orientation = 'horizontal', cax = ax.inset_axes([0, 0, 1, 1]))
cb.ax.set_xlabel(r'$T$ [K]')
cb.ax.set_xlim(0, 25)
fig.savefig(f'colorbar.pdf', dpi = 100)

def smooth(seq, window):
    out = []
    for i in range(len(seq)):
        out.append(np.mean(seq[max(0, int(i-window/2)): min(len(seq)-1, int(i+window/2))]))
    return np.array(out)

window = 10
for data_name in data:
    for exp, exp_data in data[data_name].items():
        fig_size, ax_size = plot_arg((0.5, 0.5), width_in, (0.03, 0.04), (data_name == 'pris', exp == 'Hall'), (1, exp == 'Hall'), (0.05, 0.05), (0.08, 0.05))
        fig = plt.figure(figsize = fig_size)
        ax = fig.add_axes(ax_size)
        
        for T, Rho in zip(np.flip(exp_data['Ts'], axis = 0), np.flip(exp_data['Rhos'], axis = 0)):
            if T > 25:
                continue
            ax.plot(Bs, smooth(Rho, window) * 1E6, '-', color = colors[int(T)])
        ax.set_xlim(0, 9)
        
        if exp != 'Hall':
            ax.set_xticklabels([])
        else:
            ax.set_xlabel('$B$ [T]')

        if data_name == 'pris':
            ax.set_ylabel('$\\rho$ [$\mu\Omega\cdot$m]')
            ax.yaxis.set_label_coords(-ax_size[0], 0.5)

        fig.savefig(f'Rho_{exp}_{data_name}.pdf', dpi = 100)

        if exp == 'Hall':
            continue

        MRs = (exp_data['Rhos'] / exp_data['Rhos'][:, :1] - 1) * 100

        fig_size, ax_size = plot_arg((0.5, 0.5), width_in, (0.03, 0.04), (data_name == 'pris', exp == 'Perp'), (1, exp == 'Perp'), (0.05, 0.05), (0.08, 0.05))
        
        fig = plt.figure(figsize = fig_size)
        ax = fig.add_axes(ax_size)
        
        for T, MR in zip(np.flip(exp_data['Ts'], axis = 0), np.flip(MRs, axis = 0)):
            if T > 25:
                continue
            ax.plot(Bs, smooth(MR, window), '-', color = colors[int(T)])

        ax.set_xlim(0, 9)
        if exp != 'Perp':
            ax.set_xticklabels([])
        else:
            ax.set_xlabel('$B$ [T]')

        if data_name == 'pris':
            ax.set_ylabel('MR [\%]')
            ax.yaxis.set_label_coords(-ax_size[0], 0.5)

        fig.savefig(f'MR_{exp}_{data_name}.pdf', dpi = 100)



