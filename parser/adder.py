import os
import pandas as pd
from . import ProjectData
from . import InvoiceParser
import logging


def is_active_project(data, inactive_delay, date=pd.Timestamp.now()):
    """
    Check if the project was active at a given date
    :param date: a date given as a pandas Timestamp
    :return: true if the project is active, false otherwise
    """
    if date < data.index[0]:
        return False
    else:
        return date - data.index[-1] < inactive_delay


def add_project_data(total_data, project_data, project_idx, column_to_average, inactive_delay=pd.Timedelta(3, unit='M')):

    index = 0
    initial_total_data = total_data.copy()
    prev_date = None

    for date, invoice in project_data.iterrows():

        if is_active_project(project_data, inactive_delay, date):

            if date in total_data.index:  # adding invoice number with current invoice data

                for name, value in invoice.iteritems():
                    if name in column_to_average:
                        total_data.loc[date][name] = (total_data.loc[date][name]*project_idx + value) / (project_idx + 1)
                    else:
                        total_data.loc[date][name] += value
            else:  # inserting a new date


                if not initial_total_data.empty and date > initial_total_data.index[-1] and project_idx > 0:
                    last_row = initial_total_data.iloc[-1]
                    total_data.loc[date] = invoice

                    for name, value in invoice.iteritems():
                        if name in column_to_average:
                            total_data.loc[date][name] = (last_row[name] * project_idx + value) / (project_idx + 1)
                        else:
                            total_data.loc[date][name] = value + last_row[name]

                else:
                    total_data.loc[date] = invoice


                #
                #current_index = total_data.index.get_loc(date)
                #total_data.loc[date] = total_data.loc[date] + total_data.iloc[current_index -1]  # todo, normalize CPI

            # todo, consider case where one project starts before the other
            # todo: Consider case where project is missing invoices (week(s))
            # todo: consider case where project ends before the other

        prev_date = date
        index += 1

    if index == len(project_data) - 1:  # if there are customer financial data AFTER the last date of the project
        print("last date")
        #print('----------- last row----------')
        # go through all the remaning row in the ppoject...and add!
        #print(total_data.loc[date + pd.Timedelta(1, unit='d'): date + inactive_delay])

    total_data.sort_index(inplace=True)
    total_data.sort_index(axis=1, inplace=True)
