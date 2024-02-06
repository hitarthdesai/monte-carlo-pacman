from gameState import Directions


def direction_to_elec_move(dir: Directions) -> Directions:
    match dir:
        case Directions.UP:
            return "N"
        case Directions.LEFT:
            return "W"
        case Directions.DOWN:
            return "S"
        case Directions.RIGHT:
            return "E"
        case Directions.NONE:
            return "NONE"
