import json

with open('devnet_env_var.json', 'r') as variables:
    my_dict = json.load(variables)

print(my_dict['ios_nx_ip'])