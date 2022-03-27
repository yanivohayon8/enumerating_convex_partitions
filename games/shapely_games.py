from shapely.geometry import Polygon,Point,MultiPoint

mp = MultiPoint([(1,1),(2,3)])

for p in list(mp):
    print(p)

a = list(mp.coords)

as_tuple = Point((2,2))

poly = Polygon([(1,1),(2,2),(6,1)])
bla = poly.exterior.coords.xy

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
