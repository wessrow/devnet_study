import json
import xmltodict
from ncclient import manager

def load_device():

    with open("dev/netconf_lab1/connection_details.json" , "r") as handle:
        devices = json.load(handle)
        return devices

def get_capabilites():

    connect_info = load_device()["R5"]

    with manager.connect(**connect_info) as conn:

        for capability in conn.server_capabilities:
            print(capability)

def get_interfaces():

    connect_info = load_device()["R5"]

    with manager.connect(**connect_info) as conn:

        config = open("dev/netconf_lab1/interface_template.xml").read()
            
        payload = config.format(int_name="GigabitEthernet4",
                                int_desc="Testing!",
                                int_state="true",
                                ip_address="5.5.5.5",
                                subnet_mask="255.255.255.0"            
                                )

        #response = conn.get_config(source="running", filter=("xpath", "/native/interface/GigabitEthernet"))
        response = conn.edit_config(target="running", config=payload)

        # Parse interfaces on device
        jresponse = xmltodict.parse(response.xml)

    return jresponse

def get_telemetry_sub():

    connect_info = load_device()["R6"]

    with manager.connect(**connect_info) as conn:

        response = conn.get_config(source="running", filter=("xpath", "/mdt-config-data"))  # ("xpath", "/mdt-config-data")
        jresponse = xmltodict.parse(response.xml)

    return jresponse

def create_telemetry_sub():

    connect_info = load_device()["R6"]

    payload = open("dev/netconf_lab1/telemetry_ospf.xml").read()

    with manager.connect(**connect_info) as conn:

        response = conn.edit_config(target="running", config=payload)
        jresponse = xmltodict.parse(response.xml)["rpc-reply"]

    return jresponse

if __name__ == "__main__":
    #get_capabilites()
    
    #print(json.dumps(get_interfaces(), indent=2))

    print(json.dumps(get_telemetry_sub(), indent=2))

    #print(json.dumps(create_telemetry_sub(), indent=2))