import base64
import secrets

# ----------------Domotz API INFO----------------
domotz_api_key = secrets.domotz_api_key
domotz_url = "https://api-us-east-1-cell-1.domotz.com/public-api/v1"

# ----------------Connectwise Manage API Info----------------

# Connectwise uses a normal basic api auth that requires you to format and encode it in a certain way in order to use it.
def generate_cw_token(Company_ID, Public_Key, Private_Key):
    token = "{}+{}:{}".format(Company_ID, Public_Key, Private_Key)
    token = base64.b64encode(bytes(token, "utf-8"))
    token = token.decode("utf-8")
    return token


cw_manage_url = "https://api-na.myconnectwise.net/v2022_1/apis/3.0"
company_id = secrets.company_id
cw_manage_public = secrets.cw_manage_public
cw_manage_private = secrets.cw_manage_private
client_id = secrets.client_id
cw_token = generate_cw_token(company_id, cw_manage_public, cw_manage_private)


headers_domotz = {"X-Api-Key": domotz_api_key, "Accept": "application/json"}
headers_cw = {
    "Authorization": "Basic " + cw_token,
    "clientId": client_id,
    "Accept": "*/*",
    "Content-Type": "application/json",
}


domotz_type_to_cwmanage_type ={
    1: #Generic
        {
        "id": 55,
        "name": "Device - Generic"
        },
    2: #Home Automation
        {
        "id": 153,
        "name": "Managed Network Home Automate"
        },
    4: #Notebook
        {
        "id": 24,
        "name": "Managed Workstation"
        },
    5: #Server
        {
        "id": 25,
        "name": "Managed Server"
        },
    6: #Network Equipment
        {
        "id": 140,
        "name": "Managed Network Device"
        },
    7: #NAS
        {
        "id": 59,
        "name": "Storage - Network (NAS)"
        },
    8: #Printer & Fax
        {
        "id": 57,
        "name": "Printer - Networked"
        },
    9: #Mobile
        {
        "id": 136,
        "name": "Managed Mobile Phone"
        },
    10: #Tablet
        {
        "id": 137,
        "name": "Managed Mobile Tablet"
        },
    11: #VoIP
        {
        "id": 60,
        "name": "VoIP"
        },
    12: #Game Console
        {
        "id": 55,
        "name": "Device - Generic"
        },
    13: #Wearable
        {
        "id": 55,
        "name": "Device - Generic"
        },
    14: #Smart Power Plug
        {
        "id": 104,
        "name": "Smart Power Plug"
        },
    15: #lighting
        {
        "id": 77,
        "name": "Lighting Controller"
        },
    16: #Sensor
        {
        "id": 55,
        "name": "Device - Generic"
        },
    17: #Heating and Cooling
        {
        "id": 55,
        "name": "Device - Generic"
        },
    18: #Security System
        {
        "id": 55,
        "name": "Device - Generic"
        },
    19: #TV
        {
        "id": 55,
        "name": "Device - Generic"
        },
    20: #Audio & Video
        {
        "id": 55,
        "name": "Device - Generic"
        },
    21: #Speaker & Amp
        {
        "id": 75,
        "name": "Audio - Amplifier"
        },
    22: #Camera
        {
            "id": 61,
            "name": "Camera - IP"
        },
    23: #Guest Device
        {
        "id": 55,
        "name": "Device - Generic"
        },
    24: #Custom Device
        {
        "id": 55,
        "name": "Device - Generic"
        },
    25: #Healthcare Device
        {
        "id": 55,
        "name": "Device - Generic"
        },
    26: #Appliance
        {
        "id": 55,
        "name": "Device - Generic"
        },
    27: #Robot
        {
        "id": 55,
        "name": "Device - Generic"
        },
    28: #PoE Switch
        {
        "id": 93,
        "name": "Network Switch - Managed (PoE)"
        },
    29: #Media Player
        {
        "id": 97,
        "name": "Media Player"
        },
    30: #Audio Player
        {
        "id": 90,
        "name": "Audio - Streamer"
        },
    31: #Desktop
        {
        "id": 24,
        "name": "Managed Workstation"
        },
    32: #Wi-Fi
        {
        "id": 66,
        "name": "Wi-Fi Access Point"
        },
    33: #MP3 Player
        {
        "id": 90,
        "name": "Audio - Streamer"
        },
    34: #Ebook Reader
        {
        "id": 55,
        "name": "Device - Generic"
        },
    35: #Smart Watch
        {
        "id": 55,
        "name": "Device - Generic"
        },
    36: #Car
        {
        "id": 55,
        "name": "Device - Generic"
        },
    37: #Streaming Dongle
        {
        "id": 55,
        "name": "Device - Generic"
        },
    38: #Cable Box
        {
        "id": 101,
        "name": "Modem - Cable"
        },
    39: #Disc Player
        {
        "id": 55,
        "name": "Device - Generic"
        },
    40: #Satallite
        {
        "id": 55,
        "name": "Device - Generic"
        },
    41: #Radio
        {
        "id": 90,
        "name": "Audio - Streamer"
        },
    42: #Photo Camera
        {
        "id": 55,
        "name": "Device - Generic"
        },
    43: #Photo Display
        {
        "id": 55,
        "name": "Device - Generic"
        },
    44: #Mic
        {
        "id": 55,
        "name": "Device - Generic"
        },
    45: #Projector
        {
        "id": 55,
        "name": "Device - Generic"
        },
    46: #Computer
        {
        "id": 24,
        "name": "Managed Workstation"
        },
    47: #Scanner
        {
        "id": 55,
        "name": "Device - Generic"
        },
    48: #Point of Sale
        {
        "id": 55,
        "name": "Device - Generic"
        },
    49: #Clock
        {
        "id": 55,
        "name": "Device - Generic"
        },
    50: #Barcode Scanner
        {
        "id": 55,
        "name": "Device - Generic"
        },
    51: #Smart Device
        {
        "id": 55,
        "name": "Device - Generic"
        },
    52: #Voice Control
        {
        "id": 55,
        "name": "Device - Generic"
        },
    53: #Thermostat
        {
        "id": 105,
        "name": "Thermostat"
        },
    54: #Power System
        {
        "id": 98,
        "name": "Power System"
        },
    55: #Solar Panel
        {
        "id": 55,
        "name": "Device - Generic"
        },
    56: #Smart Meter
        {
        "id": 103,
        "name": "Smart Meter"
        },
    57: #Smart Washer
        {
        "id": 55,
        "name": "Device - Generic"
        },
    58: #Smart Fridge
        {
        "id": 55,
        "name": "Device - Generic"
        },
    59: #Smart Cleaner
        {
        "id": 55,
        "name": "Device - Generic"
        },
    60: #Sleep Touch
        {
        "id": 55,
        "name": "Device - Generic"
        },
    61: #Garage Door
        {
        "id": 55,
        "name": "Device - Generic"
        },
    62: #Sprinkler
        {
        "id": 55,
        "name": "Device - Generic"
        },
    63: #Electric
        {
        "id": 55,
        "name": "Device - Generic"
        },
    64: #Doorbell
        {
        "id": 55,
        "name": "Device - Generic"
        },
    65: #Smart Lock
        {
        "id": 55,
        "name": "Device - Generic"
        },
    66: #Touch Panel
        {
        "id": 106,
        "name": "Automation - Touch Panel"
        },
    67: #Controller
        {
        "id": 91,
        "name": "Access Control - Panel"
        },
    68: #Scale
        {
        "id": 55,
        "name": "Device - Generic"
        },
    69: #Toy
        {
        "id": 55,
        "name": "Device - Generic"
        },
    70: #Weather Station
        {
        "id": 55,
        "name": "Device - Generic"
        },
    71: #Baby Monitor
        {
        "id": 55,
        "name": "Device - Generic"
        },
    72: #Pet Monitor
        {
        "id": 55,
        "name": "Device - Generic"
        },
    73: #Motion Detector
        {
        "id": 55,
        "name": "Device - Generic"
        },
    74: #Smoke Dectector
        {
        "id": 55,
        "name": "Device - Generic"
        },
    75: #Water Sensor
        {
        "id": 55,
        "name": "Device - Generic"
        },
    76: #FingBox
        {
        "id": 55,
        "name": "Device - Generic"
        },
    77: #Domotz Box
        {
        "id": 140,
        "name": "Managed Network Device"
        },
    78: #Router
        {
        "id": 147,
        "name": "Managed Network Router"
        },
    79: #Wi-Fi Exstender
        {
        "id": 66,
        "name": "Wi-Fi Access Point"
        },
    80: #modem
        {
        "id": 101,
        "name": "Modem - Cable"
        },
    81: #Switch
        {
        "id": 96,
        "name": "Network Switch - Managed (non-PoE)"
        },
    82: #Gateway
        {
        "id": 92,
        "name": "Router"
        },
    83: #Firewall
        {
        "id": 148,
        "name": "Managed Network Firewall"
        },
    84: #VPN
        {
        "id": 92,
        "name": "Router"
        },
    85: #USB
        {
        "id": 55,
        "name": "Device - Generic"
        },
    86: #Smart Cell
        {
        "id": 55,
        "name": "Device - Generic"
        },
    87: #Cloud
        {
        "id": 55,
        "name": "Device - Generic"
        },
    88: #UPS
        {
        "id": 98,
        "name": "Power System"
        },
    89: #Virtual Machine
        {
        "id": 55,
        "name": "Device - Generic"
        },
    90: #Terminal
        {
        "id": 25,
        "name": "Managed Server"
        },
    91: #Mail Server
        {
        "id": 25,
        "name": "Managed Server"
        },
    92: #File Server
        {
        "id": 25,
        "name": "Managed Server"
        },
    93: #Proxy Server
        {
        "id": 25,
        "name": "Managed Server"
        },
    94: #Web Server
        {
        "id": 25,
        "name": "Managed Server"
        },
    95: #Domain Server
        {
        "id": 25,
        "name": "Managed Server"
        },
    96: #Communication
        {
        "id": 25,
        "name": "Managed Server"
        },
    97: #Database
        {
        "id": 25,
        "name": "Managed Server"
        },
    98: #Raspberry
        {
        "id": 55,
        "name": "Device - Generic"
        },
    99: #Arduino
        {
        "id": 55,
        "name": "Device - Generic"
        },
    100: #Process Unit
        {
        "id": 55,
        "name": "Device - Generic"
        },
    101: #RFID Tag
        {
        "id": 55,
        "name": "Device - Generic"
        },
    102: #AV Reciever
        {
        "id": 55,
        "name": "Device - Generic"
        },
    103: #Monitoring Box
        {
        "id": 76,
        "name": "Monitor"
        },
}