import json
import logging
from util.json_util import JsonUtil

log = logging.getLogger(__name__)


class OptionData:

    def __init__(self, params=None):
        self.strike_price = None
        self.expiry_date = None
        self.underlying = None
        self.identifier = None
        self.open_interest = None
        self.change_in_open_interest = None
        self.p_change_in_open_interest = None
        self.total_traded_volume = None
        self.implied_volatility = None
        self.last_price = None
        self.change = None
        self.p_change = None
        self.total_buy_quantity = None
        self.total_sell_quantity = None
        self.bid_qty = None
        self.bid_price = None
        self.ask_qty = None
        self.ask_price = None
        self.underlying_value = None
        self.parse_params(params)

    def parse_params(self, params=None):
        if params is None:
            return
        self.strike_price = params['strikePrice']
        self.expiry_date = params['expiryDate']
        self.underlying = params['underlying']
        self.identifier = params['identifier']
        self.open_interest = params['openInterest']
        self.change_in_open_interest = params['changeinOpenInterest']
        self.p_change_in_open_interest = params['pchangeinOpenInterest']
        self.total_traded_volume = params['totalTradedVolume']
        self.implied_volatility = params['impliedVolatility']
        self.last_price = params['lastPrice']
        self.change = params['change']
        self.p_change = params['pChange']
        self.total_buy_quantity = params['totalBuyQuantity']
        self.total_sell_quantity = params['totalSellQuantity']
        self.bid_qty = params['bidQty']
        self.bid_price = params['bidprice']
        self.ask_qty = params['askQty']
        self.ask_price = params['askPrice']
        self.underlying_value = params['underlyingValue']

    def __str__(self):
        return self.do_jsonify()

    def do_jsonify(self, pretty_print=False):
        return JsonUtil.jsonify(self, OptionDataEncoder, pretty_print)


class OptionDataEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__
