import requests
import json
import constants
import re

# Rexex exspresion to find an ip address or mac address if we need to pull form a large string.
regex_ip = re.compile(
    """((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"""
)
regex_mac = re.compile(r"(?:[0-9a-fA-F]:?){12}")
regex_device_name = re.compile(r"(?<=Device Name: ).*")
regex_domotz_device_id = re.compile(r"/devices/(.*?)\?notify=ticketing")

# get a dictionary with cw manage bopard names and there id's
def get_all_cw_manage_board_id():
    board_ids = {}
    url = constants.cw_manage_url + "/service/boards"
    boards_info = requests.get(headers=constants.headers_cw, url=url).json()
    for board in boards_info:
        board_ids[board["name"]] = board["id"]
    return board_ids


# get a list of tickets that are created by the domotz api with the conditions of not being closed, organaized in desc order
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
def get_testing_ticket():
    url = constants.cw_manage_url + "/service/tickets"
    # ticket_id = 30705
    ticket_id = 30441
    params = {
        # "conditions":f"board/name='alerts' AND enteredBy='DomotzAPI' AND id={ticket_id}",
        "conditions": f"board/name='alerts' AND enteredBy='DomotzAPI'",
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
    print(f"Configuration:{config_id} - Added the Domotz ID ({domotz_id})")


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
            print(
                f"\nTicket:{ticket['id']} ({ticket_company}) - No configuration assaigned! Attempting to find one."
            )
            # Get the initial note so we can parse it for information we can use to find the configuration.
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
                            print(
                                f"Ticket:{ticket_id} - Set Configuration (ID:{configuration_id['id']}) ({config_post_response.json()['_info']['name']}), Based on: {i} ({regex_parse[i]})"
                            )
                            config_set = True
                            break
                        else:
                            print(
                                f"Ticket:{ticket_id} - Unable to find a configuration Based on the {i}: {regex_parse[i]}"
                            )
                    except:
                        print(f"An exception occurred. ({i}) Ticket ID {ticket_id}")
                    # add the domotz id to the config
            if config_set == True and regex_parse["domotz_id"] != "":
                print(
                    f"Ticket:{ticket_id} - Configuration found but not using Domotz ID, Attempting to add the Domotz ID to Configuration."
                )
                add_domotz_id_to_config(
                    regex_parse["domotz_id"], configuration_id["id"]
                )
        else:
            print(
                f"\nTicket:{ticket_id} for ({ticket_company}) - is already assigned a configuration. ({ticket_configurations[0]['_info']['name']})"
            )
