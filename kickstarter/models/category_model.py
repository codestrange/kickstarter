from pydantic import BaseModel


class CategoryBaseModel(BaseModel):
    id: int


class CategoryModel(CategoryBaseModel):
    name: str
    translation: str
    position: int

    def to_json(self):
        return self.dict()

    def __eq__(self, o: "CategoryModel") -> bool:
        return self.id == o.id

    def __hash__(self) -> int:
        return self.id
