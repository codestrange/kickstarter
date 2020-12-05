import os
from typing import Set


def test_requirements():
    os.system(
        "poetry export -f requirements.txt -o requirements_temp.txt --without-hashes"
    )
    with open("./requirements.txt") as actual:
        with open("./requirements_temp.txt") as temp:
            actual_lines = actual.readlines()
            temp_lines = temp.readlines()
            actual_set: Set[str] = set()
            temp_set: Set[str] = set()
            for actual_line, temp_line in zip(actual_lines, temp_lines):
                actual_line = actual_line.split(";")[0].strip("\r\n").strip("\n")
                temp_line = temp_line.split(";")[0].strip("\r\n").strip("\n")
                actual_set.add(actual_line)
                temp_set.add(temp_line)
            assert actual_set == temp_set, "requirements.txt not updated"
