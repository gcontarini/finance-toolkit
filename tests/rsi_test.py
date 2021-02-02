import os
import unittest
import pandas as pd
from context import technical as ti

# Change working directory
# This enable running tests from repository root
if os.getcwd() != os.path.abspath(os.path.dirname(__file__)):
    os.chdir('tests/')

# Test results
class ResultsRSI(unittest.TestCase):
    # Input data
    test_data = pd.read_csv('test_data/correct_series.csv')
    test_data_df = pd.read_csv('test_data/correct_ohlc.csv').drop(columns=['Close'])

    # Expected results output
    results_rsi = pd.Series([None, None, None, None, None, None,
      None, None, None, None, None, None,
      47.25280022804261, 46.88077998698816, 47.101267162264016, 47.00929322452039, 46.7165184370504, 47.15738539063636,
      46.77617492442675, 46.89141568802567, 47.055962508174325, 46.75436640536967, 47.22730953343007, 48.15725812972951,
      48.388571703427004, 48.80045436339292, 49.799615719433724, 50.749816167931876, 51.71693204342112, 52.62985533413443,
      53.758601079486596, 53.89482377914421, 54.17495518260089, 54.736926654922605, 55.13423749963049, 55.442951738396005,
      56.739537559474186, 57.26885485742762, 57.500127463438524, 57.14236479747808, 57.54149746743077, 57.905820742390425,
      58.17383724213553, 59.059331336307984, 60.457448003690054, 61.11872163570835, 61.66694808843557, 62.074080067528016,
      62.20694317850205, 63.45076515475267, 64.61890382304387, 66.27248731535836, 67.42124873044372, 67.9395808355508,
      68.37488505254538, 68.84210071524612, 69.17189954309868, 70.12209998782939, 70.28368853923217, 70.03506574509129,
      68.80640030241051, 67.91980536038358, 66.48142225875074, 64.7679765608068, 62.68677670273754, 61.158316243822775,
      59.26206075171424, 57.9066342975084, 56.56970803414393, 55.33354873756501, 54.63870450844905])
    
    # Input paramter
    ma = 12

    def test_result_rsi(self):
        '''rsi function must return series equal to expected'''
        results = ti.RSI(self.test_data, self.ma)
        pd.testing.assert_series_equal(self.results_rsi, results, check_names=False)

    def test_result_df_lenght(self):
        '''rsi result must have the expected lenght'''
        results = ti.RSI(self.test_data, self.ma)
        self.assertEqual(self.results_rsi.shape[0], results.shape[0])

    def test_result_df_columns_number_full(self):
        '''rsi result must have the expected columns number for full output'''
        series_og_columns = 2
        result_columns = 5
        results = ti.RSI(self.test_data, self.ma, full_output=True)
        self.assertEqual(series_og_columns+result_columns, results.shape[1])

    def test_result_df_columns_number_full_if_df(self):
        '''rsi result must have the expected columns number for full output if input data is ohlc'''
        result_columns = 5
        results = ti.RSI(self.test_data_df, self.ma, full_output=True)
        self.assertEqual(self.test_data_df.shape[1]+result_columns, results.shape[1])

# Test input data
class BadInputRSI(unittest.TestCase):
  # Input data
  test_data = pd.read_csv('test_data/correct_series.csv')
  test_data_list = list(test_data.values)
  test_data_df_no_close = pd.read_csv('test_data/correct_ohlc.csv').drop(columns=['Close', 'Adj Close'])
  test_data_df_more_close = pd.read_csv('test_data/correct_ohlc.csv')

  # Input parameters
  ma = 12

  def test_parameter_not_int(self):
    '''if ma is not integer should raise TypeError'''
    self.assertRaises(TypeError, ti.RSI, self.test_data, 11.59)

  def test_input_data_not_series_or_df(self):
    '''if data is not a valid type should raise TypeError'''
    self.assertRaises(TypeError, ti.RSI, self.test_data_list, self.ma)

  def test_df_no_close_column(self):
    '''if df has not close column than should raise IndexError'''
    self.assertRaises(IndexError, ti.RSI, self.test_data_df_no_close, self.ma)

  def test_df_more_than_one_close_column(self):
    '''if df has more than one close column than should raise KeyError'''
    self.assertRaises(KeyError, ti.RSI, self.test_data_df_more_close, self.ma)

if __name__ == '__main__':
    unittest.main()