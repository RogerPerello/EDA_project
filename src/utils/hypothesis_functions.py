from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from scipy.stats import f


'''Calculates the gini coefficient for a dataframe column. Returns the coefficient as well as a dataframe with the corresponding calculations'''
def calculate_gini(dataframe, x_column):
    '''Requires a dataframe and the name (string) of a column of numeric values'''
    dataframe = dataframe.copy()
    dataframe.insert(0, 'x_column_counts', 1)
    dataframe = dataframe.groupby(x_column).count()
    dataframe = dataframe.reset_index()
    dataframe.rename(columns={x_column:'xi','x_column_counts':'ni'}, inplace=True)
    dataframe = dataframe[['xi','ni']]
    dataframe['Ni'] = dataframe['ni'].cumsum()
    n = float(dataframe['Ni'][-1:])
    dataframe['xi·ni'] = dataframe['xi'] * dataframe['ni']
    dataframe['ui'] = dataframe['xi·ni'].cumsum()
    bigger_ui = float(dataframe['ui'][-1:])
    dataframe['pi'] = dataframe['Ni'] / n
    dataframe['qi'] = dataframe['ui'] / bigger_ui
    gini = 1 - sum(dataframe['qi'][:-1]) / sum(dataframe['pi'][:-1])
    return gini, dataframe


'''Based on a dataframe with a datetime index, creates a single column dataframe where each index represents a month and contains the sum of the values of the previous interval. 
Returns the same resulting dataframe with both a datetime index and an integer index'''
def date_index_to_monthly(dataframe, column_init, column_final, new_index):
    '''Requires a dataframe with a datetime index, the column to sum (string), the name for that column in the resulting dataframe (string), 
    and a list with the months of the new index (list of datetimes)'''
    '''Requires relativedelta from dateutil.relativedelta and pandas as pd'''
    losses_list = []
    for date in new_index:
        monthly_changes = dict()
        previous_date = date - relativedelta(months=1)
        df_rango = dataframe[(dataframe.index < date) & (dataframe.index >= previous_date)]
        changes_of_month = sum(df_rango[column_init])
        monthly_changes[column_final] = changes_of_month
        losses_list.append(monthly_changes)
    df_monthly = pd.DataFrame(losses_list)
    df_monthly_int_index = df_monthly.copy()
    df_monthly.index = new_index
    df_monthly_int_index.index = [str(period.month) for period in new_index]
    return df_monthly, df_monthly_int_index


''' Conditions a dataframe by a column value, applies a group by index, aggregates it by mean by default (median may be preferred) and drops some of the index values (or none)'''
def apply_condition_groupby_mean_drop(dataframe, column, index_name, value, index_drops=None, median=False):
    '''Requires a dataframe, a column name (string), the index name (string) and value to condition for. Accepts a list of index values and a boolean type as optional key arguments'''
    dataframe = dataframe[dataframe[column] == value]
    if median:
        dataframe = dataframe.groupby(index_name).median(numeric_only=True)
    else:
        dataframe = dataframe.groupby(index_name).mean(numeric_only=True)
    if index_drops[0]:
        dataframe = dataframe.drop(index=index_drops)
    return dataframe


'''In a datetime-indexed dataframe, for each datetime in the supplied list, looks for the duplicated string-values of the chosen column of strings. 
If one is not found for a certain datetime, looks for it at the next existent datetime (default increase = 1 day) until it's found. Then, assigns that string-value to the original supplied datetime
In the subsequent table, sums the corresponding number-values (that are in the chosen column of numeric values) for each string-value found for every datetime, and returns a two-column dataframe with each sum and its datetime'''
def sum_by_duplicated_values_and_datetime(dataframe, duplicated_column, sum_colum, datetime_list, days_increase=1):
    '''Requires positional arguments: a dataframe with a datetime index, the name (string) of a column of strings, the name (string) of a numeric column and a list of datetimes
    Accepts an integer as a key argument (default is 1)'''
    '''Requires relativedelta from dateutil.relativedelta and pandas as pd'''
    duplicated_list = dataframe[duplicated_column].drop_duplicates() 
    pre_dataframe_list = []
    for date in datetime_list: 
        current_date = date
        current_sum_list = [] 
        current_duplicated_list = []
        print(f'Now checking for {date}')
        while len(current_duplicated_list) != len(duplicated_list): 
            try:
                current_table = dataframe.loc[[date], [duplicated_column, sum_colum]] 
                if current_duplicated_list: 
                    missing_duplicates = list(set(duplicated_list) - set(current_duplicated_list)) 
                    print(f'Missing: {missing_duplicates}')
                    for duplicate in missing_duplicates: 
                        if duplicate in list(current_table[duplicated_column]):  
                            print(f'{duplicate} found at {date}')
                            current_sum_list.append(int(current_table.loc[current_table[duplicated_column] == duplicate][sum_colum])) 
                            current_duplicated_list.append(duplicate)
                    if len(current_duplicated_list) != len(duplicated_list): 
                        date += relativedelta(days=days_increase) 
                        print(f'Add {days_increase} day/s. Current date: {date}')
                else: 
                    current_sum_list.append(sum(current_table[sum_colum]))
                    current_duplicated_list += list(current_table[duplicated_column]) 
            except KeyError:
                print(f'{date} does not exist in the dataframe')
                date += relativedelta(days=days_increase)
                print(f'Add {days_increase} day/s. Current date: {date}')
        current_dict = {'date':current_date,
                        'Total': sum(current_sum_list)
                        }
        pre_dataframe_list.append(current_dict) 
        print(f'{current_date} has been filled')
        print('\n')
    df_total = pd.DataFrame(pre_dataframe_list) 
    return df_total


'''Calculates ftest (are both variances equal?) and returns its pvalue'''
def Ftest(group_1,group_2):
    '''Requires two lists as positional arguments'''
    '''Requires numpy as np and f from scipy.stats'''
    a1 = 1.0*np.array(group_1)
    n1 = len(a1)
    a2 = 1.0*np.array(group_2)
    n2 = len(a2)
    s1, s2 = np.std(a1,ddof=1), np.std(a2,ddof=1)
    test=(s1/s2)**2
    p_value=2*min(f.cdf(test,n1-1,n2-1),1-f.cdf(test,n1-1,n2-1))
    return p_value
