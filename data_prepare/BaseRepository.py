# -*- coding: utf-8 -*-


import pymysql

from common.AppConfig import AppConfig
from common.Logger import logger_factory


class BaseRepository:

    def __init__(self, cfg: AppConfig):
        self.cfg = cfg
        self.logger = logger_factory(__name__)

    def _insert(self, sql, arg_list):
        if not arg_list or len(arg_list) < 1: return
        connection = self._get_connection()
        try:
            # insert item list within a connection
            for arg in arg_list:
                with connection.cursor() as cursor:
                    cursor.execute(sql, arg)
                connection.commit()
        except Exception as ex:
            self.logger.error(f"Mysql insert failed: {ex}. \r\n {sql}")
        finally:
            connection.close()

    def _query_all(self, sql, args):
        connection = self._get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                results = cursor.fetchall()
                return results
        except Exception as ex:
            self.logger.error(f"Mysql query failed: {ex}. \r\n {sql}")
        finally:
            connection.close()

    def _get_connection(self):
        connection = pymysql.connect(
            host=self.cfg.database("host"),
            user=self.cfg.database("user"),
            password=self.cfg.database("passwd"),
            db=self.cfg.database("db"),
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
        return connection
