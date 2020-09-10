#!/usr/bin/env python3

import json
import time
import requests
from requests.auth import HTTPBasicAuth

host = "sandboxdnac.cisco.com"
#host = "10.10.20.85"
requests.packages.urllib3.disable_warnings()

def get_token():
    with open("credentials.json", "r") as handle:
        login = json.load(handle)['DevNet_Always_On']
        #login = json.load(handle)['Sandbox 7/9']

    response = requests.post(url=f"https://{host}/dna/system/api/v1/auth/token", auth=HTTPBasicAuth(login['username'], login['password']), verify=False)

    return response.json()['Token']

def req(resource, method="GET", payload=None):
    
    basicURL = f"https://{host}/api/v1"

    #basicURL = f"https://{host}dna/intent/api/v1"
         
    headers = {
        "content-type": "application/json",
        "accept": "application/json",
        "X-Auth-Token": f"{get_token()}"
    }

    url = f"{basicURL}{resource}"

    response = requests.request(method, url=url, headers=headers, data=json.dumps(payload), verify=False)

    #print(response.status_code)

    return response.json()

def wait_for_task(taskId, wait_time=5 , attempts=3):

    for i in range(attempts):
        time.sleep(wait_time)

        task_resp = req(f"/task/{taskId}")

        if "endTime" in task_resp["response"]:
            fileId = json.loads(task_resp["response"]["progress"])

            return fileId

    total = wait_time * attempts
    raise TimeoutError(f"Timed out after {total} seconds")

def load_task_result(fileId):

    response = req(f"/file/{fileId}")

    return response[0]["commandResponses"]

