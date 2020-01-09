# -*- coding: utf-8 -*-
"""
Created on 2018/9/20

@author: gaoan
"""
import logging
import traceback

from tigeropen.trade.domain.order import OrderStatus
from tigeropen.trade.request.model import AccountsParams
from tigeropen.common.response import TigerResponse
from tigeropen.tiger_open_client import TigerOpenClient
from tigeropen.trade.trade_client import TradeClient
from tigeropen.quote.request import OpenApiRequest
from tigeropen.examples.client_config import get_client_config
# from tigeropen.common.util.contract_utils import stock_contract, option_contract_by_symbol, future_contract, \
#     war_contract_by_symbol, iopt_contract_by_symbol
from tigeropen.common.util.order_utils import limit_order, limit_order_with_legs, order_leg

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a', )
logger = logging.getLogger('TigerOpenApi')

client_config = get_client_config()


def get_account_info():
    from tigeropen.common.consts.service_types import ACCOUNTS
    openapi_client = TigerOpenClient(client_config)
    account = AccountsParams()
    account.account = client_config.account
    request = OpenApiRequest(method=ACCOUNTS, biz_model=account)

    response_content = None
    try:
        response_content = openapi_client.execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed to execute")
    else:
        response = TigerResponse()
        response.parse_response_content(response_content)
        if response.is_success():
            print("get response data:" + response.data)
        else:
            print("%d,%s,%s" % (response.code, response.message, response.data))


def get_account_apis():
    openapi_client = TradeClient(client_config, logger=logger)
    openapi_client.get_managed_accounts()
    # 获取订单
    openapi_client.get_orders()
    # 获取未成交订单
    # openapi_client.get_open_orders()
    # 获取已成交订单
    # openapi_client.get_filled_orders(start_time='2019-05-01', end_time='2019-05-21')
    # 获取持仓
    openapi_client.get_positions()
    # 获取资产
    openapi_client.get_assets()


def trade_apis():
    account = client_config.account
    openapi_client = TradeClient(client_config, logger=logger)

    # stock
    contract = openapi_client.get_contracts('AAPL')[0]
    # 或者本地构造合约对象
    # contract = stock_contract(symbol='AAPL', currency='USD')

    # option
    # contract = option_contract(identifier='AAPL  190118P00160000')
    # future
    # contract = future_contract('CHF', 'USD', '20190617', multiplier=125000, exchange='GLOBEX')

    order = openapi_client.create_order(account, contract, 'BUY', 'LMT', 100, limit_price=5.0)
    # 或者本地构造订单对象
    # order = limit_order(account=account, contract=contract, action='BUY', quantity=100, limit_price=5.0)
    openapi_client.place_order(order)
    order_id = order.order_id  # you can operate order via id too

    new_order = openapi_client.get_order(order_id=order.order_id)
    assert order.order_id == new_order.order_id
    openapi_client.modify_order(new_order, quantity=150)
    new_order = openapi_client.get_order(order_id=order_id)
    assert new_order.quantity == 150
    openapi_client.cancel_order(order_id=order_id)
    new_order = openapi_client.get_order(order_id=order_id)
    assert new_order.status == OrderStatus.CANCELLED or new_order.status == OrderStatus.PENDING_CANCEL

    # 预览订单 (下单前后保证金要求, 佣金等预览)
    result = openapi_client.preview_order(order)
    print(result)

    # 限价单 + 附加订单 (仅主订单为限价单时支持附加订单)
    main_order = openapi_client.create_order(account, contract, 'BUY', 'LMT', quantity=100, limit_price=10.0,
                                             order_legs=order_leg(type='BRACKETS', stop_loss_price=8.0,
                                                                  stop_loss_tif='GTC', profit_taker_price=12.0,
                                                                  profit_taker_tif='GTC'))
    # 本地构造限价单 + 附加订单
    # main_order = limit_order_with_legs(account, contract, 'BUY', 100, limit_price=10.0, order_legs=order_leg(
    #     type='LOSS', stop_loss_price=8.0, stop_loss_tif='DAY'))
    openapi_client.place_order(main_order)
    print(main_order)
    # 查询主订单所关联的附加订单
    order_legs = openapi_client.get_open_orders(account, parent_id=main_order.order_id)
    print(order_legs)


if __name__ == '__main__':
    get_account_info()
    get_account_apis()
    trade_apis()
