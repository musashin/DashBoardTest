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
        total = pd.DataFrame(columns=['X', 'Y', 'CPI'])

        date_today = datetime.now()
        invoice_weeks = pd.date_range(date_today, periods = 3, freq='W')

        project1 = pd.DataFrame(index=invoice_weeks, data= {'X': [40, 50, 60],
                                                            'Y': [10000, 20000, 30000],
                                                            'CPI': [10, 20, 30]})

        project2 = pd.DataFrame(index=invoice_weeks, data={'X': [10, 10, 10],
                                                           'Y': [30, 40, 50],
                                                           'CPI': [100, 20, 100]})

        for idx, project in enumerate((project1, project2)):
            adder.add_project_data(total, project, idx, column_to_average = ('cpi'))

            #print(total)

        expected_result = pd.DataFrame(index=invoice_weeks, data={'X': [50, 60, 70],
                                                                  'Y': [10030, 20040, 30060],
                                                                  'CPI': [55, 20, 65]})

        print(total)
        print(expected_result)
        #self.assertEqual(total, expected_result)

