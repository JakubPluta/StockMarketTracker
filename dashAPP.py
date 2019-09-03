import dash
import dash_core_components as dcc
import dash_html_components as html
from ScrapeStockExchange import GetData as GD
import plotly.graph_objs as go
from BolingerBands import bolinger

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# stocks = input('Enter Company Ticker: ')
# stocks = str(stocks.strip())
df = GD('KGHM',start='2018-01-01')
df['MA_15'] = df['Close'].rolling(window=15).mean()
df2 = bolinger(df=df,days=30,num=2)

print(df2)

trace1 = {
  'name': 'stocks',
  'type': 'candlestick',
    'x':df.index,
    'yaxis':'y2',
    'open': df['Open'],
    'high':df['High'],
    'low':df['Low'],
          'close':df['Close'],
  "decreasing": {"line": {"color": '#c55572'}},
  "increasing": {"line": {"color": '#79BD9A'}}
}
trace2 = {
  'name': 'Volume',
  'type': 'bar',
    'x':df.index,
    'y':df['Volume'],
    'yaxis':'y',
    'marker':dict(
        color='rgb(204,204,204)')
}
trace3 = {
  'name': 'MA 15',
  'type': 'scatter',
    'mode' : 'lines',
    'x':df.index,
    'y':df['MA_15'],
    'yaxis':'y2',
    'marker': {"color": "#E377C2"},
    'line' : {'width' : 1 }
}
trace4 = {
  'name': 'MA 30',
  'type': 'scatter',
    'mode' : 'lines',
    'x':df.index,
    'y':df['MA_30'],
    'yaxis':'y2',
    'marker': {"color": "#0B486B"},
    'line' : {'width' : 1 }
}
bolinger_upper = {
  'name': 'Bolinger Upper',
  'type': 'scatter',
    'mode' : 'lines',
    'x':df.index,
    'y':df['Upper Band'],
    'yaxis':'y2',
    'marker': {"color": "#ccc"},
    'line' : {'width' : 1 }
}
bolinger_lower = {
  'name': 'Bolinger Lower',
  'type': 'scatter',
    'mode' : 'lines',
    'x':df.index,
    'y':df['Lower Band'],
    'yaxis':'y2',
    'marker': {"color": "#ccc"},
    'line' : {'width' : 1 }
}


layout = {
  "xaxis": {"rangeselector": {
      "x": 0,
      "y": 0.9,
      "font": {"size": 13},
      "visibe": True,
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
    }},
'height':700,
  "yaxis": {
    "domain": [0, 0.7],
    "showticklabels": False
  },
  "legend": {
    "x": 0.4,
    "y": 0.8,
    "yanchor": "bottom",
    "orientation": "h"
  },
  "margin": {
    "b": 10,
    "l": 40,
    "r": 40,
    "t": 10
  },
  "yaxis2": {"domain": [0.2, 0.8]},
  "plot_bgcolor": "rgb(250, 250, 250)"
}





app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H1(children='Stock Tracker'),

    html.Div(children='''
        by Jakub Pluta.
    '''),

    dcc.Graph(
        id='Stock Graph',
        figure={
            'data': [trace1,trace2,trace3,trace4,bolinger_lower,bolinger_upper],
            'layout': layout
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)