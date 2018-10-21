"""
	Author: Madhivarman
	contact: madhi@pluto7.com
	File Description: Analytics of Customer
	Project: Customer Segmentation Dash board
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import dash
import time
import json
import sys
sys.path.append("F://work projects/Dash Application")
from app import app
from Cloud_API.datastore import Datastore

#import necessary libraries to do plot
import pandas as pd
import plotly.plotly as py 
import plotly.figure_factory as ff 
import plotly.graph_objs as go

layout = html.Div(id='main-page-content',children=[
    html.Div(className='container-fluid', children=[
            #nav wrapper starts here
            html.Div(
                children=[
                    #nav bar
                    html.Nav(
                        #inside div
                        html.Div(
                            children=[
                                html.A(
                                    'Dashboard Analytics',
                                    className='brand-logo',
                                    href='/'
                                ),
                                #ul list components
                                html.Ul(
                                    children=[
                                       html.Li(html.A('Configuration', href='/apps/config')),
                                       html.Li(html.A('Segmentation', href='/apps/segmentation')),
                                       html.Li(html.A('Main Page', href='/apps/users')), 
                                    ],
                                    id='nav-mobile',
                                    className='right hide-on-med-and-down'
                                ), 
                            ],
                            className='nav-wrapper'
                        ),style={'background-color':'#008EFE'}),

                ],
                className='navbar-fixed'
            )

    ]),

    #the main container
    html.Div(className='row', children=[
        #the empty  div
        html.Div(className='col s12 m2 l2'),
        #the main div where the graph comes
        html.Div(className='col s12 m8 l8', children=[
            #cards here
            html.Div(id='graph-components',className='card-panel white col s12 m12 l12', children=[
                #title comes here
                html.Div(className='row', children=[
                    html.Div(className='col s12 m2 l2'),
                    html.Div(className='col s12 m8 l8', children=[
                         html.Center(children=[
                            html.Span(html.B('ANALYTICS FOR USER ID:'), style={'font-size':20}),
                            html.Span(id='unique_id', style={'padding':10,'font-size': 20})
                         ])
                    ]),
                    html.Div(className='col s12 m2 l2')
                ]),

                #this is the hidden div where all graphs components are stored here
                html.Div(className='row', children=[  
                    html.Div(className='col s12 m12 l12', id='all-graph-distributions', style={'margin-top': 30})
                ])
            ])
        ]),
        #the empty div
        html.Div(className='col s12 m2 l2')
    ])
], className='col s12 m12 l12')

#call back function to get the user id
@app.callback(
    Output('unique_id', 'children'),
    [Input('user-id', 'children')]
)

def get_user_id(unique_id):

    return "{}".format(unique_id)

#call back function to get all information about user id's
@app.callback(
    Output('all-graph-distributions', 'children'),
    [Input('user-id', 'children')]
)

def get_relevant_information(unique_id):
    #create an object for the datastore
    datastore = Datastore()
    #[START fetching the data from the datastore]
    #here we need to do batch lookups, so first get the snapshot ids
    snapshot_ids = datastore.get_distinct_id()
    info = datastore.batch_lookup(unique_id, snapshot_ids) #return as lists

    r, m, f = [], [], []
    #info datatype lists
    for all_info in info:
        r.append(all_info['Recency'])
        m.append(all_info['Monetarty'])
        f.append(all_info['Frequency'])

    #now create a dictionary
    all_info_as_dict = {
        'Snapshot': snapshot_ids,
        'Recency': r,
        'Monetary': m,
        'Frequency': f
    }

    if len(all_info_as_dict['Snapshot']) == len(all_info_as_dict['Recency']):

        #recency graph
        recency_graph = go.Scatter(
            x= all_info_as_dict['Snapshot'],
            y= all_info_as_dict['Recency'],
            name='Recency-Graph',
            fill = 'tozeroy'
        )

        #monetary graph
        monetary_graph = go.Scatter(
            x= all_info_as_dict['Snapshot'],
            y= all_info_as_dict['Monetary'],
            name= 'Monetary',
            fill = 'tonexty'
        )

        #frequency graph
        frequency_graph = go.Scatter(
            x= all_info_as_dict['Snapshot'],
            y= all_info_as_dict['Frequency'],
            name= 'Frequency-Graph',
            fill = 'tozeroy'
        )

        data = [recency_graph, monetary_graph, frequency_graph]

        fig = py.iplot(data, filename= 'basic-area', file_id='overall-analytics')

        return  dcc.Graph(
            id = 'example',
            figure = fig
        )


    else:

        #get the difference
        diff = len(all_info_as_dict['Snapshot']) - len(all_info_as_dict['Recency'])

        for i in range(diff):
            all_info_as_dict['Recency'].append(0)
            all_info_as_dict['Monetary'].append(0)
            all_info_as_dict['Frequency'].append(0)

        #recency graph
        recency_graph = go.Scatter(
            x= all_info_as_dict['Snapshot'],
            y= all_info_as_dict['Recency'],
            name='Recency Graph',
            fill = 'tozeroy'
        )

        #monetary graph
        monetary_graph = go.Scatter(
            x= all_info_as_dict['Snapshot'],
            y= all_info_as_dict['Monetary'],
            name='Monetary Graph',
            fill = 'tonexty'
        )

        #frequency graph
        frequency_graph = go.Scatter(
            x= all_info_as_dict['Snapshot'],
            y= all_info_as_dict['Frequency'],
            name='Frequency Graph',
            fill = 'tozeroy'
        )

        data = [recency_graph, monetary_graph, frequency_graph]

        return dcc.Graph(
            figure = {'data': data},
            id='analytics'
        )


