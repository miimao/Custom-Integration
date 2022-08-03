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


devices = domotz_api_functions.get_nocwconfig_domotz_devices()
#Add Devices that do not have a configuration into cw manage
logging.info(f"Device Sync Initiated. New Devices Found: {len(devices)}")
for device in devices:
    cwmanage_api_functions.post_domotz_device_to_cwmanage_as_config(device)


domotz_agents = domotz_api_functions.get_all_domotz_agents_id()

# Look for changes in the CW config and update according to the information we find in Domotz
configurations = cwmanage_api_functions.get_all_configs_with_domotz_id()
domotz_devices = domotz_api_functions.get_all_devices()

# Keys translations from CWManage config to Domotz Device json data
changed_configs = []
sync_checks = {
    "name": "display_name",
    "modelNumber": [["user_data", "model"], "model"],
    # "modelNumber":"model",
    "macAddress": "hw_address",
    "ipAddress": "ip_addresses",
}
for config in configurations:
    config_changes = {}
    if config["company"]["name"] in domotz_agents.keys():
        domotz_agent_id = domotz_agents[config["company"]["name"]]
        for customField in config["customFields"]:
            if customField["caption"] == "Domotz ID":
                domotz_device_id = int(customField["value"])
        device = next(
            (
                domotz_device
                for domotz_device in domotz_devices
                if domotz_device["id"] == domotz_device_id
                and domotz_device["agent_id"] == domotz_agent_id
            ),
            None,
        )
        if device != None:
            for key in sync_checks:
                if type(sync_checks[key]) != list and sync_checks[key] in device.keys():
                    if type(device[sync_checks[key]]) == list:
                        if config[key] != device[sync_checks[key]][0]:
                            config_changes[key] = device[sync_checks[key]][0]
                    elif config[key] != device[sync_checks[key]]:
                        config_changes[key] = device[sync_checks[key]]
                else:
                    for i in sync_checks[key]:
                        if type(i) != list and i in device.keys():
                            if config[key] != device[i]:
                                config_changes[key] = device[i]
                        elif (
                            type(i) == list
                            and i[0] in device.keys()
                            and i[1] in device[i[0]].keys()
                        ):
                            if config[key] != device[i[0]][i[1]]:
                                config_changes[key] = device[i[0]][i[1]]
                            elif config[key] == device[i[0]][i[1]]:
                                break

        if device == None and config["status"]["id"] != 3:
            device = domotz_api_functions.get_domotz_device(
                domotz_agent_id, domotz_device_id
            )
            if device != None and device.status_code == 404:
                logging.info(
                    f"Unable to find Domotz Device assosicated with CW Configuration:{config['id']} Changing status to inactive"
                )
                cwmanage_api_functions.patch_config(config["id"], "status", {"id": 3})

    else:
        logging.error(
            f"Device Sync:CW Config:{config['id']} - {config['company']['name']} not found in list of domotz agents"
        )
    if config_changes != {}:
        logging.info(
            f"Device Sync:CW Config:{config['id']} - Changed Detected - DomotzAgent: {domotz_agent_id}, DomotzID: {domotz_device_id}"
        )
        changed_configs.append(config_changes)
        for key in config_changes:
            logging.info(
                f"Device Sync:CW Config:{config['id']} - {key}: {config[key]}  -->  {config_changes[key]}"
            )
            cwmanage_api_functions.patch_config(config["id"], key, config_changes[key])
