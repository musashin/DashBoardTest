from . import InvoiceParser
import os


class CustomerProject:

    def __init__(self):
        self.parser = InvoiceParser.Invoice()


    def load_data(self, invoice_path):

        for file in os.listdir(os.fsencode(invoice_path)):

            filename = os.fsdecode(file)
            if filename.endswith(".xlsx") or filename.startswith("invoice"):

        #TODO try catch
                res = self.parser.extract(os.path.join(invoice_path,filename))

                print(res)



