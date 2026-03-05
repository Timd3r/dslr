import pandas as pd
from sklearn.model_selection import train_test_split
import os


def create_splits():
    # Load original data
    source = "dataset_train.csv"
    if not os.path.exists(source):
        source = "data/dataset_train.csv"

    df = pd.read_csv(source)

    # 80/20 Split
    # We use random_state=42 so the split is consistent
    train_df, test_df = train_test_split(df, test_size=0.15, random_state=42)

    # 1. Save Training Split
    # Your trainer expects the full 19-column format
    train_df.to_csv("test/dataset_train.csv", index=False)

    # 2. Save Truth File for tester.py
    test_df[["Index", "Hogwarts House"]].to_csv("test/dataset_truth.csv", index=False)

    # 3. Save Test Split (The Mimic)
    # Your predictor crashes if columns are missing.
    # We keep the 'Hogwarts House' column but make it empty.
    test_mimic = test_df.copy()
    test_mimic["Hogwarts House"] = ""
    test_mimic.to_csv("test/dataset_test.csv", index=False)

    print("✅ Splits created successfully.")
    print("   - test/dataset_train.csv (Use this for training)")
    print("   - test/dataset_truth.csv  (Use this for predicting)")


if __name__ == "__main__":
    create_splits()
