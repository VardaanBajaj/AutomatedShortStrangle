import pause
from datetime import datetime, date, time, timedelta
from .start_trade_service import StartTradeService
from adapter.nse_options_service_adapter import NSEOptionsServiceAdapter
from model.trade_details import TradeDetails
from model.option_data import OptionData
from model.option_data_details import OptionDataDetails
from config.app_constants import START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS, \
    END_TIME_HOURS, END_TIME_MINS, END_TIME_SECS, TRADE_START_DAY, \
    TRADE_END_DAY, DAYs_28_OR_29, DAYS_30, DAYS_31, DAY_DIFF_CUTOFF, NEW_POSITION_PREMIUM_CUTOFF_LB, \
    NEW_POSITION_PREMIUM_CUTOFF_UB, BROKER_CHARGES, MAX_PROFIT, MARKET_CLOSE_DIFF_CUTOFF, DELTA_MARGIN, \
    BANK_NIFTY_LOT_SIZE

# last argument will be be greater in value
constraint_2 = lambda premium1, premium2: abs(premium2 - premium1) >= (DAY_DIFF_CUTOFF * premium2)
constraint_3 = lambda premium1, premium2: abs(premium2 - premium1) >= (MARKET_CLOSE_DIFF_CUTOFF * premium2)

class UpdateTradeService:

    def __init__(self):
        self.start_trade_service = StartTradeService()
        self.nse_options_service_adapter = NSEOptionsServiceAdapter()
        self.trade_details = TradeDetails()
        self.option_data = OptionData()
        self.option_data_details = OptionDataDetails()

    def start_new_trade(self, security):
        return self.start_trade_service.create_strangle(security)

    def get_update_times(self):
        initial_execution_time = time(START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS)
        final_execution_time = time(END_TIME_HOURS, END_TIME_MINS, END_TIME_SECS)
        update_execution_time = list()
        temp_time = initial_execution_time
        while temp_time < final_execution_time:
            # print(temp_time)
            update_execution_time.append(temp_time)
            dt = str((datetime.combine(date.today(), temp_time) + timedelta(minutes=5)).time()).split(":")
            temp_time = time(int(dt[0]), int(dt[1]))
        update_execution_time.append(temp_time)
        print(update_execution_time)
        return update_execution_time

    def input_existing_trade_details(self):
        put_strike = int(input("Put strike: "))
        put_premium = int(input("Put premium: "))
        call_strike = int(input("Call strike: "))
        call_premium = int(input("Call premium: "))
        strange_lots = int(input("Strangle lots: "))
        current_profit = int(input("Current profit: "))

        return self.start_trade_service.execute_first_trade(initial_put_strike=put_strike,
                                                            initial_call_strike=call_strike,
                                                            initial_put_premium=put_premium,
                                                            initial_call_premium=call_premium, num_lots=strange_lots,
                                                            security="BANKNIFTY",
                                                            profit=current_profit)

    def is_trade_details_none(self, trade_details: TradeDetails):
        return trade_details.security is None and \
               trade_details.open_put_positions is None and \
               trade_details.open_call_positions is None and \
               trade_details.put_strike is None and \
               trade_details.call_strike is None and \
               trade_details.put_premium is None and \
               trade_details.call_premium is None and \
               trade_details.calls_sold is None and \
               trade_details.puts_sold is None and \
               trade_details.strangle_num_lots is None and \
               trade_details.modifications_in_trade_so_far is None and \
               trade_details.profit is None and \
               trade_details.profit_exit is None and \
               trade_details.failure_exit is None

    # this function to be called every 5-10 mins starting 9:20am and ending at 3:20am
    def get_open_positions_details(self, security, trade_details):
        if TRADE_START_DAY <= datetime.today().weekday() <= TRADE_END_DAY:
            if self.is_trade_details_none(trade_details):
                trade_details = self.start_new_trade(security)
            else:
                print(f"Current open position details: {self.print_trade_details(trade_details)}")
        else:
            print("Market closed today")
        # print(f"Trade details: {self.print_trade_details(trade_details)}")

        if input("Are these details correct? (y/n)") == "n".lower():
            trade_details = self.input_existing_trade_details()
        return trade_details

    def option_details_in_optimal_range(self, high_premium, low_premium_option_data: dict):
        strike = None
        new_low_premium = None
        for strike_price in low_premium_option_data.keys():
            if self.start_trade_service.is_strike_price_sane(low_premium_option_data[strike_price]):
                if NEW_POSITION_PREMIUM_CUTOFF_LB * high_premium \
                        <= (high_premium - low_premium_option_data[strike_price].last_price) \
                        <= NEW_POSITION_PREMIUM_CUTOFF_UB * high_premium:
                    new_low_premium = low_premium_option_data[strike_price].last_price
                    strike = strike_price
                    break

        if strike is None or new_low_premium is None:
            for strike_price in low_premium_option_data.keys():
                if self.start_trade_service.is_strike_price_sane(low_premium_option_data[strike_price]):
                    if (NEW_POSITION_PREMIUM_CUTOFF_LB - DELTA_MARGIN) * high_premium \
                            <= (high_premium - low_premium_option_data[strike_price].last_price) \
                            <= (NEW_POSITION_PREMIUM_CUTOFF_UB + DELTA_MARGIN) * high_premium:
                        new_low_premium = low_premium_option_data[strike_price].last_price
                        strike = strike_price
                        break

        # handle None, None scenario in the parent function
        return strike, new_low_premium

    def print_trade_details(self, trade_details: TradeDetails):
        print("Trade Details: ")
        print(f"Security: {trade_details.security}")
        print(f"Calls sold: {trade_details.calls_sold}")
        print(f"Puts sold: {trade_details.puts_sold}")
        print(f"Call strike: {trade_details.call_strike}")
        print(f"Put strike: {trade_details.put_strike}")
        print(f"Call premium: {trade_details.call_premium}")
        print(f"Put premium: {trade_details.put_premium}")
        print(f"Open call positions: {trade_details.open_call_positions}")
        print(f"Open put positions: {trade_details.open_put_positions}")
        print(f"Strangle num lots: {trade_details.strangle_num_lots}")
        print(f"Modifications in trade so far: {trade_details.modifications_in_trade_so_far}")
        print(f"Current profit: {trade_details.profit}")
        print(f"Profit exit: {trade_details.profit_exit}")
        print(f"Failure exit: {trade_details.failure_exit}")

    def modify_trade_details(self, option_strike, option_premium, trade_details: TradeDetails, option_data: dict, type):
        if option_strike is None or option_premium is None:
            if type == "PE":
                print(
                    f"Put strike: {option_strike}, Put premium: {option_data[option_strike].last_price}, hence squaring off put position")
                self.start_trade_service.execute_dummy_buy_trade(strike_price=option_strike,
                                                                 premium=option_data[option_strike].last_price,
                                                                 call_or_put="PE",
                                                                 no_of_lots=trade_details.open_put_positions,
                                                                 security=trade_details.security)
                trade_details.put_premium = option_premium
                trade_details.put_strike = option_strike
                trade_details.modifications_in_trade_so_far += 1
                trade_details.open_put_positions = 0
            elif type == "CE":
                print(
                    f"Call strike: {option_strike}, Call premium: {option_data[option_strike].last_price}, hence squaring off put position")
                self.start_trade_service.execute_dummy_buy_trade(strike_price=option_strike, premium=option_premium,
                                                                 call_or_put="CE",
                                                                 no_of_lots=trade_details.open_put_positions,
                                                                 security=trade_details.security)
                trade_details.call_premium = option_premium
                trade_details.call_strike = option_strike
                trade_details.modifications_in_trade_so_far += 1
                trade_details.open_call_positions = 0

        else:
            if type == "CE":
                # TODO: need to fetch premium for existing strike price to square off position : DONE
                self.start_trade_service.execute_dummy_buy_trade(strike_price=trade_details.call_strike,
                                                                 premium=option_data[option_strike].last_price,
                                                                 call_or_put="CE",
                                                                 no_of_lots=trade_details.open_call_positions,
                                                                 security=trade_details.security)
                trade_details.profit += trade_details.call_premium - option_premium  # only call position booked profit updated
                trade_details.profit *= (1 - BROKER_CHARGES)
                trade_details.profit *= BANK_NIFTY_LOT_SIZE
                trade_details.call_strike = option_strike
                trade_details.call_premium = option_premium
                self.start_trade_service.execute_dummy_sell_trade(strike_price=option_strike, premium=option_premium,
                                                                  call_or_put="CE",
                                                                  no_of_lots=trade_details.open_call_positions,
                                                                  security=trade_details.security)
            elif type == "PE":
                # TODO: need to fetch premium for existing strike price to square off position : DONE
                self.start_trade_service.execute_dummy_buy_trade(strike_price=option_strike,
                                                                 premium=option_data[option_strike].last_price,
                                                                 call_or_put="PE",
                                                                 no_of_lots=trade_details.open_put_positions,
                                                                 security=trade_details.security)
                trade_details.profit += trade_details.put_premium - option_premium  # only put position booked profit updated
                trade_details.profit *= (1 - BROKER_CHARGES)
                trade_details.profit *= BANK_NIFTY_LOT_SIZE
                trade_details.put_strike = option_strike
                trade_details.put_premium = option_premium
                self.start_trade_service.execute_dummy_sell_trade(strike_price=option_strike, premium=option_premium,
                                                                  call_or_put="PE",
                                                                  no_of_lots=trade_details.open_put_positions,
                                                                  security=trade_details.security)
            trade_details.modifications_in_trade_so_far += 1

        # constraint 4
        if trade_details.put_strike >= trade_details.call_strike:
            trade_details.failure_exit = True

        return trade_details

    def close_modification_logic(self, trade_details: TradeDetails, security="BANKNIFTY"):
        # TODO: check for exit condition for old trade and new trade : not reqd, program terminates after trade exit
        put_option_data, call_option_data, expiry_date = self.nse_options_service_adapter.get_reqd_fields(security)
        call_premium = trade_details.call_premium
        put_premium = trade_details.put_premium

        if put_premium < call_premium and constraint_3(put_premium, call_premium):
            new_put_strike_price, new_put_premium = self.option_details_in_optimal_range(call_premium, put_option_data)
            trade_details = self.modify_trade_details(new_put_strike_price, new_put_premium, trade_details,
                                                      put_option_data, type="PE")
            trade_details.profit += trade_details.call_premium - call_option_data[trade_details.call_strike].last_price
            trade_details.profit *= BANK_NIFTY_LOT_SIZE

        elif put_premium > call_premium and constraint_3(call_premium, put_premium):
            new_call_strike_price, new_call_premium = self.option_details_in_optimal_range(put_premium,
                                                                                           call_option_data)
            trade_details = self.modify_trade_details(new_call_strike_price, new_call_premium, trade_details,
                                                      call_option_data, type="CE")
            trade_details.profit += trade_details.put_premium - call_option_data[trade_details.put_strike].last_price
            trade_details.profit *= BANK_NIFTY_LOT_SIZE

        else:  # update the profit if everything is normal
            trade_details.profit += (
                    trade_details.put_premium - put_option_data[trade_details.put_strike].last_price
                    + trade_details.call_premium - call_option_data[trade_details.call_strike].last_price)
            trade_details.profit *= BANK_NIFTY_LOT_SIZE

        # constraint 4
        if trade_details.profit >= (MAX_PROFIT + (BROKER_CHARGES * MAX_PROFIT)):
            trade_details.profit_exit = True
            return trade_details

        if datetime.now().time().hour == START_TIME_HOURS and \
                datetime.now().time().minute >= START_TIME_MINS and \
                datetime.today().weekday() == 3:  # thursday 9.20am
            trade_details.failure_exit = True

        if trade_details.failure_exit is True:
            return trade_details

        return trade_details

    def day_modification_logic(self, trade_details, security="BANKNIFTY"):
        # TODO: check for exit condition for old trade and new trade : not reqd, program terminates after trade exit
        put_option_data, call_option_data, expiry_date = self.nse_options_service_adapter.get_reqd_fields(security)
        call_premium = trade_details.call_premium
        put_premium = trade_details.put_premium

        if put_premium < call_premium and constraint_2(put_premium, call_premium):
            new_put_strike_price, new_put_premium = self.option_details_in_optimal_range(call_premium, put_option_data)
            trade_details = self.modify_trade_details(new_put_strike_price, new_put_premium, put_option_data,
                                                      trade_details, type="PE")
            trade_details.profit += trade_details.call_premium - call_option_data[trade_details.call_strike].last_price
            trade_details.profit *= BANK_NIFTY_LOT_SIZE

        elif put_premium > call_premium and constraint_2(call_premium, put_premium):
            new_call_strike_price, new_call_premium = self.option_details_in_optimal_range(put_premium,
                                                                                           call_option_data)
            trade_details = self.modify_trade_details(new_call_strike_price, new_call_premium, call_option_data,
                                                      trade_details, type="CE")
            trade_details.profit += trade_details.put_premium - call_option_data[trade_details.put_strike].last_price
            trade_details.profit *= BANK_NIFTY_LOT_SIZE

        else:  # update the profit if everything is normal
            trade_details.profit += (
                    trade_details.put_premium - put_option_data[trade_details.put_strike].last_price
                    + trade_details.call_premium - call_option_data[trade_details.call_strike].last_price)
            trade_details.profit *= BANK_NIFTY_LOT_SIZE

        # constraint 4
        if trade_details.profit >= (MAX_PROFIT + (BROKER_CHARGES * MAX_PROFIT)):
            trade_details.profit_exit = True
            return trade_details

        if datetime.now().time().hour == START_TIME_HOURS and \
                datetime.now().time().minute >= START_TIME_MINS - 1 and \
                datetime.today().weekday() == 3:  # thursday 9.20am
            trade_details.failure_exit = True

        if trade_details.failure_exit is True:
            return trade_details

        return trade_details

    def close_all_positions(self, trade_details: TradeDetails):
        if trade_details.profit_exit is True or trade_details.failure_exit is True:
            print(f"Total profit: {trade_details.profit}")
            print(f"Trade details: {self.print_trade_details(trade_details)}")
            self.start_trade_service.execute_dummy_buy_trade(strike_price=trade_details.call_strike,
                                                             premium=trade_details.call_premium,
                                                             call_or_put="CE",
                                                             no_of_lots=trade_details.open_call_positions,
                                                             security=trade_details.security)

            self.start_trade_service.execute_dummy_buy_trade(strike_price=trade_details.put_strike,
                                                             premium=trade_details.put_premium,
                                                             call_or_put="PE",
                                                             no_of_lots=trade_details.open_put_positions,
                                                             security=trade_details.security)
        else:
            print("Exit conditions are not met")
            return trade_details

        trade_details = TradeDetails()
        return trade_details
