# to import this module insert the following in the submodule:
# sys.path.insert(0, os.getcwd()+'/f1_pipeline')

import logging
import os

logging.basicConfig( 
     handlers=[
        logging.FileHandler(os.getcwd() + '/f1_pipeline/logs/update_db.log'),
        logging.StreamHandler()
    ],
    level = logging.DEBUG, 
    format = '%(levelname)s:  %(asctime)s:  %(process)s: %(module)s: %(lineno)d: %(funcName)s:  %(message)s')

logger = logging.getLogger(__file__)


