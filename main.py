import requests
import json
import re
import logging
import time

# local imports
import constants
import cwmanage_api_functions
import domotz_api_functions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
    filename="CTC-Custom-Integration.log",
)

# ---Get a list of open tickets created by the "DomtozAPI"---
# test_tickets = cwmanage_api_functions.get_testing_ticket()
open_tickets = cwmanage_api_functions.get_open_domotz_tickets()
domotz_agents = domotz_api_functions.get_all_domotz_agents_id()
cw_companys_ids = cwmanage_api_functions.get_all_cw_manage_company_id()
checked_tickets = []
# print(json.dumps(cw_companys_ids,indent=4))
# print(open_tickets)
test_configs = cwmanage_api_functions.get_all_configs_with_domotz_id()
devices = domotz_api_functions.get_nocwconfig_domotz_devices(test_configs)
# print(test_configs[0])
print(len(devices))
# print(devices[0:2])
for device in devices:
    # print(device)
    # print(device['user_data']['model'])
    cwmanage_api_functions.post_domotz_device_to_cwmanage_as_config(device)

# cwmanage_api_functions.post_domotz_device_to_cwmanage_as_config(devices[0:2])
# for device in devices:
#     url = constants.cw_manage_url + "/company/configurations"
#     params = {
#         "conditions": f"name='{device['display_name']}'",
#     }
#     config_data = requests.get(headers=constants.headers_cw, url=url, params=params).json()
#     print(config_data)
#     print(len(config_data))
#     if config_data != [] and len(config_data) <= 1:
#         print(f'yes')
#         cwmanage_api_functions.add_domotz_id_to_config(device['id'],config_data[0]['id'])


# # print(domotz_agents)
# while True:
#     time.sleep(5)
#     # Get a list of open tickets made by "DomotzAPI" and then remove the tickets that have already been checked
#     open_tickets = [
#         ticket
#         for ticket in cwmanage_api_functions.get_open_domotz_tickets()
#         if ticket not in checked_tickets
#     ]

#     # Attempt to add a configuration to these tickets
#     cwmanage_api_functions.add_configuration_to_ticket(open_tickets)
#     # Add these tickets to the list of already proccessed tickets
#     checked_tickets.extend(open_tickets)

# Look for missing domotz devices in all the configurations for a property
# for property in domotz_agents:
#     pass
