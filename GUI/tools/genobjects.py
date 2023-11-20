#!/usr/bin/env python3

import os
import random
import sys
from pathlib import Path

main_dir = Path(os.path.dirname(__file__)) / ".." / ".."
sys.path.insert(1, str(main_dir))
from common.game import MapObject
from common.models import init_db

MAP_SIZE = (3840, 1920)


def main():
    db_path = main_dir / "db.sqlite"
    init_db(db_path)
    MapObject.clear()
    for i in range(10000):
        coords = (random.randint(0, MAP_SIZE[0]), random.randint(0, MAP_SIZE[1]))
        MapObject.create(name=f"Object {i}", coord_x=coords[0], coord_y=coords[1])


if __name__ == "__main__":
    main()
