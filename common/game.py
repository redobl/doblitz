from typing import Optional, get_type_hints

from common.misc import BaseArbitraryModel
from common.models import CharacterModel, GameObjectModel, MapObjectModel


class Game(BaseArbitraryModel):
    in_game_chars: list["Character"]

    @classmethod
    def sync(cls):
        in_game_chars = list(Character.select(CharacterModel.in_game == True))
        cls.in_game_chars = in_game_chars


class Player(BaseArbitraryModel):
    id: int

    def select_characters(self, *criteria) -> list["Character"]:
        return Character.select(CharacterModel.player_id == self.id, *criteria)

    def get_character(self, *criteria) -> "Character":
        return Character.get(CharacterModel.player_id == self.id, *criteria)

    def count_characters(self, *criteria) -> int:
        return Character.count(CharacterModel.player_id == self.id, *criteria)

    def create_character(self, **kwargs) -> "Character":
        return Character.create(player_id=self.id, **kwargs)


class GameObject(BaseArbitraryModel):
    """
    A game object with a database representation.
    """

    model: GameObjectModel

    @classmethod
    def _from_model(cls, model: GameObjectModel) -> "GameObject":
        return cls(model=model)

    @classmethod
    def select(cls, *criteria) -> list["GameObject"]:
        model_type = get_type_hints(cls)["model"]
        if len(criteria) == 0:
            return map(cls._from_model, list(model_type.select()))
        else:
            return map(cls._from_model, list(model_type.select().where(*criteria)))

    @classmethod
    def get(cls, *criteria) -> "GameObject":
        model_type = get_type_hints(cls)["model"]
        return cls._from_model(model_type.get(*criteria))

    @classmethod
    def get_or_create(cls, **kwargs) -> "GameObject":
        model_type = get_type_hints(cls)["model"]
        get_or_create_res = model_type.get_or_create(**kwargs)
        return (cls._from_model(get_or_create_res[0]), get_or_create_res[1])

    @classmethod
    def count(cls, *criteria) -> int:
        model_type = get_type_hints(cls)["model"]
        return model_type.select().where(*criteria).count()

    @classmethod
    def create(cls, **kwargs) -> "GameObject":
        model_type = get_type_hints(cls)["model"]
        return cls._from_model(model_type.create(**kwargs))

    @classmethod
    def clear(cls, *criteria):
        model_type = get_type_hints(cls)["model"]
        if len(criteria) == 0:
            return model_type.delete().execute()
        else:
            return model_type.delete().where(*criteria).execute()

    def delete(self):
        return self.model.delete_instance()


class Character(GameObject):
    model: CharacterModel
    map_object: Optional["MapObject"]

    @classmethod
    def _from_model(cls, model: CharacterModel) -> "Character":
        map_object = MapObject.get_or_create(
            obj_type="character",
            obj_id=model.id,
            defaults={
                "height": 2,
            },
        )[0]
        return cls(model=model, map_object=map_object)

    def delete(self):
        if self.model.in_game:
            Game.in_game_chars.remove(self)
        if self.map_object:
            self.map_object.delete()
        return super().delete()

    def join_game(self):
        self.model.in_game = True
        self.model.save()
        Game.in_game_chars.append(self)

    def leave_game(self):
        self.model.in_game = False
        self.model.save()
        Game.in_game_chars.remove(self)


class MapObject(GameObject):
    """
    An object's representation on the map.
    NOTE: Creation or deletion of a MapObject instance does not create
    or delete a corresponding GameObject instance. Such methods should
    be called on the GameObject instance instead.
    """

    model: MapObjectModel

    def get_game_object(self) -> Optional[GameObject]:
        if self.model.obj_type == "character":
            return Character.get(CharacterModel.id == self.model.obj_id)
        return None

    def get_display_name(self):
        if self.model.name:
            return self.model.name
        game_object = self.get_game_object()
        if game_object and game_object.model.name:
            return game_object.model.name
        return "Что-то"
