import json
from typing import Dict, List

from kickstarter.models import CategoryModel, CreatorModel, ProjectModel


def process_json(
    filename: str,
    projects: Dict[int, ProjectModel],
    categories: Dict[int, CategoryModel],
    creators: Dict[int, CreatorModel],
):
    with open(
        filename,
        "r",
        encoding="utf-8",
    ) as file:
        filetype = file.read(1)
        file.seek(0)
        if filetype == "[":
            jsondata: List[dict] = json.load(file)
            for proyects_dict_wrapper in jsondata:
                projects_dict_list: List[dict] = proyects_dict_wrapper["projects"]
                for project_dict in projects_dict_list:
                    process_new_project(project_dict, projects, categories, creators)
        elif filetype == "{":
            for line in file:
                project_dict = json.loads(line)["data"]
                process_new_project(project_dict, projects, categories, creators)
        else:
            raise Exception("Invalid file format")


def process_new_project(
    project_dict: dict,
    projects: Dict[int, ProjectModel],
    categories: Dict[int, CategoryModel],
    creators: Dict[int, CreatorModel],
):
    project = ProjectModel(**project_dict)
    category = CategoryModel(**project_dict["category"])
    creator = CreatorModel(**project_dict["creator"])

    if (
        project.id not in projects
        or project.state_changed_at > projects[project.id].state_changed_at
    ):
        projects[project.id] = project
        categories[category.id] = category
        creators[creator.id] = creator

