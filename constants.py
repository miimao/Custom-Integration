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


domotz_type_to_cwmanage_type = {
    1: {"id": 55, "name": "Device - Generic"},  # Generic
    2: {"id": 153, "name": "Managed Network Home Automate"},  # Home Automation
    4: {"id": 24, "name": "Managed Workstation"},  # Notebook
    5: {"id": 25, "name": "Managed Server"},  # Server
    6: {"id": 140, "name": "Managed Network Device"},  # Network Equipment
    7: {"id": 59, "name": "Storage - Network (NAS)"},  # NAS
    8: {"id": 57, "name": "Printer - Networked"},  # Printer & Fax
    9: {"id": 136, "name": "Managed Mobile Phone"},  # Mobile
    10: {"id": 137, "name": "Managed Mobile Tablet"},  # Tablet
    11: {"id": 60, "name": "VoIP"},  # VoIP
    12: {"id": 55, "name": "Device - Generic"},  # Game Console
    13: {"id": 55, "name": "Device - Generic"},  # Wearable
    14: {"id": 104, "name": "Smart Power Plug"},  # Smart Power Plug
    15: {"id": 77, "name": "Lighting Controller"},  # lighting
    16: {"id": 55, "name": "Device - Generic"},  # Sensor
    17: {"id": 55, "name": "Device - Generic"},  # Heating and Cooling
    18: {"id": 55, "name": "Device - Generic"},  # Security System
    19: {"id": 55, "name": "Device - Generic"},  # TV
    20: {"id": 55, "name": "Device - Generic"},  # Audio & Video
    21: {"id": 75, "name": "Audio - Amplifier"},  # Speaker & Amp
    22: {"id": 61, "name": "Camera - IP"},  # Camera
    23: {"id": 55, "name": "Device - Generic"},  # Guest Device
    24: {"id": 55, "name": "Device - Generic"},  # Custom Device
    25: {"id": 55, "name": "Device - Generic"},  # Healthcare Device
    26: {"id": 55, "name": "Device - Generic"},  # Appliance
    27: {"id": 55, "name": "Device - Generic"},  # Robot
    28: {"id": 93, "name": "Network Switch - Managed (PoE)"},  # PoE Switch
    29: {"id": 97, "name": "Media Player"},  # Media Player
    30: {"id": 90, "name": "Audio - Streamer"},  # Audio Player
    31: {"id": 24, "name": "Managed Workstation"},  # Desktop
    32: {"id": 66, "name": "Wi-Fi Access Point"},  # Wi-Fi
    33: {"id": 90, "name": "Audio - Streamer"},  # MP3 Player
    34: {"id": 55, "name": "Device - Generic"},  # Ebook Reader
    35: {"id": 55, "name": "Device - Generic"},  # Smart Watch
    36: {"id": 55, "name": "Device - Generic"},  # Car
    37: {"id": 55, "name": "Device - Generic"},  # Streaming Dongle
    38: {"id": 101, "name": "Modem - Cable"},  # Cable Box
    39: {"id": 55, "name": "Device - Generic"},  # Disc Player
    40: {"id": 55, "name": "Device - Generic"},  # Satallite
    41: {"id": 90, "name": "Audio - Streamer"},  # Radio
    42: {"id": 55, "name": "Device - Generic"},  # Photo Camera
    43: {"id": 55, "name": "Device - Generic"},  # Photo Display
    44: {"id": 55, "name": "Device - Generic"},  # Mic
    45: {"id": 55, "name": "Device - Generic"},  # Projector
    46: {"id": 24, "name": "Managed Workstation"},  # Computer
    47: {"id": 55, "name": "Device - Generic"},  # Scanner
    48: {"id": 55, "name": "Device - Generic"},  # Point of Sale
    49: {"id": 55, "name": "Device - Generic"},  # Clock
    50: {"id": 55, "name": "Device - Generic"},  # Barcode Scanner
    51: {"id": 55, "name": "Device - Generic"},  # Smart Device
    52: {"id": 55, "name": "Device - Generic"},  # Voice Control
    53: {"id": 105, "name": "Thermostat"},  # Thermostat
    54: {"id": 98, "name": "Power System"},  # Power System
    55: {"id": 55, "name": "Device - Generic"},  # Solar Panel
    56: {"id": 103, "name": "Smart Meter"},  # Smart Meter
    57: {"id": 55, "name": "Device - Generic"},  # Smart Washer
    58: {"id": 55, "name": "Device - Generic"},  # Smart Fridge
    59: {"id": 55, "name": "Device - Generic"},  # Smart Cleaner
    60: {"id": 55, "name": "Device - Generic"},  # Sleep Touch
    61: {"id": 55, "name": "Device - Generic"},  # Garage Door
    62: {"id": 55, "name": "Device - Generic"},  # Sprinkler
    63: {"id": 55, "name": "Device - Generic"},  # Electric
    64: {"id": 55, "name": "Device - Generic"},  # Doorbell
    65: {"id": 55, "name": "Device - Generic"},  # Smart Lock
    66: {"id": 106, "name": "Automation - Touch Panel"},  # Touch Panel
    67: {"id": 91, "name": "Access Control - Panel"},  # Controller
    68: {"id": 55, "name": "Device - Generic"},  # Scale
    69: {"id": 55, "name": "Device - Generic"},  # Toy
    70: {"id": 55, "name": "Device - Generic"},  # Weather Station
    71: {"id": 55, "name": "Device - Generic"},  # Baby Monitor
    72: {"id": 55, "name": "Device - Generic"},  # Pet Monitor
    73: {"id": 55, "name": "Device - Generic"},  # Motion Detector
    74: {"id": 55, "name": "Device - Generic"},  # Smoke Dectector
    75: {"id": 55, "name": "Device - Generic"},  # Water Sensor
    76: {"id": 55, "name": "Device - Generic"},  # FingBox
    77: {"id": 140, "name": "Managed Network Device"},  # Domotz Box
    78: {"id": 147, "name": "Managed Network Router"},  # Router
    79: {"id": 66, "name": "Wi-Fi Access Point"},  # Wi-Fi Exstender
    80: {"id": 101, "name": "Modem - Cable"},  # modem
    81: {"id": 96, "name": "Network Switch - Managed (non-PoE)"},  # Switch
    82: {"id": 92, "name": "Router"},  # Gateway
    83: {"id": 148, "name": "Managed Network Firewall"},  # Firewall
    84: {"id": 92, "name": "Router"},  # VPN
    85: {"id": 55, "name": "Device - Generic"},  # USB
    86: {"id": 55, "name": "Device - Generic"},  # Smart Cell
    87: {"id": 55, "name": "Device - Generic"},  # Cloud
    88: {"id": 98, "name": "Power System"},  # UPS
    89: {"id": 55, "name": "Device - Generic"},  # Virtual Machine
    90: {"id": 25, "name": "Managed Server"},  # Terminal
    91: {"id": 25, "name": "Managed Server"},  # Mail Server
    92: {"id": 25, "name": "Managed Server"},  # File Server
    93: {"id": 25, "name": "Managed Server"},  # Proxy Server
    94: {"id": 25, "name": "Managed Server"},  # Web Server
    95: {"id": 25, "name": "Managed Server"},  # Domain Server
    96: {"id": 25, "name": "Managed Server"},  # Communication
    97: {"id": 25, "name": "Managed Server"},  # Database
    98: {"id": 55, "name": "Device - Generic"},  # Raspberry
    99: {"id": 55, "name": "Device - Generic"},  # Arduino
    100: {"id": 55, "name": "Device - Generic"},  # Process Unit
    101: {"id": 55, "name": "Device - Generic"},  # RFID Tag
    102: {"id": 55, "name": "Device - Generic"},  # AV Reciever
    103: {"id": 76, "name": "Monitor"},  # Monitoring Box
}
