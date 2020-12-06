from typing import Union

from pydantic import BaseModel


class CategoryBaseModel(BaseModel):
    id: int


class CategoryModel(CategoryBaseModel):
    name: str
    slug: str
    position: int
    a: Union[str, int]
