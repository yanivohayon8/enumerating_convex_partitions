import os
import logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("logger")

def get_file_handler(filepath,**kwargs):
    log_handler = logging.FileHandler(filepath,**kwargs)
    # log_handler.setLevel(logging.DEBUG)
    log_handler.setLevel(logging.ERROR)
    log_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    return log_handler

current_working_dir = os.getcwd()
__debug_dir__ = os.path.join(current_working_dir,"data","debug_powergroup_creator","simple_square") #os.path.join(current_working_dir,"data","debug_random_creator","last_run") 

def get_cwd():
    return os.getcwd()

def get_debug_lastrun_dir():
    global __debug_dir__
    return __debug_dir__

def get_debug_log_file():
    dir = get_debug_lastrun_dir()
    return os.path.join(dir,"run.log")

def set_debug_lastrun_dir(folder):
    global __debug_dir__
    __debug_dir__ = folder