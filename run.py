# run_file_demo
from rqalpha import run_file

config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "BTCUSDT",
    "accounts": {
        "stock": 100000
    },
    "future_info": {}
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    },
    #"rqalpha-mod-biance":{
    #  "enabled": True,
    #  "configpath":"/home/marisa/workspace/BTC_test/key_config.yaml"
    #}
  }
}

strategy_file_path = "/home/marisa/workspace/BTC_test/celuetest.py"

run_file(strategy_file_path, config)