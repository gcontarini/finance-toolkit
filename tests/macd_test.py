import os
import unittest
import pandas as pd
from context import technical as ti

# Change working directory
# This enable running tests from repository root
if os.getcwd() != os.path.abspath(os.path.dirname(__file__)):
    os.chdir('tests/')

# Test results and outputs
class ResultsMACD(unittest.TestCase):
    # Input data
    test_data = pd.read_csv('test_data/correct_series.csv')
    test_data_df = pd.read_csv('test_data/correct_ohlc.csv').drop(columns=['Close'])

    # Expected output results
    results_line = pd.Series([0.        , 0.00104169, 0.00270912, 0.00031245, 0.00247449,
       0.00028395, 0.00386753, 0.00524738, 0.00287725, 0.00356132,
       0.00101829, 0.00444326, 0.0068335 , 0.01014599, 0.01305172,
       0.01167535, 0.01047763, 0.007073  , 0.00497697, 0.00034765,
       0.00072977, 0.00086424, 0.00235727, 0.00545893, 0.00259956,
       0.00035291, 0.0038989 , 0.01060325, 0.01634667, 0.02331259,
       0.03048012, 0.03086871, 0.02802865, 0.02616832, 0.02788499,
       0.02887595, 0.03280708, 0.0298124 , 0.02994925, 0.02826488,
       0.03516188, 0.04295579, 0.04992572, 0.05473519, 0.05996441,
       0.05896691, 0.0603559 , 0.05996981, 0.05965617, 0.06230883,
       0.06651554, 0.07333986, 0.08139379, 0.08447225, 0.08655907,
       0.08784908, 0.08850358, 0.08719152, 0.08216639, 0.07431071,
       0.06214603, 0.05851695, 0.05276871, 0.04764448, 0.04233428,
       0.03841456, 0.03268409, 0.03223513, 0.03148887, 0.02978424,
       0.02809067])

    results_signal = pd.Series([0.        , 0.00057872, 0.00145183, 0.00106587, 0.0014849 ,
       0.00115938, 0.00184474, 0.00266246, 0.00271207, 0.00290235,
       0.00249013, 0.00290958, 0.00374002, 0.00508015, 0.00673261,
       0.00774979, 0.00830792, 0.00805641, 0.00743152, 0.00599822,
       0.00493472, 0.00411457, 0.00376102, 0.00410221, 0.00380054,
       0.00310893, 0.0032673 , 0.00473734, 0.0070628 , 0.01031679,
       0.01435345, 0.01765912, 0.01973434, 0.02102179, 0.02239499,
       0.0236916 , 0.02551517, 0.02637479, 0.0270898 , 0.02732485,
       0.02889242, 0.03170534, 0.03534966, 0.03922698, 0.04337464,
       0.04649321, 0.04926582, 0.05140667, 0.0530566 , 0.05490707,
       0.05722879, 0.06045103, 0.06463962, 0.06860617, 0.07219676,
       0.07532724, 0.07796251, 0.07980832, 0.08027993, 0.07908609,
       0.07569807, 0.07226184, 0.06836321, 0.06421946, 0.05984242,
       0.05555685, 0.0509823 , 0.04723286, 0.04408406, 0.0412241 ,
       0.03859741])

    # Input parameters
    slow = 24
    fast = 12
    ma = 9

    # Tests
    def test_result_macd_line(self):
        '''macd function must return macd line with values equal to expected'''
        result = ti.MACD(self.test_data, self.slow, self.fast, self.ma)
        pd.testing.assert_series_equal(self.results_line, result['macd_line'], check_names=False)

    def test_result_macd_signal(self):
        '''macd function must return macd signal with values equal to expected'''
        result = ti.MACD(self.test_data, self.slow, self.fast, self.ma)
        pd.testing.assert_series_equal(self.results_signal, result['macd_signal'], check_names=False)

    def test_result_macd_line_lenght_size(self):
        '''macd result line must have the same lenght as input'''
        result = ti.MACD(self.test_data, self.slow, self.fast, self.ma)
        self.assertEqual(self.results_line.shape[0], result.shape[0])

    def test_result_macd_signal_lenght_size(self):
        '''macd result signal must have the same lenght as input'''
        result = ti.MACD(self.test_data, self.slow, self.fast, self.ma)
        self.assertEqual(self.results_signal.shape[0], result.shape[0])

    def test_output_result_matrix_cols_number(self):
        '''macd result df must have 2 columns'''
        result = ti.MACD(self.test_data, self.slow, self.fast, self.ma)
        self.assertEqual(2, result.shape[1])

    def test_output_result_matrix_cols_number_full_if_input_series(self):
        '''macd result df must have original series plus 4'''
        result = ti.MACD(self.test_data, self.slow, self.fast, self.ma, full_output=True)
        self.assertEqual((2+4), result.shape[1])

    def test_output_result_matrix_cols_number_full_if_input_df(self):
        '''macd result df must have original df columns plus 4'''
        result = ti.MACD(self.test_data_df, self.slow, self.fast, self.ma, full_output=True)
        self.assertEqual((self.test_data_df.shape[1] + 4), result.shape[1])

# Test input data
class BadInputMACD(unittest.TestCase):
  # Input data
  test_data = pd.read_csv('test_data/correct_series.csv')
  test_data_list = list(test_data.values)
  test_data_df_no_close = pd.read_csv('test_data/correct_ohlc.csv').drop(columns=['Close', 'Adj Close'])
  test_data_df_more_close = pd.read_csv('test_data/correct_ohlc.csv')

  # Input parameters
  slow = 24
  fast = 12
  ma = 9

  def test_parameter_not_int(self):
    '''all parameters must be integer type'''
    self.assertRaises(TypeError, ti.MACD, self.test_data, 15.5, 9, 5)

  def test_input_data_not_series_or_df(self):
    '''input data must be a pd.DataFrame or pd.Series'''
    self.assertRaises(TypeError, ti.MACD, self.test_data_list, self.slow, self.fast, self.ma)

  def test_slow_is_less_than_fast(self):
    '''slow parameter must be greater than fast'''
    self.assertRaises(ValueError, ti.MACD, self.test_data, 12, 24, self.ma)

  def test_df_no_close_column(self):
    '''pd.DataFrame as input must have close column'''
    self.assertRaises(IndexError, ti.MACD, self.test_data_df_no_close, self.slow, self.fast, self.ma)

  def test_df_more_than_one_close_column(self):
    '''pd.DataFrame as input must have only one close column'''
    self.assertRaises(KeyError, ti.MACD, self.test_data_df_more_close, self.slow, self.fast, self.ma)

if __name__ == '__main__':
    unittest.main()