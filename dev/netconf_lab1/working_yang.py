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
                        <GigabitEthernet>
                            <name>{}</name>
                        </GigabitEthernet>
                    </interface>   
                </native>
            </filter>
            '''

    with manager.connect(**connect_info) as conn:

        response = conn.get_config(source='running', filter=(filter.format(2)))

    jresp = xmltodict.parse(response.xml)

    print(json.dumps(jresp, indent=2))

if __name__ == '__main__':
    main()