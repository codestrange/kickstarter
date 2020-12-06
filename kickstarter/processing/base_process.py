from typing import Any, Dict, List

from ..models import CategoryModel, ProjectModel

processors: list = []


def subscribe(processor):
    global processors
    processors.append(processor)
    return processor


def process(projects: List[ProjectModel], categories: Dict[int, CategoryModel]):
    global processors
    acummulators: List[Any] = [None] * len(processors)
    for project in projects:
        for index, processor in enumerate(processors):
            acummulators[index] = processor(categories, project, acummulators[index])
    return acummulators
