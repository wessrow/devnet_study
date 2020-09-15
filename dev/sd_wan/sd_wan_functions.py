import sys
import requests
import json

requests.packages.urllib3.disable_warnings()

class SD_Wan():

    def __init__(self, vmanage, username, password):
        self.vmanage = vmanage
        self.session = {}
        self.open_session(self.vmanage, username, password)

    def open_session(self, vmanage, username, password):

        headers = {"Accept": "content/json", "Content-Type": "application/x-www-form-urlencoded"} 
        url = f"https://{vmanage}:443/j_security_check"
        parameters = {"j_username": username, "j_password": password}
        session = requests.session()

        response = session.post(url=url, headers=headers, data=parameters, verify=False)

        if b"<html>" in response.content:
            print("Error authenticating")
            sys.exit(0)

        self.session[vmanage] = session

    def get_request(self, resource):

        url = f"https://{self.vmanage}:443{resource}"

        response = self.session[self.vmanage].get(url, verify=False)

        # print(response.status_code)
        data = response.json()

        return data

    def post_request(self, resource, payload={}):

        headers = {"Accept": "content/json", "Content-Type": "application/json"} 
        url = f"https://{self.vmanage}:443{resource}"   
        payload = json.dumps(payload)

        response = self.session[self.vmanage].post(url=url, data=payload, headers=headers, verify=False)

        # print(response.status_code)
        if response.status_code != 403:
            data = response.json()

            return data

        else:
            print("Bad post-request - Check payload and/or resource")
            sys.exit(0)

if __name__ == "__main__": 

    with open("dev/sd_wan/sd_wan_devices.json", "r") as handle:
        
        details = json.load(handle)["DevNet_Always_On"]
        vmanage = details["host"]
        username = details["username"]
        password = details["password"]      

    sdwan = SD_Wan(vmanage, username, password)

    devices = sdwan.get_request("/dataservice/device")
    
    # print(json.dumps(devices["data"][0], indent=2))

    for device in devices["data"]:
        print(f"Host {device['host-name']} has system-IP-address {device['system-ip']}")

    # test_post = sdwan.post_request("/dataservice/admin/usergroup")
    # print(test_post)