import json
from typing import Union

from . import abilities
from .ability import Ability
from .content import Content


def dict_to_content(dict_: dict) -> Content:
    content_type = dict_["type"]
    cls = dict_["class"]
    if content_type == "ability":
        return getattr(abilities, cls).from_dict(dict_)


def content_list_to_json(list_: list[Content]) -> str:
    content_dict_list = []
    for c in list_:
        content_dict_list.append(c.to_dict())
    return json.dumps(content_dict_list)


def json_to_content_list(json_: str) -> list[Content]:
    content_dict_list = json.loads(json_)
    content_list = []
    for cd in content_dict_list:
        content_list.append(dict_to_content(cd))
    return content_list


def default_abilities() -> list[Ability]:
    return [abilities.BlinkEye()]
