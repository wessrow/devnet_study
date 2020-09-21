import requests
import json

# Disable unsigned certificate warnings
requests.packages.urllib3.disable_warnings()

meraki_key = "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"
base_url = "https://api.meraki.com/api/v1"
headers = {
    "X-Cisco-Meraki-API-Key": meraki_key
}

def get_orgs():

    resource = "/organizations"

    response = requests.get(f"{base_url}{resource}", headers=headers, verify=False).json()

    for org in response:
        print(org["id"])

    return response

def get_org_networks():

    orgId= "681155"

    resource = f"/organizations/{orgId}/networks"

    response = requests.get(f"{base_url}{resource}", headers=headers, verify=False).json()

    return response

def get_network_devices():

    networkId = "L_566327653141843049"

    resource = f"/networks/{networkId}/devices"

    response = requests.get(f"{base_url}{resource}", headers=headers, verify=False).json()

    devices = {}

    for device in response:
        try:
            devices.update({f"{device['model']}_{device['name']}": device['serial']})

        except: 
            devices.update({f"{device['model']}": device['serial']})
        # print(f"{device['name']}_{i} - {device['serial']}")

    return devices

def get_device(networkId="L_566327653141843049", serial="Q2LD-AN9B-S6AJ"):

    resource = f"/devices/{serial}"

    response = requests.get(f"{base_url}{resource}", headers=headers, verify=False).json()

    return response

if __name__ == "__main__":

    devices = get_network_devices()

    for device in devices:
        try:
            print(device)
            print(get_device(serial=(devices[device]))["mac"])

        except:
            print("Error")

    #print(json.dumps(get_device(serial="Q2QW-W2W4-MCNR"), indent=2))
    #get_mtu()