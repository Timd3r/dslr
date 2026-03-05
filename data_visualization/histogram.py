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
        print(
            "Please ensure the dataset is in the correct location or pass the path as an argument."
        )
        sys.exit(1)

    # load the dataset
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        sys.exit(1)

    house_col = "Hogwarts House"
    if house_col not in df.columns:
        print(f"Error: '{house_col}' column not found in the dataset.")
        sys.exit(1)

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    courses = [col for col in numeric_cols if col != "Index"]

    houses = df[house_col].dropna().unique()
    colors = {
        "Ravenclaw": "blue",
        "Slytherin": "green",
        "Gryffindor": "red",
        "Hufflepuff": "#FFD700",  # Gold/Yellow
    }

    # matplotlib figure setup
    num_courses = len(courses)
    cols = 4
    rows = (num_courses + cols - 1) // cols

    # seaborn theme and figure setup
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(rows, cols, figsize=(20, 4 * rows))
    fig.suptitle(
        "Score Distribution by Course and Hogwarts House",
        fontsize=20,
        fontweight="bold",
        y=0.98,
    )
    axes = axes.flatten()

    # plot histograms for each course and house
    for i, course in enumerate(courses):
        ax = axes[i]
        for house in houses:
            # drop NaN values for the current course and house
            subset = df[df[house_col] == house][course].dropna()

            # seaborn histplot for better aesthetics and handling of overlaps
            sns.histplot(
                subset,
                ax=ax,
                label=house,
                color=colors.get(house),
                alpha=0.5,
                element="step",  # step to make overlaps clearer
                stat="density",  # normalize distributions
                kde=False,
            )

        ax.set_title(course, fontsize=14)
        ax.set_xlabel("Scores")
        ax.set_ylabel("Density" if i % cols == 0 else "")

        if i == 0:
            ax.legend(title="Hogwarts House")

    # remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # type: ignore
    plt.savefig("histogram_grid.png", dpi=300)

    print("\nBased on the visualizations, answer the following question:")
    print(
        "Which Hogwarts course has a homogeneous score distribution between all four houses?"
    )
    print(
        "-> Hint: Look for the plot where all four colors overlap almost perfectly into a single shape (e.g., Care of Magical Creatures).\n"
    )


if __name__ == "__main__":
    main()
