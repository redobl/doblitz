import peewee

db = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Character(BaseModel):
    name = peewee.CharField()
    player_id = peewee.IntegerField(null=True, index=True)
    active = peewee.BooleanField(default=True)

    hp = peewee.IntegerField(default=100, null=True)
    max_hp = peewee.IntegerField(default=100, null=True)
    ap = peewee.IntegerField(default=100, null=True)
    max_ap = peewee.IntegerField(default=100, null=True)

    coordX = peewee.IntegerField(null=True)
    coordY = peewee.IntegerField(null=True)
    layer = peewee.IntegerField(default=0, null=True)

    sizeX = peewee.IntegerField(default=4)
    sizeY = peewee.IntegerField(default=4)
    height = peewee.IntegerField(default=2)

    inventory = peewee.CharField(default="{}")
    inventorySize = peewee.IntegerField(default=10)

    abilities = peewee.CharField(default="{}")
    maxAbilities = peewee.IntegerField(default=10)

    effects = peewee.CharField(default="{}")
    extra = peewee.CharField(default="{}")


def init_db(path: str) -> peewee.Database:
    db.init(database=path)
    db.connect()
    db.create_tables((Character,))
    return db
