import requests
import datetime

import BaseConfig

if __name__ == '__main__':
    print(BaseConfig.host_address)
    BaseConfig.host_address = "0_1_0_1_0_1_0"
    print(BaseConfig.host_address)


