#!/usr/bin/env python3

import configparser
import logging
import os
from pathlib import Path

from common.models import init_db
from discord_bot.bot import get_bot


def main():
    logging.basicConfig(level=logging.DEBUG)
    config = configparser.ConfigParser()
    config_path = Path(os.path.dirname(__file__)) / "config.ini"
    db_path = Path(os.path.dirname(__file__)) / "db.sqlite"
    config.read(config_path)
    init_db(db_path)
    bot = get_bot()
    bot.run(config["bot"]["token"])


if __name__ == "__main__":
    main()
