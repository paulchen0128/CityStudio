import urllib.request
import json
import os.path
from os import path
import csv

def get_data_from_records():
    with open('record.json') as f:
        list_of_entries = json.load(f)
    return list_of_entries

def get_data_from_single_entry(single_entry):
    with urllib.request.urlopen(single_entry["api_endpoint"]) as url:
        data = json.loads(url.read().decode())
    if single_entry["metric_parse_code"] != "":
        metric_value = eval(single_entry["metric_parse_code"])
    else:
        metric_value = "-"
    if single_entry["date_parse_code"] != "":
        date_value = eval(single_entry["date_parse_code"])
    else:
        date_value = "-"
    return {'Serial No.': "",
            'Metric Name': single_entry["metric_name"],
            'City': single_entry["city"],
            'Metric Value': metric_value,
            'Date': date_value,
            'CoV Dimension ID': single_entry["cov_dimesion_id"] if single_entry["cov_dimesion_id"] != "" else "-",
            'CoV Metric Name' : single_entry["cov_metric_name"] if single_entry["cov_metric_name"] != "" else "-",
            'API Endpoint': single_entry["api_endpoint"]
    }
    
def put_single_entry_in_csv(data_dict):
    filename = f"{data_dict['City']}.csv"
    if not path.exists(filename):
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerow([key for key in data_dict.keys()])
    with open(filename, 'r') as csvfile:
        existing_data = csv.reader(csvfile)
        next(existing_data, None)
        existing_metrics = []
        existing_cities = []
        for row in existing_data:
            existing_metrics.append(row[1])
            existing_cities.append(row[2])
        if data_dict['Metric Name'] not in existing_metrics or data_dict['City'] not in existing_cities:
            with open(filename, 'a') as csvfile:
                writer = csv.writer(csvfile, lineterminator='\n')
                data_dict["Serial No."] = len(existing_metrics) + 1
                writer.writerow([value for value in data_dict.values()])
            
if __name__ == "__main__":
    list_of_entries = get_data_from_records()
    for single_entry in list_of_entries:
        data_dict = get_data_from_single_entry(single_entry)
        put_single_entry_in_csv(data_dict)
