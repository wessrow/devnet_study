import json
from netmiko import ConnectHandler

def load_variables():

    with open('../nexus_handler/devnet_env_var.json', 'r') as variables:
        device = json.load(variables)

    ios_device = {
        'device_type': 'cisco_ios',
        'ip': device['Devnet_Nexus']['ios_nx_ip'],
        'username': device['Devnet_Nexus']['ios_nx_user'],
        'password': device['Devnet_Nexus']['ios_nx_password'],
        'port': 8181
    }

    return ios_device

print(json.dumps(load_variables(), indent=2))