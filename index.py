import sys
sys.path.append("F:/work projects/Dash Application")

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import users, segmentation, cs_id, config

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', style={'width':'100%'}),
    #this div element is Hidden
    html.Div(id='user-id', style={'display':'none'})

], style={'width':'100%', 'margin-left':'0%'})

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])


def display_page(pathname):
    #check if pathname carries any uniqueId to review
    separate_uid = pathname
    print("URL PAGE:{}".format(separate_uid))

    if pathname == '/apps/users':
         return users.layout

    elif pathname == '/apps/segmentation':
        return segmentation.layout

    elif pathname == '/apps/config':
        return config.layout

    elif '=' in separate_uid:
        return cs_id.layout

    else:
        return users.layout


@app.callback(Output('user-id', 'children'),
    [Input('url', 'pathname')])

def get_user_id(pathname):
    #check if pathname carries any uniqueId to review
    separate_uid = pathname

    uid = None

    if '=' in separate_uid:
        uid = separate_uid.split('=')[1]
        return uid 


if __name__ == '__main__':
    app.run_server(debug=True)