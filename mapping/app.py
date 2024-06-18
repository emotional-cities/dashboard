#!/usr/bin/env python
# coding: utf-8

# In[8]:


import csv
import pandas as pd 
import matplotlib.pyplot as plt 
from tkinter import filedialog as fd
from flask import Flask


# In[9]:


df_London = pd.read_csv('df_London.csv', sep=',', on_bad_lines='skip')
df_Lisbon = pd.read_csv('df_Lisbon.csv', sep=',', on_bad_lines='skip')
df_Lansing = pd.read_csv('df_Lansing.csv', sep=',', on_bad_lines='skip')
df_Outdoor_London = pd.read_csv('OutdoorWalks_London.csv', sep=',', on_bad_lines='skip')
df_Lisbon_Img = pd.read_csv('BAP_Image_table.csv', sep=',', on_bad_lines='skip')
df_Copenhagen = pd.read_csv('df_Copenhagen.csv', sep=',', on_bad_lines='skip')

df_London.columns.name = None
df_London.index.name = None

df_Lisbon.columns.name = None
df_Lisbon.index.name = None 

df_Lansing.columns.name = None 
df_Lansing.index.name = None 

df_Outdoor_London.columns.name = None
df_Outdoor_London.index.name = None

df_Lisbon_Img.columns.name = None
df_Lisbon_Img.index.name = None

df_Copenhagen.columns.name = None
df_Copenhagen.index.name = None

#df_London
#df_Lisbon
#df_Lansing


# In[24]:


import dash
from dash import dcc, html, Input, Output, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go 
import plotly.express as px  
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler
import dash_bootstrap_components as dbc
import folium
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# In[34]:


default_map_content = folium.Map(location=[0, 0], zoom_start=2)
default_map_content.save('basemap.html')


# In[82]:


# Define a list of cities and the number of layers for each city
cities_data = {
    'London': 20,
    'Lisbon': 31,
    'Lansing': 19,
    'Copenhagen': 4,
}

# Create a dictionary to map cities to their respective data layer options

