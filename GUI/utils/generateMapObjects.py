#!/usr/bin/env python3

import os
import random
import sys
from pathlib import Path

main_dir = Path(os.path.dirname(__file__)) / ".." / ".."
sys.path.insert(1, str(main_dir))
from common.game import MapObject
from common.models import init_db
from GUI.utils.progressBar import progressBar

MAP_SIZE = (3840, 1920)


def main():
    db_path = main_dir / "db.sqlite"
    init_db(db_path)
    MapObject.clear()
    for i in progressBar(range(10000), "Generating: "):
        coords = (random.randint(0, MAP_SIZE[0]), random.randint(0, MAP_SIZE[1]))
        bottom_layer = random.randint(0, 128)
        MapObject.create(
            name=f"Object {i}", 
            location_x=coords[0], 
            location_y=coords[1],
            bottom_layer=bottom_layer,
            top_layer=bottom_layer + random.randint(0, 5),
            height=random.randint(0, 2)
        )


if __name__ == "__main__":
    main()
