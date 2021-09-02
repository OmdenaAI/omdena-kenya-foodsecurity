import json
import numpy as np
from pathlib import Path
import geopandas as gpd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go


ROOT_FOLDER = Path.cwd().parent. parent.parent
DATA_FOLDER = ROOT_FOLDER.joinpath("data", "external", 'asap', 'region')
GEO_FOLDER = Path(ROOT_FOLDER).joinpath('data',  'external',  'RegionsShapefiles')
MAX_SEVERITY = 5


# ================================================================
# DATA FOR PLOTS
# ================================================================

with open(Path(ROOT_FOLDER).joinpath("mapbox_token.txt")) as f:
    token = f.read()

files = list(Path(GEO_FOLDER).glob('*'))

from src.data.task_1_food_security.dataset import Dataset

# ds = Dataset(root_folder=ROOT_FOLDER)
# ds.prepare_dataset_array()
# units = ds.code2unit()
# unit_names = units['adm2_name'].values
# unit_dict = {'type': 'FeatureCollection', 'features': []}
#
# for file in files:
#     loaded_name = str(file).split('/')[-1].split('.')[0]
#     unit_name = ds.match_unit(loaded_name, unit_names)
#     unit_code = units[units['adm2_name'] == unit_name]['code'].values[0]
#     with open(file) as f:
#         loaded_feature = json.load(f)
#     if len(loaded_feature['features']) > 1:
#         print("More than one feature. Stopping...")
#         break
#     loaded_feature = loaded_feature['features'][0]
#     loaded_feature['properties']['NAME'] = unit_name
#     loaded_feature['properties']['COUNTY'] = unit_code
#     loaded_feature['geometry']['id'] = unit_code
#     unit_dict['features'].append(loaded_feature)
#
# df_unit = gpd.GeoDataFrame.from_features(unit_dict)
# df_unit.columns = ['geometry', 'NAME', 'adm2_name_code']
# df_unit.set_index('adm2_name_code', inplace=True)
# for y in range(2013, 2020):
#     df_y = ds.df_y.copy()
#     df_y.reset_index(inplace=True)
#     df_y =  df_y[df_y['season'] == y]
#     df_y = df_y[['adm2_name_code', 'severity'] + [f"phase{i}" for i in range(1, 6)]]
#     df_y.columns = ['adm2_name_code', f'severity_{y}'] + [f"phase{i}_{y}" for i in range(1, 6)]
#     df_y['adm2_name_code'] = df_y['adm2_name_code'].astype(int)
#     df_y.set_index('adm2_name_code', inplace=True)
#     df_unit = df_unit.join(df_y)
#
# # ASAP Data
# df_unit.to_file("data/geodf_unit.shp")
#
#
# df_asap = pd.read_csv(ROOT_FOLDER.joinpath('data', 'external', 'asap', 'region','SEN_asap_region.csv'))
# df_asap['dec_day'] = df_asap['yearday'].apply(lambda x: (x//10)*10)

df_unit = gpd.read_file("data/geodf_unit.json")

# ================================================================
# SECTION FUNCTIONS
# ================================================================

def header_section():
    return html.Div(
        [
            # html.Img(src=app.get_asset_url("dash-logo.png"), className="logo"),
            html.H4("Food Insecurity Metrics"),
        ],
        className="header__title",
    )

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# =====================================================================
# LAYOUT
# =====================================================================

# YEARS = list(range(2013, 2020))
# MAP_VARS = ["severity", "severity_LSTM_2019"]
# MAP_VARS_NAMES = ["Food Insecurity", "Neural Network Prediction"]



