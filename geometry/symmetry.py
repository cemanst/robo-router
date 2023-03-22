from math import pi

from model.model import Point
from geometry.vector import Vector


def symmetry(A, B):
    middle = Point()
    middle.x = (A.x + B.x) / 2
    middle.y = (A.y + B.y) / 2

    direction = Vector(B, middle)

    p1 = direction.rotate(angle= pi/2).shift(point=middle, inplace=False)
    p2 = direction.rotate(angle= -pi/2).shift(point=middle, inplace=False)

    return p1, middle, p2
