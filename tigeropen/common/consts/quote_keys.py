# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class QuoteChangeKey(Enum):
    timestamp = 'timestamp'
    latest_price = 'latestPrice'
    prev_close = 'preClose'
    volume = 'volume'
    open = 'open'
    high = 'high'
    low = 'low'
    close = 'close'
    ask_price = 'askPrice'
    ask_size = 'askSize'
    bid_price = 'bidPrice'
    bid_size = 'bidSize'
    minute = 'mi'


@unique
class QuoteKeyType(Enum):
    ALL = None  # 所有行情数据
    QUOTE = 'askPrice,askSize,bidPrice,bidSize'  # 盘口数据
    TRADE = 'open,high,low,close,preClose,volume,latestPrice'  # 成交数据
    TIMELINE = 'mi'  # 分钟数据
