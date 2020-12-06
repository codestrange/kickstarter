from datetime import datetime

from pydantic import BaseModel

from . import CategoryBaseModel, CreatorBaseModel


class ProjectModel(BaseModel):
    id: int
    name: str
    goal: int
    pledged: int
    state: str
    country: str
    currency: str
    deadline: datetime
    state_changed_at: datetime
    created_at: datetime
    launched_at: datetime
    backers_count: int
    category: CategoryBaseModel
    creator: CreatorBaseModel

    def to_json(self):
        result = self.dict()
        result["deadline"] = self.deadline.timestamp()
        result["state_changed_at"] = self.state_changed_at.timestamp()
        result["created_at"] = self.created_at.timestamp()
        result["launched_at"] = self.launched_at.timestamp()
        return result

    def __eq__(self, o: "ProjectModel") -> bool:
        return self.id == o.id

    def __hash__(self) -> int:
        return self.id
