import requests
import json
import constants
import re

#Rexex exspresion to find an ip address or mac address if we need to pull form a large string.
regex_ip = re.compile('''((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)''')
regex_mac = re.compile(r'(?:[0-9a-fA-F]:?){12}')
regex_device_name = re.compile(r'(?<=Device Name: ).*')

#get a dictionary with cw manage bopard names and there id's
def get_all_cw_manage_board_id():
    board_ids = {}
    url = constants.cw_manage_url+"/service/boards"
    boards_info = requests.get(headers=constants.headers_cw,url=url).json()
    for board in boards_info:
        board_ids[board["name"]] = board["id"]
    return(board_ids)

#get a list of tickets that are created by the domotz api with the conditions of not being closed, organaized in desc order
def get_open_domotz_tickets():
    url = constants.cw_manage_url+"/service/tickets"
    params = {
        "conditions":"board/name='alerts' AND enteredBy='DomotzAPI' AND status/name!='>Closed'",
        "orderBy":"id desc",
        "pageSize":"500"
    }
    tickets_data = requests.get(headers=constants.headers_cw,url=url,params=params)
    return tickets_data.json()

#Pull a specific ticket/s for testing (This should not be used unless for debuging)
def get_testing_ticket():
    url = constants.cw_manage_url+"/service/tickets"
    # ticket_id = 30705
    ticket_id = 30441
    params = {
        # "conditions":f"board/name='alerts' AND enteredBy='DomotzAPI' AND id={ticket_id}",
        "conditions":f"board/name='alerts' AND enteredBy='DomotzAPI'",
        "orderBy":"id desc",
        "pageSize":"1000"
    }
    tickets_data = requests.get(headers=constants.headers_cw,url=url,params=params)
    return tickets_data.json()

#add a configuration to a ticket/s if it does not already have one.
def add_configuration_to_ticket(ticket):
    for ticket in ticket:
        ticket_id = ticket["id"]
        #Sometimes a company name will have a " ' " in its name, we want to get rid of these or they cause errors
        ticket_company = ticket['company']['name'].replace("'","\\'")
        #Checking to see if we already have a configuration assigned to the ticket.
        ticket_configurations = requests.get(url=ticket['_info']['configurations_href'],headers=constants.headers_cw).json()
        if ticket_configurations == []:
            config_set = False
            print(f"\nTicket:{ticket['id']} - No configuration assaigned! Attempting to find one.")
            #Get the initial note so we can parse it for information we can use to find the configuration.
            ticket_note = requests.get(headers=constants.headers_cw, url=f"https://api-na.myconnectwise.net/v2021_3/apis/3.0/service/tickets/{ticket_id}/allNotes", params={"conditions":"noteType='TicketNote'","orderBy":"id asc","pageSize":"1","fields":"text"}).json()[0]["text"]
            # print(ticket_note)
            try:
                mac_address = re.search(regex_mac,ticket_note).group()
            except:
                mac_address = None
            try:
                ip_address = re.search(regex_ip,ticket_note).group()
            except:
                ip_address = None
            try:
                device_name = re.search(regex_device_name,ticket_note).group()
            except:
                device_name = None
            print(f"Ticket:{ticket_id} - Found (NAME: {device_name} - MAC: {mac_address} - IP: {ip_address})")
            #using the information we can search for a configuration that matches any of the data.
            if mac_address != None:
                try:
                    configuration_id = requests.get(headers=constants.headers_cw, url=f"https://api-na.myconnectwise.net/v2021_3/apis/3.0/company/configurations/", params={"conditions":f"macAddress='{mac_address}' AND company/name='{ticket_company}'","fields":"id"}).json()
                    if configuration_id != []:
                        configuration_id = configuration_id[0]
                        config_post_response = requests.post(url=f"https://api-na.myconnectwise.net/v2021_3/apis/3.0/service/tickets/{ticket_id}/configurations",headers=constants.headers_cw,data=f"{configuration_id}")
                        print(f"Set Configuration - ID:{configuration_id['id']} ({config_post_response.json()['_info']['name']}) for Ticket: {ticket_id},")
                        config_set = True
                    else:
                        print(f"Ticket:{ticket_id} - Unable to find a configuration Based on the Mac Address: {mac_address}")
                except:
                    print(f"An exception occurred. (MAC CHECK) Ticket ID {ticket_id}")
            if ip_address != None and config_set != True:
                try:
                    configuration_id = requests.get(headers=constants.headers_cw, url=f"https://api-na.myconnectwise.net/v2021_3/apis/3.0/company/configurations/", params={"conditions":f"ipAddress='{ip_address}' AND company/name='{ticket_company}'","fields":"id"}).json()
                    if configuration_id != []:
                        configuration_id = configuration_id[0]
                        config_post_response = requests.post(url=f"https://api-na.myconnectwise.net/v2021_3/apis/3.0/service/tickets/{ticket_id}/configurations",headers=constants.headers_cw,data=f"{configuration_id}")
                        print(f"Set Configuration - ID:{configuration_id['id']} ({config_post_response.json()['_info']['name']}) for Ticket: {ticket_id},")
                        config_set = True
                    else:
                        print(f"Ticket:{ticket_id} - Unable to find a configuration Based on the IP Address: {ip_address}")
                except:
                    print(f"An exception occurred. (IP CHECK) Ticket ID {ticket_id}")
            if device_name != None and config_set != True:
                try:
                    configuration_id = requests.get(headers=constants.headers_cw, url=f"https://api-na.myconnectwise.net/v2021_3/apis/3.0/company/configurations/", params={"conditions":f"name='{device_name}' AND company/name='{ticket_company}'","fields":"id"}).json()
                    if configuration_id != []:
                        configuration_id = configuration_id[0]
                        config_post_response = requests.post(url=f"https://api-na.myconnectwise.net/v2021_3/apis/3.0/service/tickets/{ticket_id}/configurations",headers=constants.headers_cw,data=f"{configuration_id}")
                        print(f"Set Configuration - ID:{configuration_id['id']} ({config_post_response.json()['_info']['name']}) for Ticket: {ticket_id},")
                        config_set = True
                    else:
                        print(f"Ticket:{ticket_id} - Unable to find a configuration Based on the Device Name: {device_name}")
                except:
                    print(f"An exception occurred. (NAME CHECK) Ticket ID {ticket_id}")
        else:
            print(f"\nTicket:{ticket_id} for ({ticket_company}) - is already assigned a configuration. ({ticket_configurations[0]['_info']['name']})")