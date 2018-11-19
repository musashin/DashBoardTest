from . import InvoiceParser
import os
import pandas as pd
import logging


class CustomerProject:

    def __init__(self, customer_name, project_name, inactive_delay=pd.Timedelta(3,unit='M'), low_cpi = 90):
        self.parser = InvoiceParser.Invoice()
        self.data = pd.DataFrame()
        self.customer_name = customer_name
        self.project_name = project_name
        self.inactive_delay = inactive_delay
        self.low_cpi = low_cpi
        self.warning_list = list()
        self.evaluation_functions = (self.__evaluate_cpi, self.__evaluate_budget)

    def __evaluate_cpi(self):
        """
        Add a warning if the project is active and CPI is below the threshold
        :return:
        """

        try:
            print(self.data)
            if self.data['cpi'].iloc[-1] < self.low_cpi and self.is_active_project():
                self.warning_list.append("Customer {!s} Project {!s} has a low cpi {!s}".format(self.customer_name,
                                                                                                self.project_name,
                                                                                                self.data['cpi'].iloc[-1]))

        except ... as e:
            logging.warning("Could not evaluate CPI {!s}:{!s} [{!s}]".format(self.customer_name, self.project_name, e))

    def __evaluate_budget(self):
        # TODO add eval function on budget exhaustion
        pass

    def __analyse(self):
        """
        Analyse project finantial data and update warning list accordingly
        :return:
        """
        for func in self.evaluation_functions:
            func()

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
        self.__analyse()
        print(self.warning_list)

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

    def is_active_project(self, date=pd.Timestamp.now()):
        """
        Check if the project was active at a given date
        :param date: a date given as a pandas Timestamp
        :return: true if the project is active, false otherwise
        """
        if date<self.data.index[0]:
            return False
        else:
            return date - self.data.index[-1] < self.inactive_delay