city_data_layers = {
    'London': [
        {'label': 'Normalized difference vegetation index (NDVI)', 'value': 'London_layer1'},
        {'label': 'Annual mean PM2.5', 'value': 'London_layer2'},
        {'label': 'Annual mean PM10', 'value': 'London_layer3'},
        {'label': 'Annual mean NO2 concentrations', 'value': 'London_layer4'},
        {'label': 'Annual average noise levels of rail noise', 'value': 'London_layer5'},
        {'label': 'Risk of flooding from rivers and seas', 'value': 'London_layer6'},
        {'label': 'Major summer heat spots', 'value': 'London_layer7'},
        {'label': 'Cycling routes density map', 'value': 'London_layer8'},
        {'label': 'Land use diversity', 'value': 'London_layer9'},
        {'label': 'Proportion of population with access to public open space', 'value': 'London_layer10'},
        {'label': 'Prevalence rates of cardiovascular diseases', 'value': 'London_layer11'},
        {'label': 'Prevalence rates of obesity', 'value': 'London_layer12'},
        {'label': 'Prevalence rates of depression', 'value': 'London_layer13'},
        {'label': 'Prevalence rates of mental health issues', 'value': 'London_layer14'},
        {'label': 'Prevalence rates of dementia', 'value': 'London_layer15'},
        {'label': 'Population density map', 'value': 'London_layer16'},
        {'label': 'Gender ratio map', 'value': 'London_layer17'},
        {'label': 'Map of the ratio of elder people', 'value': 'London_layer18'},
        {'label': 'Map of ratio of active people', 'value': 'London_layer19'},
        {'label': 'Map of number of recorded crimes', 'value': 'London_layer20'},
    ],
    'Lisbon': [
        {'label': 'Positive tweets', 'value': 'Lisbon_layer1'},
        {'label': 'Life births rate', 'value': 'Lisbon_layer2'},
        {'label': 'Mortality rate', 'value': 'Lisbon_layer3'},
        {'label': 'Patients with diabetes mellitus', 'value': 'Lisbon_layer4'},
        {'label': 'Patients with chronic alcohol abuse', 'value': 'Lisbon_layer5'},
        {'label': 'Patients with tobacco abuse', 'value': 'Lisbon_layer6'},
        {'label': 'Patients with obesity', 'value': 'Lisbon_layer7'},
        {'label': 'Patients with hypertension', 'value': 'Lisbon_layer8'},
        {'label': 'Patients diagnosed with dementia', 'value': 'Lisbon_layer9'},
        {'label': 'Patients diagnosed with anxiety disorder', 'value': 'Lisbon_layer10'},
        {'label': 'Patients diagnosed with depressive disorder', 'value': 'Lisbon_layer11'},
        {'label': 'People with low low literacy ratio','value':'Lisbon_layer12'},
        {'label': 'Unemployed people ratio','value':'Lisbon_layer13'},
        {'label': 'Population density','value':'Lisbon_layer14'},
        {'label': 'Gender ratio','value':'Lisbon_layer15'},
        {'label': 'Youth people ratio','value':'Lisbon_layer16'},
        {'label': 'Elderly people ratio','value':'Lisbon_layer17'},
        {'label': 'Average age of buildings', 'value':'Lisbon_layer18'},
        {'label': 'Buildings with repair needs ratio', 'value':'Lisbon_layer19'},
        {'label': 'Walkability index', 'value':'Lisbon_layer20'},
        {'label': 'Altimery', 'value':'Lisbon_layer21'},
        {'label': 'Beds/customers in tourist accomodations', 'value':'Lisbon_layer22'},
        {'label': 'Density of fast food outlets', 'value':'Lisbon_layer23'},
        {'label': 'Normalized difference vegetation index (NDVI)', 'value':'Lisbon_layer24'},
        {'label': 'Noise level', 'value':'Lisbon_layer25'},
        {'label': 'Particulate Matter (PM2.5)', 'value':'Lisbon_layer26'},
        {'label': 'Mean temperature', 'value':'Lisbon_layer27'},
        {'label': 'Extreme heat vulnerability', 'value':'Lisbon_layer28'},
        {'label': 'Vulnerability to flash floods index', 'value':'Lisbon_layer29'},
        {'label': 'Nitrogen Dioxide', 'value':'Lisbon_layer30'},
        {'label': 'Distance to green spaces', 'value':'Lisbon_layer31'},
    ],
    'Lansing': [
        {'label': 'Chroni obstructive pulmonary disease', 'value': 'Lansing_layer1'},
        {'label': 'Area deprivation index', 'value': 'Lansing_layer2'},
        {'label': 'Gender ratio', 'value': 'Lansing_layer3'},
        {'label': 'National walkability index', 'value': 'Lansing_layer4'},
        {'label': 'Per capita income', 'value': 'Lansing_layer5'},
        {'label': 'Crude percent of adults with depression', 'value': 'Lansing_layer6'},
        {'label': 'Percentage of people with disability', 'value': 'Lansing_layer7'},
        {'label': 'Life expectancy at birth', 'value': 'Lansing_layer8'},
        {'label': 'Number of people travel by bicycle to work', 'value': 'Lansing_layer9'},
        {'label': 'Number of people with disability - Aged 5 and above', 'value': 'Lansing_layer10'},
        {'label': 'Average travel time to work', 'value': 'Lansing_layer11'},
        {'label': 'Coronary heart disease', 'value': 'Lansing_layer12'},
        {'label': 'Current ashthma', 'value': 'Lansing_layer13'},
        {'label': 'Diabeties', 'value': 'Lansing_layer14'},
        {'label': 'High blood pressure', 'value': 'Lansing_layer15'},
        {'label': 'No leisure time physical activity', 'value': 'Lansing_layer16'},
        {'label': 'Obesity', 'value': 'Lansing_layer17'},
        {'label': 'Physical health not good for people aged above 18', 'value': 'Lansing_layer18'},
        {'label': 'Stroke', 'value': 'Lansing_layer19'},
    ],
    'Copenhagen': [
        {'label':'Nitrogen Dioxide', 'value':'Copenhagen_layer1'},
        {'label':'Particulate Matter (PM2.5)', 'value':'Copenhagen_layer2'},
        {'label':'Particulate Matter (PM10)', 'value':'Copenhagen_layer3'},
        {'label':'Noise level', 'value':'Copenhagen_layer4'},
    ]
}

