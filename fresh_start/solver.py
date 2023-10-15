import sys

import pandas as pd

import feelpp
from feelpp.toolboxes.core import *
from feelpp.toolboxes.heat import *

from case_generator_thermal_fin import generate_thermal_fin

# Load feelpp environment
def init_env():
    feelpp_env = feelpp.Environment(
        ['my_app'],
        config=feelpp.localRepository("."),
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
    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument("--N", help="number of fins [default=4]", type=str, default="4")
    parser.add_argument("--L", help="width of a fin [default=2.5]", type=str, default="2.5")
    parser.add_argument("--d", help="distance between two fins [default=0.75]",
                        type=str, default="0.75")
    parser.add_argument("--t", help="thickness of a fin [default=0.25]", type=str,
                        default="0.25")
    parser.add_argument("--dim", help="dimension of the case (2 or 3) [default=2]", type=str,
                        default="2")
    parser.add_argument("--cylinder",
            help="shape of fin and post (0=boxes, 1=box/cylinders, 2=cylinders) [default=0]",
            type=int, default=0)
    parser.add_argument("--odir", help="output directory", type=str, default=".")

    args = parser.parse_args()

    feelpp_env = init_env()

    generate_thermal_fin(
        N=args.N, L=args.L, d=args.d, t=args.t, dim=args.dim,
        cylinder=args.cylinder, odir=args.odir, output_str=False
    )
    meas = run_simulation(dim=args.dim, order=2)

    print("\033[91m Statistics: \033[00m")
    print(meas)