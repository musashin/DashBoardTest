import unittest
from . import adder
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class AdderTests(unittest.TestCase):
    """
    Test in normal conditions
    """

    def test_simple_addition(self):
        total = pd.DataFrame(columns=['X', 'Y', 'CPI'], dtype=float)

        date_today = datetime.now()
        invoice_weeks = pd.date_range(date_today, periods=3, freq='W')

        project1 = pd.DataFrame(index=invoice_weeks, data= {'X': [40, 50, 60],
                                                            'Y': [10000, 20000, 30000],
                                                            'CPI': [10, 20, 30]})

        project2 = pd.DataFrame(index=invoice_weeks, data={'X': [10, 10, 10],
                                                           'Y': [30, 40, 50],
                                                           'CPI': [100, 20, 100]})

        for idx, project in enumerate((project1, project2)):
            adder.add_project_data(total, project, idx, column_to_average=('CPI'))

        expected_result = pd.DataFrame(index=invoice_weeks, data={'X': [50, 60, 70],
                                                                  'Y': [10030, 20040, 30050],
                                                                  'CPI': [55, 20, 65]}, dtype=float)


        expected_result.sort_index(inplace=True, axis=1)


        self.assertTrue(total.equals(expected_result))

    def test_multiple_simple_addition(self):
        total = pd.DataFrame(columns=['X', 'CPI'], dtype=float)

        date_today = datetime.now()
        invoice_weeks = pd.date_range(date_today, periods=3, freq='W')

        project = pd.DataFrame(index=invoice_weeks, data={'X': [10, 20, 30],
                                                           'CPI': [10, 20, 30]})

        for idx in range(5):
            print(idx)
            adder.add_project_data(total, project, idx, column_to_average=('CPI'))
            print(total)

        expected_result = pd.DataFrame(index=invoice_weeks, data={'X': [10*5, 20*5, 30*5],
                                                                  'CPI': [10, 20, 30]}, dtype=float)

        expected_result.sort_index(inplace=True, axis=1)

        print(total)
        self.assertTrue(total.equals(expected_result))


