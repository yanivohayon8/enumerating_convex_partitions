import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from src.data_structures.shapes import Polygon
from src.data_structures import Point
from shapely.geometry import MultiPoint,LineString,MultiLineString
import matplotlib.pyplot as plt


no_simple_poly= Polygon([(100.0, 100.0),(0.0, 0.0),(50.0, 60.0),(0.0, 100.0)])
simple_poly= Polygon([(0.0, 0.0),(80.0, 50.0),(100.0, 100.0),(60.0, 90.0)])
print(no_simple_poly.is_simple)
print(simple_poly.is_simple)

print(simple_poly.centroid)

tr1 = Polygon([(1,1),(2,2),(3,3)])
tr2 = Polygon([(2,2),(1,1),(3,3)])
print(list(tr1.exterior.coords))
print(list(tr2.exterior.coords))

poly = Polygon([(1,2),(3,4),(5,6)])
poly.is_simple()
xs,ys = poly.exterior.coords.xy
[(x,y) for x,y in zip(xs,ys)]

ax = plt.subplot()
line = LineString([(0, 0), (1, 1)])
x, y = line.xy
ax.plot(x, y)
plt.show()

lines = MultiLineString([((1,2),(3,4)),((5,6),(7,8))])

# plot_lines(lines)
xs = []
ys = []
for l in list(lines.geoms):
    x,y = l.coords
    xs.append(x)
    ys.append(y)

plt.plot(xs,ys)

plt.show()

mp = MultiPoint([(1,1),(2,3)])

for p in list(mp):
    print(p)

a = list(mp.coords)

as_tuple = Point((2,2))



p1  = Point(1,1)
p2  = Point(2,2)
p12 = p1 - p2
p21 = p2 - p1

print(p12.x)
print(p12.y)
print(p21.x)
print(p21.y)

x1,y1 = p12.xy
x2,y2 = p21.xy
print(x1[0]-x2[0])
print(x2[0]-x1[0])

pass
