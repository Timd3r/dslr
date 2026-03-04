import sys
import os
import pandas as pd
from sklearn.metrics import accuracy_score


def evaluate(truth_path="data/dataset_truth.csv", pred_path="data/houses.csv"):
    if not os.path.exists(truth_path):
        print(f"Error: Truth file '{truth_path}' not found.")
        print("Please ensure you placed 'dataset_truth.csv' in the 'data/' folder.")
        return
    if not os.path.exists(pred_path):
        print(f"Error: Prediction file '{pred_path}' not found.")
        print("Please run the prediction script first to generate 'houses.csv'.")
        return

    try:
        # Load the data
        df_truth = pd.read_csv(truth_path)
        df_pred = pd.read_csv(pred_path)

        # Ensure we are comparing the right columns
        if (
            "Hogwarts House" not in df_truth.columns
            or "Hogwarts House" not in df_pred.columns
        ):
            print("Error: Both CSV files must contain a 'Hogwarts House' column.")
            return

        # Extract the labels
        y_true = df_truth["Hogwarts House"].tolist()
        y_pred = df_pred["Hogwarts House"].tolist()

        # Calculate accuracy
        accuracy = accuracy_score(y_true, y_pred)

        print("=======================================")
        print(f"Total Predictions: {len(y_pred)}")
        print(f"Accuracy Score:    {accuracy * 100:.2f}%")
        print("=======================================")

        if accuracy >= 0.98:
            print("Professor McGonagall approves! The Sorting Hat is ready.")
        else:
            print("The Sorting Hat needs more training. Minimum requirement is 98%.")

    except Exception as e:
        print(f"An error occurred during evaluation: {e}")


if __name__ == "__main__":
    # Allows passing custom paths via CLI, or defaults to the standard data folder paths
    truth_file = sys.argv[1] if len(sys.argv) > 1 else "data/dataset_truth.csv"
    pred_file = sys.argv[2] if len(sys.argv) > 2 else "data/houses.csv"

    evaluate(truth_file, pred_file)
