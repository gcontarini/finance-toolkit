import unittest
import numpy as np
import pandas as pd
from context import performance as pi

# Test results
class ResultsMaxDrawdown(unittest.TestCase):
    # Input data
    test_constant = pd.Series([100, 100, 100, 100, 100])
    test_yearly = pd.Series([100, 120, 110, 100, 110, 130])
    test_monthly = pd.read_csv('test_data/ohlc_monthly.csv').drop(columns=['Adj Close'])
    test_daily = pd.read_csv('test_data/series_daily.csv')

    # Expected results
    # Made with excel
    results_constant = 0
    results_yearly = 0.1666666667
    results_monthly = 0.3070333382
    results_daily = 0.06131828655

    def test_result_constant(self):
        '''result must be equal to zero with constant prices'''
        result = pi.max_dd(self.test_constant)
        self.assertEqual(self.results_constant, result)

    def test_result_yearly(self):
        '''result for yearly data expected'''
        result = pi.max_dd(self.test_yearly)
        self.assertAlmostEqual(self.results_yearly, result, places=6)

    def test_result_monthly_fraction(self):
        '''result for monthly data expected'''
        result = pi.max_dd(self.test_monthly)
        self.assertAlmostEqual(self.results_monthly, result, places=6)

    def test_result_daily_fraction(self):
        '''result for daily data expected'''
        result = pi.max_dd(self.test_daily)
        self.assertAlmostEqual(self.results_daily, result, places=6)

# Test inputs
class BadInputMaxDrawdown(unittest.TestCase):
    # Input data
    test_yearly_list = range(100, 201, 20)
    test_no_close = pd.read_csv('test_data/ohlc_monthly.csv').drop(columns=['Close', 'Adj Close'])
    test_more_close = pd.read_csv('test_data/ohlc_monthly.csv')

    def test_input_data_not_df_or_series(self):
        '''data is not a valid type raise TypeError'''
        self.assertRaises(TypeError, pi.max_dd, self.test_yearly_list)
  
    def test_input_df_no_close(self):
        '''input df has no close column'''
        self.assertRaises(IndexError, pi.max_dd, self.test_no_close)

    def test_input_df_more_close(self):
        '''input df has more than 1 close column'''
        self.assertRaises(KeyError, pi.max_dd, self.test_more_close)
    
if __name__ == '__main__':
    unittest.main()