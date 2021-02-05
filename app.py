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
        line = line[32:-5]
        api_array.append(line)

# Gets JSON from each API and puts it into api_array
def get_json(api_url):
    results = client.get(api_url)
    json_array.append(results)
    print(type(results))

# Takes json and creates excel
def convert(array):
    with open('out.xlsv') as outfile:
        for row_num, data in enumerate(array):
            writer = csv,writer(outfile)
            writer.writerows(data.iteritems())
        

# Takes json and creates excel (CURRENTLY BROKEN) 
def convert_b(array):

    df = pd.DataFrame(array)

    writer = pd.ExcelWriter('pandas_simple2.xlsx', engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Sheet1')

    writer.save()


if __name__ == "__main__":
    get_apis(api_array)
    for url in api_array:
        get_json(url)
    for json in json_array:
        convert_b(json)