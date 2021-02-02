import os
import unittest
import numpy as np
import pandas as pd
from context import performance as pi

# Change working directory
# This enable running tests from repository root
if os.getcwd() != os.path.abspath(os.path.dirname(__file__)):
    os.chdir('tests/')

# Test results
class ResultsCalmar(unittest.TestCase):
    # Input data
    test_yearly = pd.Series([100, 120, 110, 100, 110, 130])
    test_monthly = pd.read_csv('test_data/ohlc_monthly.csv').drop(columns=['Adj Close'])
    test_daily = pd.read_csv('test_data/series_daily.csv')

    # Expected results
    # Made with excel
    results_yearly = 0.05387395206 / 0.1666666667
    results_monthly = 0.4075254214 / 0.3070333382
    results_daily = -0.7543788728 / 0.06131828655
    results_daily_all_days = -0.8691260753 / 0.06131828655

    def test_result_yearly(self):
        '''result for yearly data expected'''
        result = pi.calmar(self.test_yearly, frequency='Y')
        self.assertAlmostEqual(self.results_yearly, result, places=4)

    def test_result_monthly_fraction(self):
        '''result for monthly data expected'''
        result = pi.calmar(self.test_monthly, frequency='M')
        self.assertAlmostEqual(self.results_monthly, result, places=4)

    def test_result_daily_fraction(self):
        '''result for daily data expected'''
        result = pi.calmar(self.test_daily, frequency='D')
        self.assertAlmostEqual(self.results_daily, result, places=4)

    def test_result_daily_fraction_all_days(self):
        '''result for daily with all days option'''
        result = pi.calmar(self.test_daily, frequency='D', only_business=False)
        self.assertAlmostEqual(self.results_daily_all_days, result, places=4)

# Test inputs
class BadInputSortino(unittest.TestCase):
    # Input data
    test_yearly = pd.Series(range(100, 201, 20))
    test_yearly_list = range(100, 201, 20)
    test_no_close = pd.read_csv('test_data/ohlc_monthly.csv').drop(columns=['Close', 'Adj Close'])
    test_more_close = pd.read_csv('test_data/ohlc_monthly.csv')

    def test_input_data_not_df_or_series(self):
        '''data is not a valid type raise TypeError'''
        self.assertRaises(TypeError, pi.calmar, self.test_yearly_list)
  
    def test_input_df_no_close(self):
        '''input df has no close column'''
        self.assertRaises(IndexError, pi.calmar, self.test_no_close)

    def test_input_df_more_close(self):
        '''input df has more than 1 close column'''
        self.assertRaises(KeyError, pi.calmar, self.test_more_close)
      
    def test_frequency_parameter(self):
        '''invalid string for frequency raise ValueError'''
        self.assertRaises(ValueError, pi.calmar, self.test_yearly, frequency='mo')
  
    def test_business_parameter(self):
        '''invalid value for only_business raise TypeError'''
        self.assertRaises(TypeError, pi.calmar, self.test_yearly, only_business='Yes')
  
if __name__ == '__main__':
    unittest.main()