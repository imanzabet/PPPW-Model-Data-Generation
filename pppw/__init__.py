import random
random.seed(22)
import json
import logging
import logging.config
import os
import platform
import time
import configparser
from .data_processing import DfProcss
from .unos_process import Unos_Prep
from .pppw_generator import PPPW_Generator

parser = configparser.ConfigParser()
# check if in notebook mode then set path for config files
def is_in_ipynb():
    from ipykernel.zmqshell import ZMQInteractiveShell as Zshell
    try:
        if get_ipython():
            return True
        else:
            return False
    except NameError:
        return False

if is_in_ipynb():
    import os, sys
    FLAG_Ipynb = True
    module_path = os.path.abspath("./pppw/")
#     if module_path not in sys.path:
#         sys.path.append(module_path)
#         # print(module_path + ' is set for notebook!')
#     else:
#         print(module_path + ' found in sys.path')
#     module_path = os.path.abspath(os.path.join('../..'))
#     if module_path not in sys.path:
#         sys.path.append(module_path)
#         # print(module_path + ' is set for notebook!')
#     else:
#         print(module_path + ' found in sys.path')
else:
    FLAG_Ipynb = False
    module_path = os.path.abspath("./")
config_file = os.path.join(module_path,'config.ini')
if parser.read(config_file)==[]:
    if FLAG_Ipynb:
        if parser.read(config_file) == []:
            raise ValueError ('could not find config_general file!')
    if  parser.read('pppw/'+config_file)!=[]:
        pass
    else:
        raise ValueError ('could not find config file!')


if platform.system() == 'Windows':
    FLAG_OS = 'win'
    data_path = parser['win']['data_path']
elif (platform.system() == 'Linux'):
    FLAG_OS = 'linux'
    data_path = parser['linux']['data_path']


dataset_file = parser['default']['dataset_file']
unos_file = parser['default']['unos_file']

# logger = logging.getLogger(__name__)
milisecond = int(round(time.time() * 1000))
# logging.basicConfig(
#     level=logging.INFO,
#     filename="logfilename.log",
#     format='%(asctime)s %(levelname)s %(message)s',
#     handlers = [
#         logging.FileHandler("{0}/{1}.log".format(data_path, 'logger_'+str(milisecond))),
#         logging.StreamHandler()
#     ])
# logger = logging.getLogger(__name__)

# set up logging to file

logging.basicConfig(
     filename='log_file.log',
     level=logging.INFO,
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)


def init_params(**kwargs):
    d = dict(parser['default'])
    d.update(dict(parser[FLAG_OS]))
    d.update(kwargs)
    return d