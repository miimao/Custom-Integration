from xml import dom
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

domotz_agent = get_all_domotz_agents_id()
#this is so stupid why are you doing this there is a better way and you know it
agent_domotz = vocab_tage = {value: key for key, value in domotz_agent.items()}

# Get all Devices listed in a given Domotz Agent
def get_all_devices_from_domotz_agent(agent_id):
    global agent_domotz
    url = constants.domotz_url + f"/agent/{agent_id}/device"
    devices_list = requests.get(url=url, headers=constants.headers_domotz).json()
    for device in devices_list:
        device["agent_id"] = agent_id
        device["agent_name"] = agent_domotz[agent_id]
    return devices_list


# Make a list of all domotz devices that do not currently have a cwmanage configuration
def get_nocwconfig_domotz_devices(list_of_cw_configurations):
    global domotz_agent
    domotz_devices = []
    domotz_devices_no_config = []
    list_filtered_configs = []
    # Get a list of all Domotz Devices
    for agent in domotz_agent:
        domotz_devices.extend(get_all_devices_from_domotz_agent(domotz_agent[agent]))
    # Strip Everything but the cw config id, domotz id, and the property name out of the configuration info
    # print(list_of_cw_configurations)
    for config in list_of_cw_configurations:
        filtered_config = {}
        filtered_config["cw_config_id"] = config["id"]
        filtered_config["domotz_agent_id"] = domotz_agent[config["company"]["name"]]
        filtered_config["domotz_id"] = int(
            list(
                filter(
                    lambda domotz_info: domotz_info["id"] == 12, config["customFields"]))[0]["value"])
        # print(filtered_config)
        list_filtered_configs.append(filtered_config)
    # print(list_filtered_configs)
    list_configs_domotz_id_only = []
    for config in list_filtered_configs:
        list_configs_domotz_id_only.append(config['domotz_id'])
    # print(list_configs_domotz_id_only)
    # get a list of only devices that we cannot find a matching id for in and remove any device in this list that is not marked as "importance": "VITAL"
    domotz_devices_no_config = list(
        filter(
            lambda device: int(device["id"]) not in list_configs_domotz_id_only
            and device["importance"] == "VITAL",
            domotz_devices,
        )
    )
    # print(domotz_devices_no_config)
    return domotz_devices_no_config
