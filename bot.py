#!/usr/bin/env python3

import asyncio
import configparser
import logging
import os
from pathlib import Path

from common.game import Game
from common.models import init_db
from discord_bot.bot import get_bot, prepare_bot


def main():
    logging.basicConfig(level=logging.WARNING)
    config = configparser.ConfigParser()
    config_path = Path(os.path.dirname(__file__)) / "config.ini"
    db_path = Path(os.path.dirname(__file__)) / "db.sqlite"
    config.read(config_path)
    init_db(db_path)
    Game.sync()
    bot = get_bot()
    asyncio.run(prepare_bot(bot))
    bot.run(config["bot"]["token"], log_handler=None)


if __name__ == "__main__":
    main()
