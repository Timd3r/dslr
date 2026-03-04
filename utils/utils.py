def count(values):
    count = 0
    for value in values:
        if value == value:
            count += 1
    return count


def mean(values):
    total = 0
    len = count(values)
    if len == 0:
        return 0
    for value in values:
        if value == value:
            total += value
    return total / len


def std(values):
    mean_value = mean(values)
    total = 0
    len = count(values)
    if len == 0:
        return 0
    for value in values:
        if value == value:
            total += (value - mean_value) ** 2
    return (total / len) ** 0.5


def min(values):
    min_value = values[0]
    for value in values:
        if value == value and value < min_value:
            min_value = value
    return min_value


def max(values):
    max_value = values[0]
    for value in values:
        if value == value and value > max_value:
            max_value = value
    return max_value