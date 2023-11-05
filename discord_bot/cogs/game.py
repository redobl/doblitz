import logging

import discord
import peewee
from discord.ext import commands

from common.game import Character, Game, Player
from common.models import CharacterModel, db

from ..help import HelpCommand, usage_str
from .character import CharacterCog


class GameCog(commands.Cog, name="Игра"):
    @commands.command(
        name="войти",
        aliases=["join"],
        help="Входит в игру.",
        brief="Входит в игру",
        usage="[имя персонажа]",
    )
    async def join(self, ctx, *args):
        player = Player(id=ctx.author.id)
        if len(args) > 1:
            await ctx.send(usage_str(ctx))
            return
        elif len(args) == 1:
            name = args[0]
            with db.atomic():
                try:
                    character = player.get_character(CharacterModel.name == name)
                    if character.model.in_game:
                        await ctx.send(f"Персонаж {character.model.name} уже в игре.")
                    else:
                        character.join_game()
                        await ctx.send(
                            f"Персонаж {character.model.name} входит в игру."
                        )
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
                    if character.model.in_game:
                        await ctx.send(f"Персонаж {character.model.name} уже в игре.")
                    else:
                        character.join_game()
                        await ctx.send(
                            f"Персонаж {character.model.name} входит в игру."
                        )
                    return
                await ctx.send("У вас несколько персонажей. " + usage_str(ctx))

    @commands.command(
        name="выйти",
        aliases=["leave"],
        help="Выходит из игры.",
        brief="Выходит из игры",
        usage="[имя персонажа]",
    )
    async def leave(self, ctx, *args):
        player = Player(id=ctx.author.id)
        if len(args) > 1:
            await ctx.send(usage_str(ctx))
            return
        elif len(args) == 1:
            name = args[0]
            with db.atomic():
                try:
                    character = player.get_character(CharacterModel.name == name)
                    if not character.model.in_game:
                        await ctx.send(f"Персонаж {character.model.name} не в игре.")
                    else:
                        character.leave_game()
                        await ctx.send(
                            f"Персонаж {character.model.name} выходит из игры."
                        )
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
                    if not character.model.in_game:
                        await ctx.send(f"Персонаж {character.model.name} не в игре.")
                    else:
                        character.leave_game()
                        await ctx.send(
                            f"Персонаж {character.model.name} выходит из игры."
                        )
                    return
                await ctx.send("У вас несколько персонажей. " + usage_str(ctx))
