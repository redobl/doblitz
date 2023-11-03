import peewee

db = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Character(BaseModel):
    name = peewee.CharField()
    player_id = peewee.IntegerField(null=True, index=True)
    hp = peewee.IntegerField(default=100, null=True)
    max_hp = peewee.IntegerField(default=100, null=True)
    active = peewee.BooleanField(default=True)
    coordX = peewee.IntegerField(null=True)
    coordY = peewee.IntegerField(null=True)


def init_db(path: str) -> peewee.Database:
    db.init(database=path)
    db.connect()
    db.create_tables((Character,))
    return db
