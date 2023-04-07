from math import pi, sin, cos

import numpy as np

from model.model import PointType
from geometry.vector import Vector


class Bend:
    def __init__(self, npoints = 9, leaving = True, inner = True):
        angles = np.linspace(pi, pi/2, npoints) if leaving else np.linspace(pi/2, 0, npoints)

        self.vectors = []
        for a in angles:
            v = Vector()
            v.from_array([ cos(a), sin(a) ])
            self.vectors.append(v)
        
        if inner:
            self.vectors_ = self.vectors[1:-1]
    
    def apply(self, xaxis, yaxis, coord_center):
        self.intersteps_ = []
        
        for v in self.vectors_:
            newvec = v.project(xaxis, yaxis)
            int_step = newvec.shift(point = coord_center, inplace = False)
            int_step.type = PointType.SINUOSITY
            int_step.elev = coord_center.elev
            self.intersteps_.append(int_step)
        
        return self.intersteps_
        
        
    

