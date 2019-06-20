#!/usr/bin/env python
# coding=utf-8
import logging
import time


class Logger(object):
    """
        This is the class to wrap logging module
    """

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        self.name = None
        self.path = None
        self.log_name = None
        self.log_path = None
        self.log_file_status = False
        self.terminal_status = False

    def log_init(self, path, name):
        self.name = name
        self.path = path
        self.log_name = self.name + time.strftime('_%Y%m%d%H%M', time.localtime(time.time()))
        self.log_path = self.path + "/" + self.log_name + '.log'

    def save_log(self, close=False):
        log_file = logging.FileHandler(self.log_path, "a")
        log_file.setFormatter(self.formatter)
        log_file.setLevel("INFO")
        if not self.log_file_status:
            self.logger.addHandler(log_file)
            self.log_file_status = True
        if close:
            log_file.close()

    def print_log(self):
        terminal = logging.StreamHandler()
        terminal.setFormatter(self.formatter)
        terminal.setLevel("INFO")
        if not self.terminal_status:
            self.logger.addHandler(terminal)
            self.terminal_status = True

    def handel_log(self):
        self.save_log()
        self.print_log()
        return self.logger


set_log = Logger()

if __name__ == '__main__':
    set_log.log_init("../logger", 'test')
    for i in range(0, 10):
        set_log.handel_log().info("test info")
        set_log.handel_log().error("test error")
        time.sleep(1)
    set_log.save_log(close=True)
