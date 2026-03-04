import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils.utils as utils
import data_analysis.describe as describe

house_map = {
    "Gryffindor": 0,
    "Hufflepuff": 1,
    "Ravenclaw": 2,
    "Slytherin": 3
}

def get_stats(data):
    mean = utils.mean(data)
    std = utils.std(data)
    return mean, std

def scale_data(data, mean, std):
    scaled_data = []
    for value in data:
        scaled_value = (value - mean) / std if std != 0 else 0
        scaled_data.append(scaled_value)
    return scaled_data

def clean_data(lines):
    data = []
    for line in lines[1:]:
        for value in line.split(","):
            try:
                fvalue = float(value.strip())
                if fvalue == fvalue:  # Check for NaN
                    data.append(fvalue)
            except ValueError:
                continue
    return data

def train():
    with open("data/dataset_train.csv", "r") as f:
        lines = f.readlines()
        data = clean_data(lines)
        mean, std = get_stats(data)
        scaled_data = scale_data(data, mean, std)
        #print(data)

if __name__ == "__main__":
    train()