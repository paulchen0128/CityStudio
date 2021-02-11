import requests
import urllib.request, json 
import pandas as pd
from sodapy import Socrata
import xlsxwriter
import openpyxl
from openpyxl import load_workbook
import csv

# File name of API master list
api = 'record.txt'
# Array of API, name of metric and parsecode
api_array = []
# Array of JSON entries
json_array = []

client = Socrata("data.sfgov.org", None)

# Goes through file of API, 
def get_apis(array):
    f = open(api,'r')
    file = list(f)
    for line in file:
        line_split = line.split(',')
        api_array.append(line_split)
        

# Gets value needed by using parsecode from the data of API
# api[3] = city
# api[1] = metric name
def get_value(api):
    r = requests.get(api[0])
    data = r.json()
    parsecode = remove_quotes(api[2])
    value = eval(parsecode)
    city = api[3]
    metric_name = api[1]
    return value, metric_name, city

# Removes quotes around string
def remove_quotes(string):
    value = string.replace("'","")
    return value

# Takes value and city as input and places data as a row in correct excel file
def fill_excel(value, metric_name, city):
    file_name = city + '.csv'
    dict = {"Metric Name" : metric_name,
            "Value"       : value} 
    df = pd.DataFrame(dict, index=[0])
    df.to_csv(file_name, mode='a', header=False)

if __name__ == "__main__":
    get_apis(api)
    for entry in api_array:
        data = get_value(entry)
        fill_excel(data[0], data[1], data[2])