# -*- coding:utf-8 -*-
"""
"""
from utils.config import config
from utils.utility import get_file_path, load_json, save_json


# 交易仓位
class Positions:

    def __init__(self, file_name):
        self.file_name = file_name
        self.positions = {}
        # 总利润
        self.total_profit = 0
        self.read_data()  # read the saved data

    def read_data(self):
        filepath = get_file_path(self.file_name)
        data = load_json(filepath)
        if not bool(data):
            data['total_profit'] = self.total_profit
            data['positions'] = self.positions
        else:
            self.total_profit = float(data.get('total_profit', 0))
            self.positions = data.get('positions', {})

    def save_data(self):
        filename = get_file_path(self.file_name)
        save_json(filename, {'total_profit': self.total_profit, 'positions': self.positions})

    def update(self, symbol: str, trade_amount: float, trade_price: float, min_qty: float, is_buy: bool = False):
        """
        :param symbol:
        :param trade_amount:
        :param trade_price:
        :param is_buy:
        :return:
        """
        pos = self.positions.get(symbol, None)
        if pos is None:
            #
            pos = {'symbol': symbol, 'pos': 0, 'avg_price': 0, 'last_entry_price': 0, 'current_increase_pos_count': 0,
                   'profit_max_price': 0}

        if is_buy:
            # 当前加仓次数.
            pos['current_increase_pos_count'] = pos['current_increase_pos_count'] + 1
            # 均价
            pos['avg_price'] = (trade_amount * trade_price + pos['avg_price'] * pos['pos']) / (trade_amount + pos['pos'])
            # 买的总数量
            pos['pos'] = trade_amount + pos['pos']
            # 最后一次交易价格
            pos['last_entry_price'] = trade_price

        else:
            # 2 * trade_amount * trade_price * config.trading_fee 表示算出来买/卖手续费
            # config.trading_fee 交易手续费：每个帐号的等级不一样，手续费不一样
            # 总利润
            self.total_profit += (trade_price - pos['avg_price']) * trade_amount - 2 * trade_amount * trade_price * config.trading_fee
            pos['pos'] = pos['pos'] - trade_amount

        if pos['pos'] < min_qty:
            if self.positions.get(symbol, None):
                del self.positions[symbol]
        else:
            self.positions[symbol] = pos

    def update_profit_max_price(self, symbol: str, price: float):
        """
        :param symbol:
        :param price:
        :return:
        """
        if self.positions.get(symbol, None):
            self.positions[symbol]['profit_max_price'] = max(price, self.positions[symbol]['profit_max_price'])
