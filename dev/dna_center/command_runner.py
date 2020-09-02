import json
import time
import requests
from dna_functions import req, wait_for_task, load_task_result

def send_command():

    payload = {
                "name": "show ver",
                "commands": ["ping 8.8.8.8"],
                "deviceUuids": ["1cfd383a-7265-47fb-96b3-f069191a0ed5"]
            }

    response = req('/network-device-poller/cli/read-request', "POST", payload)

    return response

def main():

    taskId = send_command()['response']['taskId']
    print(taskId)

    response = load_task_result(wait_for_task(taskId))    

    return response    

if __name__ == "__main__":
    print(main())
