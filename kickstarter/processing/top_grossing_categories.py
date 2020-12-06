from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from ..models import CategoryModel, ProjectModel
from . import subscribe


class GrossingCategoriesModel:
    def __init__(self, categories: Dict[int, CategoryModel]):
        self.counter: Dict[int, int] = defaultdict(lambda: 0)
        self.categories: Dict[int, CategoryModel] = categories

    @property
    def top(self) -> List[CategoryModel]:
        order: List[Tuple[int, int]] = []
        for key, value in self.counter.items():
            order.append((value, key))
        order.sort(reverse=True)
        result: List[CategoryModel] = []
        for item in order:
            result.append(self.categories[item[1]])
        return result


@subscribe
def top_grossing_categories(
    categories: Dict[int, CategoryModel],
    project: Optional[ProjectModel] = None,
    model: Optional[GrossingCategoriesModel] = None,
) -> GrossingCategoriesModel:
    if model is None:
        model = GrossingCategoriesModel(categories)
    if project is not None:
        model.counter[project.category.id] += project.pledged
    return model
