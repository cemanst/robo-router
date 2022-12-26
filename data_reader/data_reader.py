from datetime import *

import pandas as pd

from model.model import *

# traj_points = './data/small_inst/traj_points.csv'
# sample_points = './data/small_inst/sample_points.csv'
# init_points = './data/small_inst/init_point.csv'

# traj_points = './data/large_inst/traj_points.csv'
# sample_points = './data/large_inst/sample_points.csv'
# init_points = './data/large_inst/init_point.csv'

traj_points = './data/with_elev/points_allowed.csv'
sample_points = './data/with_elev/random_samping_points.csv'
init_points = './data/with_elev/random_starting_points_with_altitudes.csv'

def read_data():

    rows = []
    ds1 = pd.read_csv(traj_points, header=0)
    for idx, row in ds1.iterrows():
        r = Row()
        r.a = Point()
        r.a.x = row['x_coord_point_1']
        r.a.y = row['y_coord_point_1']
        r.a.elev = row['altitude_point_1']

        r.b = Point()
        r.b.x = row['x_coord_point_2']
        r.b.y = row['y_coord_point_2']
        r.b.elev = row['altitude_point_2']

        if r.a.y > r.b.y:
            r.a.type = PointType.UPPER
            r.b.type = PointType.LOWER
        else:
            r.a.type = PointType.LOWER
            r.b.type = PointType.UPPER

        rows.append(r)

    samples = []
    ds2 = pd.read_csv(sample_points, header=0)
    for idx, row in ds2.iterrows():
        p = Point()
        p.x = row['x_coord']
        p.y = row['y_coord']
        p.elev = row['altitudes']
        p.type = PointType.SAMPLE
        samples.append(p)

    inits = []
    ds3 = pd.read_csv(init_points, header=0)
    for idx, row in ds3.iterrows():
        init = Point()
        init.x = row['x_coord']
        init.y = row['y_coord']
        init.elev = -1
        init.elev = row['altitudes']
        init.type = PointType.INIT
        inits.append(init)

    return rows, samples, inits
