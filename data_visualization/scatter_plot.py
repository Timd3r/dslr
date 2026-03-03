import os
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    file_path = "data/dataset_train.csv"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Error: Dataset '{file_path}' not found.")
        sys.exit(1)

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        sys.exit(1)

    house_col = "Hogwarts House"
    feature_1 = "Astronomy"
    feature_2 = "Defense Against the Dark Arts"

    if not all(col in df.columns for col in [house_col, feature_1, feature_2]):
        print("Error: Missing required columns in the dataset.")
        sys.exit(1)

    colors = {
        "Ravenclaw": "blue",
        "Slytherin": "green",
        "Gryffindor": "red",
        "Hufflepuff": "#FFD700",  # Gold/Yellow
    }

    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")

    sns.scatterplot(
        data=df,
        x=feature_1,
        y=feature_2,
        hue=house_col,
        palette=colors,
        alpha=0.7,
        edgecolor=None,
    )

    plt.title(
        f"Similar Features: {feature_1} vs {feature_2}", fontsize=16, fontweight="bold"
    )
    plt.xlabel(feature_1, fontsize=12)
    plt.ylabel(feature_2, fontsize=12)
    plt.legend(title="Hogwarts House")

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.savefig("images/scatter_plot.png", dpi=300)

    print("\nBased on the visualization, answer the following question:")
    print("What are the two features that are similar?")
    print(
        f"-> The highly similar (perfectly negatively correlated) features are '{feature_1}' and '{feature_2}'.\n"
    )


if __name__ == "__main__":
    main()
