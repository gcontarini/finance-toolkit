import unittest
import pandas as pd
from context import technical as ti

# Test results
class ResultsOBV(unittest.TestCase):
    # Input data
    test_data = pd.read_csv('test_data/correct_ohlc.csv')

    # Expected results output
    results_obv = pd.Series([0, 817700, 158400, 866400, 1229000, 745200,
      1647000, 1226300, 566400, 1129000,  801800, 407000,
      1831700, 1591700,  647700,  870800, 870800, 2239000,
      1764200, 2303300, 1855900, 1456300, 1795600, 2286600,
      1811100, 1811100, 2307400, 3956500, 4222300, 5852300,
      6215800, 5777200, 5379200, 5719100, 6114500, 6114500,
      7886400, 7598700, 7856900, 7695100, 11262900, 12875600, 
      13663500, 13663500, 13950200, 13306400, 13724200, 13210500,
      13466800, 13915500, 14785000, 15884200, 17462400, 16932300,
      17481400, 18034500, 18280100, 17941400, 17629500, 17038100,
      16464000, 17587400, 17214800, 17214800, 16976000, 17125600,
      16991100, 17376700, 17376700, 17191200, 17191200])

    def test_result_obv(self):
        '''obv function must return obv series equal to expected'''
        results = ti.OBV(self.test_data)
        pd.testing.assert_series_equal(self.results_obv, results['obv'], check_names=False)

    def test_result_df_lenght(self):
        '''obv result must have the expected lenght'''
        results = ti.OBV(self.test_data)
        self.assertEqual(self.results_obv.shape[0], results.shape[0])

    def test_result_df_columns_number(self):
        '''obv result must have the expected columns number'''
        results = ti.OBV(self.test_data)
        self.assertEqual(1, results.shape[1])

    def test_result_df_columns_number_full(self):
        '''obv result must have the expected columns number for full output'''
        ohlc_og_columns = self.test_data.shape[1]
        result_columns = 3
        results = ti.OBV(self.test_data, full_output=True)
        self.assertEqual(ohlc_og_columns+result_columns, results.shape[1])

# Test input data
class BadInputOBV(unittest.TestCase):
  # Input data
  test_data = pd.read_csv('test_data/correct_ohlc.csv')
  test_data_list = pd.read_csv('test_data/correct_series.csv').values
  test_data_missing_col = pd.read_csv('test_data/correct_ohlc.csv').drop(columns=['Close', 'Adj Close'])

  def test_input_data_not_df(self):
    '''if data is not a valid type should raise TypeError'''
    self.assertRaises(TypeError, ti.OBV, self.test_data_list)

  def test_df_missing_column(self):
    '''if df has a missing column than should raise IndexError'''
    self.assertRaises(IndexError, ti.OBV, self.test_data_missing_col)

if __name__ == '__main__':
    unittest.main()