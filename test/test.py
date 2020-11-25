import sys
import os
sys.path.append('../../')

from historical_distance import calculate_historical_distance
from datetime import datetime

path = 'Q62090804/wiki_output'
output_folder = 'output'
xlsx_path = 'output/historical_distance.xlsx'
event_date = datetime(2019,3,18)

collection = []

for root, directories, files in os.walk(path):
    for file in files:
        if file.endswith('.naf'):
            collection.append(os.path.join(root, file))

historical_distance = calculate_historical_distance(iterable_of_nafs=collection,
                                                    event_date=event_date,
                                                    xlsx_path=xlsx_path,
                                                    output_folder=output_folder)
