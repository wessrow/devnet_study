#!/usr/bin/env python3

import requests
import json
from dna_functions import req

def load_devices():

    devices = req('/network-device')['response']

    return devices

def device_uptime(devices):

    for device in devices:
        print(f"{device['hostname']} - {device['managementIpAddress']} has been up for {device['upTime']}")

def find_id_from_ip(ip):

    devices = load_devices()

    for device in devices:
        if ip == device['managementIpAddress']:
            return device['id']

        else:
            print(f"No such IP-address could be found")

def get_device_info(devices, id):

    for device in devices:
        if id == device['id']:
            print(f"{device['hostname']} has IP address {device['managementIpAddress']} - S/N: {device['serialNumber']} - Last updated: {device['lastUpdated']}")
            break

        else:
            print(f"No device could be found.")

    pass

if __name__ == "__main__":
    print(json.dumps(load_devices(), indent=2))

#   get_device_info(load_devices(), find_id_from_ip('10.10.22.253'))

#   print(find_id_from_ip('10.10.22.73'))

#    print(json.dumps(req('/network-device-poller/cli/legit-reads')['response'], indent=2))
