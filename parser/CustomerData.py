import os
import pandas as pd
from . import ProjectData
from . import InvoiceParser
import logging
from . import adder


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
                    adder.add_project_data(self.data, self.projects[custdir].data, customer_index, CustomerData.column_to_average)

                    customer_index+=1

                    print(self.projects[custdir].data)


                except ... as e:
                    logging.error("Could not data for customer {!s}:{!s} [{!s}]".format(custdir, self.customer, e))

        print('-----' + 'customer' + '-----')
        print(self.data)