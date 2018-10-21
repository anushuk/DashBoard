import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import sys
import os
import json
sys.path.append("F:/work projects/Dash Application")

from app import app
from Cloud_API.datastore import Datastore
from ml_part.cluster_analysis import ClusterAnalysis

import plotly.plotly as py 
import plotly.graph_objs as go
import math

datastore = Datastore()

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
snap_ids = distinct_snapshot_id()
default_value = get_default_value(snap_ids)



layout = html.Div(id="main-page-content",children=[
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
            ),


        #this is the main div where all the json dumps data will  be displayed as a visualization graph
        html.Div(
            className= 'row',
            children=[
                #html div to display the summary statistics
                html.Div(
                    id='summary-statistics',
                    className='col s12 m12 l12',
                    children=[

                        #div container to leave the space
                        html.Div(className='col s12 m1 l1'),

                        html.Div(
                            className='card-panel white col s12 m10 l10',
                            children=[
                                #heading goes here
                                html.Div(children=[
                                    html.Div(
                                        children=[
                                            html.Span("SUMMARY ANALYTICS",
                                            style={
                                                'color':'black',
                                                'padding': '35%',
                                                'font-weight': 'bold'
                                            })
                                        ]
                                    )
                                    ],
                                    className='col s12 m12 l12'
                                ),
                                #Div element where the pie chart comes
                                html.Div(className='row', children=[
                                    html.Div(className='col s12 m6 l6',
                                        id='pie-chart-analysis',
                                        style={
                                            'margin-top': 25
                                        }
                                    ),
                                    html.Div(className='col s12 m1 l1'),
                                    #div to display the status
                                    html.Div(className='col s12 m5 l5', id='datastore-table-info'),
                                ]),


                                #div container to leave the space
                                html.Div(className='col s12 m1 l1'),

                                #hidden div
                                html.Div(className='col s12 m12 l12', children=[
                                    dcc.Dropdown(id='dropdown', value='default')
                                ], style={'display':'none'}),
                            ]
                        )
                    ]
                ),

            ]
        ),

        #div container where all the Cluster Analysis Graph comes
        html.Div(
            className='row',children=[
                #leave one container
                html.Div(className='col s12 m1 l1'),

                #this is the div where all the graph comes
                html.Div(className='card-panel white col s12 m10 l10', children=[
                    #heading for card panel
                    html.Div(children=[
                        html.Span("CLUSTER ANALYSIS",
                            style={
                                'color':'black',
                                'padding': '37%',
                                'font-weight':'bold'
                            })
                    ], className='col s12 m12 l12'),

                    #leave the break
                    html.Br(),

                    #place the dropdown button here to get the snapshot id
                    html.Div(children=[
                        #leave
                        html.Div(className='col s12 m1 l1'),
                        #dropdown
                        html.Div(children=[
                            #leave
                            html.Div(className='col s12 m2 l2'),
                            #label comes in this div
                            html.Div(className='col s12 m3 l3', children=[
                                html.Span('SNAPSHOT ID:', style={
                                    'color':'black',
                                    'margin-top':25,
                                    'float':'right'
                                })
                            ]),
                            #dropdown comes here
                            html.Div(className='col s12 m5 l5', children=[
                                dcc.Dropdown(
                                    id='snapshot-ids',
                                    options=snap_ids,
                                    value=default_value
                                )
                            ], style={'margin-top':20}),
                            #leave
                            html.Div(className='col s12 m2 l2')

                        ],className='col s12 m10 l10'),
                        #leave
                        html.Div(className= 'col s12 m1 l1')
                    ],className='col s12 m12 l12'),

                    #hidden div where the particular Cluster Analysis data is stored
                    html.Div(id='selected_snapshot_id_cluster_analysis_data', 
                        className='col s12 m12 l12',
                        style={
                         'display':'none'
                    }),

                    #total count
                    html.Div(children=[
                        html.Div(className='col s12 m4 l4', id='recency-total-bar-graph'),
                        html.Div(className='col s12 m4 l4', id='monetary-total-bar-graph'),
                        html.Div(className='col s12 m4 l4', id='frequency-total-bar-graph')
                    ],className='col s12 m12 l12'),


                    html.Br(),

                    #all graphs comes here
                    html.Div(children=[
                        #div bar 
                        html.Div(className='col s12 m4 l4', id='recency-bar-graph'),
                        html.Div(className='col s12 m4 l4', id='monetary-bar-graph'),
                        html.Div(className='col s12 m4 l4', id='frequency-bar-graph')

                    ],className='col s12 m12 l12'),

                ]),

                #leave one container
                html.Div(className='col s12 m1 l1'),
            ]
        ),

        #hidden div
        html.Div(className='col s12 m12 l12', id='intermediate-data', style={'display':'none'})

    ])

],className='col s12 l12 m12')

