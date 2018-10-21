import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import dash
import time
import sys
sys.path.append("F://work projects/Dash Application")
from app import app
from Cloud_API.datastore import Datastore

#import necessary libraries to do plot
import plotly.plotly as py 
import plotly.figure_factory as ff 
import pandas as pd
import json

datastore = Datastore() #create an object for the datastore

def distinct_snapshot_id():
    #distinct id
    ids = datastore.get_distinct_id()
    # ids will be return as list
    X = []
    #iterate
    for i in ids:
        X.append({'label':str(i), 'value':i})

    return X

def get_default_value(dict_values):
    #[Start getting distinct values]
    ids = []
    for i in dict_values:
        ids.append(list(i.values())[0])

    frequent = len(ids) - 1 #get the frequent one
    return ids[frequent]


#[Start getting the distinct Snapshot Id here]
get_distinct_snapshot_id = distinct_snapshot_id()
default_value = get_default_value(get_distinct_snapshot_id)

#[end]

"""App Layout Starts Here!!!!!"""

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
                            className='nav-wrapper',
                        ),style={'background-color':'#008EFE'}),

                ],
                className='navbar-fixed'
            )

    ]),

    #retrieving the data entities from the Google Cloud Datastore and view them as tables\
    #get filter by snapshot date methods
    html.Div(className='row', children=[
        #filter option is set here
        html.Div(className='col s12 m2 l2'),
        html.Div(html.P("SELECT THE SNAPSHOT DATE:"),className='col s12 m2 l2'),
        html.Div(
            [
            dcc.Dropdown(id='snapshot-date-list',
            options=get_distinct_snapshot_id,
        value=default_value)
        ],className='col s12 m6 l6',style={'margin-top':10, 'color':'black'}),
        html.Div(className='col s12 m2 l2')
    ]),

    #to leave a break
    html.Div(className='row',children=[
        html.Div(className='col s12 m4 l4'),
        html.Div(html.Center(html.B("ALL DETAILS ARE SHOWN HERE")), className='col s12 m4 l4'),
        html.Div(className='col s12 m4 l4')]),

    #leave a break line here
    html.Div(className='row', children=[
        html.Div(className='col s12 m2 l2'),
        html.Div(style={'border':'1px solid black'},className='col s12 m8 l8'),
        html.Div(className='col s12 m2 l2')
    ]),

    #hidden div to store the intermediate value
    html.Div(className='row', children=[html.Div(className='col s12 m12 l12', id='intermediate-value')], style={'display':'none'}),

    #output container where table and Graph Will be Shown
    html.Div(className='row', children=[
        #table of the Data Object
        html.Div(className='col s12 m1 l1'),
        html.Div(className='col s12 m4 l4', id='table-container', style={'display':'2px solid black'}),
        html.Div(className='col s12 m1 l1', id='info-log'),
        html.Div(children=[
            html.Div(className='row', children=[
                html.Div(html.P('DISTRIBUTION: '),className='col s12 m3 l3', style={'font-size':15}),
                #dropdown box is built here
                html.Div(
                    [
                        dcc.Dropdown(id='get-attribute-value',
                        options=[
                            {'label':'Frequency', 'value':'Frequency'},
                            {'label':'Monetary', 'value':'Monetarty'},
                            {'label':'Recency', 'value':'Recency'}
                        ],
                        value='Recency')
                    ], className='col s12 m6 l6', style={'margin-top':5}
                )
            ]),
            #this where output Graph Component Should be Shown
            html.Div(className='col s12 m12 l12', id='Distribution-Graph-Component')

        ],className='col s12 m5 l5', id='distribution-Graph')
    ]),


], className='col s12 m12 l12')

#write a app callback function here
@app.callback(
    Output('intermediate-value', 'children'),
    [Input('snapshot-date-list', 'value')]
)

def caching_all_variables_in_session(value):
    #[Start Queryinhg the value from the datastore]
    uid, recency, monetary, frequency = datastore.property_filter('snapshot_Id', value)

    #create a lookup table
    lookup_table = {
      'Unique_Id': uid,
      'Recency': recency,
      'Monetarty': monetary,
      'Frequency': frequency
    }

    return json.dumps(lookup_table)
    #[End]


@app.callback(
    Output('table-container',  'children'),
    [Input('intermediate-value', 'children')]
)

def project_value_from_snapshot_id(jsonified_cleaned_data):

    datasets = json.loads(jsonified_cleaned_data)
    df = pd.DataFrame({'Unique_Id': datasets['Unique_Id'], 'Recency': datasets['Recency'],
        'Monetary': datasets['Monetarty'], 'Frequency': datasets['Frequency']})

    print('*' * 100)
    print("Json Data is Read and Stored as DataFrame")
    print("*" * 100)

    rows = []
    for i in range(len(df)):
        row = []

        for cols in df.columns:
            value = df.iloc[i][cols]
            #columns you want to show the link
            if cols == 'Unique_Id':
                cell = html.Td(html.A(value, href='/apps/cs_id/unique_id={}'.format(value)))
            else:
                cell = html.Td(children=value)

            row.append(cell) #append to the row

        rows.append(html.Tr(row))

    #return the Table
    table = html.Table(className='responsive-table', style={'background-color':'#F7F7F7',
        'border-bottom':'white'},
        children=[
            html.Tr([html.Th(col) for col in df.columns], style={'background-color':'#4285F4', 'color':'white'})
        ] + rows)

    return table

@app.callback(
    Output('Distribution-Graph-Component', 'children'),
    [Input('intermediate-value', 'children'), Input('get-attribute-value', 'value')]
)


def show_the_distribution(jsonified_cleaned_data, filter_option):
    #[START loading the jsonified dump data]
    json_data = json.loads(jsonified_cleaned_data)
    filter_attr = filter_option

    data_to_plot = None

    for k,v in json_data.items():

        if filter_attr == k:
            data_to_plot = json_data[k]


    fig = ff.create_distplot([data_to_plot], ['Dist-Plot'])

    graph = dcc.Graph(
         id= 'Distribution-plot',
        figure= fig
    )

    return graph


@app.callback(
    Output('storing-user-id', 'children'),
    [Input('persons_id', 'value')]
)

def cache_user_id(value):

    return value

"""External CSS and JS function call is done here"""

#define the external urls
external_css = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css', 
'https://codepen.io/chriddyp/pen/brPBPO.css']


for css in external_css:
    app.css.append_css({'external_url': css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']

for js in external_js:
  app.scripts.append_script({'external_url': js})
