import os, shutil
from datetime import datetime

#flask imports...
from flask import Flask, redirect

#dash imports...
from dash import Dash
from dash.dependencies import Input, Output, State

#plotly imports...
import plotly.graph_objs as go

#get layouts
from layouts.layouts import layout4 as homePage

#get models
from models.controller import getData

#configurations...
server = Flask(__name__)
dash_app = Dash(__name__, server = server, url_base_pathname='/home/' )
dash_app.scripts.config.serve_locally = True #enables you to run without internet
dash_app.config['suppress_callback_exceptions']=True #errors for objects resolved at runtime
dash_app.title = 'Home'

#assign layout
dash_app.layout = homePage

# watchdog required method...
# checks the time a file was modified to see if we should
# trigger an update. Its not required if you are not 
# saving data to a file after scraping and wat wat.
def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)

#handle root url...
@server.route('/')
def dashboard():
    return redirect('/home')


# ------------------> events callback handlers <-------------------------------

#handle watchdog or live updating...
@dash_app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    
    try:
        file = open('data\\watchdog', 'r')
        oldt = file.readline()
        file.close()

    except Exception as e:
        print("Error in watchdog: "+ str(e))
        oldt = ''
    
    d = modification_date('data\\new_data.csv')
    # print('oldt = '+str(oldt)+' and new = '+str(d))
    if str(oldt) != str(d):
        file = open('data\\watchdog', 'w')
        file.write(str(d))
        file.close()
        global trigger_update
        trigger_update = True
        return 'True'
    else:
        trigger_update = False
        return 'False'

#load data into system
@dash_app.callback(Output('storageDiv', 'children'),
                    [Input('body_home', 'children')])
def load_data(children, ):
    df = getData()
    if df.empty != True:
        global isDataAvailable
        isDataAvailable = True
        return df.to_json(date_format='iso', orient='split')

    else:
        return ''
    
#update dashboard chart-1...
@dash_app.callback(Output('dbdGraph1', 'figure'),
                    [Input('storageDiv', 'children'), Input('dummyInput', 'value'), Input('live-update-text', 'children')])
def update_outcomesGraph(data1, dummy, upda):
    df = getData()
        
    data = df[df['year'] == 2015 ]
    traces = []
    traces.append(
        go.Bar(
            x = data.c_new_tsr,
            y = data.country,
            orientation = 'h'
        )
    )

    return {
                'data': traces,
                'layout': go.Layout(
                    yaxis={
                        'zeroline': False,
                        'ticks': 'outside'
                        },
                    xaxis={
                        'title': 'Rate(%)',
                        'titlefont': dict(size=18, color='wheat'),
                        'ticks': 'outside'
                        },
                    margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
                    legend={'x': 1, 'y': 1},
                    hovermode='closest',
                    paper_bgcolor='#27293d',
                    plot_bgcolor='#27293d',
                    font={'color':'#e14eca'},
                    title='Treatment Success (2015)'
                )
            }

#update dashboard main graph...
@dash_app.callback(Output('dbdGraphMain', 'figure'),
                    [Input('storageDiv', 'children'), Input('dummyInput', 'value'), Input('live-update-text', 'children')])
def update_Main_dbd(data1, loaded, updated):
    data = getData()

    yvalues = []
    xvalues = data['year'].unique()
    for year in xvalues:
        y = data[data.year == year]
        yv = y.c_newinc.sum()
        yvalues.append(yv)

    figu = {
        'data': [
            go.Scatter(
                x=xvalues,
                y=yvalues,
                opacity=0.5,
                line = {
                    'width': 5,
                    'shape': 'spline'
                }
                )
            ],

        'layout': go.Layout(
            xaxis={
                'title': 'Year',
                'titlefont': dict(size=18, color='wheat'),
                'zeroline': False,
                'ticks': 'outside'
                },
            yaxis={
                'title': 'New Reported Cases',
                'titlefont': dict(size=18, color='wheat'),
                'ticks': 'outside'
                },
            margin={'l': 60, 'b': 60, 't': 30, 'r': 20},
            legend={'x': 1, 'y': 1},
            hovermode='closest',
            plot_bgcolor= '#27293d',
            paper_bgcolor='#27293d',
            font={'color':'#e14eca'},
            title='Reported Cases Statistics'
        )
    }

    return figu

#update dashboard chart-2...
@dash_app.callback(Output('dbdGraph2', 'figure'),
                    [Input('storageDiv', 'children'), Input('dummyInput', 'value'), Input('live-update-text', 'children')])
def update_deathsGraph(data1, loaded, updated):
    df = getData()
    dff = df[df['year'] == 2015]

    #calculate variables..
    hiv = dff['tbhiv_died'].sum()
    mdr = dff['mdr_died'].sum()
    xdr = dff['xdr_died'].sum()

    figur={
        'data':[
            {
                'x':['HIV+', 'MDR-TB', 'XDR-TB'],
                'y':[hiv, mdr, xdr],
                'type':'bar',
                'marker':{
                    'color':'#e14eca',
                    'line': {
                        'color':'rgb(158,202,225)',
                        'width':1.5
                        }
                },
                'opacity':0.6
            }
        ],
        'layout': {
            'plot_bgcolor': '#27293d',
            'paper_bgcolor': '#27293d',
            'yaxis': {
                'title': 'Number of Deaths (2015)',
                'titlefont': dict(size=18, color='wheat'),
                'ticks': 'outside'
            },
            'xaxis': {
                'title': 'Total Number of Deaths = ' + str(hiv+mdr+xdr),
                'titlefont': dict(size=14, color='lime')
            },
            'font':{
                'color': '#e14eca'
            },
            'title': 'Overview of Deaths Cases'
        }
    }

    return figur


# -------------------------> Start app <--------------------------------------------------------

#run the application
if __name__ == "__main__":
    dash_app.run_server(debug=True)