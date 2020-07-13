#!/usr/bin/env python3

import os
import json
import requests
from requests.auth import HTTPBasicAuth

dna_user = os.environ['dna_cent_usr']
dna_psswrd = os.environ['dna_cent_psswrd']
host = 'sandboxdnac.cisco.com'

def dnac_get_token(host=host, username=dna_user, password=dna_psswrd):
    login_url = 'https://{}/dna/system/api/v1/auth/token'.format(host)

    response = requests.post(url=login_url, auth=HTTPBasicAuth(username, password), verify=False)    

    return response.json()['Token']

def get_dnac_devices(host=host):
    login_url = 'https://{}/dna/intent/api/v1/network-device'.format(host)
    token = dnac_get_token()

    response = requests.get(url=login_url, headers={'X-auth-token': token}, verify=False)
    devices = len(response.json()['response'])

    return response.json()['response'], devices

def get_device_times(info, devices):

    times = []

    for x in range(devices):
        times.append('{} has been up since: {} - Uptime for: {}'.format(info[x]['hostname'], info[x]['bootDateTime'], info[x]['upTime']))

    return times

result = get_dnac_devices()

print('\n'.join(get_device_times(result[0], result[1])))

