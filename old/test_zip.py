coord_pairs = [(1,1.1),(2,2.2),(3,3.3),(4,4.4),(5,5.5)]

x_all=[]
y_all=[]
for i,point in enumerate(coord_pairs):
    lon = point[-1]
    lat = point[0]
    x,y = lon,lat
    x_all.append(x)
    y_all.append(y)
print(x_all)
print(y_all)