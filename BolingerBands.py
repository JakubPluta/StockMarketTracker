import pandas as pd
import numpy as np

def bolinger(df, days=30, num=2):
    ''' Function that takes dataframe with stock close price and count bolinger bands'''
    df[f'MA_{str(days)}'] = df['Close'].rolling(window=days).mean()
    df[f'STD_{str(days)}'] = df['Close'].rolling(window=days).std()
    df['Upper Band'] = df[f'MA_{str(days)}'] + (df[f'STD_{str(days)}'] * num)
    df['Lower Band'] = df[f'MA_{str(days)}'] - (df[f'STD_{str(days)}'] * num)
    return df

def daily_return(df):
    df['DailyReturn'] = df['Close'].pct_change()
    df['cum_returns'] = (df['Close'].pct_change() + 1).cumprod()
    return df


def get_colors(df):
    colors = []
    for i in range(len(df['DailyReturn'])):
        if i != 0:
            if df['DailyReturn'][i] > 0:
                colors.append('#336600')
            else:
                colors.append('#cc0000')
        else:
            colors.append('#cc0000')
    return colors


