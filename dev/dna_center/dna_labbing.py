#!/usr/bin/env python3

import requests
import json
from dna_functions import req

if __name__ == "__main__":
    print(json.dumps(req('/network-device/count'), indent=2))