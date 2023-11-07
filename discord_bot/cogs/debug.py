from discord.ext import commands
from discord.utils import get

from common.game import MapObject
from common.models import db


class DebugCog(commands.Cog, name="Отладка"):
    @commands.command(
        name="список",
        aliases=["list"],
        help="Показывает список объектов на карте.",
        brief="Показывает список объектов на карте",
    )
    async def map_list(self, ctx):
        to_send = []
        with db.atomic():
            map_objects = MapObject.select()
            for obj in map_objects:
                max_layer = obj.model.layer + obj.model.height
                to_send.append(
                    f"{obj.get_display_name()} ({obj.model.coord_x}, {obj.model.coord_y}, {obj.model.layer} - {max_layer})"
                )
        await ctx.send("```\n" + "\n".join(to_send) + "\n```")

    async def cog_check(self, ctx):
        maintainer_role = get(ctx.guild.roles, name="мейнтейнер бота")
        return maintainer_role in ctx.author.roles
