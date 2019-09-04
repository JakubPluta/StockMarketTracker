import quandl
import pandas as pd
import datetime as dt
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)
pd.options.mode.chained_assignment = None
import requests
import bs4
from bs4 import BeautifulSoup

st = pd.read_csv('WSE_tickers.csv')
st.dropna(inplace=True)
isins = st['ISIN'].str.split(n=2 ,expand=True)[1].str.strip().to_list()
codes = st['code'].to_list()
isin = str(isins[5])
url = f'https://www.money.pl/gielda/spolki-gpw/{isin}.html'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
wskazniki = soup.find_all('div',attrs={'class':'wi06td-1 hNfnKj'})

#print(soup.find_all('div',attrs={'class':'wi06td-1 hNfnKj'}))

for i in wskazniki:
    print(i)
    try:
        print(i.find('dt').text)
        print(i.find('dd').text)
    except:
        pass