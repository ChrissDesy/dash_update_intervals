import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# these are the html elements used on the dashboard.
# its not hard to create. am guessing you are already
# using same technique for rendering your dashboard

#home layout
layout4 = html.Div([
    html.Div([
        #dummy input to trigger chart load..
        dcc.Dropdown(
                id='dummyInput',
                value='chris',
                style={
                    'display': 'none'
                }
            ),
        
        #interval for auto update...
        dcc.Interval(
            id='interval-component',
            interval=1*30000, # in milliseconds
            n_intervals=0
        ),

        html.Div([
            html.Div(
                id='live-update-text',
                style={'display': 'none'}
                ),

            #first Graph...
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Loading(
                            id='loading-main',
                            children=[
                                html.Div([
                                    html.Div([
                                        dcc.Graph(
                                            id='dbdGraphMain',
                                            animate=True
                                        )
                                    ],
                                    className='chart-area')
                                ],
                                className='card-body')
                            ],
                            type='circle',
                            fullscreen=False
                        )
                    ],
                    className='card card-chart')
                ],
                className='col-12')
            ],
            className='row'
            ),

            #second row graphs...
            html.Div([
                #chart 1
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Loading(
                                id='loading-1',
                                children=[
                                    html.Div([
                                        dcc.Graph(
                                            id='dbdGraph1'
                                        )
                                    ],
                                    className='chart-area')
                                ],
                                type='circle',
                                fullscreen=False
                            )
                        ],
                        className='card-body')
                    ],
                    className='card card-chart')
                ],
                className='col-lg-6'
                ),
                #chart 2
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Loading(
                                id='loading-2',
                                children=[
                                    html.Div([
                                        dcc.Graph(
                                            id='dbdGraph2'
                                        )
                                    ],
                                    className='chart-area')
                                ],
                                type='circle',
                                fullscreen=False
                            )
                        ],
                        className='card-body')
                    ],
                    className='card card-chart')
                ],
                className='col-lg-6'
                )
            ],
            className='row')
        ],
        className='content'),

        # Hidden div inside the app that stores the dataset values...
        html.Div(id='storageDiv', style={'display': 'none'})
    ],
    className='main-panel')
],
id = 'body_home',
className='wrapper ')