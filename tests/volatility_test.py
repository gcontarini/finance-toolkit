import unittest
import numpy as np
import pandas as pd
from context import performance as pi

# Test results
class ResultsVol(unittest.TestCase):
    # Input data
    test_constant = pd.Series(np.ones(10))
    test_yearly = pd.Series(range(100, 201, 20))
    test_monthly = pd.read_csv('test_data/ohlc_monthly.csv').drop(columns=['Adj Close'])
    test_daily = pd.read_csv('test_data/series_daily.csv')

    # Expected results
    # Made with excel
    results_zero = 0
    results_yearly = 0.03522191463
    results_monthly = 0.3029248726
    results_daily = 0.300168400659114
    results_daily_no_buss = 0.361252726113191

    def test_result_zero_return(self):
        '''result must be zero if asset value is constant'''
        result = pi.volatility(self.test_constant)
        self.assertAlmostEqual(self.results_zero, result)

    def test_result_yearly(self):
        '''result for yearly data expected'''
        result = pi.volatility(self.test_yearly, frequency='Y')
        self.assertAlmostEqual(self.results_yearly, result)

    def test_result_monthly_fraction(self):
        '''result for monthly data expected'''
        result = pi.volatility(self.test_monthly, frequency='M')
        self.assertAlmostEqual(self.results_monthly, result)

    def test_result_daily_fraction(self):
        '''result for daily data expected'''
        result = pi.volatility(self.test_daily, frequency='D')
        self.assertAlmostEqual(self.results_daily, result)

    def test_result_daily_fraction_no_business_days(self):
        '''result for daily without only business days option'''
        result = pi.volatility(self.test_daily, frequency='D', only_business=False)
        self.assertAlmostEqual(self.results_daily_no_buss, result)

# Test inputs
class BadInputVol(unittest.TestCase):
    # Input data
    test_yearly = pd.Series(range(100, 201, 20))
    test_yearly_list = range(100, 201, 20)
    test_no_close = pd.read_csv('test_data/ohlc_monthly.csv').drop(columns=['Close', 'Adj Close'])
    test_more_close = pd.read_csv('test_data/ohlc_monthly.csv')

    def test_input_data_not_df_or_series(self):
        '''data is not a valid type raise TypeError'''
        self.assertRaises(TypeError, pi.volatility, self.test_yearly_list)
  
    def test_input_df_no_close(self):
        '''input df has no close column'''
        self.assertRaises(IndexError, pi.volatility, self.test_no_close)

    def test_input_df_more_close(self):
        '''input df has more than 1 close column'''
        self.assertRaises(KeyError, pi.volatility, self.test_more_close)
  
    def test_frequency_parameter(self):
        '''invalid string for frequency raise ValueError'''
        self.assertRaises(ValueError, pi.volatility, self.test_yearly, frequency='mo')
  
    def test_business_parameter(self):
        '''invalid value for only_business raise TypeError'''
        self.assertRaises(TypeError, pi.volatility, self.test_yearly, only_business='Yes')
  
if __name__ == '__main__':
    unittest.main()