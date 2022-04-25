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
checked_tickets = []
# print(open_tickets)

test_configs = cwmanage_api_functions.get_all_configs_with_domotz_id()
domotz_api_functions.find_missing_domotz_devices(test_configs)


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
