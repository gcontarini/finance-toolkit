import unittest
import numpy as np
import pandas as pd
from context import performance as pi

# Test results
class ResultsSharpe(unittest.TestCase):
    # Input data
    test_yearly = pd.Series(range(100, 201, 20))
    test_monthly = pd.read_csv('test_data/ohlc_monthly.csv').drop(columns=['Adj Close'])
    test_daily = pd.read_csv('test_data/series_daily.csv')

    # Expected results
    # Made with excel
    results_yearly = 1.38261521288131
    results_monthly = 1.1802445217311
    results_daily = -2.8463318287963
    results_daily_all_days = -2.6826816941942

    def test_result_yearly(self):
        '''result for yearly data expected'''
        rate = 0.1
        result = pi.sharpe(self.test_yearly, rate, frequency='Y')
        self.assertAlmostEqual(self.results_yearly, result, places=6)

    def test_result_monthly_fraction(self):
        '''result for monthly data expected'''
        rate = 0.05
        result = pi.sharpe(self.test_monthly, rate, frequency='M')
        self.assertAlmostEqual(self.results_monthly, result, places=6)

    def test_result_daily_fraction(self):
        '''result for daily data expected'''
        rate = 0.1
        result = pi.sharpe(self.test_daily, rate, frequency='D')
        self.assertAlmostEqual(self.results_daily, result, places=6)

    def test_result_daily_fraction_all_days(self):
        '''result for daily with all days option'''
        rate = 0.1
        result = pi.sharpe(self.test_daily, rate, frequency='D', only_business=False)
        self.assertAlmostEqual(self.results_daily_all_days, result, places=6)

# Test inputs
class BadInputSharpe(unittest.TestCase):
    # Input data
    test_constant = pd.Series(np.ones(10))
    test_yearly = pd.Series(range(100, 201, 20))
    test_yearly_list = range(100, 201, 20)
    test_no_close = pd.read_csv('test_data/ohlc_monthly.csv').drop(columns=['Close', 'Adj Close'])
    test_more_close = pd.read_csv('test_data/ohlc_monthly.csv')

    def test_input_data_not_df_or_series(self):
        '''data is not a valid type raise TypeError'''
        self.assertRaises(TypeError, pi.sharpe, self.test_yearly_list, rf_rate=0.1)
  
    def test_input_df_no_close(self):
        '''input df has no close column'''
        self.assertRaises(IndexError, pi.sharpe, self.test_no_close, rf_rate=0.1)

    def test_input_df_more_close(self):
        '''input df has more than 1 close column'''
        self.assertRaises(KeyError, pi.sharpe, self.test_more_close, rf_rate=0.1)
  
    def test_volatility_equal_zero(self):
        '''volatility equal zero must raise ZeroDivisionError'''
        self.assertRaises(ZeroDivisionError, pi.sharpe, self.test_constant, rf_rate=0.1)
    
    def test_frequency_parameter(self):
        '''invalid string for frequency raise ValueError'''
        self.assertRaises(ValueError, pi.sharpe, self.test_yearly, rf_rate=0.1, frequency='mo')
  
    def test_business_parameter(self):
        '''invalid value for only_business raise TypeError'''
        self.assertRaises(TypeError, pi.sharpe, self.test_yearly, rf_rate=0.1, only_business='Yes')

    def test_rf_rate_not_valid_type(self):
        '''invalid data type for rf_rate parameter raise TypeError'''
        self.assertRaises(TypeError, pi.sharpe, self.test_yearly, rf_rate=True)

    def test_rf_rate_out_of_range(self):
        '''rf_rate out of range (0-1) raise ValueError'''
        self.assertRaises(ValueError, pi.sharpe, self.test_yearly, rf_rate=1.5)
  
if __name__ == '__main__':
    unittest.main()