# Define a dictionary to store file paths for Outdoor Walks
outdoor_walks_layers = {
    'Sound Pressure': 'OutdoorWalk_London/OutdoorWalk_London_Layer1.html',
    'Humidity': 'OutdoorWalk_London/OutdoorWalk_London_Layer2.html',
    'PM1.0': 'OutdoorWalk_London/OutdoorWalk_London_Layer3.html',
    'PM2.5': 'OutdoorWalk_London/OutdoorWalk_London_Layer4.html',
    'PM10': 'OutdoorWalk_London/OutdoorWalk_London_Layer5.html',
    'Solar Light': 'OutdoorWalk_London/OutdoorWalk_London_Layer6.html',
    'Air Temperature': 'OutdoorWalk_London/OutdoorWalk_London_Layer7.html',
    'MRT': 'OutdoorWalk_London/OutdoorWalk_London_Layer8.html',
    'MRT*': 'OutdoorWalk_London/OutdoorWalk_London_Layer9.html',
    'UTCI': 'OutdoorWalk_London/OutdoorWalk_London_Layer10.html',
    # Add more layers here as needed
}

# Define a dictionary to store file paths for Lisbon Image data
exp1_layers = {
    'Images': 'EXP1/Exp1_Lisbon_Layer1.html',
}

city_data_sources = {
    'London' : ['Spatial Analysis of Urban Health', 'Outdoor Walks'],
    'Lisbon' : ['Spatial Analysis of Urban Health', 'Brain as Predictor'],
    'Lansing' : ['Spatial Analysis of Urban Health'],
    'Copenhagen': ['Spatial Analysis of Urban Health'],
}


# In[108]:


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css'])
server=app.server


# Generate the file_paths dictionary using nested loops
file_paths = {}
for city, num_layers in cities_data.items():
    for layer_number in range(1, num_layers + 1):
        key = f'{city}_layer{layer_number}'
        value = f'{city}/Output_{city}_Layer{layer_number}.html'
        file_paths[key] = value
        
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H6("Map Visualization", className='section-title'), 
                
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.H6("Select your city", className='subsection-title'), 
                            dcc.Dropdown(
                                id='city-dropdown',
                                options=[
                                    {'label': 'London', 'value': 'London'},
                                    {'label': 'Lisbon', 'value': 'Lisbon'},
                                    {'label': 'Lansing', 'value': 'Lansing'},
                                    {'label': 'Copenhagen', 'value':'Copenhagen'}
                                ],
                                value='London'
                            ),
                        ]),
                        width=12,
                    ),
                ]),
        
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.H6("Pick the data source", className='subsection-title'),
                            dcc.Dropdown(
                                id='data-source-dropdown',
                                options=[
                                    {'label': 'Spatial Analysis of Urban Health', 'value': 'Spatial Analysis of Urban Health'},
                                    {'label': 'Outdoor Walks', 'value': 'Outdoor Walks'},
                                    {'label': 'Brain as Predictor', 'value': 'Brain as Predictor'},
                                ],
                            ),
                        ]),
                        width=12,
                    ),
                ]),
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.H6("Pick the data layer", className='subsection-title'),
                            dcc.Dropdown(
                                id='data-layer-dropdown',
                                options=[
                                    {'label': 'Dataset', 'value': 'option1'},
                                ],
                                value='option1',
                            ),
                        ]),
                        width=12,
                    ),
                ]),
                
                dbc.Row([
                    dbc.Col(
                        html.Iframe(
                            id='map',
                            srcDoc=open('basemap.html', 'r').read(),
                            style={'width': '100%', 'height': '85vh', 'margin-top': '20px'}
                        ),
                        width=12,
                    ),
                ]),            
            ], className='section map-section'),
        ], width=6),

        dbc.Col([
            html.Div([
                html.H6("Graph Visualization", className='section-title'),
                
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.H6("Select two variables for correlation analysis (dependent and independent)", className='subsection-title'),
                            dcc.Dropdown(
                                id='parameter-dropdown',
                                options=[],
                                multi=True,
                            ),
                        ]),
                        width=12,
                    ),
                ]),
            ], className='section analytics-section'),
            dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='visualization-graph', config={'displayModeBar': True, 'responsive': True}), 
                        style={'width': '100%', 'height': '50%', 'margin-top': '0px'}
                    ),
            ]),
            dbc.Row([
                    dbc.Col(
                        dcc.Graph(id='hidden-graph', config={'displayModeBar': True, 'responsive': True}, style={'display': 'none'}), 
                        style={'width': '100%', 'height': '50%', 'margin-top': '0px'}
                    ),
            ]),
        ], width=6),
    ], className='main-row'),

    # Footer section
    dbc.Row([
    dbc.Col([
        html.Hr(style={'border-top': '2px solid #ddd'}),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Img(src="https://emocities.s3.eu-central-1.amazonaws.com/style/EU_Commission_Horizon_2020-1024x160.png", height='50px'),
                    html.P("This project has received funding from the European Union’s Horizon 2020 Research and Innovation Programme under Grant Agreement nº 945307. The document represents the view of the author only and is his/her sole responsibility: it cannot be considered to reflect the views of the European Commission. The European Commission does not accept responsibility for the use that may be made of the information it contains.", className='footer-text'),
                ], width=4),  # Adjust the width of the column
                dbc.Col([
                    html.Img(src="https://emocities.s3.eu-central-1.amazonaws.com/style/logo_background-slogan_blue.png", height='150px'),
                    html.P("© 2024 eMOTIONAL Cities. All rights reserved.", className='footer-text', style={'text-align': 'center'})  # Move the text here
                ], width=4, className='text-center'),  # Adjust the width of the column
            ])
        ], className='footer-content')
    ])
], className='main-container')
])


