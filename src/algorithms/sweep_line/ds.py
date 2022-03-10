from src.data_structures import binary_tree  as binary_tree
from functools import cmp_to_key

class LineStatus(binary_tree.AVL_Tree):

    def __init__(self):
        super().__init__()
        self.root = None

    def insert_segment(self, segment):
        self.root = self.insert(self.root, segment)

    def delete_segment(self,segment):
        self.root = self.delete(self.root,segment)

    def get_segment_on_line(self):
        return self.get_leafs()#super().in_order(self.root)

    def get_leafs(self):
        return None

    def get_neighbors(self,event_point):
        leafs = self.get_segment_on_line()
        neighbor_right,neighbor_left = None,None

        for seg in leafs:
            if seg < event_point:
                neighbor_right = seg
                break
        
        for seg in list(reversed(leafs)):
            if seg > event_point:
                neighbor_left = seg
                break

        return neighbor_left,neighbor_right

    def print(self):
        print("Line Status:", end="\t")
        segments = self.get_segment_on_line()
        [print(seg, end=";") for seg in segments]
        print()


class EventQueue():

    def __init__(self):
        self.queue = []

    def append(self,point):
        self.queue.append(point)
        self.queue = list(set(self.queue)) 
        self.queue = sorted(self.queue,key=cmp_to_key(sorting_order))

    def pop(self):
        return self.queue.pop(0)
    
    def print(self):
        print("Event Queue: ",end="\t")
        [print(event, end=";") for event in self.queue]
        print()



def sorting_order(point1,point2):
    '''
        Sorting mechanism for the event points
        if one have higher y-coordinated it will be sorted first.
        if the y-coordinates are equal, then the one with smaller x-coordinate will be count first
    '''
    if point1.y == point2.y:
        return point1.x-point2.x
    else:
        return point2.y-point1.y 