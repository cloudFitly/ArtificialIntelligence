from typing import Union


class Directions:
    """ Actions representing the directions that can be moved. """

    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {NORTH: WEST,
            SOUTH: EAST,
            EAST:  NORTH,
            WEST:  SOUTH,
            STOP:  STOP}

    RIGHT = dict([(y, x) for x, y in list(LEFT.items())])

    REVERSE = {NORTH: SOUTH,
               SOUTH: NORTH,
               EAST: WEST,
               WEST: EAST,
               STOP: STOP}

directions =     {Directions.NORTH: (0, 1),
                  Directions.SOUTH: (0, -1),
                  Directions.EAST:  (1, 0),
                  Directions.WEST:  (-1, 0),
                  Directions.STOP:  (0, 0)}

directions_list = list(directions.items())
print(directions_list)  