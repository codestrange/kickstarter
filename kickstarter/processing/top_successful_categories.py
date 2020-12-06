from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from ..models import CategoryModel, ProjectModel


class Model:
    def __init__(self, categories: Dict[int, CategoryModel]):
        self.categories_total: Dict[int, int] = defaultdict(lambda: 0)
        self.categories_success: Dict[int, int] = defaultdict(lambda: 0)
        self.categories: Dict[int, CategoryModel] = categories

    @property
    def top(self) -> List[CategoryModel]:
        order: List[Tuple[float, int]] = []
        for key in self.categories_success:
            total = self.categories_total[key]
            success = self.categories_success[key]
            order.append(((total / success) * 100, key))
        order.sort()
        result: List[CategoryModel] = []
        for item in order:
            result.append(self.categories[item[1]])
        return result


def top_grossing_categories(
    categories: Dict[int, CategoryModel],
    project: Optional[ProjectModel] = None,
    model: Optional[Model] = None,
) -> Model:
    if model is None:
        model = Model(categories)
    if project is not None:
        model.categories_total[project.category.id] += 1
        model.categories_success[project.category.id] += (
            1 if project.state == "successful" else 0
        )
    return model
