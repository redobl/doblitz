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
    game_obj_type = peewee.CharField(null=True)
    game_obj_id = peewee.IntegerField(null=True, index=True)

    # if either of these is null, object is not on map
    location_x = peewee.IntegerField(null=True)
    location_y = peewee.IntegerField(null=True)

    size_x = peewee.IntegerField(default=4)
    size_y = peewee.IntegerField(default=4)

    bottom_layer = peewee.IntegerField(
        default=0, null=True  # null = infinite-height object
    )
    top_layer = peewee.IntegerField(default=0)


class CharacterModel(GameObjectModel):
    name = peewee.CharField(index=True)
    player_id = peewee.IntegerField(null=True, index=True)
    active = peewee.BooleanField(default=True)

    # here null = infinite
    hp = peewee.IntegerField(default=100, null=True)  # Health Points
    max_hp = peewee.IntegerField(default=100, null=True)
    ep = peewee.IntegerField(default=100, null=True)  # Energy Points
    max_ep = peewee.IntegerField(default=100, null=True)
    ap = peewee.IntegerField(default=100, null=True)  # Action Points*100
    max_ap = peewee.IntegerField(default=100, null=True)
    mp = peewee.IntegerField(default=200, null=True)  # Movement Points*100
    max_mp = peewee.IntegerField(default=200, null=True)

    inventory = peewee.CharField(default="{}")
    inventory_size = peewee.IntegerField(default=10)

    abilities = peewee.CharField(default="{}")

    passives = peewee.CharField(default="{}")
    max_passives = peewee.IntegerField(default=10)

    in_game = peewee.BooleanField(default=False)


def init_db(path: str) -> peewee.Database:
    db.init(database=path)
    db.connect()
    db.create_tables((CharacterModel, MapObjectModel))
    return db
