from model.mapping import Mapping


class DateParserInitializer:

    def __init__(self):
        self.month = Mapping()
        self.week = Mapping()
        self.adj_week = Mapping()
        self.month_util = Mapping()
        self.week_util = Mapping()
        self.adj_week_util = Mapping()
        self.initialize()

    def initialize(self):
        self.month.month_01 = 'Jan'
        self.month.month_02 = 'Feb'
        self.month.month_03 = 'Mar'
        self.month.month_04 = 'Apr'
        self.month.month_05 = 'May'
        self.month.month_06 = 'Jun'
        self.month.month_07 = 'Jul'
        self.month.month_08 = 'Aug'
        self.month.month_09 = 'Sep'
        self.month.month_10 = 'Oct'
        self.month.month_11 = 'Nov'
        self.month.month_12 = 'Dec'
        self.month_util['01'] = self.month.month_01
        self.month_util['02'] = self.month.month_02
        self.month_util['03'] = self.month.month_03
        self.month_util['04'] = self.month.month_04
        self.month_util['05'] = self.month.month_05
        self.month_util['06'] = self.month.month_06
        self.month_util['07'] = self.month.month_07
        self.month_util['08'] = self.month.month_08
        self.month_util['09'] = self.month.month_09
        self.month_util['10'] = self.month.month_10
        self.month_util['11'] = self.month.month_11
        self.month_util['12'] = self.month.month_12

        self.week.week_0 = 'Monday'
        self.week.week_1 = 'Tuesday'
        self.week.week_2 = 'Wednesday'
        self.week.week_3 = 'Thursday'
        self.week.week_4 = 'Friday'
        self.week.week_5 = 'Saturday'
        self.week.week_6 = 'Sunday'
        self.week_util[0] = self.week.week_0
        self.week_util[1] = self.week.week_1
        self.week_util[2] = self.week.week_2
        self.week_util[3] = self.week.week_3
        self.week_util[4] = self.week.week_4
        self.week_util[5] = self.week.week_5
        self.week_util[6] = self.week.week_6

        self.adj_week.week_0 = 'Thursday'
        self.adj_week.week_1 = 'Friday'
        self.adj_week.week_2 = 'Saturday'
        self.adj_week.week_3 = 'Sunday'
        self.adj_week.week_4 = 'Monday'
        self.adj_week.week_5 = 'Tuesday'
        self.adj_week.week_6 = 'Wednesday'
        self.adj_week_util[0] = self.adj_week.week_0
        self.adj_week_util[1] = self.adj_week.week_1
        self.adj_week_util[2] = self.adj_week.week_2
        self.adj_week_util[3] = self.adj_week.week_3
        self.adj_week_util[4] = self.adj_week.week_4
        self.adj_week_util[5] = self.adj_week.week_5
        self.adj_week_util[6] = self.adj_week.week_6
