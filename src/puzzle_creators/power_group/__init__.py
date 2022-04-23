from src.data_structures.shapes import Polygon
from src.puzzle_creators import Junction
import itertools

class Snapshot():
    id_iter = itertools.count()

    def __init__(self,junction:Junction,possible_rgon_at,pieces,pieces_area,is_passed_at) -> None:
        self.id = next(self.id_iter)
        self._junction = junction # key
        self._possible_rgon_at = possible_rgon_at #self.last_possible_rgons = last_possible_rgons # maybe is not necessray
        self._pieces = tuple(pieces)
        self._pieces_area = pieces_area
        self._is_passed_at = is_passed_at
    
    def __repr__(self) -> str:
        return f"id:{self.id};{repr(self._junction) }"

    @property
    def junction(self):
        return self._junction
    
    @property
    def possible_rgon_at(self):
        return self._possible_rgon_at#[repr(junction)]

    @property
    def pieces(self):
        return self._pieces

    @property
    def pieces_area(self):
        return self._pieces_area

    @property
    def is_passed_at(self):
        return self._is_passed_at

    def is_tried_all_paths(self,history_choices):
        return len(history_choices) == len(self._possible_rgon_at[repr(self._junction)])


class HistoryManager():

    def __init__(self):
        self.choices_history_at_snap = {}
        self.passed_snapshots = []
    
    def add(self,junction,snapshot_queue,piece):
        for index in range(len(snapshot_queue) - 1,-1,-1):      
            snap_id = repr(snapshot_queue[index])
            # Find the corresponding latest snapshot at queue
            if repr(junction) in repr(snap_id):

                if isinstance(piece,Polygon):
                    if not snap_id in self.choices_history_at_snap.keys():
                        self.choices_history_at_snap[snap_id] = []
            
                    self.choices_history_at_snap[snap_id].append(piece)

                if isinstance(piece,str):
                    self.passed_snapshots.append(snap_id)

                break