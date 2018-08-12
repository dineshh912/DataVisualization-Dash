import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
import datetime
import pandas_datareader.data as web

app = dash.Dash()

app.layout = html.Div(children= [
    dcc.Input(id = 'input', value='', type='text'),
    html.Div(id = 'output-graph')
    ])

@app.callback(
    Output(component_id = 'output-graph', component_property = 'children'),
    [Input(component_id = 'input', component_property = 'value')]
    )

def update_graph(input_value):
    try:
        start = datetime.datetime(2010, 1, 1)
        end = datetime.datetime.now()

        df = web.DataReader(input_value, 'yahoo', start, end)

        return dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': df.index, 'y': df.Close, 'type': 'line', 'name': input_value},
                    ],
                    'layout': {
                        'title': input_value
                    }
                }
            )
    
    except:
        return 'Ohh Snap!!'

if __name__ == '__main__':
    app.run_server(debug=True)
