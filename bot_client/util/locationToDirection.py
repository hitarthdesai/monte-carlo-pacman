from typing import Optional
from gameState import Location, Directions


def location_to_direction(p: Location, n: Location) -> Directions:
    try:
        if p.row == n.row and p.col == n.col:
            return Directions.NONE

        if p.row == n.row:
            if p.col < n.col:
                return Directions.RIGHT
            else:
                return Directions.LEFT

        if p.col == n.col:
            if p.row < n.row:
                return Directions.DOWN
            else:
                return Directions.UP

        return Directions.NONE
    except:
        return Directions.NONE
