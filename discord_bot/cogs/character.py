import peewee
from discord.ext import commands

from common.game import Player
from common.models import CharacterModel, db

from ..help import usage_str


class CharacterCog(commands.Cog, name="Персонаж"):
    @commands.command(
        name="создать",
        aliases=["create"],
        help="Создает персонажа.",
        brief="Создает персонажа",
        usage="<имя персонажа>",
    )
    async def create(self, ctx, *args):
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
                await ctx.send(f"У вас уже есть персонаж {character.model.name}.")
            else:
                await ctx.send("У вас уже есть персонажи.")

    @commands.command(
        name="удалить",
        aliases=["delete"],
        help="Удаляет персонажа.",
        brief="Удаляет персонажа",
        usage="[имя персонажа]",
    )
    async def delete(self, ctx, *args):
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
                    await ctx.send(f"Персонаж {character.model.name} удалён.")
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
                    await ctx.send(f"Персонаж {character.model.name} удален.")
                    return
                await ctx.send("У вас несколько персонажей. " + usage_str(ctx))
