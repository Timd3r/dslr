import math
import json
import os
import sys

# House mappings corresponding to the label encoding in train
HOUSE_MAP = {0: "Gryffindor", 1: "Hufflepuff", 2: "Ravenclaw", 3: "Slytherin"}

# Columns to keep (indices into parts[6:]), dropping Arithmancy(0), DADA(3), Care of Magical Creatures(10)
KEEP_INDICES = [1, 2, 4, 5, 6, 7, 8, 9, 11, 12]


def sigmoid(z):
    # Cap z to prevent math overflow errors
    if z < -700:
        return 0
    return 1 / (1 + math.exp(-z))


def load_test_data(filepath, means):
    dataset = []
    indices = []

    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in lines[1:]:
        parts = line.split(",")
        index = parts[0].strip()
        indices.append(index)

        raw_features = parts[6:]
        features = []
        for j, i in enumerate(KEEP_INDICES):
            val = raw_features[i].strip()
            try:
                features.append(float(val))
            except ValueError:
                features.append(means[j])

        dataset.append(features)

    return dataset, indices


def scale_data(data, means, stds):
    scaled_data = []
    for row in data:
        scaled_row = []
        for i, value in enumerate(row):
            mean = means[i]
            std = stds[i]
            scaled_value = (value - mean) / std if std != 0 else 0
            scaled_row.append(scaled_value)
        scaled_data.append(scaled_row)
    return scaled_data


def predict():
    test_file = "data/dataset_test.csv"
    weights_file = "data/weights.json"

    if not os.path.exists(weights_file):
        print(f"Error: Weights file '{weights_file}' not found.")
        print("Please run the training script first (option 5) to generate weights.")
        sys.exit(1)

    if not os.path.exists(test_file):
        print(f"Error: Test dataset '{test_file}' not found.")
        print("Please ensure the test dataset is in the 'data/' folder.")
        sys.exit(1)

    try:
        with open(weights_file, "r") as f:
            model_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: '{weights_file}' is not a valid JSON file.")
        print("Please re-run the training script to regenerate it.")
        sys.exit(1)

    required_keys = ["weights", "means", "stds"]
    for key in required_keys:
        if key not in model_data:
            print(
                f"Error: '{key}' not found in weights file. The file may be corrupted."
            )
            print("Please re-run the training script to regenerate it.")
            sys.exit(1)

    all_weights = model_data["weights"]
    means = model_data["means"]
    stds = model_data["stds"]

    raw_data, indices = load_test_data(test_file, means)
    scaled_data = scale_data(raw_data, means, stds)

    X = [[1.0] + row for row in scaled_data]

    predictions = []

    for i in range(len(X)):
        best_house = None
        max_prob = -1

        for house_id_str, weights in all_weights.items():
            house_id = int(house_id_str)
            z = sum(X[i][j] * weights[j] for j in range(len(weights)))
            prob = sigmoid(z)

            if prob > max_prob:
                max_prob = prob
                best_house = house_id

        predictions.append(HOUSE_MAP[best_house])  # type: ignore

    with open("data/houses.csv", "w") as f:
        f.write("Index,Hogwarts House\n")
        for idx, house in zip(indices, predictions):
            f.write(f"{idx},{house}\n")

    print("Predictions successfully generated and saved to data/houses.csv")


if __name__ == "__main__":
    predict()
