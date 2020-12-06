from pydantic import BaseModel


class CategoryBaseModel(BaseModel):
    id: int


class CategoryModel(CategoryBaseModel):
    name: str
    slug: str
    position: int

    def to_json(self):
        return self.dict()
