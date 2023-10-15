import argparse
import sys
import json

import feelpp
from feelpp.toolboxes.core import *
from feelpp.toolboxes.heat import *

from case_generator_thermal_fin import generate_thermal_fin


def run_simulation(args):
    feelpp.Environment.setConfigFile("thermal-fin.cfg")
    f = heat(dim=args.dim, order=2)
    simulate(f)
    meas = f.postProcessMeasures().values()

    try:
        import pandas as pd

        df=pd.DataFrame([meas])
    except ImportError:
        print("cannot import pandas, no problem it was just a test")

    return not f.checkResults()

if __name__ == "__main__":
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
    generate_thermal_fin(args)

    # initialize feelpp env 
    sys.argv=['test_heat']
    feelpp_env = feelpp.Environment(sys.argv, config=feelpp.localRepository("feelppdb"),
        opts = toolboxes_options("heat"))
    

    run_simulation(args)
