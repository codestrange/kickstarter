from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from ..models import CategoryModel, ProjectModel
from . import subscribe


class MonthlyCategoriesSuccessModel:
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
        self.categories[project.id][index] += 1 if project.state == "successful" else 0
            


@subscribe
def monthly_categories_success(
    categories: Dict[int, CategoryModel],
    project: Optional[ProjectModel] = None,
    model: Optional[MonthlyCategoriesSuccessModel] = None,
) -> MonthlyCategoriesSuccessModel:
    if model is None:
        model = MonthlyCategoriesSuccessModel()
    if project is not None:
        model.count(project)
    return model
