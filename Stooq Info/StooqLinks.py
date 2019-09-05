import quandl
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



# urls = ['https://stooq.com/t/?i=523&v=0&l=1','https://stooq.com/t/?i=523&v=0&l=2','https://stooq.com/t/?i=523&v=0&l=3','https://stooq.com/t/?i=523&v=0&l=4','https://stooq.com/t/?i=523&v=0&l=5','https://stooq.com/t/?i=523&v=0&l=6']
#
# url = 'https://stooq.com/t/?i=523&v=0&l=1'
#
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')
# #print(soup.find('table',attrs={'class':'fth1'}))
# table = soup.find('table',attrs={'class':'fth1'})
# f13 = table.find_all(id='f13')

def stooq_links():
    urls = ['https://stooq.com/t/?i=523&v=0&l=1', 'https://stooq.com/t/?i=523&v=0&l=2',
            'https://stooq.com/t/?i=523&v=0&l=3', 'https://stooq.com/t/?i=523&v=0&l=4',
            'https://stooq.com/t/?i=523&v=0&l=5', 'https://stooq.com/t/?i=523&v=0&l=6']
    links = []
    for u in urls:
        page = requests.get(u)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup.find('table',attrs={'class':'fth1'}))
        table = soup.find('table', attrs={'class': 'fth1'})
        f13 = table.find_all(id='f13')
        for i in f13:
            try:
                if i.find('a')['href'][:1] == 'q':
                    link = 'https://stooq.com/' + str(i.find('a')['href'])
                    link = link.replace('/q','/q/g')
                    links.append(link)
            except:
                pass
    return links





stooqs = stooq_links()
stooqs = pd.DataFrame(stooqs)
stooqs.to_csv('CompaniesLinks.csv')
print(stooqs)
