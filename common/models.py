import peewee
from playhouse.sqlite_ext import AutoIncrementField, SqliteExtDatabase

db = SqliteExtDatabase(None)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class GameObjectModel(BaseModel):
    id = AutoIncrementField()
    name = peewee.CharField(null=True, index=True)
    description = peewee.CharField(null=True)

    effects = peewee.CharField(default="{}")
    extra = peewee.CharField(default="{}")


class MapObjectModel(GameObjectModel):
    obj_type = peewee.CharField(null=True, index=True)
    obj_id = peewee.IntegerField(null=True, index=True)

    coord_x = peewee.IntegerField(null=True)
    coord_y = peewee.IntegerField(null=True)
    layer = peewee.IntegerField(default=0, null=True)

    sizeX = peewee.IntegerField(default=4)
    sizeY = peewee.IntegerField(default=4)
    height = peewee.IntegerField(default=0)


class CharacterModel(GameObjectModel):
    name = peewee.CharField(index=True)
    player_id = peewee.IntegerField(null=True, index=True)
    active = peewee.BooleanField(default=True)

    hp = peewee.IntegerField(default=100, null=True)
    max_hp = peewee.IntegerField(default=100, null=True)
    ap = peewee.IntegerField(default=100, null=True)
    max_ap = peewee.IntegerField(default=100, null=True)

    inventory = peewee.CharField(default="{}")
    inventory_size = peewee.IntegerField(default=10)

    abilities = peewee.CharField(default="{}")
    max_abilities = peewee.IntegerField(default=10)

    in_game = peewee.BooleanField(default=False)


def init_db(path: str) -> peewee.Database:
    db.init(database=path)
    db.connect()
    db.create_tables((CharacterModel, MapObjectModel))
    return db
