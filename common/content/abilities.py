from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Character

from .ability import Ability


class BlinkEye(Ability):
    friendly_name: str = "Моргнуть"
    command: str = "моргнуть"
    ap_cost: int = 1

    def use(self, user: "Character"):
        pass
