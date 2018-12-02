import os
import pandas as pd
from . import ProjectData
from . import InvoiceParser
import logging


class CustomerData:

    column_to_average = ('cpi')

    def __init__(self, inactive_delay=pd.Timedelta(3, unit='M'), low_cpi=90):
        self.inactive_delay = inactive_delay
        self.low_cpi = low_cpi
        self.projects = dict()
        self.data = pd.DataFrame(columns=InvoiceParser.Invoice.get_colums())
        self.customer = None

    def load_data(self, customer_path):

        customer_index = 0

        self.customer = os.path.dirname(customer_path)

        for subdir, dirs, files in os.walk(customer_path):
            for custdir in dirs:

                print('-----'+custdir+'-----')
                try:
                    self.projects[custdir] = ProjectData.CustomerProject(self.inactive_delay, self.low_cpi)
                    self.projects[custdir].load_data(os.path.join(customer_path, custdir))
                    self.__add_project_data(self.projects[custdir], customer_index)

                    customer_index+=1

                    print(self.projects[custdir].data)

                    print('-----'+'customer'+'-----')
                    print(self.data)
                except ... as e:
                    logging.error("Could not data for customer {!s}:{!s} [{!s}]".format(custdir, self.customer, e))

    def __add_project_data(self, project_data, customer_index):

        index = 0
        prev_date = None

        for date, invoice in project_data.data.iterrows():

            if project_data.is_active_project(date):

                #TODO detedt when there is a gap between the project current time stamp and the other

                if date in self.data.index: #adding invoice number with current invoice data
                    for name, value in invoice.iteritems():
                        if name in CustomerData.column_to_average:
                            self.data.loc[date][name] = (self.data.loc[date][name] + value)/(customer_index + 1)
                        else:
                            self.data.loc[date][name] += value
                else: #inserting a new date

                    self.data.loc[date] = invoice
                    current_index = self.data.index.get_loc(date)
                    self.data.loc[date] = self.data.loc[date] + self.data.iloc[current_index-1] #todo, normalize CPI

                if index == len(project_data.data) - 1: #if there are customer financial data AFTER the last date of the project
                    print('----------- last row----------')
                    # go through all the remaning row in the ppoject...and add!
                    print(self.data.loc[date+ pd.Timedelta(1, unit='d'): date+self.inactive_delay])


                #todo, consider case where one project starts before the other
                #todo: Consider case where project is missing invoice

            prev_date = date
            index += 1

        self.data.drop('date', 1)
        self.data.sort_index(inplace=True)