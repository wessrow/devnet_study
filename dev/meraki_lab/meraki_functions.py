import os
import json
import requests

class Meraki_SDK:

    def __init__(self, api_key, verify=True):
        # Konstruktor för klassen, importerar API-nyckel och anger verifiering av
        # SSL-certifikat samt skapar variebler att referera till i klassen.

        key = api_key
        self.headers = { "X-Cisco-Meraki-API-Key": key }
        self.baseurl = "https://api.meraki.com/api/v1"
        self.verify = verify

        # Om vi inte verifierar SSL-certifikat vill vi inte få varningar
        if verify == False:
            requests.packages.urllib3.disable_warnings()

    def _req(self, resource, method="get"):        
        # Intern funktion för att utföra requests med requests-biblioteket.
        # Standard metod är GET, men andra går att utföra.        
        response = requests.request(url=f"{self.baseurl}{resource}", method=method,
                                    headers=self.headers, verify=self.verify).json()

        return response
    
    def get_orgs(self):
        # Samlar in en lista över orginisationer
        response = self._req("/organizations")
        return response

    def get_org_networks(self, orgId):
        # Samlar in en lista över nätverk i orginisationen
        try:
            response = self._req(f"/organizations/{orgId}/networks")
            return response

        except Exception as ex:
            return f"Error: {ex}\nProbable cause: invalid orgId"

    def get_network_devices(self, networkId):
        # Samlar in en lista över enheter i ett givet nätverk
        try:
            response = self._req(f"/networks/{networkId}/devices")
            return response

        except Exception as ex:
            return f"Error: {ex}\nProbable cause: invalid networkId"

    def get_device_serials(self, networkId, keyname="lanIp"):
        # Samlar serienummer identifierade med valfria keys - fallback är mac-adress som key

        serials = {}
        devices = self.get_network_devices(networkId)

        for device in devices:
            try:
                if device[keyname] == None:
                    serials.update({f"{device['mac']}": f"{device['serial']}"})
                else:
                    serials.update({f"{device[keyname]}": f"{device['serial']}"})                        
            except KeyError:
                serials.update({f"{device['mac']}": f"{device['serial']}"})
                
        return {f"{networkId}":serials}

    def get_device_serials_all(self, orgId, keyname="lanIp"):

        networks = meraki.get_org_networks(orgId)
        all_sn = {}

        for network in networks:
            networkId = network["id"]
            all_sn.update(self.get_device_serials(networkId, keyname))
            print(f"Klar med {networkId}")

        return all_sn

if __name__ == "__main__":

    # Publik DevNet-sandlåda för att testa
    key = "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"
    meraki = Meraki_SDK(api_key=key, verify=False)    

    print(json.dumps(meraki.get_device_serials_all(681155), indent=2))

    # print(json.dumps(meraki.get_network_devices("N_566327653141899127"), indent=2))
