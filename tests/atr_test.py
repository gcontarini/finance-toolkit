import unittest
import pandas as pd
from context import atr

# Test results and outputs
class ResultsATR(unittest.TestCase):
    def test_result_atr(self):

    def test_result_tr(self):

    def test_result_df_lenght(self):

    def test_result_df_columns_number(self):

    def test_result_df_columns_number_full(self):

# Test input data
class BadInputATR(unittest.TestCase):
    def test_ma_not_integer(self):

    def test_input_data_not_df(self):

    def test_input_data_missing_column(self):

if __name__ == '__main__':
    unittest.main()