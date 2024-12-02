class Snapshot():
    def __init__(self,kernel_point,puzzle,options) -> None:
        self._kernel_point = kernel_point
        self._puzzle = puzzle
        self._options = options
    
    @property
    def kernel_point(self):
        return self._kernel_point
    
    @property
    def puzzle(self):
        return self._puzzle

    @property
    def options(self):
        return self._options
    
    def __repr__(self) -> str:
        return str(self.kernel_point)

    def is_tried_all_paths(self,next_choice_index):
        return next_choice_index >= len(self.options)

class HistoryManager():
    def __init__(self):
        self.choices_history_at_snap = {}
        self.tilings_at_snap = {}

    def is_recorded(self,snap_repr):
        return snap_repr in self.choices_history_at_snap.keys()

    def head_availiable(self,snap_repr):

        if not self.is_recorded(snap_repr):
            self.choices_history_at_snap[snap_repr] = 0
        #     tiling = None
        # else:
        #     tiling = self.tilings_at_snap[snap_repr]

        tiling_index = self.choices_history_at_snap[snap_repr]
        
        return tiling_index#,tiling

    def next_availiable(self,snap_repr):
        choice = self.head_availiable(snap_repr)
        self.choices_history_at_snap[snap_repr] +=1
        return choice

    def clear(self,remember_keys):
        new_choices_dict = {}
        new_tiling_dict = {}

        for _key in remember_keys:
            if _key in self.choices_history_at_snap.keys() and _key in self.tilings_at_snap.keys():
                new_choices_dict[_key] = self.choices_history_at_snap[_key]
                new_tiling_dict[_key] = self.tilings_at_snap[_key]
        
        self.choices_history_at_snap = new_choices_dict
        self.tilings_at_snap = new_tiling_dict
    
    def record_tilings(self,snap_repr,tilings:list):
        self.tilings_at_snap[snap_repr] = tilings
    
    def get_recorded_tilings(self,snap_repr):
        return self.tilings_at_snap[snap_repr]


class Choice():
    def __init__(self,val,name,is_single=False) -> None:
        if isinstance(val,list): # This should be list of pieces
            self.name = name
            if is_single:
                self.name = "s"
            self.val = val
        if isinstance(val,str):
            self.name = "p"
            self.val = None
    
    def __repr__(self) -> str:
        return self.name
        