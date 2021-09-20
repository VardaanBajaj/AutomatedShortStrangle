import logging
from datetime import datetime, timedelta, date
from model.option_data_details import OptionDataDetails
from model.option_data import OptionData
from service.nse_options_service import NseOptionsService
from parsers.date_parser import DatesParser

log = logging.getLogger(__name__)


class NSEOptionsServiceAdapter:

    def __init__(self):
        self.nse_options_service = NseOptionsService()
        self.dates_parser = DatesParser()
        self.put_option_data = OptionDataDetails()
        self.call_option_data = OptionDataDetails()

    # this assumes only 1 expiry per week.
    def actual_next_weekly_expiry_date(self, option_chain, next_expiry_date):
        proposed_next_expiry = None
        expiry_on_thursday = False

        # expiry_dates = option_chain['records']['expiryDates']
        # expiry_dates[1] = '15-Sep-2021'
        for expiry_date in option_chain['records']['expiryDates']:
            if next_expiry_date == expiry_date:
                expiry_on_thursday = True  # 90% of time it will be the case (expiry on Thursday)
                break

        # if expiry is not on Thursday, assuming it will be either on Monday, Tuesday, Wednesday or Friday
        if not expiry_on_thursday:
            proposed_next_expiry = self.dates_parser.date_parser_init.change_date_format_2(next_expiry_date)
            formatted_date = proposed_next_expiry.split('-')
            proposed_next_expiry = date(int(formatted_date[0]), int(formatted_date[1]), int(formatted_date[2]))

            for expiry_date in option_chain['records']['expiryDates']:
                expiry_date = self.dates_parser.date_parser_init.change_date_format_2(expiry_date)
                formatted_date = expiry_date.split('-')
                expiry_date = date(int(formatted_date[0]), int(formatted_date[1]), int(formatted_date[2]))
                if datetime.today().date() >= expiry_date:
                    continue
                else:
                    if proposed_next_expiry - timedelta(1) == expiry_date:
                        proposed_next_expiry = expiry_date
                        break
                    if proposed_next_expiry - timedelta(2) == expiry_date:
                        proposed_next_expiry = expiry_date
                        break

                    if proposed_next_expiry - timedelta(3) == expiry_date:
                        proposed_next_expiry = expiry_date
                        break
                    if proposed_next_expiry + timedelta(1) == expiry_date:
                        proposed_next_expiry = expiry_date
                        break
                    else:
                        print("No expiry this week.")
                        print()
                        exit(0)
            proposed_next_expiry = self.dates_parser.date_parser_init.change_date_format_1(proposed_next_expiry)

        if expiry_on_thursday:
            return next_expiry_date
        else:
            return proposed_next_expiry

    def get_reqd_fields(self, security):
        option_chain = self.nse_options_service.get_option_chain(security)

        # only for testing purposes, in real scenario API will be called as above
        # with open(f"../test_data/option_chain_BANKNIFTY_2021_09_11 02_36_25_562800", "r") as f:
        #     option_chain = json.loads(f.read())

        next_expiry_date = self.dates_parser.proposed_next_weekly_expiry_date(datetime.today().date())
        actual_next_weekly_expiry = self.actual_next_weekly_expiry_date(option_chain, next_expiry_date)
        print(actual_next_weekly_expiry)
        print()

        put_option_data = dict()
        call_option_data = dict()
        start_time = datetime.now()
        for option_data in option_chain['records']['data']:
            if option_data['expiryDate'] == actual_next_weekly_expiry:
                self.put_option_data.strike_price = option_data['strikePrice']
                self.put_option_data.option_data = OptionData(option_data['PE'])
                put_option_data[self.put_option_data.strike_price] = self.put_option_data.option_data
                self.call_option_data.strike_price = option_data['strikePrice']
                self.call_option_data.option_data = OptionData(option_data['CE'])
                call_option_data[self.call_option_data.strike_price] = self.call_option_data.option_data

        end_time = datetime.now()
        total_time = end_time - start_time
        print(f"Total time: {total_time}")
        print()

        return put_option_data, call_option_data, actual_next_weekly_expiry


# nse_option_adapter = NSEOptionsServiceAdapter()
# print(nse_option_adapter.get_reqd_fields("BANKNIFTY"))
