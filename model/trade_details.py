import json
import logging
from util.json_util import JsonUtil

log = logging.getLogger(__name__)


class TradeDetails:

    def __init__(self, params=None):
        self.security = None
        self.open_put_positions = None
        self.open_call_positions = None
        self.put_strike = None
        self.call_strike = None
        self.put_premium = None
        self.call_premium = None
        self.calls_sold = None
        self.puts_sold = None
        self.modifications_in_trade_so_far = None
        self.strangle_num_lots = None
        self.profit = None
        self.profit_exit = None
        self.failure_exit = None
        self.parse_params(params)

    def parse_params(self, params=None):
        if params is None:
            return
        self.security = params['security']
        self.open_put_positions = params['open_put_positions']
        self.open_call_positions = params['open_call_positions']
        self.put_strike = params['put_strike']
        self.call_strike = params['call_strike']
        self.put_premium = params['put_premium']
        self.call_premium = params['call_premium']
        self.calls_sold = params['calls_sold']
        self.puts_sold = params['puts_sold']
        self.modifications_in_trade_so_far = params['modifications_in_trade_so_far']
        self.strangle_num_lots = params['strangle_num_lots']
        self.profit = params['profit']
        self.profit_exit = params['profit_exit']
        self.failure_exit = params['failure_exit']

    def __str__(self):
        return self.do_jsonify()

    def do_jsonify(self, pretty_print=False):
        return JsonUtil.jsonify(self, TradeDetailsEncoder, pretty_print)

class TradeDetailsEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__
