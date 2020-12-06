from typing import List, Set


def select_recurrents(list_set: List[List], lenght: int):
    result: List = []
    query: Set = set()
    for ls in list_set:
        for i in ls:
            if i not in query:
                result.append(i)
                query.add(i)

    def count_recurrence(item):
        count = 0
        for ls in list_set:
            if item in ls:
                count += 1
        return count

    result.sort(key=lambda i: count_recurrence(i), reverse=True)

    for i in range(lenght):
        if i < len(result):
            yield result[i]
