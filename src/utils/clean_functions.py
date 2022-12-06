import pandas as pd


def decumulate_columns(dataframe, excluded=None):
    '''Turns values in cumulative columns to absolute values'''
    '''Requires a dataframe with a standard numerical index as a positional argument and it may have a list of excluded columns (list of strings) as a key argument'''
    if excluded is None:
        excluded = []
    for column in dataframe.columns:
        if column not in excluded:
            for index, value in reversed(list(enumerate(dataframe[column]))):
                if index != 0:
                    dataframe.loc[[index], column] = value - dataframe[column][index-1]


def index_by_datetime(dataframe, name='date'):
    '''Sets a datetime column as an index'''
    '''Requires a dataframe with a datetime column as a positional argument and it may have an alternative name (string) for that column as a key argument'''
    '''Requires pandas as pd'''
    dataframe.sort_values(name, inplace=True)
    dataframe[name] = pd.to_datetime(dataframe[name], exact=False)
    dataframe.set_index(name, inplace=True)
