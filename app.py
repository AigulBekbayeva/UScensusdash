#importing libraries
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template('vapor')
app = Dash(__name__,
           external_stylesheets=[dbc.themes.CYBORG])

#importing dataset and select interested columns
df = pd.read_csv("USCensus1990.data.txt")
df_clean = df[["caseid", "dAge", "iSex", "dOccup", "iMarital", "iFertil","iImmigr", "dIndustry","dRearning", "dRpincome"]]
df_clean = df_clean.iloc[-100:]
df_clean = df_clean.copy()
df_clean.head()
#change labels,
df_clean['iSex'] = df_clean['iSex'].replace([0, 1], ['male', 'female'])
df_clean['dAge'] = df_clean['dAge'].replace([0, 1, 2, 3, 4, 5, 6, 7, 8], ['Less Than 1 Year', '1-13','13-20','20-30','30-40','40-50','50-66','65-90','>90'])
df_clean['dOccup'] = df_clean['dOccup'].replace([0, 1, 2, 3, 4, 5, 6, 7, 8], ['N/a Less Than 16 Yrs. Old/unemp. Who Never empl', 'MANAGERIAL AND PROFESSIONAL SPECIALTY OCCUPATIONS','TECHNICAL, SALES, AND ADMINISTRATIVE SUPPORT OCCUPATIONS','FARMING, FORESTRY, AND FISHING OCCUPATIONS','PRECISION PRODUCTION, CRAFT, AND REPAIR OCCUPATIONS','OPERATORS, FABRICATORS, AND LABORERS','MILITARY OCCUPATIONS','EXPERIENCED UNEMPLOYED NOT CLASSIFIED BY OCCUPATION','others'])
df_clean['iMarital'] = df_clean['iMarital'].replace([0, 1, 2, 3, 4], ['Now married, except separated', 'Widowed','Divorced','Separated','Never married or under 15 years old'])
df_clean['iFertil'] = df_clean['iFertil'].replace([0, 1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13], ['N/a Less Than 15 Yrs./male', 'No Chld.','1 Child','2 Child.','3 Child.','4 Child.','5 Child.','6 Child.', '7 Child.', '8 Child.', '9 Child.', '10 Child.', '11 Child.', '12 or more Child.'])
df_clean['dIndustry'] = df_clean['dIndustry'].replace([0, 1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12], ['N/a Less Than 16 Yrs. Old/unemp. Who Nev', 'AGRICULTURE, FORESTRY, AND FISHERIES', 'MINING', 'CONSTRUCTION', 'MANUFACTURING', 'TRANSPORTATION, COMMUNICATIONS, AND OTHER PUBLIC UTILITIES', 'WHOLESALE TRADE', 'RETAIL TRADE', 'FINANCE, INSURANCE, REAL ESTATE, BUSINESS AND REPAIR SERVICES, PERSONAL SERVICES', 'ENTERTAINMENT AND RECREATION SERVICES, PROFESSIONAL AND RELATED SERVICES', 'PUBLIC ADMINISTRATION', 'ACTIVE DUTY MILITARY', 'EXPERIENCED UNEMPLOYED NOT CLASSIFIED BY INDUSTRY' ])


#treemap
fig2 = px.treemap(df_clean, path=[px.Constant("all"), 'iSex', 'dOccup', 'dIndustry'],
                         values='dRpincome', width=800, height=800)
fig2.data[0].textinfo = 'label+text+value'
fig2.update_layout(title_text="Income by gender, occupation, and industry")

#web app layot
app.layout = html.Div(
    children=[
        html.Header(children="US CENSUS 1990 DATA analysis", style={'text-align': 'center', 'fontSize': 48, 'color': 'white'}),
                html.Div([
                    html.H4(children="Ratio of demographic data by gender, marital status, occupation, industry and presence of children", style={'text-align': 'center', 'fontSize': 28, 'color': 'orange'}),
                    dcc.Dropdown(
                        id='my_dropdown',
                        options=[
                            {'label': 'gender', 'value': 'iSex'},
                            {'label': 'marital status', 'value': 'iMarital'},
                            {'label': 'occupation', 'value': 'dOccup'},
                            {'label': 'industry', 'value': 'dIndustry'},
                            {'label': 'children', 'value': 'iFertil'},
                            ],
                        value='iSex',
                        multi=False,
                        clearable=False,
                        style={"width": "50%"}),
                    html.Div([
                            dcc.Graph(id="graph"),
                        ],style={"display": "inline-block", "width": "48%"}),
                    html.Div([
                            dcc.Graph(id="graph-bar"),
                        ],style={"display": "inline-block", "width": "48%"}),
                ]),

                html.Div([
                    dcc.Graph(
                        id='tree-map',
                        figure=fig2)
                    ], style={"display": "inline-block", "width": "48%"}
                 ),

                html.Div([
                    html.H3("Analysis of the income and earnings by occupation, age, gender, marital status", style={'text-align': 'left', 'fontSize': 28, 'color': 'orange'}),
                    html.P("x-axis:"),
                    dcc.Checklist(
                        id='x-axis',
                        options=['dOccup', 'dAge', 'iSex', 'iMarital'],
                        value=['iSex'],
                        inline=True
                    ),
                    html.P("y-axis:"),
                    dcc.RadioItems(
                        id='y-axis',
                        options=['dRearning', 'dRpincome'],
                        value='dRearning',
                        inline=True
                    ),
                    dcc.Graph(id="graph3"),
                    ],style={"display": "inline-block", "width": "48%"}),
        html.P('US census data is 1% of sample of the Public Use Microdata Samples (PUMS) person records drawn from the full 1990 census sample.'),
        html.A('original data download link', href="https://archive.ics.uci.edu/dataset/116/us+census+data+1990")
],
)

@app.callback(
    Output(component_id="graph", component_property="figure"),
    [Input(component_id="my_dropdown", component_property="value")]
)
def generate_chart(my_dropdown):
    dff = df_clean
    fig = px.pie(data_frame=dff, names=my_dropdown,  hole=.3)
    return fig
@app.callback(
    Output(component_id="graph-bar", component_property="figure"),
    [Input(component_id="my_dropdown", component_property="value")]
)
def generate_bar_chart(my_dropdown):
    dff = df_clean
    fig1 = px.bar(data_frame=dff, x=my_dropdown, y="dRearning",
                 barmode="group")

    return fig1

@app.callback(
    Output(component_id="graph3", component_property="figure"),
    Input(component_id="x-axis", component_property="value"),
    Input(component_id="y-axis", component_property="value"))
def generate_chart(x, y):
    df = df_clean
    fig3 = px.box(df, x=x, y=y, width=800, height=800)
    return fig3

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
