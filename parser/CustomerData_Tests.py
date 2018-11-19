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
        pass
