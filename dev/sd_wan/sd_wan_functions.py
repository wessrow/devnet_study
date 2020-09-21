import sys
import requests
import json

requests.packages.urllib3.disable_warnings()

class SD_Wan():

    def __init__(self, vmanage, port, username, password):
        self.vmanage = vmanage
        self.port = port
        self.session = {}
        self._open_session(self.vmanage, port, username, password)

    def _open_session(self, vmanage, port, username, password):

        headers = {"Accept": "content/json", "Content-Type": "application/x-www-form-urlencoded"} 
        url = f"https://{vmanage}:{port}/j_security_check"
        parameters = {"j_username": username, "j_password": password}
        session = requests.session()

        response = session.post(url=url, headers=headers, data=parameters, verify=False)

        if b"<html>" in response.content:
            print("Error authenticating")
            sys.exit(0)

        self.session[vmanage] = session

    def _get_request(self, resource, params=None):

        url = f"https://{self.vmanage}:{self.port}{resource}"

        response = self.session[self.vmanage].get(url=url, params=params, verify=False)

        # print(response.status_code)
        data = response.json()

        return data

    def _post_request(self, resource, payload={}):

        headers = {"Accept": "content/json", "Content-Type": "application/json"} 
        url = f"https://{self.vmanage}:{self.port}{resource}"   
        payload = json.dumps(payload)

        response = self.session[self.vmanage].post(url=url, data=payload, headers=headers, verify=False)

        # print(response.status_code)
        if response.status_code != 403:
            data = response.json()

            return data

        else:
            print("Bad post-request - Check payload and/or resource")
            print(response.status_code)
            sys.exit(0)

    def get_all_devices(self, model=None):

        params = {"device-model": model} if model else None
        return self._get_request("/dataservice/device", params=params)

    def get_vedge_devices(self):

        return self._get_request("/dataservice/system/device/vedges")

    def get_certificate_list(self):

        return self._get_request("/dataservice/certificate/vsmart/list")

    def get_feature_templates(self):

        return self._get_request("/dataservice/template/feature")

    def create_user(self, username, password, group):

        resource = "/dataservice/admin/user"
        payload = {
            "group": [group],
            "description": "Added via API",
            "userName": username,
            "password": password
        }

        print(payload)

        return self._post_request(resource, payload)

def show_data():

    devices = sdwan.get_certificate_list()
    ammount = len(devices["data"])    
    print(json.dumps(devices["data"], indent=2), ammount)

    for device in devices["data"]:
        print(f"Host {device['host-name']} has system-IP-address {device['system-ip']}")

if __name__ == "__main__": 

    with open("dev/sd_wan/sd_wan_devices.json", "r") as handle:
        
        details = json.load(handle)["DevNet_Always_On"]
        vmanage = details["host"]
        port = details["port"]
        username = details["username"]
        password = details["password"]    

    sdwan = SD_Wan(vmanage, port, username, password)

    print(json.dumps(sdwan.get_all_devices()["data"], indent=2))

    #show_data()    

    # print(sdwan.create_user("wessrow", "cisco123", "netadmin"))

    # test_post = sdwan.post_request("/dataservice/admin/usergroup")
    # print(test_post)