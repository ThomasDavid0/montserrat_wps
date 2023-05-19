from geometry import Point, GPS, PZ
import numpy as np
import pandas as pd
from flightplotting.plots import create_3d_plot
from flightplotting.traces import trace3d
import plotly.graph_objects as go



def plot_wpxys(ps: Point):
    fig = create_3d_plot(trace3d(ps.x, -ps.y, -ps.z))

    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[950], mode="markers"))
    fig.show()
    

if __name__ == "__main__":

    with open("vertical_xsection_without_auto_takeoff.txt", "r") as f:
        data = [l.split()[8:11] for l in f.readlines()[1:]]
        
    df = pd.DataFrame(data, columns=["lat", "long", "alt"]).astype(float)

    top = GPS(16.71036180777751, -62.1768528125355)

    points = GPS(df.iloc[:,:2])

    xyz = (points - top) - PZ(1) * df.alt.to_numpy()

    fig = create_3d_plot(trace3d(xyz.x, -xyz.y, -xyz.z))

    fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[950], mode="markers"))

    fig.show()

