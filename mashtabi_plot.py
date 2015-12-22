# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from transliterate import translit
import matplotlib.cm as cm

## Installed LaTeX needed for cyrilic text
# from matplotlib import rc
# font = {'family': 'Droid Sans',
#         'weight': 'normal',
#         'size': 14}

print(24*265)

fig = plt.figure("caption",figsize=(10,10))
ax = fig.add_subplot(111)
title_text = translit(u"Характерные масштабы задачи управления распределением отходов",'ru',reversed=True)
ax.set_title(title_text)
ax.set_xlabel(translit(u'Время, ч','ru',reversed=True))
ax.set_ylabel(translit(u'Вес, кг','ru',reversed=True))
xy_pairs = [(1,1),(1e3,1),(1e3,10),(1e3,100),(1e3,1e5)]


# colors = list(cm.rainbow(np.linspace(0, 1, len(xy_pairs))))
# for y, c in zip(xy_pairs, colors):
#     plt.scatter(x, y, color=c)
# print(colors)
point_size = 50

import itertools
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

color_iter_lines=iter(cm.rainbow(np.linspace(0,1,len(xy_pairs))))
color_iter_points=iter(cm.rainbow(np.linspace(0,1,len(xy_pairs))))
# color=iter(cm.rainbow(np.linspace(0,1,len(xy_pairs))))
for points_pair in pairwise(xy_pairs):
# for points_pair,col in zip(pairwise(xy_pairs), colors[0:len(xy_pairs)-1]):
	x_list = [points_pair[0][0],points_pair[1][0]]
	y_list = [points_pair[0][1],points_pair[1][1]]
	# ax.loglog(x_list,y_list,ls='-',lw=point_size,alpha=0.5,solid_capstyle='round',color=col)
	c=next(color_iter_lines)
	ax.loglog(x_list,y_list,ls='-',lw=point_size,alpha=0.5,solid_capstyle='round',color=c)
	# line.set_solid_capstyle('round')

# color_iter=iter(['r','g','b','c','m',])
# colors1 = list(cm.rainbow(np.linspace(0, 1, len(xy_pairs))))
for pair in xy_pairs:
# for pair,col in zip(xy_pairs, colors1[0:len(xy_pairs)]):
	c=next(color_iter_points)
	print("color = %s" % c)
	ax.loglog(pair[0],pair[1],marker='o',ms=point_size,mec='None',alpha=1,color=c)
	# ax.loglog(pair[0],pair[1],marker='o',ms=point_size,mfc=(1.,0.,0.,0.5),mec='None',alpha=1,color =col)

y_sublist = [xy_pairs[i][1] for i in range(len(xy_pairs))]
x_sublist = [xy_pairs[i][0] for i in range(len(xy_pairs))]
ax.set_autoscaley_on(False)
ax.set_xlim([0.1*min(x_sublist),10*max(x_sublist)]) # must be after plot
ax.set_ylim([0.1*min(y_sublist),10*max(y_sublist)]) # must be after plot

plt.show()
print("end")
# print(y_sublist)
