import json
import xmltodict
from ncclient import manager

def load_devices():
    with open('dev/netconf_lab1/connection_details.json', 'r') as info:

        devices = json.load(info)

        return devices
    
def main():

    connect_info = load_devices()['R5']

    

    with manager.connect(**connect_info) as conn:
        print('Connecting to {}'.format(connect_info['host']))

        response = add_interface(conn)

        if response.ok:
            print('Interface added, closing connection to {}'.format(connect_info['host']))

def add_interface(conn):

    payload = {
        "config": {
            "native":{
                "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
                "interface": {
                    "Loopback": {
                        "name": "7",
                        "ip": {
                            "address": {
                                "primary": {
                                    "address": "7.7.7.7",
                                    "mask": "255.255.255.255"
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    xpayload = xmltodict.unparse(payload)

    config_response = conn.edit_config(target='running', config=xpayload)

    return config_response

if __name__ == '__main__':
    main()