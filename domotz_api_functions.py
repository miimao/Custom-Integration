import requests
import json
import re
import constants
import logging

# get a dictionary of all active domotz agents and there id's
def get_all_domotz_agents_id():
    agents_ids = {}
    url = constants.domotz_url + "/agent"
    agents_info = requests.get(url=url, headers=constants.headers_domotz).json()
    for agent in agents_info:
        agents_ids[agent["display_name"]] = agent["id"]
    return agents_ids


# Check for out of date information in a cw_manage configuration
def check_cwconfig_against_domotz(configuration):
    pass
