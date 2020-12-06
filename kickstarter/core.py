import json
import os
from typing import Dict, List, Tuple, cast

from .models import CategoryModel, ProjectModel
from .processing import top_grossing_categories  # noqa: F401
from .processing import top_successful_categories  # noqa: F401
from .processing import GrossingCategoriesModel, SuccessfulCategoriesModel, process


def load_json() -> Tuple[
    List[ProjectModel],
    Dict[int, CategoryModel],
]:
    file = open(os.path.join("data", "projects.json"), mode="r", encoding="utf-8")
    projects_json = json.load(file)
    file.close()
    file = open(os.path.join("data", "categories.json"), mode="r", encoding="utf-8")
    categories_json = json.load(file)
    file.close()
    projects: List[ProjectModel] = []
    for item in projects_json:
        projects.append(ProjectModel(**item))
    categories: Dict[int, CategoryModel] = {}
    for key, value in categories_json.items():
        categories[int(key)] = CategoryModel(**value)
    return projects, categories


def get_favorite_categories(
    projects: List[ProjectModel],
    categories: Dict[int, CategoryModel],
) -> Tuple[
    GrossingCategoriesModel,
    SuccessfulCategoriesModel,
    List[CategoryModel],
    List[CategoryModel],
    List[CategoryModel],
]:
    results = process(projects, categories)
    grossing_categories: List[CategoryModel] = []
    successful_categories: List[CategoryModel] = []
    crossing_categories_model: GrossingCategoriesModel = None  # type: ignore
    successful_categories_model: SuccessfulCategoriesModel = None  # type: ignore
    for item in results:
        if isinstance(item, GrossingCategoriesModel):
            item = cast(GrossingCategoriesModel, item)
            grossing_categories = item.top[:25]
            crossing_categories_model = item
        elif isinstance(item, SuccessfulCategoriesModel):
            item = cast(SuccessfulCategoriesModel, item)
            successful_categories = item.top[:25]
            successful_categories_model = item
    grossing_categories_set = set(grossing_categories)
    successful_categories_set = set(successful_categories)
    inter = cast(
        List[CategoryModel],
        list(set.intersection(grossing_categories_set, successful_categories_set)),
    )
    return (
        crossing_categories_model,
        successful_categories_model,
        grossing_categories,
        successful_categories,
        list(inter),
    )