############################ pop up window ###########################


# Create a modal for displaying the disclaimer
disclaimer_modal = dbc.Modal(
    [
        dbc.ModalHeader(html.Strong("Welcome to our Open Data Platform, an integral part of the eMOTIONAL Cities Project!"), close_button=False),
        dbc.ModalBody(
            html.Div([
                html.P(
                    "Here, we provide a geo-visualization dashboard that showcases maps and data for various cities, making this information openly accessible to all."
                ),
                html.P(
                    "Our platform features geographically referenced data, enabling users to interactively explore different cities and locations. This interactive environment supports mutual learning and collaboration by providing insights into how artificial urban environments—encompassing urban structures, elements, and design—influence the mental and physical well-being of individuals. By facilitating spatial analysis and the integration of new and existing datasets, this platform serves as a powerful tool for comprehensive spatial examinations."
                ),
                html.P(
                    "Our goal is to provide you with a detailed understanding of the collected data in a spatial framework, enhancing your ability to analyze and interpret the impact of urban environments on human health and behavior."
                ),
                html.P(
                    [html.Strong("Disclaimer:"), " The analysis and maps presented in these reports should not be subject to extrapolation that leads to direct causation in analysis and conclusions as it can produce unintended consequences."]
                ),
            ])
        ),
        dbc.ModalFooter(
            dbc.Button("Continue", id="disclaimer-close", className="ml-auto")
        ),
    ],
    id="disclaimer-modal",
    centered=True,
    is_open=True,
    backdrop="static",
    size='lg',
)

# Append the disclaimer modal to the app layout
app.layout = html.Div([disclaimer_modal, app.layout])

# Define callback to close the modal when the button is clicked
@app.callback(
    Output("disclaimer-modal", "is_open"),
    [Input("disclaimer-close", "n_clicks")],
    [State("disclaimer-modal", "is_open")],
)
def close_modal(n, is_open):
    if n:
        return not is_open
    return is_open

##############################################################################



@app.callback(
    Output('data-source-dropdown', 'options'),
    [Input('city-dropdown', 'value')]
)
def update_data_sources(selected_city):
    # Get the data sources for the selected city from the dictionary
    data_sources = city_data_sources.get(selected_city, [])

    # Create dropdown options based on data sources
    data_source_options = [{'label': source, 'value': source} for source in data_sources]

    return data_source_options


@app.callback(
    Output('parameter-dropdown', 'options'),
    [Input('city-dropdown', 'value'),
     Input('data-source-dropdown', 'value')]
)

def update_parameter_checklist(selected_city, selected_data_source):
    if selected_city == 'London':
        if selected_data_source == 'Spatial Analysis of Urban Health':
            parameter_options = [{'label': col, 'value': col} for col in df_London.columns[1:]]
        elif selected_data_source == 'Outdoor Walks':
            selected_columns = ['Sound_Pressure', 'Humidity', 'PM1_0', 'PM2_5', 'PM10_0', 'Solar_Light', 'Air_Temperature', 'MRT', 'MRT_S', 'UTCI']
            parameter_options = [{'label': col, 'value': col} for col in selected_columns]
        else:
            parameter_options = []
    elif selected_city == 'Lisbon':
        if selected_data_source == 'Spatial Analysis of Urban Health':
            parameter_options = [{'label': col, 'value': col} for col in df_Lisbon.columns[1:]]
        elif selected_data_source == 'Brain as Predictor':
            selected_columns = ['GREENINDEX', 'POPULARITY', 'VIEWS', 'DENSITY']
            parameter_options = [{'label': col, 'value': col} for col in selected_columns]
        else:
            parameter_options = []
    elif selected_city == 'Lansing':
        parameter_options = [{'label': col, 'value': col} for col in df_Lansing.columns[1:]]
    elif selected_city == 'Copenhagen':
        parameter_options = [{'label': col, 'value': col} for col in df_Copenhagen.columns[:]]
    else:
        parameter_options = []

    return parameter_options


