class Polygon():
    def __init__(self):
        self.vertcies = []

    def add_vertex(self,point):
        self.vertcies.append(point)

    def plot(self,fig,ax):
        verts = self.vertcies + [self.vertcies[0]]
        ax.plot([p[0] for p in verts], [p[1] for p in verts])