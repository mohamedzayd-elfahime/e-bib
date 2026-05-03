from pydantic import BaseModel

class FavoriteIn(BaseModel):
    isbn: str
