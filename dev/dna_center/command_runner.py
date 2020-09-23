#!/usr/bin/env python3

import json
import sys
from dna_functions import req, wait_for_task, load_task_result

def get_deviceId():

    devices = req('/network-device')['response']

    uuids = []

    for device in devices:
       uuids.append(device["id"])

    return uuids

def send_command(command="show clock", devices=["1cfd383a-7265-47fb-96b3-f069191a0ed5"]):

    taskIds = []

    for device in devices:
        
        payload = {
                    "commands": [f"{command}"],
                    "deviceUuids": [f"{device}"]
                }

        response = req('/network-device-poller/cli/read-request', "POST", payload)

        if response == None:
            taskIds.append("Error")

        else:
            taskIds.append(response)

    return taskIds

def main(command="ping 10.10.22.253"):
    
    taskIds = send_command(command, get_deviceId())
    finished_tasks = []
    
    try:
        for taskId in taskIds:
            id = taskId["response"]["taskId"]
            response = load_task_result(wait_for_task(id)["fileId"])
            finished_tasks.append(response)
            print(f"Finished with Task ID: {id}")

        return finished_tasks  

    except Exception as ex:
        print(f"Error: {ex}")
        sys.exit(1)     

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(json.dumps(main(), indent=2))

    else:
        print(json.dumps(main(sys.argv[1]), indent=2))
        
