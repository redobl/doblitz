from common.misc import BaseArbitraryModel
from common.models import CharacterModel


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


class Character(BaseArbitraryModel):
    model: CharacterModel
    name: str

    @classmethod
    def _from_model(cls, model: CharacterModel) -> "Character":
        return cls(model=model, name=model.name)

    @classmethod
    def select(cls, *criteria) -> "Character":
        return [cls._from_model(m) for m in CharacterModel.select().where(*criteria)]

    @classmethod
    def get(cls, *criteria) -> "Character":
        return cls._from_model(CharacterModel.get(*criteria))

    @classmethod
    def count(cls, *criteria) -> int:
        return CharacterModel.select().where(*criteria).count()

    @classmethod
    def create(cls, **kwargs) -> "Character":
        return cls._from_model(CharacterModel.create(**kwargs))

    def delete(self):
        self.model.delete_instance()
        if self.model.in_game:
            Game.in_game_chars.remove(self)

    def join_game(self):
        self.model.in_game = True
        self.model.save()
        Game.in_game_chars.append(self)

    def leave_game(self):
        self.model.in_game = False
        self.model.save()
        Game.in_game_chars.remove(self)
