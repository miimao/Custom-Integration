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


# Get all Devices listed in a given Domotz Agent
def get_all_devices_from_domotz_agent(agent_id):
    url = constants.domotz_url + f"/agent/{agent_id}/device"
    devices_list = requests.get(url=url, headers=constants.headers_domotz).json()
    for device in devices_list:
        device["agent_id"] = agent_id
    return devices_list


# Make a list of all domotz devices that do not currently have a cwmanage configuration
def get_nocwconfig_domotz_devices(list_of_cw_configurations):
    domotz_agents = get_all_domotz_agents_id()
    domotz_devices = []
    domotz_devices_no_config = []
    # Get a list of all Domotz Devices
    for agent in domotz_agents:
        domotz_devices.extend(get_all_devices_from_domotz_agent(domotz_agents[agent]))
    # Strip Everything but the cw config id, domotz id, and the property name out of the configuration info
    list_filtered_configs = []
    for config in list_of_cw_configurations:
        filtered_config = {}
        filtered_config["cw_config_id"] = config["id"]
        # we probbaly dont need the domotz agent id but im leaving it here incase I find out the device id is not unique
        filtered_config["domotz_agent_id"] = domotz_agents[config["company"]["name"]]
        filtered_config["domotz_id"] = int(
            list(
                filter(
                    lambda domotz_info: domotz_info["id"] == 12, config["customFields"]
                )
            )[0]["value"]
        )
        list_filtered_configs.append(filtered_config)
    # get a list of only devices that we cannot find a matching id for in and remove any device in this list that is not marked as "importance": "VITAL"
    domotz_devices_no_config = list(
        filter(
            lambda device: device["id"] != filtered_config["domotz_id"]
            and device["importance"] == "VITAL",
            domotz_devices,
        )
    )
    return domotz_devices_no_config
