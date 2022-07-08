from datetime import *

import pandas as pd

from model import Row, Point


def read_data():

    rows = []
    ds1 = pd.read_csv('/data/traj_points.csv', header=0)
    for row in ds1.iterrows():
        r = Row()
        r.a = Point()
        r.a.x = row['x_coord_point_1']
        r.a.y = row['y_coord_point_1']
        r.b.x = row['x_coord_point_2']
        r.b.y = row['y_coord_point_2']
        rows.append(r)

    samples = []
    ds2 = pd.read_csv('/data/sample_points.csv', header=0)
    for row in ds2.iterrows():
        p = Point()
        p.x = row['x_coord']
        p.y = row['y_coord']
        samples.append(p)

    init = Point()
    ds3 = pd.read_csv('/data/init_point.csv', header=0)
    for row in ds3.iterrows():
        init.x = row['x_coord']
        init.y = row['y_coord']

    return rows, samples, init
