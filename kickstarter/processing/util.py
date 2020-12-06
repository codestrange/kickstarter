from typing import List


def select_recurrents(list_set: List[List], lenght: int):
    result: List = []
    for ls in list_set:
        for i in ls:
            if i not in result:
                result.append(i)

    def count_recurrence(item):
        count = 0
        for ls in list_set:
            if item in ls:
                count += 1
        return count

    result.sort(key=lambda i: count_recurrence(i))

    for i in range(lenght):
        if i < len(result):
            yield result[i]
