from . import InvoiceParser
import os
import pandas as pd


class CustomerProject:

    def __init__(self):
        self.parser = InvoiceParser.Invoice()
        self.data = pd.DataFrame() #todo

    def load_data(self, invoice_path):

        for file in os.listdir(os.fsencode(invoice_path)):

            filename = os.fsdecode(file)

            if filename.endswith(".xlsx") or filename.startswith("invoice"):

        #TODO try catch
                values = self.parser.extract(os.path.join(invoice_path,filename))

                self.data = self.data.append(values,ignore_index=True)

        self.data.set_index('date',inplace=True)
        self.data.index = self.data.index.map(pd.DatetimeIndex.to_pydatetime)
        self.data.sort_index(inplace=True)
        print(self.data)

