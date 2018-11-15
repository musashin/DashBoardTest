from . import InvoiceParser
import os
import pandas as pd
import logging


class CustomerProject:

    def __init__(self, project_name, inactive_delay=pd.Timedelta(3,unit='M'), low_cpi = 90):
        self.parser = InvoiceParser.Invoice()
        self.data = pd.DataFrame()
        self.project_name = project_name
        self.inactive_delay = inactive_delay
        self.low_cpi = low_cpi

    def load_data(self, invoice_path):

        for file in os.listdir(os.fsencode(invoice_path)):

            try:
                filename = os.fsdecode(file)

                if filename.endswith(".xlsx") or filename.startswith("invoice"):

                    values = self.parser.extract(os.path.join(invoice_path,filename))

                    self.data = self.data.append(values,ignore_index=True)

            except ... as e:
                logging.error("Could not load invoice {!s}:{!s} [{!s}]".format(self.project_name, filename, e))

        self.data.set_index('date', inplace=True)
        self.data.index = self.data.index.map(pd.DatetimeIndex.to_pydatetime)
        self.data.sort_index(inplace=True)
        #print(self.data)

    def get_value(self, date, field):
        """
        Given a date, get the value, the value at the date BEFORE the selected date is always returned
        :param date: a date given as a pandas Timestamp
        :param field: a field
        :return: value of the field at the given date
        """

        try:
            return self.data.iloc[self.data.index.get_loc(date, method='ffill')][field]
        except KeyError:
            return None

    def is_active_project(self, date):
        """
        Check if the project was active at a given date
        :param date: a date given as a pandas Timestamp
        :return: true if the project is active, false otherwise
        """
        if date<self.data.index[0]:
            return False
        else:
            return date - self.data.index[-1] < self.inactive_delay


    #TODO: warning messages



