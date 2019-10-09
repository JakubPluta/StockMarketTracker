import quandl
import pandas as pd
import datetime as dt
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)
pd.options.mode.chained_assignment = None
import re
import os


api_key = os.environ.get('API_KEY')

def CleanTickers():
    ''' Main Goal is to Exclude all companies which weren't quotated for period longer then 30 days back since today
    and also to extract isin number for other purpose like scrape data about company'''

    ticker_list = pd.read_csv(r'WSE_metadata.csv')
    back_30days = dt.date.today() - dt.timedelta(days=30) # get only companies which are quotated
    tickers = ticker_list[ticker_list['to_date']>str(back_30days)]
    tickers['ISIN'] = tickers['name'].str.split(', ',expand=True)[1].str.strip()
    tickers['StockExchange'] = 'WSE'
    tickers = tickers[['StockExchange','code','ISIN']]
    #tickers.to_csv(f'{tickers.iloc[0][0]}_tickers.csv') # uncomment if you want to save cleaned data to csv file
    return tickers

wigs = ['MWIG40', 'MWIG40DVP', 'MWIG40TR', 'SWIG80', 'SWIG80DVP', 'SWIG80TR', 'WIG20', 'WIG20DVP', 'WIG20LEV', 'WIG20SHORT', 'WIG20TR', 'WIG30', 'WIG30TR', 'WIG_BANKI', 'WIG_BUDOW', 'WIG_CEE', 'WIG_CHEMIA', 'WIGDIV', 'WIG_ENERG', 'WIG_GAMES', 'WIG_GORNIC', 'WIG_INFO', 'WIG_LEKI', 'WIG_MEDIA', 'WIG_MOTO', 'WIG_MS_BAS', 'WIG_MS_FIN', 'WIG_MS_PET', 'WIG_NRCHOM', 'WIG_ODZIEZ', 'WIG_PALIWA', 'WIG_POLAND', 'WIG_SPOZYW', 'WIGTECH', 'WIG_TELKOM', 'WIG_UKRAIN','WIG']


def GetData(ticker,start='2017-01-01'):
    '''Simple Function that get stock data by given ticker an start date'''
    df = quandl.get("WSE/"+ticker,authtoken=api_key,start_date=start,index_col='Date')
    if ticker in wigs: # There is a problem when we look at index like WIG, WIG20 etc. Then there is no columns Volume but Turnover
        df = df[['Open', 'High', 'Low', 'Close', 'Turnover (1000s)']]
        df.rename(columns={'Turnover (1000s)':'Volume'},inplace=True)
    else:
        df = df[['Open','High','Low','Close','Volume']]
    #df_cv = df[['Close','Volume']]
    return df










