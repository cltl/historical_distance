from .utils import timestamps_collection, validate_publication_date, calculate_difference, timestamps_to_format, categorize_in_time_buckets


def calculate_historical_distance(iterable_of_nafs,
                                    event_date,
                                    time_buckets,
                                    xlsx_path=None,
                                    output_folder=None,
                                    start_from_scratch=True):
    '''
    provides the spread of historical distance in days for a corpus of reference texts
    :param path_to_nafs: path to a directory containing a collection of naf files
    :param event_date: the date of the event (YY-MM-DD)
    :param filename: name.type for the output table
    :type iterable_of_nafs: list
    :type event_date: datetime.datetime
    '''
    timestamps = timestamps_collection(collection=iterable_of_nafs)
    known_timestamps, unknown_timestamps = validate_publication_date(event_date=event_date,
                                                                    timestamps=timestamps)
    known_distance = calculate_difference(list_of_timestamps=known_timestamps,
                                                event_date=event_date)
    known_distance_time_buckets = categorize_in_time_buckets(known_distance=known_distance,
                                                            time_buckets=time_buckets)
    df = timestamps_to_format(known_timestamps=known_distance_time_buckets,
                            unknown_timestamps=unknown_timestamps,
                            xlsx_path=xlsx_path,
                            output_folder=output_folder,
                            start_from_scratch=start_from_scratch)
    return df
