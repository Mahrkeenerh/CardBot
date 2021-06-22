import json

with open("oath_reference.json") as json_file:
    data = json.load(json_file)

out_dict = {}

for item in data:
    out_dict[item["Card Name"].lower()] = [(x, item[x]) for x in item]

with open("database.json", "w") as json_file:
    json.dump(out_dict, json_file)
