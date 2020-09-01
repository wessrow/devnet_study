#!/usr/bin/env python3

import json
import requests
from requests.auth import HTTPBasicAuth

host = "sandboxdnac.cisco.com"

def get_token():
    with open("dev/dna_center/credentials.json", "r") as handle:
        login = json.load(handle)['DevNet_Always_On']

    response = requests.post(url=f"https://{host}/dna/system/api/v1/auth/token", auth=HTTPBasicAuth(login['username'], login['password']), verify=False)

    return response.json()['Token']

def req(resource, method="GET", json=None):
    
    basicURL = f"https://{host}/dna/intent/api/v1"
    
    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "X-Auth-Token": f"{get_token()}"
    }

    url = f"{basicURL}{resource}"

    response = requests.request(method, url=url, headers=headers, data=json, verify=False)

    return response.json()