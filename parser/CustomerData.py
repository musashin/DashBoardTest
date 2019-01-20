import os
import pandas as pd
from parser import ProjectData
from parser import InvoiceParser
import logging
from parser import adder


class CustomerData:

    column_to_average = ('cpi')

    def __init__(self, inactive_delay=pd.Timedelta(3, unit='M'), low_cpi=90):
        #todo set options as dico
        self.inactive_delay = inactive_delay
        self.low_cpi = low_cpi
        self.projects = dict()
        self.data = pd.DataFrame(columns=InvoiceParser.Invoice.get_colums())
        self.customer = None

    def load_data(self, customer_path):

        customer_index = 0

        self.customer = os.path.dirname(customer_path)

        for subdir, dirs, files in os.walk(customer_path):
            for projdir in dirs:
                # TODO log
                try:
                    self.projects[projdir] = ProjectData.CustomerProject(self.inactive_delay, self.low_cpi)
                    self.projects[projdir].load_data(os.path.join(customer_path, projdir))
                    adder.add_project_data(self.data, self.projects[projdir].data, customer_index, CustomerData.column_to_average)

                    customer_index += 1

                except ... as e:
                    logging.error("Could not data for customer {!s}:{!s} [{!s}]".format(projdir, self.customer, e))
