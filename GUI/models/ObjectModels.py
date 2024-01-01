from typing import Optional

from pydantic import BaseModel


class BaseObjectModel(BaseModel):
    location_x: int
    location_y: int

    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        use_enum_values = True

class MapObjectModel(BaseObjectModel):
    size_x: int
    size_y: int

    layer: Optional[int] = None
