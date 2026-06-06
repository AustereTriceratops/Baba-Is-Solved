from typing import Final

# 0: empty
# 1: goal
# 2: wall
# >= 3: pushable
# 3: box
# 4: wall text
# 5: is stop text

EMPTY: Final = 0
GOAL: Final = 1
WALL: Final = 2
WATER: Final = 3
BOX: Final = 4
WALL_TXT: Final = 5
WATER_TXT: Final = 6
BOX_TXT: Final = 7
STOP_TXT: Final = 8
PUSH_TXT: Final = 9
SINK_TXT: Final = 10
WIN_TXT: Final = 11
TILE_CAP: Final = 12
