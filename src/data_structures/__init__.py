import numpy as np


class Point(object):
    def __init__(self,x,y): #*args):
        self.x = float(round(x,2))
        self.y = float(round(y,2))
        # if len(args) == 2:
        #     self.x = args[0]
        #     self.y = args[1]
        # if len(args) == 1:
        #     tuple_ = eval(args[0])
        #     self.x = args[tuple_[0]]
        #     self.y = args[tuple_[1]]

    def get_as_tuple(self):
        return (self.x,self.y)

    def get_as_np(self):
        return np.asarray([self.x,self.y])

    def __eq__(self,p):
        return self.x==p.x and self.y==p.y
    
    def __ne__(self,p):
        return not (self.x == p.x and self.y==p.y)
    
    def __hash__(self):
        return hash(self.get_as_tuple())

    @staticmethod
    def scatter_points(ax,points,color="blue"):
        xs = [point.x for point in points]
        ys = [point.y for point in points]

        ax.scatter(xs,ys,color=color)

    def __sub__(self,p):
        if isinstance(p, Point):
            return Point(self.x-p.x,self.y-p.y)

    def __str__(self):
        return "({0},{1})".format(self.x,self.y) #"(" + str(self.x) +","+str(self.y)+")"




