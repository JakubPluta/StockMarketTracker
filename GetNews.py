import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
from pandas.io.html import read_html
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
import dash
import dash_html_components as html
import pandas as pd


def get_news():
    url = requests.get(f'https://www.stockwatch.pl/wiadomosci/najnowsze')
    soup = BeautifulSoup(url.content, 'html.parser')
    news = soup.find(id='hpbxNwsWP')
    news = news.find_all('a')
    nws,lnks = [],[]
    for i in news:
        nws.append(i.text.strip())
        lnks.append(i['href'])
    dfs = pd.DataFrame(nws[:-1],lnks[:-1])
    dfs.reset_index(inplace=True)
    dfs.columns=['Link','News']
    return dfs

a = get_news()


def Table(df):

    return html.Div(
        [
            html.Div(
                html.Table(
                    # Header
                    [html.Tr([html.Th()])]
                    +
                    # Body
                    [
                        html.Tr(
                            [
                                html.Td(
                                    html.A(
                                        df.iloc[i]["News"],
                                        href=df.iloc[i]["Link"],
                                        target="_blank"
                                    )
                                )
                            ]
                        )
                        for i in range(0,len(df))
                    ]
                ),
                style={"height": "400px", "overflowY": "scroll"},
            ),
        ],
        style={"height": "100%"}, )


# app = dash.Dash()
# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/dZVMbK.css'})
#
# app.layout = html.Div(children=[
#     Table(get_news())
# ])
#
# if __name__ == '__main__':
#     app.run_server(debug=True)