import datetime
from dateutil.relativedelta import relativedelta
import nsepy as nse
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from stats import df, zipped_ind

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server


NAV_STYLE = {
    'padding':'1rem',
    'background':'black',
    'height':'100'
}

app.layout = html.Div([
    dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('StockView', style={'fontSize':35, 'textAlign':'center'})
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Nav([
                dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.NavItem(dcc.Dropdown(
                            id='stock-search',
                            options=[{'label':x, 'value':y} for x,y in zip(df['Company Name'], df['Symbol'])],
                            clearable=True,
                            placeholder='Search Stock',
                            multi=False,
                            style={'textAlign':'left', 'color':'black'}
                        ))
                    ], width=6),
                    dbc.Col([
                        dbc.NavItem(dbc.Button('1W', outline=True, color='danger',
                                               className='mr-1', id='1week', active='exact'))
                    ], width={'size':1, 'offset':1}),
                    dbc.Col([
                        dbc.NavItem(dbc.Button('1M', outline=True, color='danger',
                                               className='mr-1', id='1month', active='exact'))
                    ], width=1),
                    dbc.Col([
                        dbc.NavItem(dbc.Button('3M', outline=True, color='danger',
                                               className='mr-1', id='3month', active='exact'))
                    ], width=1),
                    dbc.Col([
                        dbc.NavItem(dbc.Button('6M', outline=True, color='danger',
                                               className='mr-1', id='6month', active='exact'))
                    ], width=1),
                    dbc.Col([
                        dbc.NavItem(dbc.Button('1Y', outline=True, color='danger',
                                               className='mr-1', id='1year', active='exact'))
                    ], width=1),

                ], id='dpr-row')
                    ])
            ], justified=True, fill=True, style=NAV_STYLE),
            ])
        ]),
    html.Br(),

    dbc.Row(children=[
        dbc.Col([
            dbc.Card(id='ticker'),
        ], width=3),
        dbc.Col([
            dbc.Card(id='industry'),
        ], width=3),
        dbc.Col([
            dbc.Card(id='time-max'),
        ], width=3),
        dbc.Col([
            dbc.Card(id='time-min')
        ], width=3)
    ], id='card-row'),
    html.Br(),
    dbc.Row([
        dbc.Col(children=[], width=8),
        dbc.Col(children=[], width=4)
    ], id='graph-row', style={'columnCount':2})
])])

#Designs_____________________________________________
card_col = 'black'
ticker_card_font_col = '#e69c15'
ticker_card_font_size = 26
ind_card_font_col = '#6badc9'
ind_card_font_size = 19
high_card_font_col = '#f02669'
high_card_font_size = ticker_card_font_size
low_card_font_col = '#3ac418'
low_card_font_size = ticker_card_font_size
card_bg_color = 'black'
plot_bgcolor = 'rgba(0,0,0,0)'
paper_bgcolor = 'black'
linecolor = 'white'
#______________________________________________________

@app.callback(
    [Output('card-row', 'children'),
    Output('graph-row', 'children')],
    [Input('stock-search', 'value'),
     Input('1week', 'n_clicks'),
     Input('1month', 'n_clicks'),
     Input('3month', 'n_clicks'),
     Input('6month', 'n_clicks'),
     Input('1year', 'n_clicks')
     ]
)
def update_page(value, btn1, btn2, btn3, btn4, btn5):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if value:

