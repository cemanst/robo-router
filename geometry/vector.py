from math import pi, sin, cos
from copy import copy

import numpy as np

from model.model import Point

class Vector:
    def __init__(self, p1 = Point(), p0 = Point()):
        self.dx = p1.x - p0.x
        self.dy = p1.y - p0.y


    def from_array(self, arr):
        self.dx = arr[0]
        self.dy = arr[1]


    def to_array(self):
        return np.array([self.dx, self.dy])


    def get_length(self):
        return (self.dx ** 2 + self.dy ** 2) ** 0.5


    def set_length(self, length = 1):
        prev_len = self.get_length()
        scale = (length/prev_len) ** 0.5
        
        self.dx *= scale 
        self.dy *= scale


    def shift(self, point, inplace = True):
        if inplace:
            point.x += self.dx
            point.y += self.dy
            return
        else:
            retval = Point()
            retval.x = point.x + self.dx
            retval.y = point.y + self.dy
            return retval


    def rotate(self, angle = pi/2):
        R = np.array([
            [cos(angle), -sin(angle)],
            [sin(angle), cos(angle)]
        ])        
        newx, newy = R @ np.array([ self.dx, self.dy ])

        retval = copy(self)
        retval.dx = newx
        retval.dy = newy
        return retval
    

    def project(self, xaxis, yaxis):
        xaxis = xaxis.to_array()
        yaxis = yaxis.to_array()
        result = self.dx * xaxis + self.dy * yaxis

        retval = Vector()
        retval.from_array(result)
        return retval
        

