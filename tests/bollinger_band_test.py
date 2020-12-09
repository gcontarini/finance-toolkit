import unittest
import pandas as pd
from context import bollinger_band

# Test results
class ResultsBollBand(unittest.TestCase):
    # Input data
    test_data = pd.read_csv('test_data/correct_series.csv')
    test_data_df = pd.read_csv('test_data/correct_ohlc.csv').drop(columns=['Close'])

    # Expected results output
    results_up = pd.Series([None, None, None, None, None, None,
        None, None, None, None, None, None, 
        None, None, None, None, None, None, 
        None, None, None, None, 26.21228851, 26.21842961,
        26.21536401, 26.21854247, 26.23283952, 26.25184116, 26.2737371,  26.29666398,
        26.32348597, 26.33612174, 26.34830112, 26.36086398, 26.37022444, 26.37874382,
        26.39844624, 26.40980235, 26.41730796, 26.41604871, 26.42503333, 26.43523417,
        26.44668632, 26.46460913, 26.49085775, 26.51208908, 26.53217248, 26.55029129,
        26.5658781,  26.59462801, 26.62424345, 26.66094788, 26.69159394, 26.71388736,
        26.73224366, 26.750159,   26.76647677, 26.78669296, 26.79782092, 26.80324433,
        26.79602473, 26.79071002, 26.77744539, 26.75989564, 26.73706692, 26.71710932,
        26.69443393, 26.67920573, 26.66880665, 26.66609397, 26.66793366])
    
    results_low = pd.Series([None, None, None, None, None, None, 
        None, None, None, None, None, None, 
        None, None, None, None, None, None, 
        None, None, None, None, 26.16104447, 26.17657021, 
        26.18296922, 26.18812429, 26.19716047, 26.20149206, 26.20459605, 26.20666943, 
        26.21151419, 26.20887833, 26.21003259, 26.21746956, 26.22477583, 26.23125647, 
        26.2482206, 26.26019773, 26.26935885, 26.27395151, 26.28663341, 26.2980991, 
        26.30664709, 26.32039104, 26.33747547, 26.34791089, 26.35782755, 26.36804208, 
        26.37412211, 26.38870557, 26.40242351, 26.42238577, 26.43673978, 26.44777983, 
        26.46108997, 26.47650777, 26.49019005, 26.50830711, 26.52217909, 26.5367555, 
        26.55064161, 26.56928964, 26.58422066, 26.59343688, 26.59793249, 26.60622315, 
        26.61056542, 26.61579371, 26.61452618, 26.60557224, 26.59873244])

    # Input paramter
    ma = 12

    def test_result_up(self):
        '''bollband function must return up line with values equal to expected'''
        results = bollinger_band.bollband(self.test_data, self.ma)
        pd.testing.assert_series_equal(self.results_up, results['bollband_up'], check_names=False)

    def test_result_low(self):
        '''bollband function must return low line with values equal to expected'''
        results = bollinger_band.bollband(self.test_data, self.ma)
        pd.testing.assert_series_equal(self.results_low, results['bollband_low'], check_names=False)

    def test_result_df_lenght(self):
        '''bollband result must have the expected lenght'''
        results = bollinger_band.bollband(self.test_data, self.ma)
        self.assertEqual(self.results_up.shape[0], results.shape[0])

    def test_result_df_columns_number(self):
        '''bollband result must have the expected columns number'''
        results = bollinger_band.bollband(self.test_data, self.ma)
        self.assertEqual(2, results.shape[1])

    def test_result_df_columns_number_full(self):
        '''bollband result must have the expected columns number for full output'''
        series_og_columns = 2
        result_columns = 3
        results = bollinger_band.bollband(self.test_data, self.ma, full_output=True)
        self.assertEqual(series_og_columns+result_columns, results.shape[1])

    def test_result_df_columns_number_full_if_df(self):
        '''bollband result must have the expected columns number for full output if input data is ohlc'''
        results = bollinger_band.bollband(self.test_data_df, self.ma, full_output=True)
        self.assertEqual(self.test_data_df.shape[1]+3, results.shape[1])

# Test input data
class BadInputBollBand(unittest.TestCase):
  # Input data
  test_data = pd.read_csv('test_data/correct_series.csv')
  test_data_list = list(test_data.values)
  test_data_df_no_close = pd.read_csv('test_data/correct_ohlc.csv').drop(columns=['Close', 'Adj Close'])
  test_data_df_more_close = pd.read_csv('test_data/correct_ohlc.csv')

  # Input parameters
  ma = 12

  def test_parameter_not_int(self):
    '''if ma is not integer should raise TypeError'''
    self.assertRaises(TypeError, bollinger_band.bollband, self.test_data, 11.59)

  def test_input_data_not_series_or_df(self):
    '''if data is not an valid type should raise TypeError'''
    self.assertRaises(TypeError, bollinger_band.bollband, self.test_data_list, self.ma)

  def test_df_no_close_column(self):
    '''if df has not close column than should raise IndexError'''
    self.assertRaises(IndexError, bollinger_band.bollband, self.test_data_df_no_close, self.ma)

  def test_df_more_than_one_close_column(self):
    '''if df has more than one close column than should raise KeyError'''
    self.assertRaises(KeyError, bollinger_band.bollband, self.test_data_df_more_close, self.ma)

if __name__ == '__main__':
    unittest.main()