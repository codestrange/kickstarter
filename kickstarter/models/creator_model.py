from pydantic import BaseModel


class CreatorBaseModel(BaseModel):
    id: int


class CreatorModel(CreatorBaseModel):
    id: int
    name: str

    def to_json(self):
        return self.dict()
