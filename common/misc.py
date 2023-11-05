from pydantic import BaseModel


class BaseArbitraryModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
