# -*- coding: utf-8 -*-

from common.AppConfig import AppConfig
from common.Logger import logger_factory
from data_prepare.BaseRepository import BaseRepository
from data_prepare.utils import config
from data_prepare.utils import format_tushare_date
from data_prepare.utils import tushare
from data_prepare.utils import tushare_api

ts = tushare_api()
_logger = logger_factory(__name__)


def prepare_fund_index():
    """get index fund data and persist into mysql"""
    fund_pool = ["399300.SZ"]
    years = range(2018, 2020)
    months = range(1, 13)

    fund_index_repo = FundIndexRepository(config)

    for fund in fund_pool:
        for year in years:
            for month in months:
                _logger.info(f"Begin to load Index Fund [{fund}] on [{year}/{month}]...")
                funds_result = list(get_month_index(fund, year, month))
                fund_index_repo.insert(funds_result)


@tushare()
def get_month_index(index_code, year, month):
    start = "%04d%02d01" % (year, month)
    end = "%04d%02d28" % (year, month)
    df = ts.pro_api().index_weight(index_code=index_code, start_date=start, end_date=end)
    for idx, row in df.iterrows():
        yield FundIndex(
            row["index_code"],
            row["con_code"],
            format_tushare_date(row["trade_date"]),
            row["weight"])


class FundIndex:

    def __init__(self,
                 index_code,
                 con_code,
                 trade_date,
                 weight):
        self.index_code = index_code
        self.con_code = con_code
        self.trade_date = trade_date
        self.weight = weight

    def __str__(self):
        return f"{self.index_code}, {self.con_code}, {self.trade_date}, {self.weight}"


class FundIndexRepository(BaseRepository):

    def __init__(self, cfg: AppConfig):
        super().__init__(cfg)

    def insert(self, items):
        """items is a list of FundIndex"""
        sql = """INSERT INTO `fund_index` (
                    `index_code`, 
                    `con_code`,
                    `trade_date`,
                    `weight`)
                VALUES (%s, %s, %s, %s)"""
        args_list = [(item.index_code, item.con_code, item.trade_date, item.weight) for item in items]
        super()._insert(sql, args_list)

    def get_all_consist_stocks(self, index_code, year_start, year_end):
        sql = "SELECT DISTINCT `con_code` FROM `fund_index` " \
              "WHERE `index_code`=%s and YEAR(`trade_date`) between %s and %s"
        args = (index_code, year_start, year_end)
        results = super()._query_all(sql, args)
        return list(map(lambda r: r["con_code"], results))


if __name__ == '__main__':
    # prepare_fund_index()
    fund_index_repo = FundIndexRepository(config)
    all_stocks = fund_index_repo.get_all_consist_stocks("399300.SZ", 2015, 2016)
    print(all_stocks)
