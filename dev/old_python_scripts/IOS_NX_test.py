#!/usr/bin/env python3
import os
import json
from netmiko import ConnectHandler

def Get_Information():
    xe_os = {
    'device_type': 'cisco_ios',
    'ip': os.environ['ios_nx_ip'],
    'username': os.environ['ios_nx_usr'],
    'password': os.environ['ios_nx_psswrd'],
    'port': 8181
    }

    net_connect = ConnectHandler(**xe_os)
    output = net_connect.send_command('show ip int brief | json-pretty')
    
    json_data = json.loads(output)

    int_number = len(json_data['TABLE_intf']['ROW_intf'])

    return int_number, json_data

def Down_Interface(int_number, json_data):
    down = 'down'
    
    interfaces_down = []

    for x in range(int_number):
        if json_data['TABLE_intf']['ROW_intf'][x]['proto-state'] == down:
            interfaces_down.append('{}: {} is {}'.format(json_data['TABLE_intf']['ROW_intf'][x]['intf-name'], json_data['TABLE_intf']['ROW_intf'][x]['prefix'], json_data['TABLE_intf']['ROW_intf'][x]['proto-state']))

    return interfaces_down

def Up_Interface(int_number, json_data):
    up= 'up'
    
    interfaces_up = []

    for x in range(int_number):
        if json_data['TABLE_intf']['ROW_intf'][x]['proto-state'] == up:
            interfaces_up.append('{}: {} is {}'.format(json_data['TABLE_intf']['ROW_intf'][x]['intf-name'], json_data['TABLE_intf']['ROW_intf'][x]['prefix'], json_data['TABLE_intf']['ROW_intf'][x]['proto-state']))

    return interfaces_up

result = Get_Information()

print('\n'.join(Down_Interface(result[0], result[1])))
print('\n'.join(Up_Interface(result[0], result[1])))