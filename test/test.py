import sys
import os
sys.path.append('../../')

from historical_distance import calculate_historical_distance

path = 'Q62090804/wiki_output'
filename = 'historical_distance.xlsx'
event_date = "2019-03-18T00:00:00UTC"

collection = []
for root, directories, files in os.walk(path):
    for file in files:
        if file.endswith('.naf'):
            collection.append(os.path.join(root, file))

historical_distance = calculate_historical_distance(iterable_of_nafs=collection,
                                                    event_date=event_date)
