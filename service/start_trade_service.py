import logging
from datetime import datetime, time
from config.app_constants import INITIAL_PREMIUM, HEDGED_PREMIUM, MIN_ACCOUNT_BALANCE
from config.app_constants import START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS, \
    END_TIME_HOURS, END_TIME_MINS, END_TIME_SECS, TRADE_START_DAY, TRADE_END_DAY
from adapter.nse_options_service_adapter import NSEOptionsServiceAdapter
from model.trade_details import TradeDetails

log = logging.getLogger(__name__)


class StartTradeService:

    def __init__(self):
        self.nse_options_service_adapter = NSEOptionsServiceAdapter()
        self.trade_details = TradeDetails()

    def execute_first_trade(self, initial_put_strike, initial_call_strike, initial_put_premium, initial_call_premium,
                            num_lots,
                            security, profit=0, profit_exit=False, failure_exit=False):

        self.trade_details.security = security
        self.trade_details.open_put_positions = num_lots
        self.trade_details.open_call_positions = num_lots
        self.trade_details.put_strike = initial_put_strike
        self.trade_details.call_strike = initial_call_strike
        self.trade_details.put_premium = initial_put_premium
        self.trade_details.call_premium = initial_call_premium
        self.trade_details.calls_sold = num_lots
        self.trade_details.puts_sold = num_lots
        self.trade_details.modifications_in_trade_so_far = 0
        self.trade_details.strangle_num_lots = num_lots
        self.trade_details.profit = profit
        self.trade_details.profit_exit = profit_exit
        self.trade_details.failure_exit = failure_exit

        self.execute_dummy_sell_trade(strike_price=initial_put_strike, premium=initial_put_premium,
                                      call_or_put="PE", no_of_lots=num_lots, security=security)

        self.execute_dummy_sell_trade(strike_price=initial_call_strike, premium=initial_call_premium,
                                      call_or_put="CE", no_of_lots=num_lots, security=security)

        return self.trade_details

    def time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def execute_dummy_buy_trade(self, strike_price, premium, call_or_put, no_of_lots=1, security="BANKNIFTY"):
        if strike_price is None or premium is None:
            print(f"Error squaring off {call_or_put} position")
        print(
            f"{no_of_lots} lot(s) of {security} bought successfully. {call_or_put}: Strike price {strike_price} @ Premium: {premium}")

    def execute_dummy_sell_trade(self, strike_price, premium, call_or_put, no_of_lots=1, security="BANKNIFTY"):
        if strike_price is None or premium is None:
            print(f"Error squaring off {call_or_put} position")
        print(
            f"{no_of_lots} lot(s) of {security} sold successfully. {call_or_put}: Strike price {strike_price} @ Premium: {premium}")

    def is_strike_price_sane(self, strike_price):
        return strike_price.open_interest > 0 and strike_price.change_in_open_interest != 0 and \
               strike_price.total_traded_volume > 0 and strike_price.implied_volatility > 0 and \
               strike_price.last_price > 0 and strike_price.change != 0

    def strike_price_with_desired_premium(self, option_data, expiry_date, hedged=False):
        '''
            Current implementation is only for non-hedged trades
        '''

        min_diff = 1e9
        premium = -1e9
        strike = 1e9
        for strike_price in option_data.keys():
            if option_data[strike_price].expiry_date == expiry_date:
                if self.is_strike_price_sane(option_data[strike_price]):
                    if abs(option_data[strike_price].last_price - INITIAL_PREMIUM) < min_diff:
                        min_diff = abs(option_data[strike_price].last_price - INITIAL_PREMIUM)
                        premium = option_data[strike_price].last_price
                        strike = option_data[strike_price].strike_price

        if premium != -1e9 and min_diff != 1e9:
            # print(strike, premium)
            return strike, premium

    def create_strangle(self, security):
        put_option_data, call_option_data, expiry_date = self.nse_options_service_adapter.get_reqd_fields(security)
        initial_put_strike, initial_put_premium = self.strike_price_with_desired_premium(put_option_data, expiry_date)
        initial_call_strike, initial_call_premium = self.strike_price_with_desired_premium(call_option_data,
                                                                                           expiry_date)

        res = input("Want to create a new strangle? (y/n): ")
        if res == 'y'.lower() or res == 'yes'.lower():
            num_lots = int(input("No. of lots (1 Ce and 1 Pe combined represents 1 lot of strangle):  "))
            # while num_lots <= 0:
            #     num_lots = int(input("No. of lots (1 Ce and 1 Pe combined represents 1 lot of strangle) > 0 :  "))
            res2 = input("Are you sure you want to start a new strangle? (y/n): ")
            if res2 == 'y'.lower() or res == 'yes'.lower():
                time_obj = datetime.now()
                if TRADE_START_DAY <= time_obj.weekday() <= TRADE_END_DAY:
                    print(time_obj.hour, time_obj.minute)
                    if self.time_in_range(time(START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS),
                                          time(END_TIME_HOURS, END_TIME_MINS, END_TIME_SECS),
                                          time_obj.time()):
                        trade_details = self.execute_first_trade(initial_put_strike, initial_call_strike,
                                                                 initial_put_premium, initial_call_premium, num_lots,
                                                                 security)
                    else:
                        print("Can't execute trade right now. Please try between 9:20am and 3:15pm on weekdays")
                else:
                    print("Market closed on weekends")
            else:
                print("No strangle created")
        else:
            print("No strangle created")
        # subject to change (this is used to see open positions. once broker is included, will fetch from there)
        return self.trade_details

# sts = StartTradeService()
# print(sts.create_strangle("BANKNIFTY"))
