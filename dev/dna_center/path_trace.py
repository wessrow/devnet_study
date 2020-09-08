import json
import time
from dna_functions import req, wait_for_task

def main():

    payload = {
        "destIP": "10.10.22.253",
        "sourceIP": "10.10.22.114",
    }

    flowId = req("/flow-analysis", "POST", payload)
    print(flowId["response"]["taskId"])

    time.sleep(10)

    #response = req(f"/flow-analysis/{flowId['response']['flowAnalysisId']}")

    #return response

if __name__ == "__main__":
    print(json.dumps(main(), indent=2)) 