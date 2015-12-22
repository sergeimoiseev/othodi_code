# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection


fig = plt.figure("caption",figsize=(10,10))
ax1 = fig.add_subplot(111)
ax1.set_title("text")

# add an ellipse
ellipse = mpatches.Ellipse([0.5,0.5], 0.2, 0.1)
collection = PatchCollection([ellipse], cmap=plt.cm.hsv, alpha=0.3)
# collection.set_array(np.array(colors))
ax1.add_collection(collection)

x= 0.3
y= 0.3
ax1.plot(x,y,marker='o',ms=50,mfc=(1.,0.,0.,0.5),mec='None',alpha=0.5)

plt.show()
print("end")
# print("test2")
# patches.append(ellipse)
# label(grid[4], "Ellipse")

# plt.subplots_adjust(hspace=0.4)
# t = np.arange(0.01, 20.0, 0.01)

# log y axis
# plt.subplot(221)
# plt.semilogy(t, np.exp(-t/5.0))
# plt.title('semilogy')
# plt.grid(True)

# # log x axis
# plt.subplot(222)
# plt.semilogx(t, np.sin(2*np.pi*t))
# plt.title('semilogx')
# plt.grid(True)

# # log x and y axis
# plt.subplot(223)
# plt.loglog(t, 20*np.exp(-t/10.0), basex=2)
# plt.grid(True)
# plt.title('loglog base 4 on x')

# # with errorbars: clip non-positive values
# ax = plt.subplot(224)
# ax.set_xscale("log", nonposx='clip')
# ax.set_yscale("log", nonposy='clip')

# x = 10.0**np.linspace(0.0, 2.0, 20)
# y = x**2.0
# plt.errorbar(x, y, xerr=0.1*x, yerr=5.0 + 0.75*y)
# ax.set_ylim(ymin=0.1)
# ax.set_title('Errorbars go negative')


plt.show()