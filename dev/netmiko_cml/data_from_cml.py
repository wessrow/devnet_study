import json
from netmiko import ConnectHandler

def load_device_information():

    with open('dev/netmiko_cml/connection_details.json', 'r') as variables:

        devices = json.load(variables)
        return devices

def get_interface_information(device, number):

    try:
        router = device['{}'.format(number)]

        net_connect = ConnectHandler(**router)
        output = net_connect.send_command('sh ip int brief', use_textfsm=True)

        int_number = len(output)

        return output, int_number

    except:
        
        print('Failure to connect to {}, {}'.format(number, router['ip']))
        return False
        
def get_up_interfaces(data, interfaces):

    up = 'up'
    up_interfaces = []

    for x in range(interfaces):
        if data[x]['proto'] == up:
            up_interfaces.append('\t {} is up, IP-address: {}'.format(data[x]['intf'], data[x]['ipaddr']))

    return up_interfaces

def presenting_interfaces():

    devices = list(load_device_information())
    count = len(devices)

    for x in range(count):

        try:
            data = get_interface_information(load_device_information(), devices[x])

            if data == False:
                raise Exception

            else:
                print('Device {} has the following active interfaces:'.format(devices[x]))
                print('\n'.join(get_up_interfaces(data[0], data[1])), '\n')

        except Exception:
            print('\t Connection Error - No interfaces to display.', '\n')

presenting_interfaces()
