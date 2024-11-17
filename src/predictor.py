import numpy as np 
import pandas as pd
from statsmodels.tsa.api import SimpleExpSmoothing
import sys

class PricePredictor:

    '''
    Function used to predict next values starting from a series.
    To achieve this the exponential smoothining method was used.
     - Exponential smoothing is based on the assumption that the future values of a time series are a function of its past values.
    '''
    def predict(self, csv_data, num_predictions):

        df = pd.DataFrame(csv_data, columns=['Name', 'Date', 'Price'])
        df = df.drop('Name', axis=1)
        df = df.sort_values(by=['Date'])
        df = df.drop('Date', axis=1)
        
        values = df['Price'].astype(float).to_numpy().flatten()
        values_len = len(values)

        model = SimpleExpSmoothing(values)
        model = model.fit(smoothing_level  = 0.2, optimized = False)
        return model.forecast(num_predictions)