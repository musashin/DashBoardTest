import os
import pandas as pd
from . import ProjectData
from . import InvoiceParser
import logging


class CustomerData:

    def __init__(self, inactive_delay=pd.Timedelta(3,unit='M'), low_cpi = 90):
        self.inactive_delay = inactive_delay
        self.low_cpi = low_cpi
        self.projects = dict()
        self.data = pd.DataFrame(columns = InvoiceParser.Invoice.get_colums())


    def load_data(self, customer_path):

        for subdir, dirs, files in os.walk(customer_path):
            for custdir in dirs:

                self.projects[custdir] = ProjectData.CustomerProject(self.inactive_delay, self.low_cpi)
                self.projects[custdir].load_data(os.path.join(customer_path, custdir))

                print(custdir)
                print(self.projects[custdir].data)
                #TODO handle eceptions
