from dash import Dash, html, dcc, Input, Output, callback, dash_table
import plotly.graph_objects as go

from skimage import data
from PIL import Image
import base64
from io import BytesIO

import sys

import pandas as pd

import feelpp
from feelpp.toolboxes.core import *
from feelpp.toolboxes.heat import *

from solver import run_simulation, init_env
from case_generator_thermal_fin import generate_thermal_fin

# import pyvista as pv
import plotly.express as px

# Dash app
app = Dash(__name__)


"""
Layout Description
------------------

Inputs:
* Finite element parameters:
  * mesh rafinement size
* Thermal caracteristics of the fin:
  * Bi: Biot number
  * k^i: thermal conductivity of the ith subfin
* Geometrical caracteristics of the subfin:
  * L: length of the fin
  * t: thickness of the fin
* Geometrical caracteristics of the root:
  * Lr: length of the root
  * tr: thickness of the roots

Outputs:

* Finite element mesh
* Temperature distribution
"""

# Layout
app.layout = html.Div([
    html.H1("Thermal Fin Simulation"),
    html.Div([
        html.Label("Number of fins"),
        dcc.Input(id="N", type="number", value=4),
        html.Label("Width of a fin"),
        dcc.Input(id="L", type="number", value=2.5),
        html.Label("Distance between two fins"),
        dcc.Input(id="d", type="number", value=0.75),
        html.Label("Thickness of a fin"),
        dcc.Input(id="t", type="number", value=0.25),
        html.Label("Shape of fin and post"),
        dcc.Dropdown(
            id="cylinder",
            options=[
                {'label': 'Boxes', 'value': 0},
                {'label': 'Box/Cylinders', 'value': 1},
                {'label': 'Cylinders', 'value': 2}
            ],
            value=0
        )
    ], style={'columnCount': 2}),
    html.Div([
        html.Label("Mesh"),
        dcc.Graph(id="mesh"),
    ], style={'columnCount': 2}),
    html.Div(id="temp")
])

# Control
@callback(
    Output("mesh", "figure"),
    Output("temp", "children"),
    Input("N", "value"),
    Input("L", "value"),
    Input("d", "value"),
    Input("t", "value"),
    Input("cylinder", "value"),
)
def update_mesh(N, L, d, t, cylinder):
    generate_thermal_fin(
        N=N, L=L, d=d, t=t, dim="2",
        cylinder=cylinder, odir=".", output_str=False
    )

    meas = run_simulation(dim=2, order=2)

    # img = data.astronaut()  # numpy array
    # pil_img = Image.fromarray(img) # PIL image object
    # prefix = "data:image/png;base64,"
    # with BytesIO() as stream:
    #     pil_img.save(stream, format="png")
    #     base64_string = prefix + base64.b64encode(stream.getvalue()).decode("utf-8")
    # fig = go.Figure(go.Image(source=base64_string))

    
    return html.P(f"Temperature: {meas['temperature']}")


if __name__ == '__main__':
    feelpp_env = init_env()
    app.run_server(debug=True, port=8050)