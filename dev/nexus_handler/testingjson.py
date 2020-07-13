import json

with open('../nexus_handler/devnet_env_var.json', 'r') as variables:
    my_dict = json.load(variables)

print(my_dict['Devnet_Nexus']['ios_nx_ip'])