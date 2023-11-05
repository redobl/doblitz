import logging

import discord
from discord.ext import commands

from .cogs.character import CharacterCog
from .cogs.game import GameCog
from .help import HelpCommand


def get_bot() -> commands.Bot:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=".", intents=intents)
    bot.help_command = HelpCommand()

    @bot.event
    async def on_ready():
        logger.info(f"We have logged in as {bot.user}")

    @bot.event
    async def on_command(ctx: commands.Context):
        logger.info(f"Command received by {ctx.author.name}: {ctx.message.content}")

    @bot.command(
        name="пинг",
        aliases=["ping"],
        help="Проверяет работоспособность бота.",
        brief="Проверяет работоспособность бота",
    )
    async def ping(ctx):
        await ctx.send("Понг!")

    return bot


async def prepare_bot(bot):
    cogs = (CharacterCog, GameCog)
    for cog in cogs:
        await bot.add_cog(cog())
