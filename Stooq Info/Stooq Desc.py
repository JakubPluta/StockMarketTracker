
import pandas as pd
from pandas.io.html import read_html
import datetime as dt
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)
pd.options.mode.chained_assignment = None
import requests
import bs4
from bs4 import BeautifulSoup
from StooqLinks import stooq_links

stooqs = stooq_links()

for i in stooqs[:20]:
    u = i
   # u = 'https://stooq.com/q/g/?s=cfg'
    e = u[-3:]
    try:
        infoboxes = read_html(u,index_col=0,attrs={'id':'t1'})
        t1 = infoboxes[0].T
        t2 = infoboxes[1].T
        t3 = infoboxes[3].T
        t3.index = pd.RangeIndex(len(t3.index))

        result = pd.concat([t1, t2,t3], axis=1, sort=False)
        result.dropna(how='any',inplace=True)
        result['Code'] = str(e).upper()
        result = result[['Code','Kapitalizacja','Wartość księgowa','C/WK','1 tydzień', '1 miesiąc', '3 miesiące', '6 miesięcy', 'YTD', '1 rok']]
        result.rename(columns={'Kapitalizacja':'Market capitalization',
                               'Wartość księgowa':'Booking Value',
                               'C/WK':'P/BV','1 tydzień' :'Return Rate 1W', '1 miesiąc':'Return Rate 1M', '3 miesiące': 'Return Rate 3M',
                               '6 miesięcy':'Return Rate 6M', 'YTD':'Return Rate YTD', '1 rok':'Return Rate 1Y'
        }, inplace=True)
    except:
        pass
    print(result)
