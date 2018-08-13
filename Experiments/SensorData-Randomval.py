import dash
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader.data import DataReader
import time
from collections import deque
import plotly.graph_objs as go
import random

app = dash.Dash('Sensor Data')

max_length = 50
times = deque(maxlen=max_length)
room_temp = deque(maxlen=max_length)
footfall  = deque(maxlen=max_length)
humidity = deque(maxlen=max_length)
water_level = deque(maxlen=max_length)

data_dict = {"Room Temperature":room_temp,
"footfall count": footfall,
"humidity": humidity,
"Water Level":water_level}


def update_obd_values(times, room_temp, footfall, humidity, water_level):

    times.append(time.time())
    if len(times) == 1:
        #starting relevant values
        room_temp.append(random.randrange(18,50))
        footfall.append(random.randrange(0,1000))
        humidity.append(random.randrange(40,60))
        water_level.append(random.randrange(1000,9500))
    else:
        for data_of_interest in [room_temp, footfall, humidity, water_level]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))

    return times, room_temp, footfall, humidity, water_level

times, room_temp, footfall, humidity, water_level = update_obd_values(times, room_temp, footfall, humidity, water_level)

app.layout = html.Div([
    html.Div([
        html.H2('Sensor Data',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='sensor-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Room Temperature'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('sensor-data-name', 'value')],
    events=[dash.dependencies.Event('graph-update', 'interval')]
    )

def update_graph(data_names):
    graphs = []
    update_obd_values(times, room_temp, footfall, humidity, water_level)
    if len(data_names)>2:
        class_choice = 'col s12 m6 l4'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 l6'
    else:
        class_choice = 'col s12'


    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs



external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-rc.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=True)
