import json
import xmltodict
from ncclient import manager

def load_devices():
    with open('dev/netconf_lab1/connection_details.json', 'r') as info:

        devices = json.load(info)

        return devices

def main():

    connect_info = load_devices()['R5']

    filter ='''
            <filter>
                <native>
                    <interface>
                        <Loopback>
                        </Loopback>
                    </interface>   
                </native>
            </filter>
            '''

    with manager.connect(**connect_info) as conn:

        response = conn.get_config(source='running', filter=(filter))

    jresp = xmltodict.parse(response.xml)

    print(json.dumps(jresp['rpc-reply']['data'], indent=2))

if __name__ == '__main__':
    main()