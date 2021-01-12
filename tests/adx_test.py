import unittest
import pandas as pd
from context import technical as ti

# Test results
class ResultsADX(unittest.TestCase):
    # Input data
    test_data = pd.read_csv('test_data/correct_ohlc.csv')

    # Expected results output
    results_adx = pd.Series([None, None, None, None, None, None,
      None, None, None, None, None, None,
      None, None, None, None, None, None,
      None, None, None, None, None, 17.62448233,
      17.25492242, 16.69742726, 17.16854805, 18.2926569 , 19.45489649, 21.25379975,
      22.90279442, 23.07300776, 22.97606451, 22.88719987, 22.98861282, 23.61422571,
      25.08682302, 25.24231335, 25.38484615, 25.51550121, 27.5558831, 30.1110554,
      32.45329669, 34.60035119, 36.56848449, 37.9998013, 38.5673745, 39.60509371,
      40.18165197, 41.22252456, 42.80118464, 44.59110054, 46.88599005, 48.98963877,
      50.91798342, 53.02509961, 54.95662278, 56.88585779, 57.46284565, 55.67556595,
      52.48512707, 49.56055811, 47.55431921, 44.70536415, 42.09382202, 39.6999084,
      37.21834795, 35.62271838, 34.95403454, 33.70682011, 32.24852831,])

    results_dx = pd.Series([None, None, None, None, None, None,
      None, None, None, None, None, None,
      18.36809367, 13.32211289, 13.32211289,  0.56701934,  0.56701934, 25.40991127,
      17.75250619, 30.15823446, 22.59361195, 22.59361195, 19.83087082, 27.00868322,
      13.18976342, 10.56498044, 22.35087674, 30.65785424, 32.23953196, 41.0417357,
      41.0417357, 24.94535453, 21.90968879, 21.90968879, 24.1041553, 30.49596754,
      41.28539337, 26.95270694, 26.95270694, 26.95270694, 50.00008384, 58.21795078,
      58.21795078, 58.21795078, 58.21795078, 53.74428615, 44.81067969, 51.02000504,
      46.52379282, 52.67212308, 60.16644553, 64.28017546, 72.12977465, 72.12977465,
      72.12977465, 76.20337763, 76.20337763, 78.10744292, 63.80971219, 36.01548919,
      17.39029945, 17.39029945, 25.48569134, 13.36685854, 13.36685854, 13.36685854,
      9.921183, 18.07079314, 27.5985123, 19.98746139, 16.20731847])
    
    # Input paramter
    ma = 12

    def test_result_adx(self):
        '''adx function must return series adx equal to expected'''
        results = ti.ADX(self.test_data, self.ma)
        pd.testing.assert_series_equal(self.results_adx, results['adx'], check_names=False)

    def test_result_dx(self):
        '''adx function must return series dx equal to expected'''
        results = ti.ADX(self.test_data, self.ma)
        pd.testing.assert_series_equal(self.results_dx, results['dx'], check_names=False)

    def test_result_df_lenght(self):
        '''adx result must have the expected lenght'''
        results = ti.ADX(self.test_data, self.ma)
        self.assertEqual(self.results_adx.shape[0], results.shape[0])

    def test_result_df_columns_number(self):
        '''adx result must have the expected columns number'''
        results = ti.ADX(self.test_data, self.ma)
        self.assertEqual(2, results.shape[1])

    def test_result_df_columns_number_full(self):
        '''adx result must have the expected columns number for full output'''
        ohlc_og_columns = self.test_data.shape[1]
        result_columns = 12
        results = ti.ADX(self.test_data, self.ma, full_output=True)
        self.assertEqual(ohlc_og_columns+result_columns, results.shape[1])

# Test input data
class BadInputADX(unittest.TestCase):
  # Input data
  test_data = pd.read_csv('test_data/correct_ohlc.csv')
  test_data_list = pd.read_csv('test_data/correct_series.csv').values
  test_data_missing_col = pd.read_csv('test_data/correct_ohlc.csv').drop(columns=['Close', 'Adj Close'])

  # Input parameters
  ma = 12

  def test_parameter_not_int(self):
    '''if ma is not integer should raise TypeError'''
    self.assertRaises(TypeError, ti.ADX, self.test_data, 11.59)

  def test_input_data_not_df(self):
    '''if data is not a valid type should raise TypeError'''
    self.assertRaises(TypeError, ti.ADX, self.test_data_list, self.ma)

  def test_df_missing_column(self):
    '''if df has a missing column than should raise IndexError'''
    self.assertRaises(IndexError, ti.ADX, self.test_data_missing_col, self.ma)

if __name__ == '__main__':
    unittest.main()