#1WEEK________________________________________________________________________________________________________________
        if '1week' in changed_id:
            end = datetime.date.today()
            diff = relativedelta(weeks=1)
            start = end - diff
            frame = nse.get_history(value, start, end)

            # Cards____________________
            card1 = dbc.Card([
                dbc.CardHeader('Ticker'),
                dbc.CardBody(value, style={'fontSize':ticker_card_font_size, 'color':ticker_card_font_col})
            ], id='ticker', style={'textAlign':'center','height':130}, color=card_bg_color)

            card2 = dbc.Card([
                dbc.CardHeader('Industry'),
                dbc.CardBody(zipped_ind.loc[zipped_ind[0]==value, 1], style={'fontSize':ind_card_font_size,
                                                                             'color':ind_card_font_col})
            ], id='industry', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card3 = dbc.Card([
                dbc.CardHeader('1 Week High'),
                dbc.CardBody(frame['High'].max(), style={'fontSize':high_card_font_size, 'color':high_card_font_col})
            ], id='time-max', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card4 = dbc.Card([
                dbc.CardHeader('1 Week Low'),
                dbc.CardBody(frame['Low'].min(), style={'fontSize':low_card_font_size, 'color':low_card_font_col})
            ], id='time-min', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            row1 = dbc.Container([
                dbc.Row(children=[
                    dbc.Col([
                        card1,
                    ], width=3),
                    dbc.Col([
                        card2,
                    ], width=3),
                    dbc.Col([
                        card3,
                    ], width=3),
                    dbc.Col([
                        card4
                    ], width=3)
                ], id='card-row')])

            #Graph____________________________
            fig = go.Figure(data=[go.Candlestick(
                x=frame.index,
                open=frame.Open,
                high=frame.High,
                low=frame.Low,
                close=frame.Close
            )])
            fig.update_xaxes(showgrid=False, linecolor=linecolor)
            fig.update_yaxes(showgrid=False, linecolor=linecolor)
            fig.update_layout({'plot_bgcolor':plot_bgcolor, 'paper_bgcolor':paper_bgcolor},
                              xaxis_rangeslider_visible=False, yaxis=dict(color=linecolor),
                              xaxis=dict(color=linecolor))
            ending = datetime.date.today()
            difference = relativedelta(weeks=52)
            starting = ending - difference
            new = nse.get_history(value, starting, ending)
            row2 = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='chart', figure=fig),
                    ], width=8),
                    dbc.Col([
                        dbc.Card([
                            dbc.ListGroup([
                                dbc.ListGroupItem('52 Week High'),
                                dbc.ListGroupItem(new.High.max(), style={'fontSize': ticker_card_font_size, 'color':high_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('52 Week Low'),
                                dbc.ListGroupItem(new.Low.min(), style={'fontSize': ticker_card_font_size, 'color':low_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average Volume (1 Week)'),
                                dbc.ListGroupItem(frame.Volume.mean().round(2), style={'fontSize': ticker_card_font_size, 'color':ind_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average VWAP (1 Week)'),
                                dbc.ListGroupItem(frame.VWAP.mean().round(2), style={'fontSize': ticker_card_font_size, 'color':ticker_card_font_col}, color=card_bg_color)
                            ])
                        ], style={'textAlign':'center'})
                    ], width=4)
                ], id='graph-row', style={'columnCount':2})
            ])

            return row1, row2

# 1MONTH________________________________________________________________________________________________________________
        if '1month' in changed_id:
            end = datetime.date.today()
            diff = relativedelta(months=1)
            start = end - diff
            frame = nse.get_history(value, start, end)
            frame['SMA_10'] = frame.Close.rolling(10, min_periods=1).mean()
            frame['SMA_20'] = frame.Close.rolling(20, min_periods=1).mean()

            # Cards____________________
            card1 = dbc.Card([
                dbc.CardHeader('Ticker'),
                dbc.CardBody(value, style={'fontSize':ticker_card_font_size, 'color':ticker_card_font_col})
            ], id='ticker', style={'textAlign':'center','height':130}, color=card_bg_color)

            card2 = dbc.Card([
                dbc.CardHeader('Industry'),
                dbc.CardBody(zipped_ind.loc[zipped_ind[0]==value, 1], style={'fontSize':ind_card_font_size,
                                                                             'color':ind_card_font_col})
            ], id='industry', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card3 = dbc.Card([
                dbc.CardHeader('1 Month High'),
                dbc.CardBody(frame['High'].max(), style={'fontSize':high_card_font_size, 'color':high_card_font_col})
            ], id='time-max', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card4 = dbc.Card([
                dbc.CardHeader('1 Month Low'),
                dbc.CardBody(frame['Low'].min(), style={'fontSize':low_card_font_size, 'color':low_card_font_col})
            ], id='time-min', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            row1 = dbc.Container([
                dbc.Row(children=[
                    dbc.Col([
                        card1,
                    ], width=3),
                    dbc.Col([
                        card2,
                    ], width=3),
                    dbc.Col([
                        card3,
                    ], width=3),
                    dbc.Col([
                        card4
                    ], width=3)
                ], id='card-row')])

            #Graph__________________________________________
            fig = go.Figure(data=[go.Candlestick(
                x=frame.index,
                open=frame.Open,
                high=frame.High,
                low=frame.Low,
                close=frame.Close,
                showlegend = False
            )])
            fig.update_xaxes(showgrid=False, linecolor=linecolor)
            fig.update_yaxes(showgrid=False, linecolor=linecolor)
            fig.update_layout({'plot_bgcolor': plot_bgcolor, 'paper_bgcolor': paper_bgcolor},
                              xaxis_rangeslider_visible=False, yaxis=dict(color=linecolor),
                              xaxis=dict(color=linecolor), legend_title_text='Select Moving Average',
                              legend=dict(title_font_family='Times New Roman', font=dict(size=12, color='white'), bordercolor='white', borderwidth=2))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_10'], name='10 SMA', line=dict(color='#a5f2f1'), visible='legendonly'))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_20'], name='20 SMA', line=dict(color='#f0ee8d'), visible='legendonly'))

            ending = datetime.date.today()
            difference = relativedelta(weeks=52)
            starting = ending - difference
            new = nse.get_history(value, starting, ending)

            row2 = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='chart', figure=fig),
                    ], width=8),
                    dbc.Col([
                        dbc.Card([
                            dbc.ListGroup([
                                dbc.ListGroupItem('52 Week High'),
                                dbc.ListGroupItem(new.High.max(), style={'fontSize':ticker_card_font_size, 'color':high_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('52 Week Low'),
                                dbc.ListGroupItem(new.Low.min(), style={'fontSize':ticker_card_font_size, 'color':low_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average Volume (1 Month)'),
                                dbc.ListGroupItem(frame.Volume.mean().round(2), style={'fontSize':ticker_card_font_size, 'color':ind_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average VWAP (1 Month)'),
                                dbc.ListGroupItem(frame.VWAP.mean().round(2), style={'fontSize':ticker_card_font_size, 'color':ticker_card_font_col}, color=card_bg_color)
                            ])
                        ], style={'textAlign':'center'})
                    ], width=4)
                ], id='graph-row', style={'columnCount':2})
            ])



            return row1, row2

# 3 MONTHS________________________________________________________________________________________________________________
        if '3month' in changed_id:
            end = datetime.date.today()
            diff = relativedelta(months=3)
            start = end - diff
            frame = nse.get_history(value, start, end)
            frame['SMA_10'] = frame['Close'].rolling(10,min_periods=1).mean()
            frame['SMA_20'] = frame['Close'].rolling(20, min_periods=1).mean()
            frame['SMA_50'] = frame['Close'].rolling(50, min_periods=1).mean()

            # Cards____________________
            card1 = dbc.Card([
                dbc.CardHeader('Ticker'),
                dbc.CardBody(value, style={'fontSize':ticker_card_font_size, 'color':ticker_card_font_col})
            ], id='ticker', style={'textAlign':'center','height':130}, color=card_bg_color)

            card2 = dbc.Card([
                dbc.CardHeader('Industry'),
                dbc.CardBody(zipped_ind.loc[zipped_ind[0]==value, 1], style={'fontSize':ind_card_font_size, 'color':ind_card_font_col})
            ], id='industry', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card3 = dbc.Card([
                dbc.CardHeader('3 Month High'),
                dbc.CardBody(frame['High'].max(), style={'fontSize':high_card_font_size, 'color':high_card_font_col})
            ], id='time-max', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card4 = dbc.Card([
                dbc.CardHeader('3 Month Low'),
                dbc.CardBody(frame['Low'].min(), style={'fontSize':low_card_font_size, 'color':low_card_font_col})
            ], id='time-min', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            row1 = dbc.Container([
                dbc.Row(children=[
                    dbc.Col([
                        card1,
                    ], width=3),
                    dbc.Col([
                        card2,
                    ], width=3),
                    dbc.Col([
                        card3,
                    ], width=3),
                    dbc.Col([
                        card4
                    ], width=3)
                ], id='card-row')])

            # Graph__________________________________________
            fig = go.Figure(data=[go.Candlestick(
                x=frame.index,
                open=frame.Open,
                high=frame.High,
                low=frame.Low,
                close=frame.Close,
                showlegend=False
            )])
            fig.update_xaxes(showgrid=False, linecolor=linecolor)
            fig.update_yaxes(showgrid=False, linecolor=linecolor)
            fig.update_layout({'plot_bgcolor': plot_bgcolor, 'paper_bgcolor': paper_bgcolor},
                              xaxis_rangeslider_visible=False, yaxis=dict(color=linecolor),
                              xaxis=dict(color=linecolor), legend_title_text='Select Moving Average',
                              legend=dict(title_font_family='Times New Roman', font=dict(size=12, color='white'), bordercolor='white', borderwidth=2))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_10'], name='10 SMA', line=dict(color='#a5f2f1'), visible='legendonly'))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_20'], name='20 SMA', line=dict(color='#f0ee8d'), visible='legendonly'))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_50'], name='50 SMA', line=dict(color='#f5a887'), visible='legendonly'))

            ending = datetime.date.today()
            difference = relativedelta(weeks=52)
            starting = ending - difference
            new = nse.get_history(value, starting, ending)

            row2 = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='chart', figure=fig),
                    ], width=8),
                    dbc.Col([
                        dbc.Card([
                            dbc.ListGroup([
                                dbc.ListGroupItem('52 Week High'),
                                dbc.ListGroupItem(new.High.max(), style={'fontSize': ticker_card_font_size,
                                                                         'color': high_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('52 Week Low'),
                                dbc.ListGroupItem(new.Low.min(), style={'fontSize': ticker_card_font_size,
                                                                        'color': low_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average Volume (3 Months)'),
                                dbc.ListGroupItem(frame.Volume.mean().round(2),
                                                  style={'fontSize': ticker_card_font_size,
                                                         'color': ind_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average VWAP (3 Months)'),
                                dbc.ListGroupItem(frame.VWAP.mean().round(2), style={'fontSize': ticker_card_font_size,
                                                                                     'color': ticker_card_font_col}, color=card_bg_color)
                            ])
                        ], style=dict(textAlign='center'))
                    ], width=4)
                ], id='graph-row', style={'columnCount':2})
            ])
            return row1, row2

# 6 MONTHS________________________________________________________________________________________________________________
        if '6month' in changed_id:
            end = datetime.date.today()
            diff = relativedelta(months=6)
            start = end - diff
            frame = nse.get_history(value, start, end)
            frame['SMA_10'] = frame.Close.rolling(10, min_periods=1).mean()
            frame['SMA_20'] = frame.Close.rolling(20, min_periods=1).mean()
            frame['SMA_50'] = frame.Close.rolling(50, min_periods=1).mean()
            frame['SMA_100'] = frame.Close.rolling(100, min_periods=1).mean()

            # Cards____________________
            card1 = dbc.Card([
                dbc.CardHeader('Ticker'),
                dbc.CardBody(value, style={'fontSize':ticker_card_font_size, 'color':ticker_card_font_col})
            ], id='ticker', style={'textAlign':'center','height':130}, color=card_bg_color)

            card2 = dbc.Card([
                dbc.CardHeader('Industry'),
                dbc.CardBody(zipped_ind.loc[zipped_ind[0]==value, 1], style={'fontSize':ind_card_font_size, 'color':ind_card_font_col})
            ], id='industry', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card3 = dbc.Card([
                dbc.CardHeader('6 Month High'),
                dbc.CardBody(frame['High'].max(), style={'fontSize':high_card_font_size, 'color':high_card_font_col})
            ], id='time-max', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card4 = dbc.Card([
                dbc.CardHeader('6 Month Low'),
                dbc.CardBody(frame['Low'].min(), style={'fontSize':low_card_font_size, 'color':low_card_font_col})
            ], id='time-min', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            row1 = dbc.Container([
                dbc.Row(children=[
                    dbc.Col([
                        card1,
                    ], width=3),
                    dbc.Col([
                        card2,
                    ], width=3),
                    dbc.Col([
                        card3,
                    ], width=3),
                    dbc.Col([
                        card4
                    ], width=3)
                ], id='card-row')])

            # Graph__________________________________________
            fig = go.Figure(data=[go.Candlestick(
                x=frame.index,
                open=frame.Open,
                high=frame.High,
                low=frame.Low,
                close=frame.Close,
                showlegend=False
            )])
            fig.update_xaxes(showgrid=False, linecolor=linecolor)
            fig.update_yaxes(showgrid=False, linecolor=linecolor)
            fig.update_layout({'plot_bgcolor': plot_bgcolor, 'paper_bgcolor': paper_bgcolor},
                              xaxis_rangeslider_visible=False, yaxis=dict(color=linecolor),
                              xaxis=dict(color=linecolor),legend_title_text='Select Moving Average',
                              legend=dict(title_font_family='Times New Roman', font=dict(size=12, color='white'), bordercolor='white', borderwidth=2))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_10'], name='10 SMA', line=dict(color='#a5f2f1'), visible='legendonly'))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_20'], name='20 SMA', line=dict(color='#f0ee8d'), visible='legendonly'))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_50'], name='50 SMA', line=dict(color='#f5a887'), visible='legendonly'))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_100'], name='100 SMA', line=dict(color='#78e874'), visible='legendonly'))

            ending = datetime.date.today()
            difference = relativedelta(weeks=52)
            starting = ending - difference
            new = nse.get_history(value, starting, ending)

            row2 = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='chart', figure=fig),
                    ], width=8),
                    dbc.Col([
                        dbc.Card([
                            dbc.ListGroup([
                                dbc.ListGroupItem('52 Week High'),
                                dbc.ListGroupItem(new.High.max(), style={'fontSize': ticker_card_font_size,
                                                                         'color': high_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('52 Week Low'),
                                dbc.ListGroupItem(new.Low.min(), style={'fontSize': ticker_card_font_size,
                                                                        'color': low_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average Volume (6 Months)'),
                                dbc.ListGroupItem(frame.Volume.mean().round(2),
                                                  style={'fontSize': ticker_card_font_size,
                                                         'color': ind_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average VWAP (6 Months)'),
                                dbc.ListGroupItem(frame.VWAP.mean().round(2), style={'fontSize': ticker_card_font_size,
                                                                                     'color': ticker_card_font_col}, color=card_bg_color)
                            ])
                        ], style={'textAlign':'center'})
                    ], width=4)
                ], id='graph-row', style={'columnCount':2})
            ])
            return row1, row2

# 1 YEAR________________________________________________________________________________________________________________
        if '1year' in changed_id:
            end = datetime.date.today()
            diff = relativedelta(years=1)
            start = end - diff
            frame = nse.get_history(value, start, end)
            frame['SMA_10'] = frame.Close.rolling(10, min_periods=1).mean()
            frame['SMA_20'] = frame.Close.rolling(20, min_periods=1).mean()
            frame['SMA_50'] = frame.Close.rolling(50, min_periods=1).mean()
            frame['SMA_100'] = frame.Close.rolling(100, min_periods=1).mean()

            # Cards____________________
            card1 = dbc.Card([
                dbc.CardHeader('Ticker'),
                dbc.CardBody(value, style={'fontSize':ticker_card_font_size, 'color':ticker_card_font_col})
            ], id='ticker', style={'textAlign':'center','height':130}, color=card_bg_color)

            card2 = dbc.Card([
                dbc.CardHeader('Industry'),
                dbc.CardBody(zipped_ind.loc[zipped_ind[0]==value, 1], style={'fontSize':ind_card_font_size, 'color':ind_card_font_col})
            ], id='industry', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card3 = dbc.Card([
                dbc.CardHeader('1 Year High'),
                dbc.CardBody(frame['High'].max(), style={'fontSize':high_card_font_size, 'color':high_card_font_col})
            ], id='time-max', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            card4 = dbc.Card([
                dbc.CardHeader('1 Year Low'),
                dbc.CardBody(frame['Low'].min(), style={'fontSize':low_card_font_size, 'color':low_card_font_col})
            ], id='time-min', style={'textAlign':'center', 'height':130}, color=card_bg_color)

            row1 = dbc.Container([
                dbc.Row(children=[
                    dbc.Col([
                        card1,
                    ], width=3),
                    dbc.Col([
                        card2,
                    ], width=3),
                    dbc.Col([
                        card3,
                    ], width=3),
                    dbc.Col([
                        card4
                    ], width=3)
                ], id='card-row')])

            # Graph__________________________________________
            fig = go.Figure(data=[go.Candlestick(
                x=frame.index,
                open=frame.Open,
                high=frame.High,
                low=frame.Low,
                close=frame.Close,
                showlegend=False
            )])
            fig.update_xaxes(showgrid=False, linecolor=linecolor)
            fig.update_yaxes(showgrid=False, linecolor=linecolor)
            fig.update_layout({'plot_bgcolor': plot_bgcolor, 'paper_bgcolor': paper_bgcolor},
                              xaxis_rangeslider_visible=False, yaxis=dict(color=linecolor),
                              xaxis=dict(color=linecolor), legend_title_text='Select Moving Average',
                              legend=dict(title_font_family='Times New Roman', font=dict(size=12, color='white'), bordercolor='white', borderwidth=2))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_10'], name='10 SMA', line=dict(color='#a5f2f1'), visible='legendonly'))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_20'], name='20 SMA', line=dict(color='#f0ee8d'), visible='legendonly'))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_50'], name='50 SMA', line=dict(color='#f5a887'), visible='legendonly'))
            fig.add_trace(go.Scatter(x=frame.index, y=frame['SMA_100'], name='100 SMA', line=dict(color='#78e874'), visible='legendonly'))

            ending = datetime.date.today()
            difference = relativedelta(weeks=52)
            starting = ending - difference
            new = nse.get_history(value, starting, ending)

            row2 = dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='chart', figure=fig),
                    ], width=8),
                    dbc.Col([
                        dbc.Card([
                            dbc.ListGroup([
                                dbc.ListGroupItem('52 Week High'),
                                dbc.ListGroupItem(new.High.max(), style={'fontSize': ticker_card_font_size,
                                                                         'color': high_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('52 Week Low'),
                                dbc.ListGroupItem(new.Low.min(), style={'fontSize': ticker_card_font_size,
                                                                        'color': low_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average Volume (1 Year)'),
                                dbc.ListGroupItem(frame.Volume.mean().round(2),
                                                  style={'fontSize': ticker_card_font_size,
                                                         'color': ind_card_font_col}, color=card_bg_color),
                                dbc.ListGroupItem('Average VWAP (1 Year)'),
                                dbc.ListGroupItem(frame.VWAP.mean().round(2), style={'fontSize': ticker_card_font_size,
                                                                                     'color': ticker_card_font_col}, color=card_bg_color)
                            ])
                        ], style={'textAlign':'center'})
                    ], width=4)
                ], id='graph-row', style={'columnCount':2})
            ])
            return row1, row2





if __name__ == '__main__':
    app.run_server(debug=False, port=8000)