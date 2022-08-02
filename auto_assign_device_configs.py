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
attempts_before_exception_raise = 100
for i in range(attempts_before_exception_raise):
    try:
        while True:
            time.sleep(10)
            # Get a list of open tickets made by "DomotzAPI" and then remove the tickets that have already been checked
            open_tickets = [
                ticket
                for ticket in cwmanage_api_functions.get_open_domotz_tickets()
                if ticket not in checked_tickets
            ]

            # Attempt to add a configuration to these tickets
            cwmanage_api_functions.add_configuration_to_ticket(open_tickets)
            # Add these tickets to the list of already proccessed tickets
            checked_tickets.extend(open_tickets)
    except KeyError as e:
        if i < attempts_before_exception_raise - 1:  # i is zero indexed
            continue
        else:
            raise
        break
