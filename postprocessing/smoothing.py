from model.model import PointType


from geometry.field_analysis import locate_centroid, mean_row_width
from geometry.polygon import sinuosity

def insert_sinuosities(solution, rows):
    centroid = locate_centroid(rows)
    width = mean_row_width(rows)

    previous = solution[0]
    retval = [previous]
    for current in solution[1:]:
        if previous.type in [PointType.LOWER, PointType.UPPER] and previous.type == current.type:
            intersteps = sinuosity(previous, current, centroid, width)
            for ist in intersteps:
                retval.append(ist)

        retval.append(current)
        previous = current
    
    return retval

