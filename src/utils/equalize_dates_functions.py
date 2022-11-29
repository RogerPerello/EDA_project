def return_optimal_datetime(dataframes):
    '''Checks optimal index range'''
    '''Requires a list of dataframes, all with a datetime index, as a positional argument'''
    '''Used by equalize_indexes() in merge_functions.py'''
    lower_index = max([min(dataframe.index) for dataframe in dataframes])
    upper_index = min([max(dataframe.index) for dataframe in dataframes])
    return (lower_index.to_pydatetime(), upper_index.to_pydatetime())


def set_datetime_range(dataframe, min, max):
    '''Applies range to a datetime index according to a minimum and a maximum datetimes'''
    '''Requires three positional arguments: a list of dataframes with an index of datetime type, and two datetimes'''
    '''Used by equalize_indexes() in merge_functions.py'''
    dataframe_list = []
    for df in dataframe:
        df = df[df.index >= min]
        df = df[df.index <= max]
        dataframe_list.append(df)
    return dataframe_list


def equalize_indexes(dataframes):
    '''Repeatedly checks and applies optimal index until all dataframes have the same size'''
    '''Requires a list of dataframes with an index of datetime type as a positional argument'''
    '''Uses return_optimal_datetime() and set_datetime_range() from merge_functions.py'''
    current_max, current_min = 'any word', 'any word'
    while len(current_max) > 1 or len(current_min) > 1:
        min_date, max_date = return_optimal_datetime(dataframes)
        dataframes = set_datetime_range(dataframes, min_date, max_date)
        current_max = set([max(dataframe.index) for dataframe in dataframes])
        current_min = set([min(dataframe.index) for dataframe in dataframes])
    return dataframes
