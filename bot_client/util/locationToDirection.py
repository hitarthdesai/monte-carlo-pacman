from typing import Optional
from gameState import Location, Direction


def location_to_direction(p: Location, n: Location) -> Optional[Direction]:
    try:
        if p.row == n.row:
            if p.col < n.col:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        else:
            if p.row < n.row:
                return Direction.DOWN
            else:
                return Direction.UP
    except:
        return None