#CUSTOM FUNCTION
def get_properties_of_kind():
    #[START getting the properties of kind]
    summary_statistics = datastore.get_summary_statistics()
    return summary_statistics
    #[END]


#CUSTOM FUNCTION TO FIND THE MIN AND MAX FUNCTION
#custom function to find the min max function
def find_min_max(recency, monetary, frequency):
    """
        Args:
            Each object has:
                centroids, classes, X
            centroids(dictionary): {"Cluster ID": Data Points}

        Return: 
            Data Type (Dictionary): {"Key":{"cluster ID": [min, max]}}
    """
    def min_max(data_dict):
        ids, value = [], []
        for key, values in data_dict.items():
            ids.append(key)
            value.append([min(values), max(values)])

        return {'Cluster ID': ids, 'Min_Max_Values': value}


    def calculate_total_features(data_dict):
        ids, t_len = [], []
        for key, value in data_dict.items():
            ids.append(key)
            t_len.append(len(value))
        return {'Cluster_ID': ids, 'Total_Length': t_len}


    r_centroids_and_features = min_max(recency.classes) #return as dictionaries
    m_centroids_and_features = min_max(monetary.classes)
    f_centroids_and_features = min_max(frequency.classes)

    #calculating total features in the clusters
    r_total_features = calculate_total_features(recency.classes)
    m_total_features = calculate_total_features(monetary.classes)
    f_total_features = calculate_total_features(frequency.classes)

    print(r_centroids_and_features)
    print(m_centroids_and_features)
    print(f_centroids_and_features)

    return {'recency': [r_centroids_and_features, r_total_features],
            'monetary': [m_centroids_and_features, m_total_features],
            'frequency': [f_centroids_and_features, f_total_features]}


#this function is the important function
#do not mess this function, it will create catastrophic!
def cluster_analysis_overall():
    """
        ToDo:
            1. Get all the SnapshotId
            2. Do Cluster Analysis in the data
            3. return as json dumps
    """
    overall_data = [] #list to store overall information
    snapshots_ids = datastore.get_distinct_id() #return as lists
    #START Iterating the snapshot ids
    for i in snapshots_ids:
        print('$' * 100)
        print('Getting Entites from the DataStore: Snapshot_ID:{}'.format(i))

        #get all the entites from the datastore that matches the snapshot
        uid, r, m, f = datastore.property_filter('snapshot_Id', i)
        print("Data has been Received and Cached!!!!!!")
        print('*' * 50)
        print("Started Cluster Analysis for the Data")
        print('*' * 50)

        #create an obj and after caching all data's delete an obj and its values
        recency = ClusterAnalysis(3, 500, 'Recency_Cluster_Analysis', 0.0001, r)
        recency.fit() #return as dictionary

        monetary = ClusterAnalysis(3, 500, 'Monetary_Cluster_Analysis', 0.0001, m)
        monetary.fit() #return as dictionary

        frequency = ClusterAnalysis(3, 500, 'Frequency_Cluster_Analysis', 0.0001, f)
        frequency.fit() #return as dictionary

        print("-" * 100)
        print("Now Analysis Min and Max for the Features")
        print("*" * 50)

        min_max = find_min_max(recency, monetary, frequency) #return as json dump
        print("Finished Calculating Min-Max")

        #append to the list
        overall_data.append({i:min_max})
        print('$' * 100)

        #delete an object now to avoid conflicts
        del recency
        del monetary
        del frequency

    #now return the lists
    return overall_data

    #[END]


