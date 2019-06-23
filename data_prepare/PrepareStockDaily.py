# -*- coding: utf-8 -*-

from common.AppConfig import AppConfig
from common.Logger import logger_factory
from data_prepare.BaseRepository import BaseRepository
from data_prepare.PrepareFundIndex import FundIndexRepository
from data_prepare.utils import config
from data_prepare.utils import format_tushare_date
from data_prepare.utils import tushare
from data_prepare.utils import tushare_api

ts = tushare_api()
_logger = logger_factory(__name__)


def prepare_stock_daily():
    """get daily stock data and persist into mysql"""
    index_code = "399300.SZ"  # 沪深300指数
    year_start = 2005
    year_end = 2019

    # get all consist stocks
    fund_index_repo = FundIndexRepository(config)
    all_stocks = fund_index_repo.get_all_consist_stocks(index_code, year_start, year_end)
    all_stocks_count = len(all_stocks)

    # get all stocks
    stock_daily_repo = StockDailyRepository(config)
    for i, stock_code in enumerate(all_stocks):
        _logger.info(f"Begin to load Stock [{i + 1} / {all_stocks_count}][{stock_code}]...")
        stock_markets_result = list(get_years_daily_market(stock_code, year_start, year_end))  # 单股所有历史日行情（前复权）
        stock_daily_repo.insert(stock_markets_result)


@tushare()
def get_years_daily_market(ts_code, year_start, year_end):
    start = "%04d0101" % year_start
    end = "%04d1231" % year_end
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', start_date=start, end_date=end)  # 前复权
    for idx, row in df.iterrows():
        yield StockDaily(
            row["ts_code"],
            format_tushare_date(row["trade_date"]),
            row["open"],
            row["high"],
            row["low"],
            row["close"],
            row["pre_close"],
            row["vol"],
            row["amount"])


class StockDaily:

    def __init__(self,
                 ts_code,
                 trade_date,
                 open,
                 high,
                 low,
                 close,
                 pre_close,
                 vol,
                 amount):
        self.ts_code = ts_code
        self.trade_date = trade_date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.pre_close = pre_close
        self.vol = vol  # deal volume (hand)
        self.amount = amount  # deal amount (thousand)

    def __str__(self):
        return f"{self.ts_code}, {self.trade_date}, {self.open}, {self.high}, " \
            f"{self.low}, {self.close}, {self.pre_close}, {self.vol}, {self.amount}"


class StockDailyRepository(BaseRepository):

    def __init__(self, cfg: AppConfig):
        super().__init__(cfg)

    def insert(self, items):
        """items is a list of StockDaily"""
        sql = """INSERT INTO `stock_daily` (
                    `ts_code`, 
                    `trade_date`,
                    `open`,
                    `high`,
                    `low`,
                    `close`,
                    `pre_close`,
                    `vol`,
                    `amount`)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        args_list = [(item.ts_code, item.trade_date, item.open, item.high, item.low, item.close, item.pre_close,
                      item.vol, item.amount) for item in items]
        super()._insert(sql, args_list)


if __name__ == '__main__':
    prepare_stock_daily()
