from rqalpha.interface import AbstractMod

from .BianceData import BianceDataSource


class BianceDataMode(AbstractMod):
    def __init__(self):
        pass

    def start_up(self, env, mod_config):
        # 设置 data_source 为 TushareKDataSource 类的对象
        env.set_data_source(BianceDataSource(env.config.base.data_bundle_path))

    def tear_down(self, code, exception=None):
        pass
    
"""
from .mod import TushareKDataMode


def load_mod():
    return TushareKDataMode()
"""