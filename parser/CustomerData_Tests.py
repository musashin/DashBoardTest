import unittest
from . import CustomerData
import pandas as pd
import numpy as np


class ProjectDataTests(unittest.TestCase):
    """
    Test in normal conditions
    """

    def setUp(self):
        self.customer = CustomerData.CustomerData()
        self.customer.load_data(r'/home/nicolas/PycharmProjects/DashBoardTest/parser/test_data/CustomerX')

    def test_loaded_project_field(self):
        invoice_weeks = pd.date_range(pd.Timestamp('20181204 0:0:0'), periods=5, freq='7D')

        expected_result = pd.DataFrame(index=invoice_weeks, data={'bodies': [np.nan, np.nan, 3.125,np.nan,np.nan],
                                                                  'budget': [150300, 100300, 90300, 50300, 50300],
                                                                  'cpi': [99, 96.5, 70, 45, 89],
                                                                  'date': [np.nan, np.nan, np.nan, np.nan, np.nan],
                                                                  'hours': [np.nan, np.nan, 125, np.nan, np.nan],
                                                                  'value': [50080, 4160, 50040, 100000, 50100]},
                                                                  dtype = float)

        expected_result.sort_index(inplace=True, axis=1)

        print(self.customer.data)
        print(expected_result)

        self.assertTrue(self.customer.data.equals(expected_result))