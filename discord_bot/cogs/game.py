import peewee
from discord.ext import commands

from common.game import Player
from common.models import CharacterModel, db

from ..help import usage_str


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
        with db.atomic():
            if len(args) == 1:
                name = args[0]
                try:
                    character = player.get_character(CharacterModel.name == name)
                except peewee.DoesNotExist:
                    await ctx.send(f"Персонаж {name} не найден.")
                    return
            else:
                character_count = player.count_characters()
                if character_count == 0:
                    await ctx.send("У вас нет персонажей.")
                    return
                elif character_count == 1:
                    character = player.get_character()
                else:
                    await ctx.send("У вас несколько персонажей. " + usage_str(ctx))
                    return
            if character.model.in_game:
                await ctx.send(f"Персонаж {character.model.name} уже в игре.")
                return
            try:
                character.get_mapobject()
            except peewee.DoesNotExist:
                await ctx.send(f"Персонаж {character.model.name} не на карте.")
            else:
                character.join_game()
                await ctx.send(f"Персонаж {character.model.name} входит в игру.")

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
        with db.atomic():
            if len(args) == 1:
                name = args[0]
                try:
                    character = player.get_character(CharacterModel.name == name)
                except peewee.DoesNotExist:
                    await ctx.send(f"Персонаж {name} не найден.")
                    return
            else:
                character_count = player.count_characters()
                if character_count == 0:
                    await ctx.send("У вас нет персонажей.")
                    return
                elif character_count == 1:
                    character = player.get_character()
                else:
                    await ctx.send("У вас несколько персонажей. " + usage_str(ctx))
                    return
            if not character.model.in_game:
                await ctx.send(f"Персонаж {character.model.name} не в игре.")
            else:
                character.leave_game()
                await ctx.send(f"Персонаж {character.model.name} выходит из игры.")
