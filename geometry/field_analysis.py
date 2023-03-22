from model.model import Point

from geometry.vector import Vector


def mean_row_width(rows):
    first_row = rows[0]
    last_row = rows[-1]

    dist_a = Vector(first_row.a, last_row.a)
    dist_b = Vector(first_row.b, last_row.b)

    return (dist_a.get_length() + dist_b.get_length()) / (2*len(rows))


def locate_centroid(rows):
    first_row = rows[0]
    last_row = rows[-1]
    
    corners = [first_row.a, first_row.b, last_row.a, last_row.b]
    centroid = Point()
    for c in corners:
        centroid.x += c.x / 4
        centroid.y += c.y / 4 # centroid of a field used to detect side of initial point
    return centroid