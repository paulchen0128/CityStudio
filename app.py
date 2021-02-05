import requests
import urllib.request, json 
import pandas as pd
from sodapy import Socrata
import xlsxwriter
import csv

# File name of API master list
api = 'api-list.txt'
# Array of API links
api_array = []
# Array of JSON entries
json_array = []

client = Socrata("data.sfgov.org", None)

# Goes through list and puts each API endpoint as array entry
def get_apis(array):
    f = open(api,'r')
    file = list(f)
    for line in file:
        line = line[:-1]
        api_array.append(line)

# Gets JSON from each API and puts it into api_array
def get_json(api_url):
    r = requests.get(api_url)
    json_dict = r.json()
    json_array.append(json_dict)

# Takes json and creates excel
def convert(json_dict):
    # file_name = str(str(counter)+ '.xlsx')
    file_name = input('Enter file name: ')
    file_name = file_name + '.xlsx'
    df = pd.DataFrame(json_dict)
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

if __name__ == "__main__":
    get_apis(api_array)
    for url in api_array:
        get_json(url)
    for json in json_array:
        convert(json)