from typing import Self

from common.misc import BaseArbitraryModel


class Content(BaseArbitraryModel):
    friendly_name: str

    def to_dict(self) -> dict:
        return NotImplementedError()

    @classmethod
    def from_dict(cls, dict_: dict) -> Self:
        if dict_["class"] != cls.__name__:
            raise Exception(
                f"wrong content class, expected {cls.__name__}, got {dict_['class']}"
            )
        return cls()
