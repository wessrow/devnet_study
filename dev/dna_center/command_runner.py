import json
import time
import sys
import requests
from dna_functions import req, wait_for_task, load_task_result

def send_command(command="show clock"):

    payload = {
                "commands": [f"{command}"],
                "deviceUuids": ["1cfd383a-7265-47fb-96b3-f069191a0ed5"]
            }

    response = req('/network-device-poller/cli/read-request', "POST", payload)

    return response

def main(command="show clock"):

    taskId = send_command(command)['response']['taskId']

    response = load_task_result(wait_for_task(taskId, 5, 10))    

    return response    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(main())

    else:
        print(main(sys.argv[1]))
        
