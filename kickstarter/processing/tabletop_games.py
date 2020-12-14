from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from ..models import CategoryModel, ProjectModel
from . import subscribe


class TabletopGamesModel:
    def __init__(
        self,
        category_id: int = 34,
        start_year: int = 2009,
        end_year: int = 2020,
    ):
        self.category_id = category_id
        self.projects: List[ProjectModel] = []
        self.dates: Dict[int, datetime] = dict()
        self._index: Dict[datetime, int] = dict()
        counter = 0
        for year in range(start_year, end_year + 1):
            date = datetime(year, 1, 1)
            self.dates[counter] = date
            self._index[date] = counter
            counter += 1
        self.date_list = [self.dates[i] for i, _ in enumerate(self.dates)]

    def is_tabletop_game(self, project: ProjectModel) -> bool:
        return project.category.id == self.category_id

    def add_project(self, project: ProjectModel):
        self.projects.append(project)

    def pleged_by_year(self) -> Tuple[List[datetime], List[int]]:
        result: Dict[int, int] = defaultdict(lambda: 0)
        for project in self.projects:
            to_count_date: datetime = datetime(project.state_changed_at.year, 1, 1)
            index: int = self._index[to_count_date]
            result[index] += project.pledged if project.state == "successful" else 0
        values = [result[i] for i, _ in enumerate(self.dates)]
        return self.date_list, values

    def successful_vs_total_by_year(
        self,
    ) -> Tuple[List[datetime], List[int], List[int]]:
        successful: Dict[int, int] = defaultdict(lambda: 0)
        total: Dict[int, int] = defaultdict(lambda: 0)
        for project in self.projects:
            to_count_date: datetime = datetime(project.state_changed_at.year, 1, 1)
            index: int = self._index[to_count_date]
            successful[index] += 1 if project.state == "successful" else 0
            total[index] += 1
        successful_values = [successful[i] for i, _ in enumerate(self.dates)]
        total_values = [total[i] for i, _ in enumerate(self.dates)]
        return self.date_list, successful_values, total_values

    def successful_vs_total_percent_by_year(self) -> Tuple[List[datetime], List[float]]:
        successful: Dict[int, int] = defaultdict(lambda: 0)
        total: Dict[int, int] = defaultdict(lambda: 0)
        for project in self.projects:
            to_count_date: datetime = datetime(project.state_changed_at.year, 1, 1)
            index: int = self._index[to_count_date]
            successful[index] += 1 if project.state == "successful" else 0
            total[index] += 1
        values = [successful[i] * 100 / total[i] for i, _ in enumerate(self.dates)]
        return self.date_list, values

    def successful_segmented_by_year(
        self,
    ) -> Tuple[List[datetime], List[List[int]], List[str]]:
        result: List[Dict[int, int]] = [defaultdict(lambda: 0) for _ in range(5)]
        for project in self.projects:
            to_count_date: datetime = datetime(project.state_changed_at.year, 1, 1)
            index: int = self._index[to_count_date]
            segment = self._segmented_project_by_pledged(project)
            result[segment][index] += 1 if project.state == "successful" else 0
        values = [[result[s][i] for i, _ in enumerate(self.dates)] for s in range(5)]
        texts = [
            "<= 10 mil",
            "10 mil - 50 mil",
            "50 mil - 100 mil",
            "100 mil - 500 mil",
            "> 500 mil",
        ]
        return self.date_list, values, texts

    def pledged_segmented_by_year(
        self,
    ) -> Tuple[List[datetime], List[List[int]], List[str]]:
        result: List[Dict[int, int]] = [defaultdict(lambda: 0) for _ in range(5)]
        for project in self.projects:
            to_count_date: datetime = datetime(project.state_changed_at.year, 1, 1)
            index: int = self._index[to_count_date]
            segment = self._segmented_project_by_pledged(project)
            result[segment][index] += (
                project.pledged if project.state == "successful" else 0
            )
        values = [[result[s][i] for i, _ in enumerate(self.dates)] for s in range(5)]
        texts = [
            "<= 10 mil",
            "10 mil - 50 mil",
            "50 mil - 100 mil",
            "100 mil - 500 mil",
            "> 500 mil",
        ]
        return self.date_list, values, texts

    def _segmented_project_by_pledged(self, project: ProjectModel) -> int:
        pledged = project.pledged
        if pledged <= 10000:
            return 0
        if pledged <= 50000:
            return 1
        if pledged <= 100000:
            return 2
        if pledged <= 500000:
            return 3
        return 4

    def top_ten_all_the_time_games(self) -> List[ProjectModel]:
        projects = [project for project in self.projects]
        projects.sort(key=lambda x: x.pledged, reverse=True)
        return projects[:10]

    def top_ten_2020_games(self) -> List[ProjectModel]:
        projects = [
            project
            for project in self.projects
            if project.state_changed_at.year == 2020
        ]
        projects.sort(key=lambda x: x.pledged, reverse=True)
        return projects[:10]

    def to_json(self):
        return {
            "projects": [value.to_json() for value in self.projects],
        }

    @staticmethod
    def from_json(data):
        projects = [ProjectModel(**value) for value in data["projects"]]
        result = TabletopGamesModel()
        result.projects = projects
        return result


@subscribe
def tabletop_games(
    categories: Dict[int, CategoryModel],
    project: Optional[ProjectModel] = None,
    model: Optional[TabletopGamesModel] = None,
) -> TabletopGamesModel:
    if model is None:
        model = TabletopGamesModel()
    if project is not None:
        if model.is_tabletop_game(project):
            model.add_project(project)
    return model
