import base64
import secrets
#----------------Domotz API INFO----------------
domotz_api_key = secrets.domotz_api_key
domotz_url = "https://api-us-east-1-cell-1.domotz.com/public-api/v1"

#----------------Connectwise Manage API Info----------------

#Connectwise uses a normal basic api auth that requires you to format and encode it in a certain way in order to use it.
def generate_cw_token(Company_ID, Public_Key, Private_Key):
    token = "{}+{}:{}".format(Company_ID, Public_Key, Private_Key)
    token = base64.b64encode(bytes(token, 'utf-8'))
    token = token.decode('utf-8')
    return token

cw_manage_url = "https://api-na.myconnectwise.net/v2021_3/apis/3.0"
company_id = secrets.company_id
cw_manage_public = secrets.cw_manage_public
cw_manage_private = secrets.cw_manage_private
client_id = secrets.client_id
cw_token = generate_cw_token(company_id,cw_manage_public,cw_manage_private)

headers_domotz = {
    'X-Api-Key': domotz_api_key,
    'Accept': 'application/json'
    }
headers_cw = {
    'Authorization': "Basic " + cw_token,
    'clientId': client_id,
    'Accept': '*/*',
    'Content-Type': 'application/json'
    }