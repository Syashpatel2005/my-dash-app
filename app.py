import pandas as pd
import dash
import numpy as np
import plotly.graph_objs as go
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Load Data
p = pd.read_csv('IndividualDetails.csv')
covid = pd.read_csv('covid_19_india.csv')
age = pd.read_csv('AgeGroupDetails.csv')

# Data Processing
dbd = covid.groupby('Date')['Confirmed'].sum().reset_index()

# Summary Stats
total = p.shape[0]
active = p[p['current_status'] == 'Hospitalized'].shape[0]
recovered = p[p['current_status'] == 'Recovered'].shape[0]
death = p[p['current_status'] == 'Deceased'].shape[0]

# Dropdown Options
options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]

# App Initialization
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = html.Div([

    # Title
    html.H1(
        "CoronaVirus India's Perspective",
        style={'textAlign': 'center', 'color': '#fff', 'marginBottom': '30px'}
    ),

    # ================= ROW 1 (CARDS) =================
    html.Div([

        html.Div([
            html.Div([
                html.Div([
                    html.H4('Total Cases', className='text-light'),
                    html.H2(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger p-3 shadow')
        ], className='col-md-3 mb-4'),

        html.Div([
            html.Div([
                html.Div([
                    html.H4('Active', className='text-light'),
                    html.H2(active, className='text-light')
                ], className='card-body')
            ], className='card bg-info p-3 shadow')
        ], className='col-md-3 mb-4'),

        html.Div([
            html.Div([
                html.Div([
                    html.H4('Recovered', className='text-light'),
                    html.H2(recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-warning p-3 shadow')
        ], className='col-md-3 mb-4'),

        html.Div([
            html.Div([
                html.Div([
                    html.H4('Deaths', className='text-light'),
                    html.H2(death, className='text-light')
                ], className='card-body')
            ], className='card bg-success p-3 shadow')
        ], className='col-md-3 mb-4'),

    ], className='row mt-4'),

    # ================= ROW 2 (GRAPHS) =================
    html.Div([

        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='line',
                        figure={
                            'data': [go.Scatter(
                                x=dbd['Date'],
                                y=dbd['Confirmed'],
                                mode='lines+markers'
                            )],
                            'layout': go.Layout(title='Day by Day Analysis')
                        },
                        style={'padding': '10px'}
                    )
                ], className='card-body')
            ], className='card shadow')
        ], className='col-md-6 mb-4'),

        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='pie',
                        figure={
                            'data': [go.Pie(
                                labels=age['AgeGroup'],
                                values=age['TotalCases']
                            )],
                            'layout': go.Layout(title='Age Distribution')
                        },
                        style={'padding': '10px'}
                    )
                ], className='card-body')
            ], className='card shadow')
        ], className='col-md-6 mb-4'),

    ], className='row mt-4'),

    # ================= ROW 3 (DROPDOWN + BAR) =================
    html.Div([

        html.Div([
            html.Div([
                html.Div([

                    dcc.Dropdown(
                        id='picker',
                        options=options,
                        value='All',
                        style={'marginBottom': '15px'}
                    ),

                    dcc.Graph(id='bar')

                ], className='card-body')
            ], className='card shadow')
        ], className='col-md-12 mb-4'),

    ], className='row mt-4')

], className='container p-4', style={'backgroundColor': '#111'})

# Callback
@app.callback(Output('bar', 'figure'), [Input('picker', 'value')])
def update_graph(type):
    if type == 'All':
        pbar = p['detected_state'].value_counts().reset_index()
    else:
        npt = p[p['current_status'] == type]
        pbar = npt['detected_state'].value_counts().reset_index()

    pbar.columns = ['detected_state', 'count']

    return {
        'data': [go.Bar(
            x=pbar['detected_state'],
            y=pbar['count']
        )],
        'layout': go.Layout(title='State-wise Cases')
    }

# Run App
if __name__ == '__main__':
    app.run(port=5000, debug=True)
