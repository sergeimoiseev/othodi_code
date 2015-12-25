# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import mpld3 # in a brouser

## Installed LaTeX needed for cyrilic text
# from matplotlib import rc
# font = {'family': 'Droid Sans',
#         'weight': 'normal',
#         'size': 14}

from transliterate import translit
def tr_ru(str_):
	trans_str = translit(str_,'ru',reversed=True)
	return trans_str

fig = plt.figure("caption",figsize=(10,10))
ax = fig.add_subplot(111)
title_text = tr_ru(u"Характерные масштабы задачи управления распределением отходов")
ax.set_title(title_text)
ax.set_xlabel(tr_ru(u'Время, ч'))
ax.set_ylabel(tr_ru(u'Вес, кг'))
xy_pairs = [(1,1),(1,10),(1e1,10),(1e2,100),(1e3,1e5)]
annotations=[u"Масштаб\nотходов",u"Масштаб\nперевозок",u"Масштаб\nпроизводственных\nсмен",u"Масштаб\nпроизводственных\nциклов",u"Масштаб\nпланирования\nпроизводства"]
annotations = [tr_ru(ann) for ann in annotations]
point_size = 50

import itertools
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

color_iter_lines=iter(cm.rainbow(np.linspace(0,1,len(xy_pairs))))
color_iter_points=iter(cm.rainbow(np.linspace(0,1,len(xy_pairs))))
for points_pair in pairwise(xy_pairs):
	x_list = [points_pair[0][0],points_pair[1][0]]
	y_list = [points_pair[0][1],points_pair[1][1]]
	c=next(color_iter_lines)
	ax.loglog(x_list,y_list,ls='-',lw=point_size,alpha=0.5,solid_capstyle='round',color=c)

for pair in xy_pairs:
	c=next(color_iter_points)
	print("color = %s" % c)
	ax.loglog(pair[0],pair[1],marker='o',ms=point_size,mec='None',alpha=1,color=c)

for i, txt in enumerate(annotations):
    ax.annotate(txt, (xy_pairs[i][0],xy_pairs[i][1]))

y_sublist = [xy_pairs[i][1] for i in range(len(xy_pairs))]
x_sublist = [xy_pairs[i][0] for i in range(len(xy_pairs))]
ax.set_autoscaley_on(False)
ax.set_xlim([0.1*min(x_sublist),10*max(x_sublist)]) # must be after plot
ax.set_ylim([0.1*min(y_sublist),10*max(y_sublist)]) # must be after plot

# plt.show()
mpld3.show()
print("end")
# print(y_sublist)
