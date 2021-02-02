import os
import unittest
import pandas as pd
from context import technical as ti

# Change working directory
# This enable running tests from repository root
if os.getcwd() != os.path.abspath(os.path.dirname(__file__)):
    os.chdir('tests/')

# Test results and outputs
class ResultsATR(unittest.TestCase):
    # Input data
    test_data = pd.read_csv('test_data/correct_ohlc.csv')

    # Input parameter
    ma = 12

    # Expected results
    result_atr = pd.Series([None, None, None, None, None, None, 
        None, None, None, None, None, 0.12249947, 0.12583288, 0.12083292, 0.1099995,
       0.10249949, 0.09749969, 0.09999959, 0.09333293, 0.09166638,
       0.09166654, 0.08999999, 0.08916664, 0.08583355, 0.08583355,
       0.08333349, 0.08833361, 0.08916696, 0.08750025, 0.08166695,
       0.08083359, 0.08333349, 0.08000008, 0.07916673, 0.07916673,
       0.07749987, 0.07583316, 0.07916657, 0.07583316, 0.07166656,
       0.08249982, 0.08666643, 0.08833313, 0.08499988, 0.08416653,
       0.08416653, 0.08249998, 0.08500004, 0.08166679, 0.07916673,
       0.08083344, 0.08583339, 0.08083344, 0.07583348, 0.07250007,
       0.07416677, 0.07333342, 0.07166688, 0.07000001, 0.07249991,
       0.07749987, 0.08083328, 0.08000008, 0.07666667, 0.07166656,
       0.06833315, 0.0674998 , 0.06499974, 0.0649999 , 0.0649999 ,
       0.0649999 ])

    result_tr = pd.Series([0.06999969, 0.13999939, 0.17000008, 0.17000008, 0.11999893,
       0.13000107, 0.15999985, 0.1099987 , 0.1099987 , 0.09999847,
       0.09000015, 0.09999847, 0.11000061, 0.07999992, 0.03999901,
       0.07999992, 0.06000137, 0.15999985, 0.07999992, 0.09000015,
       0.11000061, 0.07999992, 0.07999992, 0.06000137, 0.11000061,
       0.04999924, 0.10000038, 0.09000015, 0.04000092, 0.09000015,
       0.06999969, 0.11999893, 0.06999969, 0.06999969, 0.07999992,
       0.03999901, 0.09000015, 0.09000015, 0.05999947, 0.04000092,
       0.17000008, 0.13999939, 0.09000015, 0.07999992, 0.05999947,
       0.06999969, 0.06000137, 0.06999969, 0.05000114, 0.05999947,
       0.07999992, 0.10000038, 0.11000061, 0.07999992, 0.04999924,
       0.10000038, 0.04999924, 0.05000114, 0.03999901, 0.09999847,
       0.11000061, 0.10000038, 0.0700016 , 0.05999947, 0.04999924,
       0.03999901, 0.03999901, 0.06999969, 0.05000114, 0.05000114,
       0.03999901])

    def test_result_atr(self):
        '''results must matches what is expected for atr series'''
        result = ti.ATR(self.test_data, self.ma)
        pd.testing.assert_series_equal(self.result_atr, result['atr'], check_names=False)

    def test_result_tr(self):
        '''results must matches what is expected for tr series'''
        result = ti.ATR(self.test_data, self.ma)
        pd.testing.assert_series_equal(self.result_tr, result['tr'], check_names=False)

    def test_result_df_lenght(self):
        '''results df are the expected lenght'''
        result = ti.ATR(self.test_data, self.ma)
        self.assertEqual(self.test_data.shape[0], result.shape[0])

    def test_result_df_columns_number(self):
        '''results df must have expected number of columns (2)'''
        result = ti.ATR(self.test_data, self.ma)
        self.assertEqual(2, result.shape[1])

    def test_result_df_columns_number_full(self):
        '''results df must have expected number of columns for full output (original plus 5)'''
        result = ti.ATR(self.test_data, self.ma, full_output=True)
        self.assertEqual(self.test_data.shape[1] + 5, result.shape[1])

# Test input data
class BadInputATR(unittest.TestCase):
    # Input data
    test_data = pd.read_csv('test_data/correct_ohlc.csv')
    test_wrong_type = test_data.copy().reset_index().to_dict(orient='list')
    test_missing_column = test_data.copy().drop(columns=['Close'])

    # Input parameter
    ma = 12

    def test_ma_not_integer(self):
        '''if ma parameter is not integer should raise TypeError'''
        self.assertRaises(TypeError, ti.ATR, self.test_data, 12.7)

    def test_input_data_not_df(self):
        '''if data input is not df should raise TypeError'''
        self.assertRaises(TypeError, ti.ATR, self.test_wrong_type, self.ma)

    def test_input_data_missing_column(self):
        '''if data input is missing a column or it's labeled wrong should raise IndexError'''
        self.assertRaises(IndexError, ti.ATR, self.test_missing_column, self.ma)


if __name__ == '__main__':
    unittest.main()