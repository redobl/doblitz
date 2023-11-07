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
    def count(cls, *criteria) -> int:
        model_type = get_type_hints(cls)["model"]
        return model_type.select().where(*criteria).count()

    @classmethod
    def create(cls, **kwargs) -> "GameObject":
        model_type = get_type_hints(cls)["model"]
        return cls._from_model(model_type.create(**kwargs))

    def delete(self):
        return self.model.delete_instance()


class Character(GameObject):
    model: CharacterModel

    def delete(self):
        if self.model.in_game:
            Game.in_game_chars.remove(self)
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
    model: MapObjectModel
    game_object: Optional[GameObject]

    @classmethod
    def _from_model(cls, model: GameObjectModel) -> GameObject:
        if model.obj_type == "character":
            game_object = Character.get(CharacterModel.id == model.obj_id)
        else:
            game_object = None
        return cls(model=model, game_object=game_object)

    def delete(self):
        if self.game_object:
            self.game_object.delete()
        return super().delete()

    def get_display_name(self):
        if self.game_object and self.game_object.model.name:
            return self.game_object.model.name
        if self.model.name:
            return self.model.name
        return "Что-то"