@app.callback(
    Output('intermediate-data', 'children'),
    [Input('dropdown', 'value')]
)


def get_statistical_metadata(value):

    """
        Summary Statistics  we going to calculate:
            1. How many snapshots are there?
                    1.1 Their total data entities(length)
                    1.2 Calculate average from that total and create a pie chart

            2. __Stat_Total that represents the statistics.
                    2.1 Counts, bytes, timestamp (Recently Updated)

            3. Show the Distribution of the clusters by Filter wise Operation.
                    3.1 For Particular Snapshot Data what is the distribution of cluster Segments
                    3.2 Each Cluster Minimum and Maximum value

            4. Create Bar Graph month wise Operation Bar chart

            5. 3D clustering visualization

    """

    get_all_distinct_snapshots = datastore.get_distinct_id() #to get all distinct snapshot ids (dataType: List)
    #to get total length of snapshot ids
    total_snapshots_in_datastore = len(get_all_distinct_snapshots)

    individual_snapshot_ids = [] #to store the length of individual snapshot ids
    snapshot_id_name, total_data_per_snapshot = [],[]

    for indi_lists in get_all_distinct_snapshots:
        snapshot_id_name.append(indi_lists) #to get all snapshot names
        uid, r, m, f = datastore.property_filter('snapshot_Id', indi_lists)
        total_data_per_snapshot.append(len(uid)) #to get total entity per snapshot
        individual_snapshot_ids.append([indi_lists,len(uid)]) #get length of the values

    total_entity = datastore.get_total_entries() #total number of data in the list

    """
        Args:
            individual_snapshot_ids (dict) : Key -> SnapshotId, Value -> Total Length
            Total_entity(integer): we will get total number of entries from the datastore
    """
    #now create a list to add in json data
    overall_details = {
        'Snapshot_Ids': snapshot_id_name,
        'Count': total_snapshots_in_datastore,
        'Data Count': total_data_per_snapshot
    }

    #[START Calculating Percentage Info]
    #now calculate the percentage
    #iterate through the individual_snapshot_ids dictionary
    pie_chart_percentage_info = []

    for info in individual_snapshot_ids:
        #append to the lists
        pie_chart_percentage_info.append(
            {
                info[0]: (info[1] / total_entity) * 100
            }
        )

    summary_dump = {} #dictionary to store all information
    summary_dump['Percentage_info'] = pie_chart_percentage_info #append to the dictionary

    #[END Calculated Percentage Info]

    #[START doing the Cluster Analysis Part]
    cluster_analysis_data = cluster_analysis_overall()
    summary_dump['ClusterAnalysis'] = cluster_analysis_data
    #[END]

    summary_dump['Overall_Info'] = overall_details

    return json.dumps(summary_dump)


def generate_linechart(ids, percentage):
    #do the fig
    distribution = percentage
    labels = ids

    #create and style traces
    trace = go.Scatter(
        x = labels,
        y = distribution,
        name = 'Distribution Per snapshot Ids',
        line = dict(
            color = ('rgb(22, 96, 167)'),
            width = 2
        )
    )

    data = [trace]

    #edit the layout
    layout = dict(title= "Data Distribution over Snapshot Id's",
        xaxis= dict(title= 'Snapshot Ids'),
        yaxis = dict(title= 'Distribution Percentage')
    )

    fig = dict(data = data, layout = layout)

    return fig

@app.callback(
    Output('pie-chart-analysis', 'children'),
    [Input('intermediate-data', 'children')])

