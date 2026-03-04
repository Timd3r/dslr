import csv
import sys


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


def describe():
    columns = {}
    results = {
        "count": [],
        "mean": [],
        "std": [],
        "min": [],
        "25%": [],
        "50%": [],
        "75%": [],
        "max": [],
    }
    """ 
    read the csv file and store the numeric values in a dictionary 
    where the keys are the column names 
    and the values are lists of numeric values
    """
    try:
        with open(sys.argv[1], "r") as data:
            reader = csv.DictReader(data)
            for row in reader:
                for key, value in row.items():
                    if key not in columns:
                        columns[key] = []
                    try:
                        num = float(value)
                        if num == num:
                            columns[key].append(num)
                    except ValueError:
                        continue

    except FileNotFoundError:
        print(f"File {sys.argv[1]} not found.")
        return

    # take all the columns that have at least one numeric value starting form the front
    numeric_columns = {}
    for key in columns:
        if len(columns[key]) > 0:
            numeric_columns[key] = columns[key]

    # calculate the count, mean, std, min, 25%, 50%, 75% and max for each numeric column
    # and store the results in a dictionary where the keys are the column names and
    # the values are lists of the calculated statistics
    for column in numeric_columns:
        values = numeric_columns[column]
        sorted_values = sorted(values)
        q1 = sorted_values[len(sorted_values) // 4]
        q2 = sorted_values[len(sorted_values) // 2]
        q3 = sorted_values[len(sorted_values) * 3 // 4]

        results["count"].append(count(values))
        results["mean"].append(mean(values))
        results["std"].append(std(values))
        results["min"].append(min(values))
        results["25%"].append(q1)
        results["50%"].append(q2)
        results["75%"].append(q3)
        results["max"].append(max(values))

    COL_WIDTH = 18

    header_row = f"{'':<10}"
    for header in numeric_columns:
        display_name = (
            (header[: COL_WIDTH - 8] + "..") if len(header) > COL_WIDTH - 4 else header
        )
        header_row += f"{display_name:>{COL_WIDTH}}"
    print(header_row)

    for label, values in results.items():
        row = f"{label:<10}"
        for v in values:
            row += f"{v:>{COL_WIDTH}.6f}"
        print(row)


if __name__ == "__main__":
    describe()
