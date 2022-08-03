from urllib import response
import requests
import json
import constants
import re
import logging

# Rexex exspresion to find an ip address or mac address if we need to pull form a large string.
regex_ip = re.compile(
    """((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"""
)
regex_mac = re.compile(r"(?:[0-9a-fA-F]:?){12}")
regex_device_name = re.compile(r"(?<=Device Name: ).*")
regex_domotz_device_id = re.compile(r"/devices/(.*?)\?notify=ticketing")

# Get a dictionary with cw manage bopard names and there id's
def get_all_cw_manage_board_id():
    board_ids = {}
    url = constants.cw_manage_url + "/service/boards"
    params = {
        "pageSize": "1000",
    }
    boards_info = requests.get(
        headers=constants.headers_cw, url=url, params=params
    ).json()
    for board in boards_info:
        board_ids[board["name"]] = board["id"]
    return board_ids


# Get a dictionary with cw manage Manufacturers and there id's
def get_all_cw_manage_manufacturer_id():
    vendor_ids = {}
    url = constants.cw_manage_url + "/procurement/manufacturers"
    params = {
        "pageSize": "1000",
    }
    vendor_info = requests.get(
        headers=constants.headers_cw, url=url, params=params
    ).json()
    for vendor in vendor_info:
        vendor_ids[vendor["name"]] = vendor["id"]
    return vendor_ids


# Get a dictionary with cw manage bopard names and there id's
def get_all_cw_manage_company_id():
    company_ids = {}
    url = constants.cw_manage_url + "/company/companies"
    params = {
        "pageSize": "1000",
    }
    company_info = requests.get(
        headers=constants.headers_cw, url=url, params=params
    ).json()
    for company in company_info:
        company_ids[company["name"]] = company["id"]
    return company_ids


# Get a dictionary of all configurations that contain a domotz id
def get_config(config_id):
    url = constants.cw_manage_url + f"/company/configurations/{config_id}"
    params = {}
    config_data = requests.get(headers=constants.headers_cw, url=url, params=params)
    return config_data.json()


# Get a dictionary of all configurations that contain a domotz id
def get_all_configs_with_domotz_id():
    url = constants.cw_manage_url + "/company/configurations"
    params = {
        "customFieldConditions": "caption='Domotz ID' AND value!=0",
        "orderBy": "id desc",
        "pageSize": "1000",
    }
    config_data = requests.get(headers=constants.headers_cw, url=url, params=params)
    return config_data.json()


# Get a list of tickets that are created by the domotz api with the conditions of not being closed, organaized in desc order
def get_open_domotz_tickets():
    url = constants.cw_manage_url + "/service/tickets"
    params = {
        "conditions": "board/name='alerts' AND enteredBy='DomotzAPI' AND status/name!='>Closed'",
        "orderBy": "id desc",
        "pageSize": "500",
    }
    tickets_data = requests.get(headers=constants.headers_cw, url=url, params=params)
    return tickets_data.json()


# Pull a specific ticket/s for testing (This should not be used unless for debuging)
def get_ticket(ticket_number):
    url = constants.cw_manage_url + "/service/tickets"
    # ticket_id = 30705
    ticket_id = ticket_number
    params = {
        # "conditions":f"board/name='alerts' AND enteredBy='DomotzAPI' AND id={ticket_id}",
        "conditions": f"board/name='alerts' AND enteredBy='DomotzAPI'",
        "orderBy": "id desc",
        "pageSize": "10",
    }
    tickets_data = requests.get(headers=constants.headers_cw, url=url, params=params)
    return tickets_data.json()


def get_testing_ticket_loop(last_ticket):
    url = constants.cw_manage_url + "/service/tickets"
    # ticket_id = 30705
    ticket_id = last_ticket
    params = {
        # "conditions":f"board/name='alerts' AND enteredBy='DomotzAPI' AND id={ticket_id}",
        "conditions": f"board/name='alerts' AND enteredBy='DomotzAPI' AND id<{ticket_id}",
        "orderBy": "id desc",
        "pageSize": "1000",
    }
    tickets_data = requests.get(headers=constants.headers_cw, url=url, params=params)
    return tickets_data.json()


