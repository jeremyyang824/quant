# -*- coding: utf-8 -*-

import datetime
import time

import tushare as ts

from common.AppConfig import AppConfig
from common.Logger import logger_factory

config = AppConfig()

_logger = logger_factory(__name__)
_default_interval_ms = int(config.tushare("interval_ms"))
_default_retry_count = int(config.tushare("retry_count"))


def tushare_api():
    ts.set_token(config.tushare("token"))
    return ts


def tushare(interval_ms=_default_interval_ms, retry_count=_default_retry_count):
    """ Tushare API decorator """

    def wrap(func):
        def make_decorator(*args, **kwargs):
            for _ in range(retry_count):
                try:
                    _logger.info("Begin to call tushare API [" + func.__name__ + "]...")
                    result = func(*args, **kwargs)
                except:
                    time.sleep(interval_ms / 1000)
                else:
                    _logger.info("Success to call tushare API [" + func.__name__ + "].")
                    return result
            _logger.error("Fail to call tushare API [" + func.__name__ + "]!")

        return make_decorator

    return wrap


def format_tushare_date(str_date, target_format="%Y-%m-%d"):
    return (datetime.datetime.strptime(str_date, "%Y%m%d")).strftime(target_format)


if __name__ == '__main__':
    print(format_tushare_date("20180328"))


    @tushare()
    def demo(arg):
        import random
        if random.randint(1, 2) % 2 == 0:
            raise Exception("test")
        return "execute:" + arg


    print(demo("Hello world"))
