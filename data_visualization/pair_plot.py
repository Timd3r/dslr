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
    if house_col not in df.columns:
        print(f"Error: '{house_col}' column not found.")
        sys.exit(1)

    # filter the Index column and non-numerical columns
    cols_to_drop = ["Index", "First Name", "Last Name", "Birthday", "Best Hand"]
    df_features = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

    colors = {
        "Ravenclaw": "blue",
        "Slytherin": "green",
        "Gryffindor": "red",
        "Hufflepuff": "#FFD700",  # Gold/Yellow
    }

    print(
        "Generating pair plot... This might take a minute depending on your computer's speed."
    )

    sns.set_theme(style="whitegrid")
    pair_plot = sns.pairplot(
        df_features.dropna(),
        hue=house_col,
        palette=colors,
        plot_kws={
            "alpha": 0.6,
            "s": 15,
        },  # make points slightly transparent and smaller
        diag_kws={"alpha": 0.6},
    )

    pair_plot.fig.suptitle(
        "Pair Plot of Hogwarts Courses", y=1.02, fontsize=20, fontweight="bold"
    )

    output_file = "images/pair_plot.png"
    plt.savefig(output_file, dpi=300)
    print(f"\nSuccess! The pair plot has been saved to '{output_file}'.")
    print("Please open the image file to view the matrix.\n")

    print("Based on this visualization, answer the following question:")
    print("Which features are you going to use for your logistic regression?")
    print(
        "-> Hint: Look for the features (courses) where the different colors (Houses) are clearly separated into distinct clusters."
    )
    print(
        "-> Good features separate the houses well. Bad features (like Care of Magical Creatures) mix all the houses together."
    )


if __name__ == "__main__":
    main()
