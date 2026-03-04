import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils.utils as utils


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
    if len(sys.argv) < 2:
        print("Usage: python describe.py <dataset.csv>")
        return

    try:
        with open(sys.argv[1], "r") as data:
            reader = csv.DictReader(data)
            for row in reader:
                for key, value in row.items():
                    if key not in columns:
                        columns[key] = []
                    try:
                        if value is not None:
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

        results["count"].append(utils.count(values))
        results["mean"].append(utils.mean(values))
        results["std"].append(utils.std(values))
        results["min"].append(utils.min(values))
        results["25%"].append(q1)
        results["50%"].append(q2)
        results["75%"].append(q3)
        results["max"].append(utils.max(values))

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
