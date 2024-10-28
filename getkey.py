import yaml

# 读取 YAML 文件

def readconfig(filepath):
    with open(filepath) as f:
        config = yaml.safe_load(f)

    # 获取配置值
    return config

if __name__=="__main__":
    readconfig("/home/marisa/workspace/BTC_test/key_config.yaml")