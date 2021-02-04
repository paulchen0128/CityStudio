import json
import requests
import pandas as pd

data = ["DisneyPlus", "Netflix", "Peacock"]
print(type(data))
json_string = json.dumps(data)
print(type(json_string))
print(json_string)


###json to excel
r = requests.get("https://data.sfgov.org/resource/g8m3-pdis.json")
my_dict = r.json()

print(my_dict)
df = pd.DataFrame(my_dict)

writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')


df.to_excel(writer, sheet_name='Sheet1')

writer.save()