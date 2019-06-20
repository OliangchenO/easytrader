from datetime import datetime
import logging.handlers
import logging
import os
import sys


def script_path():
    path = os.path.realpath(sys.argv[0])
    if os.path.isfile(path):
        path = os.path.dirname(path)
    return os.path.abspath(path)


LOGGING_MSG_FORMAT = "%(asctime)s [%(levelname)s] %(filename)s %(lineno)s: %(message)s"
LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO, format=LOGGING_MSG_FORMAT, datefmt=LOGGING_DATE_FORMAT)
log = logging.getLogger("easytrader")
log.propagate = False

#文件日志
log_path = os.path.join(script_path(), 'logs')
if not os.path.exists(log_path):
    os.makedirs(log_path)
file_name = datetime.now().strftime("%Y-%m-%d") + ".log"
log_file = os.path.join(log_path, file_name)
fh = logging.handlers.TimedRotatingFileHandler(log_file, 'midnight', 1, 3)
fh.suffix = '%Y%m%d.log'
fh.setFormatter(logging.Formatter(LOGGING_MSG_FORMAT))
log.handlers.append(fh)

#控制台日志
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(LOGGING_MSG_FORMAT))
log.handlers.append(ch)
