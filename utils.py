import os
from lxml import etree
from datetime import datetime, date
import pandas as pd
import shutil

def timestamp_naf(path_to_doc):
    """load NAF file and extract title, publication date nd uri"""
    doc_tree = etree.parse(path_to_doc)
    root = doc_tree.getroot()
    target = root.find('nafHeader/fileDesc')
    creation_time = target.get('creationtime')
    title = target.get('title')
    target2 = root.find('nafHeader/public')
    uri = target2.get('uri')
    title_time = {'title':title, 'creation time': creation_time, 'uri':uri}
    return title_time

def timestamps_collection(collection):
    """load collection of naf files and extract list of publication dates"""
    timestamps = []

    for file in collection:
        timestamp = timestamp_naf(file)
        timestamps.append(timestamp)
    return timestamps

def time_in_correct_format():
    "Function that returns the current time (UTC)"
    datetime_obj = datetime.now()
    return datetime_obj.strftime("%Y-%m-%dT%H:%M:%SUTC")

def range_of_dates(event_date):
    """returns a list with a range of dates between the event date and the current date"""
    bottom_date = datetime(1677,9,23)

    if event_date.date() < bottom_date.date():
        event_date = "1677-09-23"
        print('Warning: bottom value as default for this event date. Real event date not implemented in pandas time frame')
    else:
        event_date = str(event_date)[:-9]

    current_date = time_in_correct_format()[:-12]
    mydates = pd.date_range(event_date,current_date).tolist()

    range_of_dates = []

    for date in mydates:
        date = str(date.date())
        range_of_dates.append(date)
    return range_of_dates

def validate_publication_date(event_date, timestamps):
    """validates whether the publication date is within the range of the event date and the current date"""
    known_dates = []
    unknown_dates = []

    dates = range_of_dates(event_date)

    for timestamp in timestamps:
        timestamp_stripped = timestamp['creation time'][:-12]
        if timestamp_stripped in dates:
            known_dates.append(timestamp)
        else:
            unknown_dates.append(timestamp)
    return known_dates, unknown_dates

def calculate_difference(list_of_timestamps, event_date):
    """calculates the difference between the publication dates and the event date and creates new list with extended dictionaries"""
    event_date_replace = str(event_date).replace('-',',')
    event_date = event_date_replace[:10]
    event_year = int(event_date[:4])
    event_month = int(event_date[5:7])
    event_day = int(event_date[8:])

    known_distance = []

    for info in list_of_timestamps:
        timestamp = info['creation time']
        timestamp_replace = timestamp.replace('-',',')
        text_date = timestamp_replace[:10]
        text_year = int(text_date[:4])
        text_month = int(text_date[5:7])
        text_day = int(text_date[8:])
        f_date = date(event_year,event_month,event_day)
        l_date = date(text_year,text_month,text_day)
        delta = l_date - f_date
        info['historical distance'] = delta.days
    return list_of_timestamps

def categorize_in_time_buckets(known_distance,time_buckets):
    '''extend dictionary with categorization of the historical distance in time buckets'''

    for info in known_distance:
        for key, value in time_buckets.items():
            if info['historical distance'] in value:
                time_bucket = key
                info['time bucket'] = time_bucket
        if "time bucket" not in info:
            default_bucket = "outside bucket range"
            info['time bucket'] = default_bucket
            print("Warning: historical distance falls outside of time bucket range.")
    return known_distance

def create_output_folder(output_folder,start_from_scratch):
    '''creates output folder for export dataframe'''
    folder = output_folder

    if os.path.isdir(folder):
        if start_from_scratch == True:
            shutil.rmtree(folder)

    if not os.path.isdir(folder):
        os.mkdir(folder)

def timestamps_to_format(known_timestamps,unknown_timestamps,xlsx_path,output_folder,start_from_scratch):
    """
    lists of dictionaries to excel
    """
    headers = ['title', 'timestamp', 'historical distance','time bucket','uri']

    list_of_lists = []

    for info in known_timestamps:
        one_row = [info['title'],info['creation time'],info['historical distance'],info['time bucket'],info['uri']]
        list_of_lists.append(one_row)
    for info in unknown_timestamps:
        a_row = [info['title'],info['creation time'], 'unknown','unknown',info['uri']]
        list_of_lists.append(a_row)

    df = pd.DataFrame(list_of_lists, columns=headers)

    if output_folder != None:
        create_output_folder(output_folder=output_folder,
                            start_from_scratch=start_from_scratch)
        df.to_excel(xlsx_path, index=False)
    return df
