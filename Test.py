# import pandas as pd
# # from ScrapeStockExchange import GetData
# #
# # df = pd.read_csv('WSE_tickers.csv')
# # codes = df['code'].to_list()
# # full_data = pd.DataFrame(columns=['Date','Close','Volume'])
# # fd = []
# # for code in codes[:]:
# #     try:
# #         x = GetData(code,start='2018-01-01')
# #         x['code'] = code
# #         x.reset_index(inplace=True)
# #     #print(x)
# #         fd.append(x)
# #     except:
# #         pass
# # full_data = full_data.append(fd,ignore_index=True,sort=True)
# # # full_data.set_index('code',inplace=True)
# # # full_data.reset_index(inplace=True)
# # full_data = full_data[['code','Date','Close','Volume']].set_index('code')
# # print(full_data)

""" dashboard to track daily close stock price of a selection of
    companies in semiconductor industry
    Author: Yi Zhang <beingzy@gmail.com>
    Date: 2017/06/25
"""
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from pandas_datareader import data as web
from datetime import datetime as dt

app = dash.Dash('Semiconductor-Companies')

app.layout = html.Div([
    dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'AMD', 'value': 'AMD'},
            {'label': 'Nvidia', 'value': 'NVDA'},
            {'label': 'Intel', 'value': 'INTC'},
        ],
        value='AMD'
    ),
    dcc.Graph(id='stock-graph')
], style={'width': '600'})


@app.callback(Output('stock-graph', 'figure'), [Input('stock-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    # read stock price data from google-finance
    df = web.DataReader(
        selected_dropdown_value,
        'yahoo',
        dt(2016, 1, 1),
        dt.now()
    )

    return {
        'data': [{
            'x': df.index, # date
            'y': df['Close'] # close price
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }

# plotly css styling sheets
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgp.css'})

if __name__ == '__main__':
    app.run_server()