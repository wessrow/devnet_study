import xmltodict

loopback = 10

payload = {
    "config": {
        "native":{
            "@xmlns": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
            'interface operation="delete"': {
                "Loopback": {
                    "name": "{0}".format(loopback),
                    "ip": {
                        "address ": {
                            "primary": {
                                "address": "{0}.{0}.{0}.{0}".format(loopback),
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

print(xpayload)