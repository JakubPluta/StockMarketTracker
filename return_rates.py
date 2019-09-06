import numpy as np
import pandas as pd
import datetime as dt
from ScrapeStockExchange import GetData as GD

df = GD('ECHO',start='2018-01-01')


def return_rates(df):
    new_df = pd.DataFrame()
    start = dt.date(2019,1,1)
    end = df.index[df.index==max(df.index)].to_pydatetime()[0].date()
    days = np.busday_count( start, end )
    new_df['1M'] = round(df['Close'].pct_change(periods=30)*100,2)
    new_df['2M'] = round(df['Close'].pct_change(periods=60)*100,2)
    new_df['3M'] = round(df['Close'].pct_change(periods=90)*100,2)
    new_df['6M'] = round(df['Close'].pct_change(periods=180)*100,2)
    new_df['1Y'] = round(df['Close'].pct_change(periods=360)*100,2)
    new_df['YTD'] = round(df['Close'].pct_change(periods=int(days))*100,2)
    new_df = new_df[-1:].T
    new_df.columns = ['Return Rates']
    new_df['Return_Rates'] = new_df['Return Rates'].apply(lambda x: str(x) + ' %')
    return new_df

def clrs(df):
    colors = []
    for i in range(len(df['Return Rates'])):
        if i != 0:
            if df['Return Rates'][i] > 0:
                colors.append('#336600')
            else:
                colors.append('#cc0000')
        else:
            colors.append('#cc0000')
    return colors

