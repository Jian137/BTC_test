import six
from datetime import date
from dateutil.relativedelta import relativedelta
from rqalpha.data.base_data_source import BaseDataSource
import getkey
from binance.client import Client



class BianceDataSource(BaseDataSource):
    def __init__(self, path,custom_future_info):
        # 初始化
        super(BianceDataSource, self).__init__(path,custom_future_info)
        config = getkey.readconfig("/home/marisa/workspace/BTC_test/key_config.yaml")
        
        self.client = Client(config["test_config"]["API_Key"],config["test_config"]["Secret_Key"],testnet=True)
    @staticmethod
    def get_tushare_k_data(instrument, start_dt, end_dt):
        # 获取区间数据 k线数据
        order_book_id = instrument.order_book_id
        code = order_book_id.split(".")[0]

        if instrument.type == 'CS':
            index = False
        elif instrument.type == 'INDX':
            index = True
        else:
            return None
        # TODO change data type
        return client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")
        #return ts.get_k_data(code, index=index, start=start_dt.strftime('%Y-%m-%d'), end=end_dt.strftime('%Y-%m-%d'))

    def get_bar(self, instrument, dt, frequency):
        # tushare k线数据暂时只能支持日级别的回测，其他情况甩锅给默认数据源
        if frequency != '1d':
            return super(TushareKDataSource, self).get_bar(instrument, dt, frequency)

         # 调用上边写好的函数获取k线数据
        bar_data = self.get_tushare_k_data(instrument, dt, dt)
        
        # 遇到获取不到数据的情况，同样甩锅；若有返回值，注意转换格式。
        if bar_data is None or bar_data.empty:
            return super(TushareKDataSource, self).get_bar(instrument, dt, frequency)
        else:
            return bar_data.iloc[0].to_dict()

    def history_bars(self, instrument, bar_count, frequency, fields, dt, skip_suspended=True):
        # tushare 的k线数据未对停牌日期做补齐，所以遇到不跳过停牌日期的情况我们先甩锅。有兴趣的开发者欢迎提交代码补齐停牌日数据。
        if frequency != '1d' or not skip_suspended:
            return super(TushareKDataSource, self).history_bars(instrument, bar_count, frequency, fields, dt, skip_suspended)

        
        # 参数只提供了截止日期和天数，我们需要自己找到开始日期
        # 获取交易日列表，并拿到截止日期在列表中的索引，之后再算出开始日期的索引
        start_dt_loc = self.get_trading_calendar().get_loc(dt.replace(hour=0, minute=0, second=0, microsecond=0)) - bar_count + 1
        # 根据索引拿到开始日期
        start_dt = self.get_trading_calendar()[start_dt_loc]
        # 调用上边写好的函数获取k线数据
        bar_data = self.get_tushare_k_data(instrument, start_dt, dt)

        if bar_data is None or bar_data.empty:
            return super(TushareKDataSource, self).get_bar(instrument, dt, frequency)
        else:   
            # 注意传入的 fields 参数可能会有不同的数据类型
            if isinstance(fields, six.string_types):
                fields = [fields]
            fields = [field for field in fields if field in bar_data.columns]

            # 这样转换格式会导致返回值的格式与默认 DataSource 中该方法的返回值格式略有不同。欢迎有兴趣的开发者提交代码进行修改。
            return bar_data[fields].as_matrix()

    def available_data_range(self, frequency):
        return date(2005, 1, 1), date.today() - relativedelta(days=1)
    
    
