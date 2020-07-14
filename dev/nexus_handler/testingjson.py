import json
from netmiko import ConnectHandler

def load_variables():

    with open('dev/nexus_handler/devnet_env_var.json', 'r') as variables:
        device = json.load(variables)

        ios_device = {
            'device_type': 'cisco_ios',
            'ip': device['Devnet_Nexus']['ios_nx_ip'],
            'username': device['Devnet_Nexus']['ios_nx_user'],
            'password': device['Devnet_Nexus']['ios_nx_password'],
            'port': 8181
        }

        return ios_device

def get_information(device):

    net_connect = ConnectHandler(**device)
    output = net_connect.send_command('show ip int brief | json-pretty')
    
    json_data = json.loads(output)

    int_number = len(json_data['TABLE_intf']['ROW_intf'])

    return int_number, json_data

data = get_information(load_variables())

print(json.dumps((data[0], data[1]), indent=2))

#this is a test on the new branch