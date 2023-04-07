from math import pi, sin, cos, asin, acos
from copy import copy

import numpy as np

from model.model import Point

class Vector:
    def __init__(self, destination = Point(), source = Point()):
        self.dx = destination.x - source.x
        self.dy = destination.y - source.y


    def from_array(self, arr):
        self.dx = arr[0]
        self.dy = arr[1]


    def to_array(self):
        return np.array([self.dx, self.dy])


    def get_length(self):
        return (self.dx ** 2 + self.dy ** 2) ** 0.5


    def set_length(self, length = 1):
        prev_len = self.get_length()
        scale = length / prev_len
        
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

    def angle(self):
        l = self.get_length()
        referent_angle =  asin(self.dy / l)

        if self.dx >= 0:
            return referent_angle
        elif self.dx < 0:
            if referent_angle >= 0:
                diff = pi/2 - referent_angle
            elif referent_angle < 0:
                diff = (-pi/2) - referent_angle
            return 2*diff + referent_angle
    
    def dot(self, another):
        return self.dx * another.dx + self.dy * another.dy


    def angle_between(self, another):
        ratio = self.dot(another) / (self.get_length() * another.get_length())
        
        ratio = max(-1, ratio)
        ratio = min(1, ratio)

        return acos(ratio)


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
    
    def __str__(self):
        return f"({self.dx}, {self.dy}), {self.angle()}°"
    
    def __repr__(self):
        return str(self)

