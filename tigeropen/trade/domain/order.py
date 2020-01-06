# -*- coding: utf-8 -*-
"""
Created on 2018/9/20

@author: gaoan
"""
from six import text_type
from tigeropen.common.consts import OrderStatus

ORDER_FIELDS_TO_IGNORE = {'type', '_status', 'contract', '_remaining'}


class Order(object):
    __slots__ = ["account", "id", "order_id", "parent_id", "order_time", "reason", "trade_time", "contract", "action",
                 "quantity", "filled", "_remaining", "avg_fill_price", "commission", "realized_pnl", "_status",
                 "trail_stop_price", "limit_price", "aux_price", "trailing_percent", "percent_offset", "action",
                 "order_type", "time_in_force", "outside_rth", "attach_type", "stop_loss_price", "stop_loss_tif",
                 "stop_loss_rth", "stop_loss_order_id", "profit_taker_price", "profit_taker_tif", "profit_taker_rth",
                 "profit_taker_order_id"]

    def __init__(self, account, contract, action, order_type, quantity, limit_price=None, aux_price=None,
                 trail_stop_price=None, trailing_percent=None, percent_offset=None, time_in_force=None,
                 outside_rth=None, filled=0, avg_fill_price=0, commission=None, realized_pnl=None,
                 id=None, order_id=None, parent_id=None, order_time=None, trade_time=None,
                 attach_type=None, stop_loss_price=None, stop_loss_tif=None, stop_loss_rth=None,
                 stop_loss_order_id=None, profit_taker_price=None, profit_taker_tif=None, profit_taker_rth=None,
                 profit_taker_order_id=None):
        """
        - account: 订单所属的账户
        - id: 全局订单 id
        - order_id: 账户自增订单号
        - parent_id: 主订单id, 目前只用于 TigerTrade App端的附加订单中
        - order_time: 下单时间
        - reason: 下单失败时, 会返回失败原因的描述
        - trade_time: 最新成交时间
        - action: 交易方向, 'BUY' / 'SELL'
        - quantity: 下单数量
        - filled: 成交数量
        - avg_fill_price: 包含佣金的平均成交价
        - commission: 包含佣金, 印花税, 证监会费等系列费用
        - realized_pnl: 实现盈亏
        - trail_stop_price: 跟踪止损单--触发止损单的价格
        - limit_price: 限价单价格
        - aux_price: 在止损单中, 表示出发止损单的价格, 在移动止损单中, 表示跟踪的价差
        - trailing_percent:  跟踪止损单-百分比, 取值范围为0-100
        - percent_offset: None,
        - order_type: 订单类型, 'MKT' 市价单 / 'LMT' 限价单 / 'STP' 止损单 / 'STP_LMT' 止损限价单 / 'TRAIL' 跟踪止损单
        - time_in_force: 有效期,'DAY' 日内有效 / 'GTC' 撤销前有效
        - outside_rth: 是否允许盘前盘后交易(美股专属). True 允许, False 不允许
        - contract: 合约对象
        - status: Order_Status 的枚举, 表示订单状态
        - remaining: 未成交的数量

        - attach_type: 附加订单类型(仅限价单支持附加订单). PROFIT 止盈单类型,  LOSS 止损单类型, BRACKETS 括号订单类型(止损和止盈)
        - stop_loss_price: 附加止损单价格
        - stop_loss_tif: 附加止损单有效期. 同 time_in_force 字段. 'DAY' 日内有效 / 'GTC' 撤销前有效
        - stop_loss_rth: 附加止损单是否允许盘前盘后交易(美股专属). True 允许, False 不允许. 同 outside_rth 字段
        - stop_loss_order_id: 附加止损单号. 可以通过订单号接口获取, 如果传0或为空, 则服务器端会自动生成止损单号
        - profit_taker_price: 附加止盈单价格
        - profit_taker_tif: 附加止盈单有效期. 同 time_in_force 字段. 'DAY' 日内有效 / 'GTC' 撤销前有效
        - profit_taker_rth: 附加止盈单是否允许盘前盘后交易(美股专属). True 允许, False 不允许. 同 outside_rth 字段
        - profit_taker_order_id: 附加止盈单号. 可以通过订单号接口获取, 如果传0或为空, 则服务器端会自动生成止盈单号
        """

        self.id = id
        self.order_id = order_id
        self.parent_id = parent_id
        self.account = account
        self.reason = None
        self.contract = contract
        self.action = action
        self.quantity = quantity
        self.filled = filled
        self._remaining = None
        self.avg_fill_price = avg_fill_price
        self.realized_pnl = realized_pnl
        self.commission = commission
        self._status = OrderStatus.NEW
        self.time_in_force = time_in_force
        self.outside_rth = outside_rth
        self.order_type = order_type
        self.limit_price = limit_price
        self.aux_price = aux_price
        self.trail_stop_price = trail_stop_price
        self.trailing_percent = trailing_percent
        self.percent_offset = percent_offset
        self.order_time = order_time
        self.trade_time = trade_time
        self.attach_type = attach_type
        self.stop_loss_price = stop_loss_price
        self.stop_loss_tif = stop_loss_tif
        self.stop_loss_rth = stop_loss_rth
        self.stop_loss_order_id = stop_loss_order_id
        self.profit_taker_price = profit_taker_price
        self.profit_taker_tif = profit_taker_tif
        self.profit_taker_rth = profit_taker_rth
        self.profit_taker_order_id = profit_taker_order_id

    def to_dict(self):
        dct = {name: getattr(self, name) for name in self.__slots__ if name not in ORDER_FIELDS_TO_IGNORE}

        dct['contract'] = self.contract
        if self.status:
            dct['status'] = self.status.name
        dct['remaining'] = self.remaining

        return dct

    @property
    def status(self):
        if not self.remaining and self.filled:
            return OrderStatus.FILLED
        elif self._status == OrderStatus.HELD and self.filled:
            return OrderStatus.PARTIALLY_FILLED
        else:
            return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def active(self):
        return self.status in [OrderStatus.PENDING_NEW, OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED,
                               OrderStatus.HELD, OrderStatus.PENDING_CANCEL]

    @property
    def remaining(self):
        return self.quantity - self.filled

    def __repr__(self):
        """
        String representation for this object.
        """
        return "Order(%s)" % self.to_dict().__repr__()

    def __unicode__(self):
        """
        Unicode representation for this object.
        """
        return text_type(repr(self))
