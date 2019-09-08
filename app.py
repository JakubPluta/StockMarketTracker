import dash
import datetime as dt
import dash_core_components as dcc
import dash_html_components as html
from dash_core_components import Input
from dash.dependencies import Input,Output,State
from ScrapeStockExchange import GetData as GD
import plotly.graph_objs as go
from BolingerBands import bolinger, daily_return, get_colors
import pandas as pd
from return_rates import return_rates as rr, clrs
#from GetNews import Table,get_news


external_sheet1 = ['https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

tickers = pd.read_csv('WSE_tickers.csv')
ticker_list = tickers['code'][2:].to_list()

opts = [{'label' : i, 'value' : i} for i in ticker_list]

app = dash.Dash('Stock Market',external_stylesheets=external_sheet1)

app.layout = html.Div([
html.Div([

  html.Div(
    [
      html.H1(
        'Stock Market Tracker',
        style={'font-family': 'Helvetica',
               "margin-top": "15",
               "margin-bottom": "0"},
        className='eight columns'
      ),
      html.P(
        'App to track choosen stock company from Warsaw Stock Exchange',
        style={'font-family': 'Helvetica',
               "font-size": "100%",
               "width": "80%"},
        className='eight columns',
      ),
    ],
    className='row'
  ),html.Div([
        dcc.Dropdown(
            id='stock-dropdown',
            options=opts,
            value='WIG20',#className='six columns'
        ),],className='row',style = {'width': '200px',
                                    'fontSize' : '12px',
                                    'padding-top' : '10px',
                                    'display': 'inline-block'}
  ),



html.Div([
        html.Div([html.H3('Stock Quote'),
            dcc.Graph(
                 id="stock-graph")

        ], className="eight columns"),

        html.Div([
            html.H3("Stock Daily Returns"),
          dcc.Graph(
            id="stock-graph2",

           )

        ], className="four columns"),

    ],className="row"),
html.Div([html.H5('Return Rates'),
            dcc.Graph(
                 id="stock-graph3")

        ], className='four columns'),



         # html.Div([html.H5(f'Warsaw Stock Exchange News {str(dt.date.today())}'),
         #           Table(get_news())
         #           ], className="six columns",style = {
         #                            'fontSize' : '12px',
         #
         #                            'padding-right' : '200px'
         #                            }),

]),])





@app.callback(Output('stock-graph', 'figure'), [Input('stock-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    # read stock price data from google-finance
    df = GD(str(selected_dropdown_value), start='2018-01-01')
    df['MA_15'] = df['Close'].rolling(window=15).mean()
    df2 = bolinger(df=df, days=30, num=2)
    df.replace(to_replace=0, method='bfill',inplace=True)
    df = daily_return(df)


    trace1 = {
        'name': str(selected_dropdown_value),
        'type': 'candlestick',
        'x': df.index,
        'yaxis': 'y2',
        'open': df['Open'],
        'high': df['High'],
        'low': df['Low'],
        'close': df['Close'],
        "decreasing": {"line": {"color": '#c55572'}},
        "increasing": {"line": {"color": '#79BD9A'}}
    }
    trace2 = {
        'name': 'Volume',
        'type': 'bar',
        'x': df.index,
        'y': df['Volume'],
        'yaxis': 'y',
        'marker': dict(
            color='rgb(204,204,204)')
    }
    trace3 = {
        'name': 'MA 15',
        'type': 'scatter',
        'mode': 'lines',
        'x': df.index,
        'y': df['MA_15'],
        'yaxis': 'y2',
        'marker': {"color": "#E377C2"},
        'line': {'width': 1}
    }
    trace4 = {
        'name': 'MA 30',
        'type': 'scatter',
        'mode': 'lines',
        'x': df.index,
        'y': df['MA_30'],
        'yaxis': 'y2',
        'marker': {"color": "#0B486B"},
        'line': {'width': 1}
    }
    bolinger_upper = {
        'name': 'Bolinger',
        'type': 'scatter',
        'mode': 'lines',
        'x': df.index,
        'y': df['Upper Band'],
        'yaxis': 'y2',
        'marker': {"color": "#ccc"},
        'line': {'width': 1}
    }
    bolinger_lower = {
        'name': 'Bolinger',
        'showlegend': False,
        'type': 'scatter',
        'mode': 'lines',
        'x': df.index,
        'y': df['Lower Band'],
        'yaxis': 'y2',
        'marker': {"color": "#ccc"},
        'line': {'width': 1}
    }

    layout = {
        "xaxis": {"rangeselector": {
            "x": 0,
            "y": 0.87,
            "font": {"size": 10},
            "visible": True,
            "bgcolor": "rgba(150, 200, 250, 0.4)",
            "buttons": [
                {
                    "step": "all",
                    "count": 1,
                    "label": "Clear"
                },
                {
                    "step": "year",
                    "count": 1,
                    "label": "1Y",
                    "stepmode": "backward"
                },
                {
                    "step": "month",
                    "count": 3,
                    "label": "3M",
                    "stepmode": "backward"
                },
                {
                    "step": "month",
                    "count": 1,
                    "label": "1M",
                    "stepmode": "backward"
                },
                {"step": "all"}
            ]
        },'rangeslider':{'visible':'False'}},

        "yaxis": {
            "domain": [0, 0.8],
            "showticklabels": False
        },
        "legend": {
            "x": 0.4,
            "y": 0.8,
            "yanchor": "bottom",
            "orientation": "h"
        },
        "margin": {
            "b": 20,
            "l": 40,
            "r": 40,
            "t": 0
        },
        "yaxis2": {"domain": [0.2, 0.8]},
        #"plot_bgcolor": "rgb(250, 250, 250)",

    }
    return {'data': [trace1, trace2, trace3, trace4, bolinger_lower, bolinger_upper],
            'layout': layout
            }

@app.callback(Output('stock-graph2', 'figure'), [Input('stock-dropdown', 'value')])
def update_graph2(selected_dropdown_value):
    # read stock price data from google-finance
    df = GD(str(selected_dropdown_value), start='2018-01-01')
    df.replace(to_replace=0, method='bfill',inplace=True)
    df = daily_return(df)
    clr = get_colors(df)


    tdaily = {
        'name': str(selected_dropdown_value),
        'type': 'bar',
        #'mode':'bar',
        'x': df.index,
        'y': df['DailyReturn'],
        'yaxis': 'y2',

        'marker': {"color": clr}


    }



    layout = {
        "xaxis": {"rangeselector": {
            "x": 0,
            "y": 0.87,
            "font": {"size": 10},
            "visible": True,
            "bgcolor": "rgba(150, 200, 250, 0.4)",
            "buttons": [
                {
                    "step": "all",
                    "count": 1,
                    "label": "Clear"
                },
                {
                    "step": "year",
                    "count": 1,
                    "label": "1Y",
                    "stepmode": "backward"
                },
                {
                    "step": "month",
                    "count": 3,
                    "label": "3M",
                    "stepmode": "backward"
                },
                {
                    "step": "month",
                    "count": 1,
                    "label": "1M",
                    "stepmode": "backward"
                },
                {"step": "all"}
            ]
        },'rangeslider':{'visible':'False'}},

        "yaxis": {
            "domain": [0, 0.8],
            "showticklabels": False
        },
        "legend": {
            "x": 0.4,
            "y": 0.8,
            "yanchor": "bottom",
            "orientation": "h"
        },
        "margin": {
            "b": 20,
            "l": 40,
            "r": 40,
            "t": 0
        },
        "yaxis2": {"domain": [0.2, 0.8]},
        #"plot_bgcolor": "rgb(250, 250, 250)"
    }
    return {'data': [tdaily],
            'layout': layout
            }

#######################################################

@app.callback(Output('stock-graph3', 'figure'), [Input('stock-dropdown', 'value')])
def update_graph3(selected_dropdown_value):
    # read stock price data from google-finance
    df = GD(str(selected_dropdown_value), start='2018-01-01')
    df.replace(to_replace=0, method='bfill',inplace=True)
    df = rr(df)
    clr = clrs(df)


    returns = {
        'name': str(selected_dropdown_value),
        'type': 'bar'
        #'mode':'bar',
        ,'text' : df['Return_Rates'],
        'textposition' : 'auto',

        'x': df.index,
        'y': df['Return_Rates'],
        'yaxis': 'y',

        'marker': {"color": clr} }

    layout =  { "yaxis": {
            "domain": [0.1, 0.9],
            "showticklabels": True
        },


    "margin": {
        "b": 5,
        "l": 40,
        "r": 40,
        "t": 10
    },


    }
    return {'data': [returns],
            'layout': layout
            }



if __name__ == '__main__':
    app.run_server(debug=True)
