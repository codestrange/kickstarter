from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from ..models import CategoryModel, ProjectModel


class Model:
    def __init__(self, categories: Dict[int, CategoryModel]):
        self.counter: Dict[int, int] = defaultdict(lambda: 0)
        self.categories: Dict[int, CategoryModel] = categories

    @property
    def top(self) -> List[CategoryModel]:
        order: List[Tuple[int, int]] = []
        for key, value in self.counter.items():
            order.append((value, key))
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
        model.counter[project.category.id] += project.pledged
    return model
