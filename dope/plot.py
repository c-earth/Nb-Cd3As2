import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Times'
mpl.rcParams['font.size'] = '9'

width_pt = 246
width_in = width_pt/72.27

bulk_beam_path = 'D:/python_project/Cd3As2/data/beam/bulk_beam.csv'
surf_beam_path = 'D:/python_project/Cd3As2/data/beam/surf_beam.csv'

bulk_beam = np.genfromtxt(bulk_beam_path, delimiter = ',')
surf_beam = np.genfromtxt(surf_beam_path, delimiter = ',')

plt.figure(figsize = (width_in, 3*width_in/4))
plt.plot(surf_beam[:, 0], surf_beam[:, 1], '.-', label = '25 keV')
plt.plot(bulk_beam[:, 0], bulk_beam[:, 1], '.-', label = '200 keV')
plt.ylim(0, 5E20)
plt.xlim(0, 1000)
plt.xlabel('Sample Depth [$\AA$]')
plt.ylabel('Nb Concentration [atoms/cm$^3$]')
plt.legend(title = 'Ion Energy')
plt.tight_layout()
plt.savefig('test.png', dpi = 300)
