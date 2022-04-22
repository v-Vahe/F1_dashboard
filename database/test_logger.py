# https://towardsdatascience.com/what-to-log-from-python-etl-pipelines-9e0cfe29950e


import logging
import logging.handlers
import os
import psutil
 
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "database/logs.log"))
formatter = logging.Formatter('%(levelname)s:  %(asctime)s:  %(process)s:  %(funcName)s:  %(message)s')
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

logging.info('CPU usage {}%'.format(psutil.cpu_percent()))

try:
    print(sdafds)
except Exception as e:
    logging.error(e)
    # logging.exception("Exception in main()")
    exit(1)
