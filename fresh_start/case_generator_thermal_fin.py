"""
    Refactored version of the case_generator_thermal_fin.py script
    from the feel++ library.
"""
from liquid import Environment
from liquid import FileSystemLoader
import os
from typing import Optional

def generate_thermal_fin(
    N: int = 4,
    L: float = 2.5,
    d: float = 0.75,
    t: float = 0.25,
    dim: int = 2,
    cylinder: int = 0,
    odir: str = ".",
    output_str: bool = False
) -> Optional[tuple[str, str, str, str]]:
    """
        Generate a thermal fin case

        Parameters
        ----------
        N : int, optional
            number of fins [default=4]
        L : float, optional
            width of a fin [default=2.5]
        d : float, optional
            distance between two fins [default=0.75]
        t : float, optional
            thickness of a fin [default=0.25]
        dim : int, optional
            dimension of the case (2 or 3) [default=2]
        cylinder : int, optional
            shape of fin and post (0=boxes, 1=box/cylinders, 2=cylinders) [default=0]
        odir : str, optional
            output directory [default="."]
        output_str : bool, optional
            if True, return the generated files as strings
            else write the files in the output directory
            [default=False]

        Returns
        -------
        if output_str is True :
            renderGeo : str
                generated fin.geo file
            renderCfg : str
                generated thermal-fin.cfg file
            renderJson : str
                generated thermal-fin.json file
            renderCrbJson : str
                generated thermal-fin-crb.json file
        else :
            None
    """
    if not odir[-1] == "/":
        odir += "/"

    if not os.path.isdir(odir):
        os.mkdir(odir)

    if dim not in ["2","3"]:
        raise ValueError("dimension must be 2 or 3")

    if dim == "3" and cylinder not in [0, 1, 2]:
        raise ValueError("cylinder must be 0, 1 or 2")

    DIRPATH = os.path.dirname(__file__)
    if len(DIRPATH) != 0:
        DIRPATH += '/'

    # Set liquid environment
    env = Environment(loader=FileSystemLoader(DIRPATH + "templates/"))
    templateGeo = env.get_template("fin.geo")
    templateCfg = env.get_template("thermal-fin.cfg")
    templateJson = env.get_template("thermal-fin.json")
    templateCrbJson = env.get_template("thermal-fin-crb.json")

    renderGeo = ""
    renderCfg = ""

    if dim == "2":
        PostShape = "Rectangle"
        PostArgs = "{0, 0, 0, 1, N*(d+t)+t, 0}"
        FinShape = "Rectangle"
        FinArgs = "{-L, r*(d+t), 0, 2*L+1, t, 0}"
        eltDim = "Surface"
        eltDimM1 = "Curve"
        step = 2
        physicalArg = "{r,r+1}"
        diffVal = 4

    else:
        eltDim = "Volume"
        eltDimM1 = "Surface"
       
        if cylinder <= 1:
            PostShape = "Box"
            PostArgs = "{0, 0, 0, 1, 1, N*(d+t)+t}"
        else:
            PostShape = "Cylinder"
            PostArgs = "{0.5, 0.5, 0, 0, 0, N*(d+t)+t, 0.5, 2*Pi}"

        step = 1
        physicalArg = "{ r }"
       
        if cylinder >= 1:
            FinShape = "Cylinder"
            FinArgs = "{0.5, 0.5, r*(d+t), 0, 0, t, L, 2*Pi}"
           
        else:
            FinShape = "Box"
            FinArgs = "{-L, -L, r*(d+t), 2*L+1, 2*L+1, t}"

        diffVal = [5, 5, 17][cylinder]
       
    # Set template variables
    renderGeo = templateGeo.render(
        N = N,
        L = L,
        t = t,
        d = d,
        PostShape = PostShape,
        PostArgs = PostArgs,
        FinShape = FinShape,
        FinArgs = FinArgs,
        step = step,
        physicalArg = physicalArg,
        eltDim = eltDim,
        eltDimM1 = eltDimM1,
        diffVal = diffVal,
    )

    renderCfg = templateCfg.render(
        dim = dim
    )

    fins = list(range(1,int(N)+1))

    renderJson = templateJson.render(
        fins = fins,
        dim = dim
    )

    renderCrbJson = templateCrbJson.render(
        fins = fins,
        dim = dim
    )

    if output_str:
        return renderGeo, renderCfg, renderJson, renderCrbJson
    else:
        # Write files
        with open(odir+"fin.geo", "w") as fileGeo:
            a = fileGeo.write(renderGeo)

        with open(odir+"thermal-fin.cfg", "w") as fileCfg:
            a = fileCfg.write(renderCfg)

        with open(odir+"thermal-fin.json", "w") as fileJson:
            a = fileJson.write(renderJson)

        with open(odir+"thermal-fin-crb.json", "w") as fileCrbJson:
            a = fileCrbJson.write(renderCrbJson)



if __name__ == "__main__":
    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument("--N", help="number of fins [default=4]", type=str, default="4")
    parser.add_argument("--L", help="width of a fin [default=2.5]", type=str, default="2.5")
    parser.add_argument("--d", help="distance between two fins [default=0.75]", type=str, default="0.75")
    parser.add_argument("--t", help="thickness of a fin [default=0.25]", type=str, default="0.25")
    parser.add_argument("--dim", help="dimension of the case (2 or 3) [default=2]", type=str, default="2")
    parser.add_argument("--cylinder", help="shape of fin and post (0=boxes, 1=box/cylinders, 2=cylinders) [default=0]", type=int, default=0)
    parser.add_argument("--odir", help="output directory", type=str, default=".")

    args = parser.parse_args()
    generate_thermal_fin(
        N=args.N,
        L=args.L,
        d=args.d,
        t=args.t,
        dim=args.dim,
        cylinder=args.cylinder,
        odir=args.odir,
        output_str=False
    )