from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from ..game import Character

from ..misc import BaseArbitraryModel
from .content import Content


class Ability(Content):
    command: str
    ap_cost: int = 0
    mp_cost: int = 0

    def use(self, user: "Character"):
        raise NotImplementedError()

    def to_dict(self) -> dict:
        return {
            "type": "ability",
            "class": type(self).__name__,
            "ap_cost": self.ap_cost,
            "mp_cost": self.mp_cost,
        }

    @classmethod
    def from_dict(cls, dict_: dict) -> Self:
        ability = super().from_dict(dict_)
        ability.ap_cost = dict_["ap_cost"]
        ability.mp_cost = dict_["mp_cost"]
