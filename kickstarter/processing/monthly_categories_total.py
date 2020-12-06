from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from ..models import CategoryModel, ProjectModel
from . import subscribe


class MonthlyCategoriesTotalsModel:
    def __init__(self, start_year=2009, end_year=2020):
        counter: int = 0
        self.dates: Dict[int, datetime] = dict()
        self._index: Dict[datetime, int] = dict()
        self.categories: Dict[int, Dict[int, int]] = defaultdict(lambda: defaultdict(lambda: 0))

        for year in range(start_year, end_year+1):
            for month in range(1, 13):
                date = datetime(year, month, 1)
                self.dates[counter] = date
                self._index[date] = counter
                counter += 1

    def count(self, project: ProjectModel):
        to_count_date: datetime = datetime(project.state_changed_at.year, project.state_changed_at.month, 1)
        index: int = self._index[to_count_date]
        self.categories[project.id][index] += 1
            


@subscribe
def monthly_categories_totals(
    categories: Dict[int, CategoryModel],
    project: Optional[ProjectModel] = None,
    model: Optional[MonthlyCategoriesTotalsModel] = None,
) -> MonthlyCategoriesTotalsModel:
    if model is None:
        model = MonthlyCategoriesTotalsModel()
    if project is not None:
        model.count(project)
    return model
