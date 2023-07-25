# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All sites', 'value': 'all'},
                                                      {'label': 'CCAFS LC-40', 'value': '1'},
                                                      {'label': 'VAFB SLC-4E', 'value': '2'},
                                                      {'label': 'KSC LC-39A', 'value': '3'},
                                                      {'label': 'CCAFS SLC-40', 'value': '4'}],
                                             value='all',
                                             placeholder='Select a launch site here',
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', 
                                                min=0, 
                                                max=10000, 
                                                step=1000, 
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}, 
                                                value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'all':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, 
                     values='class',
                     names='Launch Site',
                     title='Total Sucess Launches By Sites')
    elif entered_site == '1':
        filtered_df = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40'].groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, 
                     values='Launch Site',
                     names='class',
                     title='title')
    elif entered_site == '2':
        filtered_df = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E'].groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, 
                     values='Launch Site',
                     names='class',
                     title='title')
    elif entered_site == '3':
        filtered_df = spacex_df[spacex_df['Launch Site']=='KSC LC-39A'].groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, 
                     values='Launch Site',
                     names='class',
                     title='title')
    elif entered_site == '4':
        filtered_df = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40'].groupby('class')['Launch Site'].count().reset_index()
        fig = px.pie(filtered_df, 
                     values='Launch Site',
                     names='class',
                     title='title')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')
             )

def scatter_plot(selected_site, selected_payload):
    if selected_site == 'all':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=selected_payload[0]) & (spacex_df['Payload Mass (kg)']<=selected_payload[1])]
        fig_1 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    elif selected_site == '1':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=selected_payload[0]) & (spacex_df['Payload Mass (kg)']<=selected_payload[1]) & (spacex_df['Launch Site'] == 'CCAFS LC-40')]
        fig_1 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    elif selected_site == '2':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=selected_payload[0]) & (spacex_df['Payload Mass (kg)']<=selected_payload[1]) & (spacex_df['Launch Site'] == 'VAFB SLC-4E')]
        fig_1 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    elif selected_site == '3':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=selected_payload[0]) & (spacex_df['Payload Mass (kg)']<=selected_payload[1]) & (spacex_df['Launch Site'] == 'KSC LC-39A')]
        fig_1 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    elif selected_site == '4':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=selected_payload[0]) & (spacex_df['Payload Mass (kg)']<=selected_payload[1]) & (spacex_df['Launch Site'] == 'CCAFS SLC-40')]
        fig_1 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    return fig_1


# Run the app
if __name__ == '__main__':
    app.run_server()
    
