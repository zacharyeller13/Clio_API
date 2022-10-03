import requests
from requests.structures import CaseInsensitiveDict

url = "https://app.clio.com/oauth/token"
client_id = ""
client_secret = ""
auth_code = ""

headers = CaseInsensitiveDict()
headers["Host"] = "app.clio.com"
headers["Content-Type"] = "application/x-www-form-urlencoded"

auth_params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "authorization_code",
    "code": auth_code,
    "client_id": client_id,
    "redirect_uri": "https://app.clio.com/oauth/approval"
}

def get_auth_token() -> str:
    resp = requests.post(url, headers=headers, params=auth_params)
    auth_token = resp.json()['auth_token']
    print(resp.json())
    return auth_token

if __name__ == "__main__":

    get_auth_token()