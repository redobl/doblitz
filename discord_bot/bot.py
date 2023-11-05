import logging

import discord
import peewee
from discord.ext import commands

from common.game import Character, Player
from common.models import CharacterModel, db

from .help import HelpCommand


def usage_str(ctx):
    command = ctx.command
    if len(command.aliases) > 0:
        aliases = "|".join(command.aliases)
        return (
            f"Использование: `{ctx.prefix}[{command.name}|{aliases}] {command.usage}`"
        )
    else:
        return f"Использование: `{ctx.prefix}{command.name} {command.usage}`"


def get_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=".", intents=intents)
    bot.help_command = HelpCommand()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

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

    @bot.command(
        name="создать",
        aliases=["create"],
        help="Создает персонажа.",
        brief="Создает персонажа",
        usage="<имя персонажа>",
    )
    async def create(ctx, *args):
        player = Player(id=ctx.author.id)
        if len(args) != 1:
            await ctx.send(usage_str(ctx))
            return
        name = args[0]
        with db.atomic():
            character_count = player.count_characters()
            if character_count == 0:
                player.create_character(name=name)
                await ctx.send(f"Персонаж {name} создан.")
            elif character_count == 1:
                character = player.get_character()
                await ctx.send(f"У вас уже есть персонаж {character.name}.")
            else:
                await ctx.send("У вас уже есть персонажи.")

    @bot.command(
        name="удалить",
        aliases=["delete"],
        help="Удаляет персонажа.",
        brief="Удаляет персонажа",
        usage="[имя персонажа]",
    )
    async def delete(ctx, *args):
        player = Player(id=ctx.author.id)
        if len(args) > 1:
            await ctx.send(usage_str(ctx))
            return
        elif len(args) == 1:
            name = args[0]
            with db.atomic():
                try:
                    character = player.get_character(CharacterModel.name == name)
                    character.delete()
                    await ctx.send(f"Персонаж {character.name} удалён.")
                except peewee.DoesNotExist:
                    await ctx.send(f"Персонаж {name} не найден.")
        else:
            with db.atomic():
                character_count = player.count_characters()
                if character_count == 0:
                    await ctx.send("У вас нет персонажей.")
                    return
                if character_count == 1:
                    character = player.get_character()
                    character.delete()
                    await ctx.send(f"Персонаж {character.name} удален.")
                    return
                await ctx.send("У вас несколько персонажей. " + usage_str(ctx))

    return bot