# app.layout = html.Div(
#     children=[
#         header_section(),
#         html.Div(
#             [
#                 html.Div(
#                     children=[
#                         html.P("Food Insecurity Phase"),
#                         html.Hr(),
#                         html.Div(
#                             children=[
#                                 dcc.Dropdown(
#                                     id='map_sec',
#                                     options=[{'value': x, 'label': y}
#                                              for x, y in zip(model_options, model_names)
#                                              ],
#                                     value=model_options[0],
#                                     multi=False
#                                 ),
#                                 dcc.Dropdown(
#                                     id='year',
#                                 ),
#                                 html.Div(id='display-selected-values')
#                                 ],
#                         ),
#                         dcc.Graph(id="choropleth"),
#                     ],
#                     className="eight columns named-card",
#                     style={'width': '30%', 'display': 'inline-block'},
#                 ),
#                 html.Div(
#                     children=[
#                         # html.P("Food Insecurity Phase"),
#                         # html.Hr(),
#                         # html.Div(
#                         #     children=[
#                         #         dcc.Dropdown(
#                         #             id='map_sec',
#                         #             options=[{'value': x, 'label': y}
#                         #                      for x, y in zip(MAP_VARS, MAP_VARS_NAMES)
#                         #                      ],
#                         #             value=MAP_VARS[0],
#                         #             multi=False
#                         #         ),
#                         #         dcc.Dropdown(
#                         #             id='year',
#                         #             options=[{'value': x, 'label': x+1}
#                         #                      for x in YEARS],
#                         #             value=YEARS[0],
#                         #         ),
#                         #         ],
#                         # ),
#                         # dcc.Graph(id="choropleth"),
#                     ],
#                     style={'width': '30%', 'display': 'inline-block'},
#                 ),
#                 # html.Div(
#                 #     children=[
#                 #         html.P("Weather Hisotry"),
#                 #         html.Hr(),
#                 #         html.Div(
#                 #             children=[
#                 #                 dcc.Dropdown(
#                 #                     id='plot_rain',
#                 #                     options=[{'value': x, 'label': y}
#                 #                              for x, y in zip(MAP_VARS, MAP_VARS_NAMES)
#                 #                              ],
#                 #                     value=MAP_VARS[0],
#                 #                     multi=False
#                 #                 ),
#                 #                 dcc.Dropdown(
#                 #                     id='year',
#                 #                     options=[{'value': x, 'label': x + 1}
#                 #                              for x in YEARS],
#                 #                     value=YEARS[0],
#                 #                 ),
#                 #             ],
#                 #         ),
#                 #         dcc.Graph(id="choropleth"),
#                 #     ],
#                 #     style={'width': '30%', 'display': 'inline-block'},
#                 # ),
#             ], className="next-level",
#         ),
#     ],
#     className="container"
# )

# =====================================================================
# CALLBACKS
# =====================================================================
# @app.callback(
#     Output("fig_weather", "figure")
#     [Input("region", "value"), Input("date", "value"),
#     Input("variable", "value")]
# )
# def display_weather(region, date, variable):
#     return
# @app.callback(
#     dash.dependencies.Output("my-dynamic-dropdown", "options"),
#     [dash.dependencies.Input("my-dynamic-dropdown", "search_value")],
# )
# def update_options(search_value):
#     if not search_value:
#         raise PreventUpdate
#     return [o for o in options if search_value in o["label"]]
all_options = {"gt": [f"severity{year}" for year in range(2013,2020)],
               "lstm": ["severity_lstm_2019"]}

all_labels = {"Ground Truth": [f"Food Insecurity {year}" for year in range(2013, 2020)],
               "Neural Network Prediction": ["Predicted Food Insecurity 2019"]}
# model_options = list(map_options.keys())
# model_names = ["Ground Truth", "Neural Network"]
# nested_options = map_options[model_options[0]]

# all_options = {
#     'America': ['New York City', 'San Francisco', 'Cincinnati'],
#     'Canada': [u'Montréal', 'Toronto', 'Ottawa']
# }
app.layout = html.Div([
    dcc.RadioItems(
        id='models-radio',
        options=[{'label': l, 'value': o} for l, o in zip(all_labels.keys(), all_options.keys())],
        value='Select type of data'
    ),

    html.Hr(),

    dcc.RadioItems(id='years-radio'),

    html.Hr(),

    html.Div(id='display-selected-values'),

    html.P("Food Insecurity Phase"),
    html.Hr(),

    dcc.Graph(id="choropleth"),
])


@app.callback(
    Output('years-radio', 'options'),
    Input('models-radio', 'value'))
def set_cities_options(selected_country):
    return [{'label': l, 'value': o} for l, o in zip(all_labels[selected_country],  all_options[selected_country])]


