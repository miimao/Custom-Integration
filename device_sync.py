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
logging.info(f"Device Sync Initiated. New Devices Found: {len(devices)}")
for device in devices:
    cwmanage_api_functions.post_domotz_device_to_cwmanage_as_config(device)