import urllib.request
import json
import os.path
from os import path
import csv
import pandas as pd

def get_data_from_records():
    """This function reads the record.json file and returns a list of dictionaries
       Every dictionary is a single entry.

    Returns:
        [list]: list of entries
    """
    with open('record.json') as f:
        list_of_entries = json.load(f)
    return list_of_entries

def get_data_from_single_entry(single_entry):
    """This function gets the data from the API, and returns a dictionary with all the key-value pairs
    
    Args:
        single_entry (dict): this is a dictionary that represents one entry/row

    Returns:
        [dict]: this dict contains the exact data in the form of key-value pairs, which will be directly filled in the csv files
    """
    # get data from api
    try: 
        with urllib.request.urlopen(single_entry["api_endpoint"]) as url:
            data = json.loads(url.read().decode())
    except ValueError as e: 
        data = pd.read_csv(single_entry["api_endpoint"],sep=',')    
    # this part checks if the value is an empty string, if it is the parse code is not evaluated and an hyphen is assigned instead 
    if single_entry["metric_parse_code"] != "":
        metric_value = eval(single_entry["metric_parse_code"])
    else:
        metric_value = "-"
    if not single_entry["date_parse_code"].isdigit() and single_entry["date_parse_code"] != "":
        date_value = eval(single_entry["date_parse_code"])
    elif single_entry["date_parse_code"] == "":
        date_value = "-"
    else:
        date_value = single_entry["date_parse_code"]

    return {'Serial No.': "", # I left this value blank because I reassign the value of serial number in line 78, so it doesn't matter what is was initially
            'Metric Name': single_entry["metric_name"],
            'City': single_entry["city"],
            'Metric Value': metric_value,
            'Date': date_value,
            'CoV Dimension ID': single_entry["cov_dimension_id"] if single_entry["cov_dimension_id"] != "" else "-", # if the value is "", assigns "-"
            'CoV Metric Name' : single_entry["cov_metric_name"] if single_entry["cov_metric_name"] != "" else "-", # if the value is "", assigns "-"
            'API Endpoint': single_entry["api_endpoint"]
    }
    
def put_single_entry_in_csv(data_dict):
    """This function takes the dictionary generated in the get_data_from_single_entry function and puts in a csv file of the city.
       If the csv file doesn't exist, it creates one with a header. The keys in the data_dict are filled in as a header. If the file 
       exists, it appends to the respective city's file.

    Args:
        data_dict (dict): This is the dict returned by get_data_from_single_entry function
    """

    filename = f"{data_dict['City']}.csv"
    df = pd.DataFrame(data_dict, index=[])
    if not path.exists(filename):
        df.to_csv(filename, mode='w', header=True, index=False)
       
    existing_data = pd.read_csv(filename)
    if len(existing_data) == 0:
        data_dict["Serial No."] = len(existing_data) + 1
        df = pd.DataFrame(data_dict, index=[])
        df = df.append(data_dict, ignore_index=True)
        df.to_csv(filename, mode='a', header=False, index=False)
        return

    for i in existing_data.index:
        existing_metric_name = existing_data['Metric Name'][i]
        existing_date = str(existing_data['Date'][i])
        existing_value = existing_data['Metric Value'][i]

        if existing_metric_name == data_dict['Metric Name'] and existing_date == data_dict['Date']:  # if a existing_data has the same metric name and date as data_dict
            if existing_value != data_dict['Metric Value']:
                existing_data.replace(existing_data['Metric Value'][i], data_dict['Metric Value'], inplace=True)
                existing_data.to_csv(filename, index=False)
            return
    
    data_dict["Serial No."] = len(existing_data) + 1
    existing_data = existing_data.append(data_dict, ignore_index=True)
    existing_data.to_csv(filename, index=False)


if __name__ == "__main__":
    list_of_entries = get_data_from_records()
    # the loop below passes a single entry to every function. The loop runs until the list of entries is exhausted
    for single_entry in list_of_entries:
        data_dict = get_data_from_single_entry(single_entry)
        put_single_entry_in_csv(data_dict)
