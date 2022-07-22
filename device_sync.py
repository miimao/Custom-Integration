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


# devices = domotz_api_functions.get_nocwconfig_domotz_devices()
# #Add Devices that do not have a configuration into cw manage
# logging.info(f"Device Sync Initiated. New Devices Found: {len(devices)}")
# for device in devices:
#     cwmanage_api_functions.post_domotz_device_to_cwmanage_as_config(device)


domotz_agents = domotz_api_functions.get_all_domotz_agents_id()
print(domotz_agents)
# Look for changes in the CW config and update according to the information we find in Domotz
configurations = cwmanage_api_functions.get_all_configs_with_domotz_id()
# Keys translations from CWManage config to Domotz Device json data
sync_checks = {
    "name":"display_name",
    "modelNumber":["model",['user_data','model']],
    # "modelNumber":"model",
    "macAddress":"hw_address",
    "ipAddress":"ip_addresses",
}
for config in configurations:
    if config['company']['name'] in domotz_agents.keys():
        domotz_agent_id = domotz_agents[config['company']['name']]
        for customField in config['customFields']:
            if customField['caption'] == "Domotz ID":
                domotz_device_id = (int(customField['value']))
        logging.info(f"Syncing CW configureation ({config['id']}) for Domotz Device - Agent: {domotz_agent_id}, ID: {domotz_device_id}")
        device = (domotz_api_functions.get_domotz_device(domotz_agent_id,domotz_device_id))
        if device != None:
            for key in sync_checks:
                try:
                    if type(sync_checks[key]) != list and sync_checks[key] in device.keys():
                        if config[key] == device[sync_checks[key]]:
                            print(True)
                        else:
                            print(False)
                    else:
                        for i in sync_checks[key]:
                            if type(i) != list and i in device.keys():
                                if config[key] == device[i]:
                                    print(True)
                                else:
                                    print(False)
                            elif type(i) == list and i[0] in device.keys() and i[1] in device[i[0]].keys():
                                if config[key] == device[i[0]][i[1]]:
                                    print(True)
                                else:
                                    print(False)
                            else:
                                pass

                except:
                    print("Failed Some How 1")
                    pass
    else:
        logging.error(f"Configuration {config['id']}: {config['company']['name']} not found in list of domotz agents")
