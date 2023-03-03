from copy import copy
from model.model import Point

class Vector:
    def __init__(self, p1 = Point(), p0 = Point()):
        self.dx = p1.x - p0.x
        self.dy = p1.y - p0.y
    
    def get_length(self):
        return (self.dx ** 2 + self.dy ** 2) ** 0.5
    
    def set_length(self, length = 1):
        prev_len = self.get_length()
        scale = (length/prev_len) ** 0.5
        
        self.dx *= scale 
        self.dy *= scale
    
    def shift(self, point):
        point.x += self.dx
        point.y += self.dy
