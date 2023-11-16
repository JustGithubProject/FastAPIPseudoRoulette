from pydantic import BaseModel


class RouletteCellCreate(BaseModel):
    weight: int
