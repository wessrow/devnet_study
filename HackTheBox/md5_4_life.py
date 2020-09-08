import requests
import hashlib
import re

url="http://docker.hackthebox.eu:32000/"

r = requests.Session()
response = r.get(url)

encode = re.search(r"<h3 align='center'>(\w*)</h3>", response.text)

md5hash = hashlib.md5(encode.group(1).encode('utf-8')).hexdigest()

payload = {"hash": md5hash}

send = r.post(url = url, data = payload)

print(send.text)