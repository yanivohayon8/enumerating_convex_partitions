import os
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("logger")

def get_file_handler(filepath,**kwargs):
    log_handler = logging.FileHandler(filepath,**kwargs)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
    return log_handler

def get_debug_dir():
    current_working_dir = os.getcwd()
    return os.path.join(current_working_dir,"data","debug","last_run")

def get_debug_log_file():
    dir = get_debug_dir()
    return os.path.join(dir,"run.log")
