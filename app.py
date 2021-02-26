import urllib.request
import json
import os.path
from os import path
import csv

def get_data_from_records():
    """This function reads the record.json file and returns a list of dictionaries
       Every dictionary is a single entry.

    Returns:
        [list]: list of entries
    """
    with open('record.json', 'rt', encoding='UTF8') as f:
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
    with urllib.request.urlopen(single_entry["api_endpoint"]) as url:
        data = json.loads(url.read().decode())

    # this part checks if the value is an empty string, if it is the parse code is not evaluated and an hyphen is assigned instead 
    if single_entry["metric_parse_code"] != "":
        metric_value = eval(single_entry["metric_parse_code"])
    else:
        metric_value = "-"
    if single_entry["date_parse_code"] != "":
        date_value = eval(single_entry["date_parse_code"])
    else:
        date_value = "-"
    return {'Serial No.': "", # I left this value blank because I reassign the value of serial number in line 78, so it doesn't matter what is was initially
            'Metric Name': single_entry["metric_name"],
            'City': single_entry["city"],
            'Metric Value': metric_value,
            'Date': date_value,
            'CoV Dimension ID': single_entry["cov_dimesion_id"] if single_entry["cov_dimesion_id"] != "" else "-", # if the value is "", assigns "-"
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
    # checks if the specific city's file doesn't exist

    if not path.exists(filename):
        # a csv file is created and a header is added 
        with open(filename, 'w', encoding='UTF8') as csvfile: # opened in write mode
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerow([key for key in data_dict.keys()]) # The keys of the dict are filled in as the header

    # this will read the existing csv file, and put the name of metrics that already exist in a list
    with open(filename, 'r', encoding='UTF8') as csvfile: # opened in read mode
        existing_data = csv.reader(csvfile)
        next(existing_data, None) # skips the header while reading
        existing_metrics = []

        # iterates through existing_data, and adds only the metric name in the existing_metrics list
        for row in existing_data:
            existing_metrics.append(row[1])

        # if the metric we are about to add doesn't exist in the existing_metrics list, then the metric is appended to the file
        if data_dict['Metric Name'] not in existing_metrics:
            with open(filename, 'a', encoding='UTF8') as csvfile: # opened in append mode
                writer = csv.writer(csvfile, lineterminator='\n')
                # Value of Serial No. is reassigned in the dict
                data_dict["Serial No."] = len(existing_metrics) + 1 # I add 1 to the lenght of existing_metrics list
                writer.writerow([value for value in data_dict.values()]) # This appends a new row with all the values in the dict.
            
if __name__ == "__main__":
    list_of_entries = get_data_from_records()
    # the loop below passes a single entry to every function. The loop runs until the list of entries is exhausted
    for single_entry in list_of_entries:
        data_dict = get_data_from_single_entry(single_entry)
        put_single_entry_in_csv(data_dict)
