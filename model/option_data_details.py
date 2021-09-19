import json
import logging

from model.option_data import OptionData
from util.json_util import JsonUtil

log = logging.getLogger(__name__)


class OptionDataDetails:

    def __init__(self, params=None):
        self.strike_price = None
        self.option_data = None
        self.parse_params(params)

    def parse_params(self, params=None):
        if params is None:
            return
        self.strike_price = params['strike_price']
        self.option_data = OptionData(params['option_data'])

    def __str__(self):
        return self.do_jsonify()

    def do_jsonify(self, pretty_print=False):
        return JsonUtil.jsonify(self, OptionDataDetailsEncoder, pretty_print)


class OptionDataDetailsEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__
