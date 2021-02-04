import json

data = ["DisneyPlus", "Netflix", "Peacock"]
print(type(data))
json_string = json.dumps(data)
print(type(json_string))
print(json_string)