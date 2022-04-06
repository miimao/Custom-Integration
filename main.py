import requests
import json
import re

#local imports
import constants
import cwmanage_api_functions
import domotz_api_functions



test_ticket = cwmanage_api_functions.get_testing_ticket()
open_tickets = cwmanage_api_functions.get_open_domotz_tickets()
domotz_agents = domotz_api_functions.get_all_domotz_agents_id()


cwmanage_api_functions.add_configuration_to_ticket(test_ticket)



# for ticket in test_tickets:
#     print(ticket["id"])
#     print(domotz_agents[ticket["company"]["name"]])