# Add a domotz id to a coniguration
def add_domotz_id_to_config(domotz_id, config_id):
    patch_data = [
        {
            "op": "replace",
            "path": "/customFields",
            "value": [{"id": "12", "value": domotz_id}],
        }
    ]
    config_patch_response = requests.patch(
        url=f"{constants.cw_manage_url}/company/configurations/{config_id}",
        headers=constants.headers_cw,
        data=f"{patch_data}",
    )
    logging.info(f"Configuration:{config_id} - Added the Domotz ID ({domotz_id})")

# Patch a configuration in connectwise
def patch_config(config_id, path, value):
    patch_data = [
        {
            "op": "replace",
            "path": f"/{path}",
            "value": value,
        }
    ]
    config_patch_response = requests.patch(
        url=f"{constants.cw_manage_url}/company/configurations/{config_id}",
        headers=constants.headers_cw,
        data=f"{patch_data}",
    )
    logging.info(f"Configuration:{config_id} - Patching: {path} ({value})")


# add a configuration to a ticket/s if it does not already have one.
def add_configuration_to_ticket(ticket):
    for ticket in ticket:
        checked_tickets = []
        ticket_id = ticket["id"]
        # Sometimes a company name will have a " ' " in its name, we want to get rid of these or they cause errors
        ticket_company = ticket["company"]["name"].replace("'", "\\'")
        # Checking to see if we already have a configuration assigned to the ticket.
        ticket_configurations = requests.get(
            url=ticket["_info"]["configurations_href"], headers=constants.headers_cw
        ).json()
        if ticket_configurations == []:
            config_set = False
            config_set_using = None
            logging.info(
                f"Ticket:{ticket['id']} ({ticket_company}) - No configuration assaigned! Attempting to find one."
            )
            # Get the initial note so we can parse it for information we can use to find the configuration.
            try:
                ticket_note = requests.get(
                    headers=constants.headers_cw,
                    url=f"{constants.cw_manage_url}/service/tickets/{ticket_id}/allNotes",
                    params={
                        "conditions": "noteType='TicketNote'",
                        "orderBy": "id asc",
                        "pageSize": "1",
                        "fields": "text",
                    },
                ).json()[0]["text"]
            except:
                ticket_note = ""
            regex_parse = {}
            try:
                regex_parse["domotz_id"] = re.search(
                    regex_domotz_device_id, ticket_note
                ).group(1)
            except:
                regex_parse["domotz_id"] = None
            try:
                regex_parse["macAddress"] = re.search(regex_mac, ticket_note).group()
            except:
                regex_parse["macAddress"] = None
            try:
                regex_parse["ipAddress"] = re.search(regex_ip, ticket_note).group()
            except:
                regex_parse["ipAddress"] = None
            try:
                regex_parse["name"] = re.search(regex_device_name, ticket_note).group()
            except:
                regex_parse["name"] = None
            for i in regex_parse:
                if regex_parse[i] != None:
                    try:
                        if i == "domotz_id":
                            configuration_id = requests.get(
                                headers=constants.headers_cw,
                                url=f"{constants.cw_manage_url}/company/configurations/",
                                params={
                                    "customFieldConditions": f"caption='Domotz ID' AND value={regex_parse[i]}",
                                    "fields": "id",
                                },
                            ).json()
                        else:
                            configuration_id = requests.get(
                                headers=constants.headers_cw,
                                url=f"{constants.cw_manage_url}/company/configurations/",
                                params={
                                    "conditions": f"{i}='{regex_parse[i]}' AND company/name='{ticket_company}'",
                                    "fields": "id",
                                },
                            ).json()
                        if configuration_id != []:
                            configuration_id = configuration_id[0]
                            config_post_response = requests.post(
                                url=f"{constants.cw_manage_url}/service/tickets/{ticket_id}/configurations",
                                headers=constants.headers_cw,
                                data=f"{configuration_id}",
                            )
                            logging.info(
                                f"Ticket:{ticket_id} - Set Configuration (ID:{configuration_id['id']}) ({config_post_response.json()['_info']['name']}), Based on: {i} ({regex_parse[i]})"
                            )
                            config_set = True
                            config_set_using = i
                            break
                        else:
                            logging.info(
                                f"Ticket:{ticket_id} - Unable to find a configuration Based on the {i}: {regex_parse[i]}"
                            )
                    except:
                        logging.warning(
                            f"An exception occurred. ({i}) Ticket ID {ticket_id}"
                        )
                    # add the domotz id to the config if it finds a domotz id for the config
            if (
                config_set == True
                and regex_parse["domotz_id"] != None
                and config_set_using != "domotz_id"
            ):
                logging.info(
                    f"Ticket:{ticket_id} - Configuration found but not using Domotz ID, Attempting to add the Domotz ID to Configuration."
                )
                add_domotz_id_to_config(
                    regex_parse["domotz_id"], configuration_id["id"]
                )
        else:
            logging.info(
                f"Ticket:{ticket_id} ({ticket_company}) - is already assigned a configuration. ({ticket_configurations[0]['_info']['name']})"
            )


