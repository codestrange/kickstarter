from pydantic import BaseModel


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
    deadline: int
    state_changed_at: int
    created_at: int
    launched_at: int
    backers_count: int
