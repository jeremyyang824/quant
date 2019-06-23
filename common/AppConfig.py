# -*- coding: utf-8 -*-

from configparser import ConfigParser


class AppConfig:

    def __init__(self):
        self.cp = ConfigParser()
        self.cp.read("../applicaiton.cfg")

    def tushare(self, item):
        return self.__get("tushare", item)

    def database(self, item):
        return self.__get("mysql", item)

    def __get(self, section, item):
        if not section:
            raise Exception("section None error")
        if not item:
            raise Exception("item None error")
        return self.cp[section][item]


if __name__ == '__main__':
    cfg = AppConfig()
    print(cfg.tushare("token"))
    print(cfg.tushare("interval_ms"))
    print(cfg.tushare("retry_count"))
