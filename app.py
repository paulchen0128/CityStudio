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
    with xlsxwriter.Workbook('test4.xlsx') as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(array):
            worksheet.write_row(row_num, 0, data)

if __name__ == "__main__":
    get_apis(api_array)
    for url in api_array:
        get_json(url)
    for json in json_array:
        convert(json)