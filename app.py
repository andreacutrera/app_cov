import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv')
#to see how many death every day--------------------------------------------------------------

n=0
df['nuovi_deceduti'] = df['deceduti'][n]
n=1
while n<len(df.tamponi):
    df['nuovi_deceduti'][n] = df['deceduti'][n]-df['deceduti'][n-1]
    n +=1

positivi = df.nuovi_positivi
positivi.index = pd.date_range("2020-02-24", freq="D", periods=len(positivi))
deceduti = df.nuovi_deceduti
deceduti.index = pd.date_range("2020-02-24", freq="D", periods=len(positivi))

app = dash.Dash()
regioni = pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv', index_col=0, parse_dates=True)

# Creates a list of dictionaries, which have the keys 'label' and 'value'.
def get_options(regioni):
    dict_list = []
    for i in np.unique(regioni['denominazione_regione']):
        dict_list.append({'label': i, 'value': i})

    return dict_list


app.layout = html.Div([

    html.H1("Covid-19-Italy",
            style={
                'textAlign': 'center',
                'color': '#008080'
            }),

    html.Div("A dashboard to quickly visualize data",
             style={
                 'textAlign': 'center',
                 'color': '#008080'
             }),

    html.Div(className='div-for-dropdown',
             children=[
                 dcc.Dropdown(id='regionselector',
                              options=get_options(regioni),
                              multi=True,
                              value=[regioni['nuovi_positivi'].sort_values()[0]],
                              style={'backgroundColor': '#1E1E1E'},
                              className='stockselector')
             ],
             style={'color': '#1E1E1E'}),

    dcc.Graph(
        id='positives',
        figure={
            'data': [
                {'x': positivi.index,
                 'y': positivi.values,
                 'type': 'bar',
                 'name': 'First_Chart'}
            ],
            'layout': {
                'plot_bgcolor': '#f0ffff',
                'paper_bgcolor': '#f0f8ff',
                'font': {
                    'color': '#008080',

                },
                'title': 'Daily Positives'
            }
        }

    ),
    dcc.Graph(
        id='deaths',
        figure={
            'data': [
                {'x': deceduti.index,
                 'y': deceduti.values,
                 'type': 'line',
                 'name': 'Second_chart'}
            ],
            'layout': {
                'plot_bgcolor': '#f0ffff',
                'paper_bgcolor': '#f0f8ff',
                'font': {
                    'color': '#008080',

                },
                'title': 'Daily deaths'
            }
        }

    ),
    html.H1("by Andrea Cutrera",
            style={
                'textAlign': 'center',
                'color': '#008080'
            })
])

if __name__ == '__main__':
    app.run_server(port=4050)