from typing import Optional

from pydantic import BaseModel


class BaseObjectModel(BaseModel):
    x: int
    y: int

    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        use_enum_values = True

class MapObjectModel(BaseObjectModel):
    width: int
    height: int

    layer: Optional[int] = None
