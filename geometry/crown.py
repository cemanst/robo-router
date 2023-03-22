from math import pi, sin, cos

import numpy as np

from model.model import PointType
from geometry.vector import Vector


class Crown:
    def __init__(self, npoints = 9, inner = True):
        angles = np.linspace(0, pi, npoints)
        self.vectors = []
        for a in angles:
            v = Vector()
            v.from_array([ cos(a), sin(a) ])
            self.vectors.append(v)
        
        self.vectors.reverse()
        if inner:
            self.vectors = self.vectors[1:-1]
    
    def apply(self, xaxis, yaxis, coord_center):
        self.intersteps = []
        for v in self.vectors:
            newvec = v.project(xaxis, yaxis)
            int_step = newvec.shift(point = coord_center, inplace = False)
            int_step.type = PointType.SINUOSITY
            self.intersteps.append(int_step)
        
        return self.intersteps
        
        
    

