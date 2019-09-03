import pandas as pd
import numpy as np

def bolinger(df, days=30, num=2):
    ''' Function that takes dataframe with stock close price and count bolinger bands'''
    df[f'MA_{str(days)}'] = df['Close'].rolling(window=days).mean()
    df[f'STD_{str(days)}'] = df['Close'].rolling(window=days).std()
    df['Upper Band'] = df[f'MA_{str(days)}'] + (df[f'STD_{str(days)}'] * num)
    df['Lower Band'] = df[f'MA_{str(days)}'] - (df[f'STD_{str(days)}'] * num)
    return df

