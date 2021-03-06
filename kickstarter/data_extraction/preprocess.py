import json
import os
from typing import Dict, Iterable, List

from kickstarter.models import CategoryModel, CreatorModel, ProjectModel


def process_file(
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
        projects_dict_list: List[dict] = []

        if filetype == "[":
            jsondata: List[dict] = json.load(file)
            for proyects_dict_wrapper in jsondata:
                projects_dict_list += proyects_dict_wrapper["projects"]
        elif filetype == "{":
            for line in file:
                maybe = json.loads(line)["data"]
                if "projects" in maybe:
                    projects_dict_list += maybe["projects"]
                else:
                    projects_dict_list.append(maybe)
        else:
            raise Exception("Invalid file format")
        for project_dict in projects_dict_list:
            process_project(project_dict, projects, categories, creators)


def process_project(
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

    projects[project.id] = project
    categories[category.id] = category
    creators[creator.id] = creator


def process(input_dir: str = ".data/raw", output_dic: str = ".data/process"):

    files: Iterable[str] = get_json_paths(input_dir)

    projects: Dict[int, ProjectModel] = {}
    categories: Dict[int, CategoryModel] = {}
    creators: Dict[int, CreatorModel] = {}

    for file in files:
        print(f"Process file:\n {file}")
        process_file(file, projects, categories, creators)
        print(f"{len(projects)} processed")

    with open(f"{output_dic}/categories.json", "w+") as file:
        json.dump(
            {str(key): value.to_json() for key, value in categories.items()},
            fp=file,
            ensure_ascii=True,
            indent=2,
            separators=(", ", ": "),
        )

    with open(f"{output_dic}/creators.json", "w+") as file:
        json.dump(
            {str(key): value.to_json() for key, value in creators.items()},
            fp=file,
            ensure_ascii=True,
            indent=2,
            separators=(", ", ": "),
        )

    with open(f"{output_dic}/projects.json", "w+") as file:
        json.dump(
            [value.to_json() for key, value in projects.items()],
            fp=file,
            ensure_ascii=True,
            indent=2,
            separators=(", ", ": "),
        )


def get_json_paths(folder_path: str) -> Iterable[str]:
    for dir_entry in os.scandir(folder_path):
        if dir_entry.is_file():
            if dir_entry.name.endswith(".json"):
                yield dir_entry.path
        elif dir_entry.is_dir():
            for item in get_json_paths(dir_entry.path):
                yield item
