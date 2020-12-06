from pydantic import BaseModel


class CreatorBaseModel(BaseModel):
    id: int


class CreatorModel(CreatorBaseModel):
    id: int
    name: str

    def to_json(self):
        return self.dict()

    def __eq__(self, o: "CreatorModel") -> bool:
        return self.id == o.id

    def __hash__(self) -> int:
        return self.id
