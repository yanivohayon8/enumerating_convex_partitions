from src.puzzle_creators.power_group.primary import PowerGroupCreator
from src.data_structures import Point
from src.data_structures.shapes import Polygon
import re
import logging
from src import setup_logger

log_handler = setup_logger.get_file_handler(setup_logger.get_debug_log_file())
logger = logging.getLogger("logger.power_group")
logger.addHandler(log_handler)

class PowerGroupRestore(PowerGroupCreator):

    def __init__(self,output_dir,log_path):
        super().__init__(output_dir)
        self.polygons_to_create = []

        with open(log_path) as f:
            f = f.readlines()

            for line in f:
                if "Next Polygon to create is" in line:
                    polygon = []
                    vertices_str = re.findall("(\([\s\d,\-.]*\);)",line) # E.g.(1.0,1.0);(11.0,5.0);(5.0,5.0);(2.0,4.0);
                    for vert_str in vertices_str:
                        vert_str = re.sub(r"[;()]","",vert_str)
                        values = vert_str.split(",")
                        vert = Point(float(values[0]),float(values[1]))
                        polygon.append(vert)
                    self.polygons_to_create.append(Polygon(polygon))
    
    def _create_rgon(self, possible_rgons):
        if len(self.polygons_to_create)>0:
            next_poly = self.polygons_to_create.pop(0)

            if any(next_poly.equals(poly) for poly in possible_rgons):
                logger.debug(f"Restoring polygon {str(next_poly)} for the creation procedure")
                
                # if len(optional_rgons) > 1:
                # self._decision_stack_head().history.append(next_poly)
                return next_poly
            
            logger.debug(f"Attempt to restore polygon {str(next_poly)} but it is not availiable")
        return super()._create_rgon(possible_rgons)
