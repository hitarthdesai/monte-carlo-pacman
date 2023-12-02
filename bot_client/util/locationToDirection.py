from typing import Optional
from gameState import Location, Directions


def location_to_direction(p: Location, n: Location) -> Directions:
    try:
        if p.row == n.row:
            if p.col < n.col:
                return Directions.RIGHT
            else:
                return Directions.LEFT
        else:
            if p.row < n.row:
                return Directions.DOWN
            else:
                return Directions.UP
    except:
        return Directions.NONE
