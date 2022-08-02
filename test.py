import requests
import json

url = "https://api-na.myconnectwise.net/v2022_1/apis/3.0/company/configurations?customFieldConditions=caption='Domotz ID' AND value!=0&orderBy=id+desc&pageSize=1000"

payload = {}
headers = {
    "clientId": "de56a7d9-b6e3-4c96-828b-106cec167f2f",
    "Authorization": "Basic Y29tbXVuaXR5dGVjK3F2TzRyY25nRTRkcld0cmw6eEZRMURIWlRNOHUzdEFWdg==",
}

response = requests.request("GET", url, headers=headers, data=payload)

print(len(response.json()))
