import pandas as pd


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

    #todo weighted average
    #todo simplify

    index = 0
    initial_total_data = total_data.copy()

    for date, invoice in project_data.iterrows():

        if is_active_project(project_data, inactive_delay, date):

            if date in total_data.index:  # adding invoice number with current invoice data

                for name, value in invoice.iteritems():
                    if name in column_to_average:
                        total_data.loc[date][name] = (total_data.loc[date][name]*project_idx + value) / (project_idx + 1)
                    else:
                        total_data.loc[date][name] += value
            else:  # inserting a new date

                if not initial_total_data.empty and date > initial_total_data.index[-1] \
                   and project_idx > 0 and date - initial_total_data.index[-1] < inactive_delay:
                    last_row = initial_total_data.iloc[-1]
                    total_data.loc[date] = invoice

                    for name, value in invoice.iteritems():
                        if name in column_to_average:
                            total_data.loc[date][name] = (last_row[name] * project_idx + value) / (project_idx + 1)
                        else:
                            total_data.loc[date][name] = value + last_row[name]

                else:
                    total_data.loc[date] = invoice

        prev_project_invoice = (date, invoice)
        index += 1

    total_data.sort_index(inplace=True)
    total_data.sort_index(axis=1, inplace=True)
    total_data.reindex(pd.date_range(total_data.index.min(), total_data.index.max(), freq='W'))

    if not total_data.empty and index == len(project_data) and \
            project_data.index[-1]<total_data.index[-1]:  # if there are customer financial data AFTER the last date of the project

        total_data.index[index]

        for i in range(index, len(total_data)):

            if total_data.index[i] - project_data.index[-1] < inactive_delay:

                last_row = project_data.iloc[-1]

                for name, value in total_data.iloc[i].iteritems():
                    if name in column_to_average:
                        total_data.iloc[i][name] = (last_row[name] * project_idx + value) / (project_idx + 1)
                    else:
                        total_data.iloc[i][name] = value + last_row[name]

