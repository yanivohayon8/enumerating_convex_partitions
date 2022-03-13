from email.mime import base
from src.data_structures.lines import Segment as GeneralSegment
from src.hypothesis.rgon_1988 import turn
from src.data_structures import Point


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

class Segment(GeneralSegment):
    
    def __init__(self,upper_point,lower_point,index=None):
        super().__init__(upper_point,lower_point)
        self.origin_upper_point = self.upper_point
        self.index = index

    def __eq__(self,segment):
        return self.origin_upper_point == segment.origin_upper_point and self.lower_point == segment.lower_point

    def __ne__(self,segment):
        return self.origin_upper_point != segment.origin_upper_point or self.lower_point != segment.lower_point

    def _calc_turn(self,other):
        if isinstance(other,Segment):
            _i = other.lower_point
            _j = other.upper_point
            _k = self.upper_point
            # Avoiding this bug (upper point is common)
            #   /\      ---
            # /    \    |
            if other.is_in_segment(self.upper_point):
                _k = self.lower_point
            return turn(_i,_j,_k)
        
        if isinstance(other,Point):
            return (-1)*turn(self.lower_point,self.upper_point,other)

    def _is_horizontal(self):
        return self.upper_point.y == self.lower_point.y
    
    def _get_turned_over(self):
        # on purose index is not inserted. Then is temporary for turn function
        return Segment(self.lower_point,self.upper_point)

    def _choose_base_segment(self,other):
        '''
            Design for implementing the operators <=,<,>,>=
            By default the self is determine whether is left\right to other.
            Unless, the other is horizontal line so need to view other as opposose to self (switch roles)
        '''
        compared_segment = self
        base_segment = other

        if isinstance(other,Segment):
            # if other is horizontal it cannot be by base measure
            #
            # | ----
            if other._is_horizontal() and not self._is_horizontal():
                compared_segment = other
                base_segment = self._get_turned_over() # get turned because we switch between the compared and base. so right and left to switched (egocentric switched)

        return compared_segment,base_segment

    def __lt__(self,other):
        '''
            Is self is left to other segment\point
        '''
        compared_segment,base_segment = self._choose_base_segment(other)
        return compared_segment._calc_turn(base_segment) > 0 
        
        
    def __le__(self,other):
        '''
            Is self segment is left or in to other segment\point
        '''
        compared_segment,base_segment = self._choose_base_segment(other)
        return compared_segment._calc_turn(base_segment) >= 0 


    def __gt__(self,other):
        '''
            Is self is right to other segment\point
        '''
        compared_segment,base_segment = self._choose_base_segment(other)
        return compared_segment._calc_turn(base_segment) < 0 

    def __ge__(self,other):
        '''
            Is self is right to other segment\point
        '''
        compared_segment,base_segment = self._choose_base_segment(other)
        return compared_segment._calc_turn(base_segment) <= 0 

    def __hash__(self):
        return hash((self.origin_upper_point,self.lower_point))

    def __str__(self):
        return "{0}--{1}".format(self.upper_point,self.lower_point)
        # return "{0}--{1}".format(self.origin_upper_point,self.lower_point) + end

    def get_parent(self):
        return GeneralSegment(self.origin_upper_point,self.lower_point) # MUST DO IT MORE ELEGEANT WITH OOP