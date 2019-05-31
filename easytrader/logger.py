import logging
from conda.cli.main_config import format_dict


# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger:
    def __init__(self, log_name, log_level, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(log_level)

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(log_name)
        fh.setLevel(log_level)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(filename)s %(lineno)s: %(message)s"
        )
        fh.setFormatter(fmt)
        ch.setFormatter(fmt)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger
