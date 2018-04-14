# -*- coding:UTF-8 -*-
from enum import Enum
import sys
import inspect
from datetime import datetime

class LogLevel(Enum):
    Debug = 0
    Info = 1
    Warn = 2
    Error = 3
    Fatal = 4

class LogUtil:
    def __init__(self, enable=True, level=LogLevel.Debug):
        self.enable = enable
        self.level = level

    def __level_label(self, level):
        if level == LogLevel.Debug:
            return 'DEBUG'
        elif level == LogLevel.Info:
            return 'INFO'
        elif level == LogLevel.Warn:
            return 'WARN'
        elif level == LogLevel.Error:
            return 'ERROR'
        elif level == LogLevel.Fatal:
            return 'FATAL'

    def __common_header(self, level):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        all_stack = inspect.stack()
        if len(all_stack) >= 5:
            caller = all_stack[4]
            file_name = caller.filename
            func_name = caller.function
            line = str(caller.lineno)
        else:
            file_name = sys._getframe().f_code.co_filename
            func_name = sys._getframe().f_code.co_name
            line = str(sys._getframe().f_lineno)
        level_label = self.__level_label(level)
        return "%s: %s/%s|%s(%s)" % (now_time[:-3], level_label, file_name, func_name, line)

    def __print_log(self, msg, level):
        print("%s: %s" % (self.__common_header(level), msg))

    def __print_internal(self, msg, level):
        if self.enable and self.level.value <= level.value:
            self.__print_log(msg, level)

    def d(self, msg):
        self.__print_internal(msg, LogLevel.Debug)

    def i(self, msg):
        self.__print_internal(msg, LogLevel.Info)

    def w(self, msg):
        self.__print_internal(msg, LogLevel.Warn)

    def e(self, msg):
        self.__print_internal(msg, LogLevel.Error)

    def f(self, msg):
        self.__print_internal(msg, LogLevel.Fatal)

WLog = LogUtil()

def segment():
    print("=================================================================")