# take a domotz device and convert it into json for a post request to cw manage
company_ids = get_all_cw_manage_company_id()  # lookuptable for company names to ids
vendor_ids = get_all_cw_manage_manufacturer_id()


def post_domotz_device_to_cwmanage_as_config(domotz_device):
    logging.info(
        f"Creating new CW Manage Configuration for Domotz Device: {domotz_device['display_name']} (ID: {domotz_device['id']}) - {domotz_device['agent_name']} (ID: {domotz_device['agent_id']}"
    )
    global company_ids
    global vendor_ids
    constants.domotz_type_to_cwmanage_type
    # a few fields might not be in the domotz device json so we can account for these here to avoid errors
    try:
        modelNumber = domotz_device["user_data"]["model"]
    except KeyError:
        try:
            modelNumber = domotz_device["model"]
        except:
            modelNumber = ""

    try:
        hw_address = domotz_device["hw_address"]
    except:
        hw_address = ""

    try:
        manufacturer_id = vendor_ids[domotz_device["vendor"]]
    except:
        manufacturer_id = ""

    if domotz_device["details"]["zone"] != None:
        try:
            sla = f"{domotz_device['details']['zone']} Device"
        except:
            sla = ""
    else:
        sla = ""

    try:
        type_id = constants.domotz_type_to_cwmanage_type[
            domotz_device["user_data"]["type"]
        ]["id"]
    except KeyError:
        try:
            type_id = constants.domotz_type_to_cwmanage_type[
                domotz_device["type"]["id"]
            ]["id"]
        except:
            type_id = 55

    payload = {
        "name": f"{domotz_device['display_name']}",
        "type": {
            "id": f"{type_id}",
            # "name": f"{constants.domotz_type_to_cwmanage_type[domotz_device['type']['id']]['name']}"
        },
        "status": {
            "id": 2,
        },
        "company": {
            "id": f"{company_ids[domotz_device['agent_name']]}",
            "name": f"{domotz_device['agent_name']}",
        },
        "modelNumber": f"{modelNumber}",
        # "installationDate": f"{domotz_device['first_seen_on']}",
        "macAddress": f"{hw_address}",
        "ipAddress": f"{domotz_device['ip_addresses'][0]}",
        "vendor": {
            "name": f"{domotz_device['vendor']}",
        },
        "activeFlag": True,
        "sla": {"name": f"{sla}"},
        "displayVendorFlag": True,
        "showRemoteFlag": True,
        "showAutomateFlag": True,
        # "needsRenewalFlag": True,
        "manufacturer": {
            "id": manufacturer_id,
        },
        "customFields": [
            {
                "id": 12,
                "caption": "Domotz ID",
                "type": "Number",
                "entryMethod": "EntryField",
                "numberOfDecimals": 0,
                "value": domotz_device["id"],
            }
        ],
    }
    try:
        post_config_response = requests.post(
            url=f"{constants.cw_manage_url}/company/configurations",
            headers=constants.headers_cw,
            json=payload,
        )
        response_json = post_config_response.json()
        logging.info(
            f"CW Manage Configuration Created - ID: {response_json['id']} Based on Domotz Device: (ID: {domotz_device['id']}) - {domotz_device['agent_name']}"
        )
    except KeyError as e:
        logging.error("Unable to post Config")
