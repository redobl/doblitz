import logging

import discord
import peewee
from discord.ext import commands

from common.models import Character

from .help import HelpCommand

db = Character._meta.database


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

    @bot.event
    async def on_ready():
        logging.debug(f"We have logged in as {bot.user}")

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
        with db.atomic():
            if len(args) != 1:
                await ctx.send(usage_str(ctx))
                return
            name = args[0]
            character_count = (
                Character.select().where(Character.player_id == ctx.author.id).count()
            )
            if character_count == 0:
                character = Character.create(name=name, player_id=ctx.author.id)
                await ctx.send(f"Персонаж {name} создан.")
            elif character_count == 1:
                character = Character.get(Character.player_id == ctx.author.id)
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
        with db.atomic():
            if len(args) > 1:
                await ctx.send(usage_str(ctx))
                return
            character_count = (
                Character.select().where(Character.player_id == ctx.author.id).count()
            )
            if character_count == 0:
                await ctx.send("У вас нет персонажей.")
                return
            if character_count == 1:
                character = Character.get(Character.player_id == ctx.author.id)
                character.delete_instance()
                await ctx.send(f"Персонаж {character.name} удален.")
                return
            if len(args) == 0:
                await ctx.send("У вас несколько персонажей. " + usage_str(ctx))
                return
            name = args[0]
            try:
                character = Character.get(
                    Character.player_id == ctx.author.id, Character.name == name
                )
                character.delete_instance()
                await ctx.send(f"Персонаж {character.name} удалён.")
            except peewee.DoesNotExist:
                await ctx.send(f"Персонаж {name} не найден.")

    return bot
