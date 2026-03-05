import csv
import os


def load_csv_no_header(filepath):
    """Loads a headerless CSV into a dictionary {Index: House}."""
    data = {}
    paths_to_check = [filepath, os.path.join("test", filepath)]

    actual_path = None
    for p in paths_to_check:
        if os.path.exists(p):
            actual_path = p
            break

    if not actual_path:
        print(f"Error: Could not find {filepath}")
        return None

    with open(actual_path, "r") as f:
        # We don't use DictReader because your output has no header
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                # Strip spaces and normalize index
                idx = row[0].strip()
                house = row[1].strip()
                # Skip the actual header string if it exists in the truth file
                if idx == "Index":
                    continue
                data[idx] = house
    return data


def main():
    # File paths
    truth_file = "dataset_truth.csv"  # Created by split_data.py
    pred_file = "houses.csv"  # Created by logreg_predict.py

    truth = load_csv_no_header(truth_file)
    preds = load_csv_no_header(pred_file)

    if not truth or not preds:
        return

    correct = 0
    evaluated = 0

    print(f"\n{'Index':<10} | {'Truth':<15} | {'Prediction':<15} | Status")
    print("-" * 65)

    # Sort indices numerically to verify matches
    for idx in sorted(truth.keys(), key=lambda x: int(x)):
        if idx in preds:
            evaluated += 1
            true_h = truth[idx]
            pred_h = preds[idx]

            status = "✅" if true_h == pred_h else "❌"
            if true_h == pred_h:
                correct += 1

            if evaluated <= 15:  # Show first 15 matches
                print(f"{idx:<10} | {true_h:<15} | {pred_h:<15} | {status}")

    print("-" * 65)
    if evaluated == 0:
        print("❌ ERROR: Still no matches. Check if Index numbers match in both files.")
        print(f"Truth sample: {list(truth.keys())[:3]}")
        print(f"Pred sample: {list(preds.keys())[:3]}")
    else:
        accuracy = (correct / evaluated) * 100
        print(f"Accuracy: {accuracy:.2f}% ({correct}/{evaluated})")
        if accuracy >= 98.0:
            print("✨ 98% REACHED! ✨")


if __name__ == "__main__":
    main()
