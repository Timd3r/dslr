import math
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils.utils as utils

# Columns to keep (indices into parts[6:]), dropping Arithmancy(0), DADA(3), Care of Magical Creatures(10)
KEEP_INDICES = [1, 2, 4, 5, 6, 7, 8, 9, 11, 12]


def get_stats(data):
    mean = utils.mean(data)
    std = utils.std(data)
    return mean, std


def scale_data(data, means, stds):
    scaled_data = []
    for row in data:
        scaled_row = []
        for i, value in enumerate(row[1:]):  # Skip house columns
            mean = means[i]
            std = stds[i]
            scaled_value = (value - mean) / std if std != 0 else 0
            scaled_row.append(scaled_value)
        scaled_data.append([row[0]] + scaled_row)  # Keep house values
    return scaled_data


def clean_data(lines):
    dataset = []
    house_map = {
        "Gryffindor": 0,
        "Hufflepuff": 1,
        "Ravenclaw": 2,
        "Slytherin": 3,
        "nan": float("nan"),
    }
    # Skip header
    for line in lines[1:]:
        parts = line.split(",")

        # 1. Handle the House (Label Encoding)
        house_name = parts[1].strip()
        house_val = house_map.get(house_name, float("nan"))

        # 3. Extract only Numeric Features (6 to end), filtering by Pair Plot results
        raw_features = parts[6:]
        features = []
        for i in KEEP_INDICES:
            val = raw_features[i].strip()
            try:
                features.append(float(val))
            except ValueError:
                features.append(float("nan"))  # Keep as NaN to fill later

        # Combine [House_ID, Feature1, Feature2, ...]
        dataset.append([house_val] + features)

    return dataset


# replace nan with the mean of the column
def replace_nan(data):
    cleaned_data = []
    feature_columns = zip(*[row[1:] for row in data])
    means = []
    for col in feature_columns:
        mean = utils.mean([x for x in col if not (isinstance(x, float) and x != x)])
        means.append(mean)
    for row in data:
        new_row = []
        for i, val in enumerate(row):
            if i < 1:  # Keep house value as is
                new_row.append(val)
            else:  # Replace NaN with mean of column
                if isinstance(val, float) and val != val:
                    new_row.append(means[i - 1])
                else:
                    new_row.append(val)
        cleaned_data.append(new_row)
    return cleaned_data


def get_clean_data():
    train_file = "data/dataset_train.csv"
    if not os.path.exists(train_file):
        print(f"Error: Training dataset '{train_file}' not found.")
        print("Please ensure the training dataset is in the 'data/' folder.")
        sys.exit(1)

    try:
        with open(train_file, "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading training data: {e}")
        sys.exit(1)

    if len(lines) < 2:
        print("Error: Training dataset is empty or has no data rows.")
        sys.exit(1)

    data = clean_data(lines)
    data = replace_nan(data)
    means = []
    stds = []
    feature_columns = zip(*[row[1:] for row in data])

    for col in feature_columns:
        mean, std = get_stats(col)
        means.append(mean)
        stds.append(std)
    scaled_data = scale_data(data, means, stds)
    return scaled_data, means, stds


def sigmoid(z):
    if z < -700:
        return 0
    return 1 / (1 + math.exp(-z))


def train():
    data, means, stds = get_clean_data()
    houses = [0, 1, 2, 3]
    all_weights = {}
    X = [[1.0] + row[1:] for row in data]  # Add bias term
    learn_rate = 0.1
    iterations = 1000
    m = len(X)

    for house in houses:
        y = [1 if row[0] == house else 0 for row in data]
        weights = [0.0] * len(X[0])
        for _ in range(iterations):
            gradeients = [0.0] * len(X[0])
            for i in range(m):
                z = sum(X[i][j] * weights[j] for j in range(len(weights)))
                pred = sigmoid(z)
                error = pred - y[i]
                for j in range(len(weights)):
                    gradeients[j] += error * X[i][j]
            for j in range(len(weights)):
                weights[j] -= learn_rate * gradeients[j] / m
        all_weights[house] = weights

    model_data = {"weights": all_weights, "means": means, "stds": stds}
    try:
        with open("data/weights.json", "w") as f:
            json.dump(model_data, f)
    except Exception as e:
        print(f"Error saving weights: {e}")
        sys.exit(1)
    print("Training complete. Weights and stats saved to data/weights.json")


if __name__ == "__main__":
    train()