@app.callback(
    Output('years-radio', 'value'),
    Input('years-radio', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    Input('models-radio', 'value'),
    Input('years-radio', 'value'))
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(
        selected_city, selected_country,
    )


@app.callback(
    Output("choropleth", "figure"),
    [Input('years-radio', "value")])
def display_choropleth(col_name):
    # color = f'{map_variable}_{year}'
    df_unit['Food Insecurity'] = df_unit[col_name]
    # if map_variable.split("_")[0] == "severity":
    #     min_color = 1
    #     max_color = MAX_SEVERITY
    #     color_scale = ["#CDFACD",
    #                     "#FAE61E",
    #                     "#E67800",
    #                     "#C80000",
    #                     "#1D1D1D"]
    # elif map_variable.split("_")[0] == "phase1":
    #     min_color = 0
    #     max_color = 1
    #     color_scale = 'blues'
    # else:
    #     min_color = 0
    #     max_color = 1
    #     color_scale = 'blues'

    color_scale = ["#CDFACD",
                   "#FAE61E",
                   "#E67800",
                   "#C80000",
                   "#1D1D1D"]

    fig = px.choropleth_mapbox(df_unit,
                                geojson=df_unit.geometry,
                                locations=df_unit.index,
                                color='Food Insecurity',
                                center={"lat": 14.4097, "lon": -14.8635},
                                zoom=5.7,
                                # projection="mercator",
                                color_continuous_scale=color_scale,
                                labels='NAME',
                                template='plotly',
                               range_color=(1, MAX_SEVERITY))
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      mapbox_accesstoken=token)
    return fig

@app.callback(
    Output("map_pred", "figure"),
    [Input("model_value", "value")])
def display_pred(model_value):
    df_unit['Food Insecurity'] = df_unit[model_value]
    # if map_variable.split("_")[0] == "severity":
    #     min_color = 1
    #     max_color = MAX_SEVERITY
    #     color_scale = ["#CDFACD",
    #                     "#FAE61E",
    #                     "#E67800",
    #                     "#C80000",
    #                     "#1D1D1D"]
    # elif map_variable.split("_")[0] == "phase1":
    #     min_color = 0
    #     max_color = 1
    #     color_scale = 'blues'
    # else:
    #     min_color = 0
    #     max_color = 1
    #     color_scale = 'blues'
    color_scale = ["#CDFACD",
                   "#FAE61E",
                   "#E67800",
                   "#C80000",
                   "#1D1D1D"]
    min_color=1
    max_color=MAX_SEVERITY

    fig = px.choropleth_mapbox(df_unit,
                                geojson=df_unit.geometry,
                                locations=df_unit.index,
                                color='Food Insecurity',
                                center={"lat": 14.4097, "lon": -14.8635},
                                zoom=5.7,
                                # projection="mercator",
                                color_continuous_scale=color_scale,
                                labels='NAME',
                                template='plotly',
                               range_color=(min_color, max_color))
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                      mapbox_accesstoken=token)
    return fig

@app.callback(
    Output("weather_plot", "figure"),
    [Input("region", "value"), Input("weather", "value")])
def plot_region_weather(reg="Kolda", weather="Rainfall", year=2019):
    df_temp = df_asap[["region_name", "variable_name", "dec_day", "value"]].copy()
    df_temp = df_temp[df_temp["variable_name"] == weather]

    df_m = df_temp.groupby(['region_name', 'dec_day']).mean()
    df_se = df_temp.groupby(['region_name', 'dec_day']).sem()

    fig = go.Figure()
    m = df_m.loc[reg]
    s = df_se.loc[reg]
    x = m.index.values
    m = m.values.flatten()
    s = s.values.flatten()
    x = np.hstack([x, x[::-1]])
    y_up = m+s*1.96
    y_low = m-s*1.96
    y_low = y_low[::-1]

    fig.add_trace(go.Scatter(
        x=x,
        y=np.hstack([y_up, y_low]),
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=True,
        name='Historical mean',
    ))
    curr = df_asap[(df_asap["year"] == year) & (df_asap["variable_name"] == weather) &
    (df_asap["region_name"] == reg)].copy()
    curr.sort_values(by="dec_day")
    curr = curr[["dec_day", "value"]]
    curr = curr.groupby("dec_day").mean()
    # x = curr["dec_day"].values.flatten()
    # y = curr["value"].values.flatten()
    fig.add_trace(go.Scatter(x=curr.index, y=curr.values.flatten(), showlegend=True, name="2019"))
    fig.update_traces(mode='lines')

    if weather == "Rainfall":
        ylabel = "Precipitation [mm]"
    else:
        ylabel = "Mean NDVI"
    fig.update_layout(
        xaxis_title="Day",
        yaxis_title=ylabel,
        legend=dict(yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
))

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)