# Callback to update the data layer dropdown options based on the selected city

@app.callback(
    Output('data-layer-dropdown', 'options'),
    [Input('city-dropdown', 'value'),
     Input('data-source-dropdown', 'value')]
)
def update_data_layers(selected_city, selected_data_source):
    # Get the data layer options for the selected city from the dictionary
    if selected_data_source == 'Outdoor Walks':
        # If "Outdoor Walks" is selected, populate the dropdown with available layers for Outdoor Walks
        data_layer_options = [{'label': layer, 'value': layer} for layer in outdoor_walks_layers.keys()]
    elif selected_data_source == 'Brain as Predictor':
        data_layer_options = [{'label': layer, 'value': layer} for layer in exp1_layers.keys()]
    else:
        data_layer_options = city_data_layers.get(selected_city, [])
    return data_layer_options

############################ GRAPH CALLBACK  #########################################

@app.callback(
    [Output('visualization-graph', 'figure'),
     Output('hidden-graph', 'figure'),
     Output('hidden-graph', 'style')],
    [Input('parameter-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('data-source-dropdown', 'value')]
)
def update_visualization_graph(selected_parameter, selected_city, selected_data_source):
    hidden_figure = go.Figure()
    main_figure = go.Figure()

    if selected_parameter and len(selected_parameter) == 2 and selected_city and selected_data_source:
        if selected_city == 'London':
            if selected_data_source == 'Spatial Analysis of Urban Health':
                df = df_London
            elif selected_data_source == 'Outdoor Walks':
                df = df_Outdoor_London
        elif selected_city == 'Lisbon':
            if selected_data_source == 'Spatial Analysis of Urban Health':
                df = df_Lisbon
            elif selected_data_source == 'Brain as Predictor':
                df = df_Lisbon_Img
        elif selected_city == 'Lansing':
            if selected_data_source == 'Spatial Analysis of Urban Health':
                df = df_Lansing
        elif selected_city == 'Copenhagen':
            if selected_data_source == 'Spatial Analysis of Urban Health':
                df = df_Copenhagen        
        else:
            df = pd.DataFrame()  # Empty DataFrame
        
        if not df.empty and all(param in df.columns for param in selected_parameter):
            main_figure = px.scatter(df, x=selected_parameter[0], y=selected_parameter[1], trendline='ols')
            
            if selected_data_source == 'Outdoor Walks':
                hidden_figure.add_trace(go.Scatter(x=df.index, y=df[selected_parameter[0]], mode='lines', name=selected_parameter[0]))
                hidden_figure.add_trace(go.Scatter(x=df.index, y=df[selected_parameter[1]], mode='lines', name=selected_parameter[1], yaxis='y2'))
                hidden_figure.update_layout(yaxis=dict(title=selected_parameter[0]), yaxis2=dict(title=selected_parameter[1], overlaying='y', side='right'))
                hidden_graph_style = {}
            else:
                hidden_graph_style = {'display': 'none'}
        else:
            hidden_graph_style = {'display': 'none'}
    else:
        hidden_graph_style = {'display': 'none'}
        df = pd.DataFrame()  # Empty DataFrame

    return main_figure, hidden_figure, hidden_graph_style

######################################################################################


# New callback to update the map based on the selected data layer
# Merge the data layer paths and data source layer paths into a single dictionary
all_layers = {**file_paths, **outdoor_walks_layers, **exp1_layers}

@app.callback(
    Output('map', 'srcDoc'),
    [Input('data-layer-dropdown', 'value')]
)

def update_map(selected_data_layer):
    if selected_data_layer:
        # Get the file path from the file_paths dictionary
        file_path = all_layers.get(selected_data_layer)

        # Read the contents of the selected HTML file
        try:
            with open(file_path, 'r') as file:
                content = file.read()
        except (FileNotFoundError, TypeError):
            content = open('basemap.html','r').read()

        return content
    else:
        # Return an empty map if no data layer is selected
        return ""


if __name__ == '__main__':
    app.run()

