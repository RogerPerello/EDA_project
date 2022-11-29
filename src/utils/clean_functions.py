import pandas as pd


def change_to_numeric(dataframe, columns):
    '''Requires a dataframe and a list of columns as positional arguments'''
    for column in columns:
        dataframe[column] = pd.to_numeric(dataframe[column])


def decumulate_columns(dataframe, excluded=None):
    '''Turns values in cumulative columns to absolute values'''
    '''Requires a dataframe with a numerical index as a positional argument and it may have a list of excluded columns as a key argument'''
    if excluded is None:
        excluded = []
    for column in dataframe.columns:
        if column not in excluded:
            for index, value in reversed(list(enumerate(dataframe[column]))):
                if index != 0:
                    dataframe.loc[[index], column] = value - dataframe[column][index-1]


def index_by_datetime(dataframe, name='date'):
    '''Sets datetime column as index'''
    '''Requires a dataframe with a datetime column as a positional argument and it may have an alternative name for that column as a key argument'''
    '''Requires pandas as pd'''
    for column in dataframe.columns:
        if column == name:
            dataframe.sort_values(column, inplace=True)
            dataframe[column] = pd.to_datetime(dataframe[column], exact=False)
            dataframe.set_index(name, inplace=True)
            break
