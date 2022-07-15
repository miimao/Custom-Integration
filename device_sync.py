import requests
import json
import re
import logging
import time

# local imports
import constants
import cwmanage_api_functions
import domotz_api_functions

configs = cwmanage_api_functions.get_all_configs_with_domotz_id()
devices = domotz_api_functions.get_nocwconfig_domotz_devices(configs)
# print(test_configs[0])
print(len(devices))
# print(devices[0:2])
for device in devices:
    print(device)
    # print(device['user_data']['model'])
    cwmanage_api_functions.post_domotz_device_to_cwmanage_as_config(device)