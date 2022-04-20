import requests
import json
import re

# local imports
import constants
import cwmanage_api_functions
import domotz_api_functions

# ---Get a list of open tickets created by the "DomtozAPI"---
test_tickets = cwmanage_api_functions.get_testing_ticket()
open_tickets = cwmanage_api_functions.get_open_domotz_tickets()
domotz_agents = domotz_api_functions.get_all_domotz_agents_id()
checked_tickets = []
# print(open_tickets)


# print(domotz_agents)
while True:
    open_tickets = (
        cwmanage_api_functions.get_open_domotz_tickets()
    )  # Get a list of open tickets made by "DomotzAPI"
    cwmanage_api_functions.add_configuration_to_ticket(
        test_tickets
    )  # Attempt to add a configuration to these tickets


# for ticket in test_tickets:
#     print(ticket["id"])
#     print(domotz_agents[ticket["company"]["name"]])
