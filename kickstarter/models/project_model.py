from datetime import datetime

from pydantic import BaseModel

from . import CategoryBaseModel, CreatorBaseModel


class ProjectModel(BaseModel):
    id: int
    name: str
    blurb: str
    goal: int
    pladged: int
    state: str
    slug: str
    disable_comunication: bool
    coutry: str
    currency: str
    currency_symbol: str
    currency_trailing_code: bool
    deadline: datetime
    state_changed_at: datetime
    created_at: datetime
    launched_at: datetime
    backers_count: int
    category: CategoryBaseModel
    creator: CreatorBaseModel
