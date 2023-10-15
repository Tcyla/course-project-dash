import sys

import pandas as pd

import feelpp
from feelpp.toolboxes.core import *
from feelpp.toolboxes.heat import *


# Load feelpp environment
def init_env():
    feelpp_env = feelpp.Environment(
        ['my_app'],
        config=feelpp.localRepository(""),
        opts = toolboxes_options("heat")
    )
    return feelpp_env

def run_simulation(dim, order):
    feelpp.Environment.setConfigFile("thermal-fin.cfg")
    f = heat(dim=dim, order=order)
    simulate(f)
    meas = f.postProcessMeasures().values()
    df=pd.DataFrame([meas])
    
    return meas

if __name__=="__main__":
    feelpp_env = init_env()
    run_simulation(dim=2, order=2)