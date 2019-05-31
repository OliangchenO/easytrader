# -*- coding: utf-8 -*-
import logging
from datetime import datetime
import os

log = logging.getLogger("easytrader")
log.setLevel(logging.DEBUG)
log.propagate = False

fmt = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(filename)s %(lineno)s: %(message)s"
)

date_str = datetime.now().strftime("%Y-%m-%d")
# 获取当前文件路径
current_path = os.path.abspath(__file__)
# 获取当前文件的父目录
father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
log_file = os.path.join(father_path, 'logs', date_str + ".log")
fh = logging.handlers.TimedRotatingFileHandler(log_file, 'midnight', 1, 3)
fh.setFormatter(logging.Formatter(fmt))
log.handlers.append(fh)

ch = logging.StreamHandler()
ch.setFormatter(fmt)
log.handlers.append(ch)