def update_graph_1(jsonified_clean_data):
    dataset = json.loads(jsonified_clean_data)
    #get percentage info
    percentage_info = dataset['Percentage_info'] #return as lists
    
    #iterate through the percentage_info
    ids, percentage = [], []
    for i in percentage_info:
        for k,v in i.items():
            ids.append(k)
            percentage.append(math.floor(v))

    fig = generate_linechart(ids, percentage)

    return dcc.Graph(
        figure = fig,
        id='pie-chart'
    )


@app.callback(
    Output('datastore-table-info', 'children'),
    [Input('intermediate-data', 'children')]
)


def generate_table_info(jsonified_data):
    #load the data
    dataset = json.loads(jsonified_data) 
    total_details_want = dataset['Overall_Info']

    keys, values = list(total_details_want.keys()), list(total_details_want.values())
    val = []

    for i in values:
        if str(type(i)) == "<class 'int'>":
            val.append(i)
        else:
            val.append(",".join([str(X) for X in i]))

    columns = ['Resource', 'Count']

    return html.Table(className='responsive-table',
        children=[
            #get head of the table
            html.Thead(
                html.Tr(
                    children=[html.Th(title) for title in columns]
                )
            ),
            #body of the table
            html.Tbody(
                children=[
                html.Tr(
                    children=[
                        html.Td(keys[0]),
                        html.Td(
                            val[0]
                        )
                    ]
                ),
                html.Tr(
                    children=[
                        html.Td(keys[1]),
                        html.Td(
                            val[1]
                        )
                    ]
                ),
                html.Tr(
                    children=[
                        html.Td(keys[2]),
                        html.Td(
                            val[2]
                        ) 
                    ]
                )],
            )
        ],
        style={
            'margin-bottom':'1px solid grey',
            'background-color': 'white',
            'border-bottom':'1px solid grey'
        }
    )


#app callback for recency
@app.callback(
    Output('selected_snapshot_id_cluster_analysis_data', 'children'),
    [Input('intermediate-data', 'children'), Input('snapshot-ids', 'value')]
)

def update_recency_bar_graph(jsonified_data, snapshot_value):
    #get the jsonified data and load
    dataset = json.loads(jsonified_data)
    selected_snapshot_id = snapshot_value

    #get the specific part of the json data
    data_for_graph = dataset['ClusterAnalysis']

    #iterate through the data_for_graph to get keys
    key_list = [(ind,list(i.keys())[0]) for ind, i in enumerate(data_for_graph)]

    #iterate through key list to get the index
    index_to_fetch_data = None 

    for key in key_list:
        #condition to fetch the data
        if selected_snapshot_id == key[1]:
            index_to_fetch_data = key[0]

    real_data  = data_for_graph[index_to_fetch_data]

    return json.dumps(real_data)


#CUSTOM FUNCTION
def get_stack_graph(X, min_val, max_val,name):
    #trace_1
    trace_1 = go.Bar(
        x = X,
        y = min_val,
        name= 'Min Value'
    )

    #trace_2 
    trace_2 = go.Bar(
        x = X,
        y = max_val,
        name= 'Max Value'
    )

    data = [trace_1, trace_2]

    title = "Min-Max value Graph({})".format(name)

    layout = go.Layout(title=title,
        barmode= 'stack', 
        xaxis=dict(title='Segment'), 
        yaxis=dict(title='Count'))

    fig = go.Figure(data = data, layout= layout)

    return fig


def get_bar_graph(X, Y, name):
    Y = Y[0]
    print(X, Y)
    
    trace = go.Bar(
        x = X,
        y = Y,
        marker=dict(
            color='rgb(158,202, 225)',
            line=dict(
                color='rgb(8,48, 107)',
                width=1.5
            )
        ),
        opacity=0.6
    )

    data = [trace]

    title = 'Total Data:{}'.format(name)

    layout = go.Layout(
        title=title,
        xaxis=dict(title='Segment'),
        yaxis=dict(title='Total Entries')
    )

    fig = go.Figure(data= data, layout=layout)

    return fig


