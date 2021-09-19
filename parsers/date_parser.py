import logging
from datetime import datetime, timedelta
from .date_parser_initializer import DateParserInitializer

log = logging.getLogger(__name__)

FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
logging.basicConfig(format=FORMAT)
logging.addLevelName(logging.INFO,
                     "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.INFO))

class DatesParser:

    def __init__(self):
        self.date_parser_init = DateParserInitializer()

    def change_date_format_1(self, date):
        '''
        Input: Date in format: YYYY-MM-DD
        Output: Date in format: DD-Mon-YYYY
        '''

        date = str(date)
        dt = date.split("-")
        dt[0], dt[2] = dt[2], dt[0]
        dt[1] = self.date_parser_init.month_util[dt[1]]

        return f"{dt[0]}-{dt[1]}-{dt[2]}"

    def change_date_format_2(self, date):
        '''
            Input: Date in format: DD-Mon-YYYY
            Output: Date in format: YYYY-MM-DD
        '''
        dt = date.split('-')
        dt[0], dt[2] = dt[2], dt[0]

        month_idx = list(self.date_parser_init.month_util.keys())
        months = list(self.date_parser_init.month_util.values())
        dt[1] = month_idx[months.index(dt[1])]
        new_date = f"{dt[0]}-{dt[1]}-{dt[2]}"
        return new_date

    def proposed_next_weekly_expiry_date(self, date):
        today_weekday = self.date_parser_init.week_util[datetime.today().weekday()]
        adj_days_index = list(self.date_parser_init.adj_week_util.keys())
        adj_days = list(self.date_parser_init.adj_week_util.values())

        delta = 7 - adj_days_index[adj_days.index(today_weekday)]
        # log.info(delta)
        delta = 7 if delta == 0 else delta
        # log.info(str(date + timedelta(delta)))
        formatted_date = self.change_date_format_1(date + timedelta(delta))
        return formatted_date


# date_parser = DatesParser()
# log.info(date_parser.proposed_next_weekly_expiry_date(datetime.today().date()))
