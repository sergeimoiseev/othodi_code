# -*- coding: utf-8 -*-
# http://matplotlib.org/basemap/users/examples.html
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
# create new figure, axes instances.
fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
# setup mercator map projection.
m = Basemap(llcrnrlon=0.,llcrnrlat=20.,urcrnrlon=80.,urcrnrlat=70.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',projection='merc',\
            lat_0=55.,lon_0=37.,lat_ts=20.)
# nylat, nylon are lat/lon of New York
nylat = 55.7522200; nylon = 37.6155600
# lonlat, lonlon are lat/lon of London.
lonlat = 59.9386300; lonlon = 30.3141300
# draw great circle route between NY and London
m.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='b')
m.drawcoastlines()
m.fillcontinents()
# draw parallels
m.drawparallels(np.arange(-20,0,20),labels=[1,1,0,1])
# draw meridians
m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
ax.set_title('Great Circle from New York to London')
plt.show()