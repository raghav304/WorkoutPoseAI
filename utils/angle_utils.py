import math

def calculate_angle(a, b, c):
    """
    Returns the angle between points a, b, c, at point b.
    a, b, c are (x, y) tuples.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c

    ba = (ax - bx, ay - by)
    bc = (cx - bx, cy - by)

    dot = ba[0]*bc[0] + ba[1]*bc[1]
    mag_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)

    if mag_ba == 0 or mag_bc == 0:
        return 0

    angle = math.acos(dot / (mag_ba * mag_bc))
    return math.degrees(angle)
