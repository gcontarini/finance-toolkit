import unittest
import numpy as np
import pandas as pd
from context import performance as pi

# Test results
class ResultsCAGR(unittest.TestCase):
    # Input data
    test_constant = pd.Series(np.ones_like((1, 10)))
    test_yearly = pd.Series(range(100, 201, 20))
    test_monthly = pd.read_csv('test_data/ohlc_monthly.csv').drop(columns=['Adj Close'])

    # Expected results
    # Made with excel
    results_zero = 0
    results_yearly = 0.148698355
    results_monthly = 0.4075254214

    def test_result_zero_return(self):
        '''result must be zero if asset value is constant'''
        result = pi.CAGR(self.test_constant)
        self.assertAlmostEqual(self.results_zero, result)

    def test_result_yearly(self):
        '''result for yearly data expected'''
        result = pi.CAGR(self.test_yearly, frequency='Y')
        self.assertAlmostEqual(self.results_yearly, result)

    def test_result_monthly_fraction(self):
        '''result for monthly data expected'''
        result = pi.CAGR(self.test_monthly, frequency='M')
        self.assertAlmostEqual(self.results_monthly, result)

    # TO DO CREATE 2 TESTS FOR DAILY DATA: business and not business days

# Test inputs
class BadInputCAGR(unittest.TestCase):
  # Input data
  test_yearly = pd.Series(range(100, 201, 20))
  test_yearly_list = range(100, 201, 20)

  def test_input_data_not_df_or_series(self):
    '''data is not a valid type raise TypeError'''
    self.assertRaises(TypeError, pi.CAGR, self.test_yearly_list)

  def test_frequency_parameter(self):
    '''invalid string for frequency raise ValueError'''
    self.assertRaises(ValueError, pi.CAGR, self.test_yearly, frequency='mo')

  def test_business_parameter(self):
    '''invalid value for only_business raise TypeError'''
    self.assertRaises(TypeError, pi.CAGR, self.test_yearly, only_business='Yes')

if __name__ == '__main__':
    unittest.main()