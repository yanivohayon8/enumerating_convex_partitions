from enum import Enum

class Direction(Enum):
    left = 1
    right = -1

class Junction():
    
    def __init__(self,kernel_point,from_direction:Direction) -> None:
        self._kernel_point = kernel_point
        self._from_direction = from_direction
    
    def __repr__(self) -> str:
        return f"from {self._from_direction.name} at {str(self._kernel_point)}"

    @property
    def kernel_point(self):
        return self._kernel_point
    
    @property
    def from_direction(self):
        return self._from_direction