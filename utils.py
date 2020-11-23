import os
from lxml import etree
from datetime import datetime, date
import pandas as pd

def timestamp_naf(path_to_doc):
    """load NAF file and extract publication date"""
    doc_tree = etree.parse(path_to_doc)
    root = doc_tree.getroot()
    target = root.find('nafHeader/fileDesc')
    creation_time = target.get('creationtime')
    title = target.get('title')
    target2 = root.find('nafHeader/public')
    uri = target2.get('uri')
    title_time = (title, creation_time, uri)
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
    event_date = event_date[:-12]
    current_date = time_in_correct_format()[:-12]
    mydates = pd.bdate_range(event_date,current_date).tolist()

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
        timestamp_stripped = timestamp[1][:-12]
        if timestamp_stripped in dates:
            known_dates.append(timestamp)
        else:
            unknown_dates.append(timestamp)
    return known_dates, unknown_dates

def calculate_difference(list_of_timestamps, event_date):
    """calculates the difference between the publication dates and the event date and creates new list with extended tuples"""
    event_date_replace = event_date.replace('-',',')
    event_date = event_date_replace[:10]
    event_year = int(event_date[:4])
    event_month = int(event_date[5:7])
    event_day = int(event_date[8:])

    known_distance = []

    for info in list_of_timestamps:
        timestamp = info[1]
        timestamp_replace = timestamp.replace('-',',')
        text_date = timestamp_replace[:10]
        text_year = int(text_date[:4])
        text_month = int(text_date[5:7])
        text_day = int(text_date[8:])
        f_date = date(event_year,event_month,event_day)
        l_date = date(text_year,text_month,text_day)
        delta = l_date - f_date
        known_distance.append((info[0],info[1],delta.days,info[2]))
    return known_distance

def categorize_in_time_buckets(known_distance):
    '''extend the tuple with categorization of the historical distance in time buckets'''
    known_distance_info = []

    for info in known_distance:
        if info[2] == 0:
            time_bucket = 1
        elif info[2] == 1:
            time_bucket = 2
        elif info[2] in range(3,30):
            time_bucket = 3
        else:
            time_bucket = 4
        known_distance_info.append((info[0],info[1],info[2],time_bucket,info[3]))
    return known_distance_info

def timestamps_to_format(known_timestamps,unknown_timestamps,output_folder):
    """
    lists of tuples to excel
    """
    headers = ['title', 'timestamp', 'hist. dist.','time buck.','uri']

    list_of_lists = []

    for info in known_timestamps:
        one_row = [info[0],info[1],info[2],info[3],info[4]]
        list_of_lists.append(one_row)
    for info in unknown_timestamps:
        a_row = [info[0],info[1], 'unknown','unknown',info[2]]
        list_of_lists.append(a_row)

    df = pd.DataFrame(list_of_lists, columns=headers)

    if output_folder != None:
        df.to_excel(output_folder, index=False)
    return df
