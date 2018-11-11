from . import InvoiceParser
import os
import pandas as pd
import logging


class CustomerProject:

    def __init__(self, project_name):
        self.parser = InvoiceParser.Invoice()
        self.data = pd.DataFrame()
        self.project_name = project_name

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
        print(self.data)

    def get_value(self, date, field):

        return self.data.loc[self.data.index == date, field]


