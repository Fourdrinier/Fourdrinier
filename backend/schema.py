from pydantic import BaseModel


class PlaysetCreateSchema(BaseModel):
    name: str
