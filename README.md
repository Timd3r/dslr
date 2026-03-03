# dslr

Discover Data Science through this project by recreating the Hogwarts Sorting Hat using logistic regression!

## Linter

This project uses [Ruff](https://docs.astral.sh/ruff/) as the VSCode linter for Python code formatting and linting.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Project Structure

```
dslr/
├── data/                   # Datasets
├── data_analysis/          # Statistical analysis scripts
│   └── describe.py
├── data_visualization/     # Visualization scripts
│   ├── histogram.py
│   ├── pair_plot.py
│   └── scatter_plot.py
├── images/                 # Output images
├── logistic_regression/    # Logistic regression scripts
│   ├── logreg_train.py
│   └── logreg_predict.py
├── data.ipynb
├── requirements.txt
└── README.md
```

## Usage

**describe.py** — Display statistical metrics for the dataset:

```bash
python data_analysis/describe.py data/dataset_train.csv
```

**histogram.py** — Display a histogram of Hogwarts course scores:

```bash
python data_visualization/histogram.py
```

![Histogram](images/histogram_grid.png)

**scatter_plot.py** — Display a scatter plot of Hogwarts course scores:

```bash
python data_visualization/scatter_plot.py
```

![Scatter Plot](images/scatter_plot.png)

**pair_plot.py** — Display a pair plot of Hogwarts course scores:

```bash
python data_visualization/pair_plot.py
```

![Pair Plot](images/pair_plot.png)