def get_data_to_make_graph(json_data, name):
    #load the data
    dataset = json.loads(json_data)
    values = list(dataset.values())[0] #get values for the particular snapshot

    data = values[name] #get recency values for this data type as dictionary
    val = []
    #iterate through the list
    for i in data:
        #iterate  through the dictionary
        for k, v in i.items():
            val.append(v)

    #condition to check if the list is clusterId, min_max or total values
    ids, min_max_value, total_count = [], [], []

    for i in val:
        #condition
        if any(isinstance(x, list) for x in i):
            min_max_value.append(i)

        elif i[0] > 0:
            total_count.append(i)

        else:
            ids.append(i)

    X_axis = ids[0]

    min_value, max_value = [], []

    for i in min_max_value[0]:
        min_value.append(i[0])
        max_value.append(i[1])

    return X_axis, min_value, max_value, total_count

"""
    App callback to get the intermediate data stored in div selected_snapshot_id_cluster_analysis_data
    and update the graph components
"""
@app.callback(
    Output('recency-bar-graph', 'children'),
    [Input('selected_snapshot_id_cluster_analysis_data', 'children')]
)

def update_recency_bar_graph(jsonified_clean_data):

    X_axis, min_value, max_value, total_count = get_data_to_make_graph(jsonified_clean_data, 'recency')

    fig = get_stack_graph(X_axis, min_value, max_value, 'Recency')

    return dcc.Graph(
        figure = fig,
        id= 'recency-graph'
    )


@app.callback(
    Output('monetary-bar-graph', 'children'),
    [Input('selected_snapshot_id_cluster_analysis_data', 'children')]
)

def update_monetary_bar_graph(jsonified_clean_data):

    X_axis, min_value, max_value, total_count = get_data_to_make_graph(jsonified_clean_data, 'monetary')

    fig = get_stack_graph(X_axis, min_value, max_value, 'Monetary')

    return dcc.Graph(
        figure = fig,
        id= 'monetary-graph'
    )


@app.callback(
    Output('frequency-bar-graph', 'children'),
    [Input('selected_snapshot_id_cluster_analysis_data', 'children')]
)

def update_frequency_bar_graph(jsonified_clean_data):

    X_axis, min_value, max_value, total_count = get_data_to_make_graph(jsonified_clean_data, 'frequency')

    fig = get_stack_graph(X_axis, min_value, max_value, 'Frequency')

    return dcc.Graph(
        figure = fig,
        id= 'frequency-graph'
    )


#3D clustering process starts here
@app.callback(
    Output('recency-total-bar-graph', 'children'),
    [Input('selected_snapshot_id_cluster_analysis_data', 'children')]
)

def recency_total_graph(snapshot_data):

    X_axis, min_value, max_value, total_count = get_data_to_make_graph(snapshot_data, 'recency')

    fig = get_bar_graph(X_axis, total_count, 'Recency')

    return dcc.Graph(
        figure = fig,
        id= 'recency-total-graph'
    )

#3D clustering process starts here
@app.callback(
    Output('monetary-total-bar-graph', 'children'),
    [Input('selected_snapshot_id_cluster_analysis_data', 'children')]
)

def monetary_total_graph(snapshot_data):

    X_axis, min_value, max_value, total_count = get_data_to_make_graph(snapshot_data, 'monetary')

    fig = get_bar_graph(X_axis, total_count, 'Monetary')

    return dcc.Graph(
        figure = fig,
        id= 'monetary-total-graph'
    )

#3D clustering process starts here
@app.callback(
    Output('frequency-total-bar-graph', 'children'),
    [Input('selected_snapshot_id_cluster_analysis_data', 'children')]
)

def recency_total_graph(snapshot_data):

    X_axis, min_value, max_value, total_count = get_data_to_make_graph(snapshot_data, 'frequency')

    fig = get_bar_graph(X_axis, total_count, 'Frequency')

    return dcc.Graph(
        figure = fig,
        id= 'frequency-total-graph'
    )


#define the external urls
external_css = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css', 
'https://codepen.io/chriddyp/pen/brPBPO.css']

for css in external_css:
    app.css.append_css({'external_url': css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']

for js in external_js:
  app.scripts.append_script({'external_url': js})