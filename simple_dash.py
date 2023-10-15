from dash import Dash, html, dcc, Input, Output
import numpy as np

app = Dash(__name__, external_stylesheets=['myStyle.css'])

app.layout = html.Div([
    html.H1('Simple Dash App'),
    dcc.Slider(id='input', min=0, max=30, step=.5, value=3),
    dcc.Graph(id='output-graph')
])

@app.callback(
    Output(component_id='output-graph', component_property='figure'),
    [Input(component_id='input', component_property='value')]
)
def update_output_div(input_value):
    try:
        bi = float(input_value)
        x = np.linspace(-3, 3, 1000)
        y = np.sin(bi*x)
        return {
            'data': [
                {'x': x, 'y': y, 'type': 'line', 'name': 'sin(x)'},
            ],
            'layout': {
                'title': f'Sin function between 0 and {bi}',
                'xaxis': {'title': 'x'},
                'yaxis': {'title': 'sin(x)'}
            }
        }
    except ValueError:
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)