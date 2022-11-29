from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy as np
from scipy.stats import f 

'''Checks if standard deviations of two groups >30 are affected by the same factors and therefore keep their proportion'''
def ftest_stds(grupo1,grupo2):
    '''Requires 2 numerical iterables >30 as positional arguments'''
    a1 = np.array(grupo1)
    n1 = len(a1)
    a2 = np.array(grupo2)
    n2 = len(a2)
    s1, s2 = np.std(a1), np.std(a2)
    test=s1/s2
    p_valor=2*min(f.cdf(test,n1,n2),1-f.cdf(test,n1,n2))
    if p_valor > 0.05:
        return True, p_valor
    else:
        return False, p_valor


'''Calculates the gini coefficient for a dataframe column. Returns the coefficient as well as a dataframe with the corresponding calculations'''
def calculate_gini(dataframe, x_column):
    '''Requires a dataframe and the name of a column of numeric values'''
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


'''Based on a dataframe with a datetime index, creates a single column dataframe with an index by month containing the sum of the values of each previous interval. 
Returns the same dataframe with a datetime index and an integer index'''
def date_index_to_monthly(dataframe, column_init, column_final, new_index):
    '''Requires a dataframe with a datetime index, the column to sum (string), the name of the column in the final dataframe (string), 
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


'''Based on a dataframe with a datetime index, creates a single column dataframe with an index by month containing the sum of the values of each previous interval. 
Returns the same dataframe with a datetime index and an integer index'''
def date_index_to_monthly(dataframe, column_init, column_final, new_index):
    '''Requires a dataframe with a datetime index, the column to sum (string), the name of the column in the final dataframe (string), 
    and a list with the months of the new index (list of datetimes)'''
    '''Requires pandas as pd'''
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

''' Limits a dataframe by a column value, applies a groupby index, aggregates it by mean by default (median may be preferred) and drops some of the index values (or none)'''
def applies_where_groupby_mean_drop(dataframe, column, index_name, value, index_drops=None, median=False):
    '''Requires a dataframe, a column name (string), an index name (string) and value to look for. Accepts a list of index values and a boolean type as optional key arguments'''
    dataframe = dataframe[dataframe[column] == value]
    if median:
        dataframe = dataframe.groupby(index_name).median(numeric_only=True)
    else:
        dataframe = dataframe.groupby(index_name).mean(numeric_only=True)
    if index_drops[0]:
        dataframe.drop(index=index_drops, inplace=True)
    return dataframe


'''Conditions a datetime-indexed dataframe, for each datetime in the supplied list, with the duplicated values of the chosen column of strings. 
If one is not found for a certain datetime, looks for it at the next existent datetime (default increase = 1 day).
In the subsequent table, sums the corresponding values for each datetime in the chosen column of numeric values, and returns a two-column dataframe that equates each sum to their index-datetime'''
def sum_by_duplicated_values_and_datetime(dataframe, duplicated_column, sum_colum, datetime_list, days_increase=1):
    '''Requires positional arguments: dataframe with datetime indexes, the name (string) of a column of strings, the name (string) of a numeric column and a list of datetimes
    Accepts an integer as a key argument (default is 1)'''
    '''Requires relativedelta from dateutil.relativedelta and pandas as pd'''
    duplicated_list = dataframe[duplicated_column].drop_duplicates() # lista de ubicaciones posibles
    pre_dataframe_list = []
    for date in datetime_list: # por cada mes en la lista de meses que estudiamos (hay 6, pero el último se ignora por falta de datos)...
        current_date = date # lo asignamos a una variable
        current_sum_list = [] # creamos una lista vacía de individuos
        current_duplicated_list = [] # creamos una lista vacía de ubicaciones
        print(f'Now checking for {date}')
        while len(current_duplicated_list) != len(duplicated_list): # mientras la lista de ubicaciones sea inferior a la lista de ubicaciones posibles...
            try: # que intente lo siguiente:
                current_table = dataframe.loc[[date], [duplicated_column, sum_colum]] # asignar a una variable current table, de df_refugees, las filas country-individuals que correspondan a la fecha
                if current_duplicated_list: # si hay alguna cosa en la lista de ubicaciones...
                    missing_duplicates = list(set(duplicated_list) - set(current_duplicated_list)) # crea una lista de ubicaciones faltantes,  restando a las posibles estas...
                    print(f'Missing: {missing_duplicates}')
                    for duplicate in missing_duplicates: # e itera por las ubicaciones que faltan
                        if duplicate in list(current_table[duplicated_column]):  # si una ubicacion se encuentra en la columna country de la variable current table
                            print(f'{duplicate} found at {date}')
                            current_sum_list.append(int(current_table.loc[current_table[duplicated_column] == duplicate][sum_colum])) # añade el valor de la otra columna a la lista de individuos los correspondientes...
                            current_duplicated_list.append(duplicate) # y la ubicacion a la lista de ubicaciones
                    if len(current_duplicated_list) != len(duplicated_list): # si todavía faltan ubicaciones
                        date += relativedelta(days=days_increase) # cuando termina, suma un día a la fecha para repetir la iteración hasta que salgan todos los duplicates
                        print(f'Add {days_increase} day/s. Current date: {date}')
                else: # si todavía no hay nada en la lista de ubicaciones (es la primera iteración para esa fecha):
                    current_sum_list.append(sum(current_table[sum_colum])) #añade los individuos actuales a su lista
                    current_duplicated_list += list(current_table[duplicated_column]) # añade la ubicación actual a la lista
            except KeyError: # si el try fracasa porque la fecha en concreto no se encuentra en la table y no se puede asignar a la variable current table...
                print(f'{date} does not exist in the dataframe')
                date += relativedelta(days=days_increase) # sumamos un día y repetimos la iteración
                print(f'Add {days_increase} day/s. Current date: {date}')
        current_dict = {'date':current_date, # creamos el diccionario de esta iteración
                        'Total': sum(current_sum_list)
                        }
        pre_dataframe_list.append(current_dict) # añadimos el diccionario a la lista para el dataframe
        print(f'{current_date} has been filled')
        print('\n')
    df_total = pd.DataFrame(pre_dataframe_list) # creamos el dataframe con el total por fecha
    return df_total
