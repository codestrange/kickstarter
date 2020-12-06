from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from ..models import CategoryModel, ProjectModel
from . import subscribe


class SuccessfulCategoriesModel:
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
            order.append((success * 100 / total, key))
        order.sort(reverse=True)
        result: List[CategoryModel] = []
        for item in order:
            result.append(self.categories[item[1]])
        return result


@subscribe
def top_successful_categories(
    categories: Dict[int, CategoryModel],
    project: Optional[ProjectModel] = None,
    model: Optional[SuccessfulCategoriesModel] = None,
) -> SuccessfulCategoriesModel:
    if model is None:
        model = SuccessfulCategoriesModel(categories)
    if project is not None:
        model.categories_total[project.category.id] += 1
        model.categories_success[project.category.id] += (
            1 if project.state == "successful" else 0
        )
    return model
