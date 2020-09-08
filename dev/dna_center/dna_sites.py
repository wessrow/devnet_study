
import json
from dna_functions import req

def get_sites():

    response = req("/site")

    return response

def create_site():
    payload = {
        "type": "building",
        "site": {
            "building": {
                "name": "Denmark",
                "parentName": "Global/Sweden"
            }
        }
    }



    response = req("/site", "POST", payload=payload)

    return response

if __name__ == "__main__":
    #print(json.dumps(create_site(), indent=2))
    print(json.dumps(get_sites(), indent=2))
