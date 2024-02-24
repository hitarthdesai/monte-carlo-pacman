from gameState import Location, Directions


# TODO: Add caching to this function
def next_move_in_direction(
    current_location: Location, direction: Directions
) -> Location:
    row, col = current_location.row, current_location.col
    new_location = Location(None)

    match direction:
        case Directions.UP:
            col += 1
        case Directions.DOWN:
            col -= 1
        case Directions.LEFT:
            row -= 1
        case Directions.RIGHT:
            row += 1

    new_location.update((row << 8) | col)

    return new_location
