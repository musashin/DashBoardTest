import os
import pandas as pd
from parser import InvoiceParser
from parser import CustomerData
import logging
from parser import adder


class Company:

    column_to_average = ('cpi')

    def __init__(self, inactive_delay=pd.Timedelta(3, unit='M'), low_cpi=90):
        # todo set options as dico
        self.inactive_delay = inactive_delay
        self.low_cpi = low_cpi
        self.projects = dict()
        self.data = pd.DataFrame(columns=InvoiceParser.Invoice.get_colums())

    def load_data(self, customer_path):

        customer_index = 0

        for subdir, dirs, files in os.walk(customer_path):
            for custdir in dirs:
                #TODO log

                try:
                    self.customer[custdir] = CustomerData.CustomerData(self.inactive_delay, self.low_cpi)
                    self.customer[custdir].load_data(os.path.join(customer_path, custdir))
                    adder.add_project_data(self.data, self.customer[custdir].data, customer_index, CustomerData.column_to_average)

                    customer_index += 1

                except ... as e:
                    logging.error("Could not data for customer {!s}:{!s} [{!s}]".format(custdir, self.customer, e))
