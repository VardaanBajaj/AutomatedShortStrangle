import pause
import time as t
from datetime import datetime, time
from config.app_constants import *
from model.trade_details import TradeDetails
from service.start_trade_service import StartTradeService
from service.update_trade_service import UpdateTradeService

if __name__ == "__main__":
    trade_details = TradeDetails()
    trade_exit = False
    start_trade_service = StartTradeService()
    update_trade_service = UpdateTradeService()

    while True:
        # for times in update_times:
        if start_trade_service.time_in_range(time(START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS),
                                             time(END_TIME_HOURS, END_TIME_MINS, END_TIME_SECS),
                                             datetime.now().time()):
            print(f"Current time: {datetime.now().time().strftime('%H:%M:%S')}")

            # a new strangle is created if not already created else open trade details are returned
            trade_details = update_trade_service.get_open_positions_details(security="BANKNIFTY",
                                                                            trade_details=trade_details)

            trade_details = update_trade_service.close_all_positions(trade_details)
            if update_trade_service.is_trade_details_none(trade_details):
                print("Trade completed")
                print()
                trade_exit = True
                break
            # open trade details are returned on which action is performed according to conditions 2 and 3
            if datetime.now().time().hour == 15 and datetime.now().time().minute >= 20:
                trade_details = update_trade_service.close_modification_logic(trade_details=trade_details,
                                                                              security="BANKNIFTY")
            else:
                trade_details = update_trade_service.day_modification_logic(trade_details=trade_details,
                                                                            security="BANKNIFTY")

            trade_details = update_trade_service.close_all_positions(trade_details)
            if update_trade_service.is_trade_details_none(trade_details):
                trade_exit = True
                break

            if datetime.now().time().hour == 15 and datetime.now().time().minute >= 20:
                # handle the case if it is friday, end of month, 31 december, or end of the trading session
                print(f"End of day trade details: {update_trade_service.print_trade_details(trade_details)}")
                print()
                now = datetime.now()
                if now.month == 12 and now.day == 31:
                    pause.until(datetime(now.year + 1, 1, 1, START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS))
                if now.month in DAYS_30 and now.day == 30:
                    pause.until(
                        datetime(now.year, now.month + 1, 1, START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS))
                if now.month in DAYS_31 and now.day == 31:
                    pause.until(
                        datetime(now.year, now.month + 1, 1, START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS))
                if now.month in DAYs_28_OR_29:
                    if now.year % 4 != 0:
                        pause.until(
                            datetime(now.year, now.month + 1, 1, START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS))
                    else:
                        if now.date == 28:
                            pause.until(
                                datetime(now.year, now.month, 29, START_TIME_HOURS, START_TIME_MINS, START_TIME_SECS))
                        elif now.date == 29:
                            pause.until(
                                datetime(now.year, now.month + 1, 1, START_TIME_HOURS, START_TIME_MINS,
                                         START_TIME_SECS))

            else:
                now = datetime.now()
                t.sleep(300)
        else:
            print("Can't execute trade right now, come back when the exchange is open")
            print(f"Trade details: {update_trade_service.print_trade_details(trade_details)}")
            print()
            break
