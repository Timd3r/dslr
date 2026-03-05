import pandas as pd
import os

def setup():
    # Ensure data directory exists
    if not os.path.exists('test'):
        os.makedirs('test')

    # FIX: Point to the 'test/' folder where your CSV actually lives
    try:
        df = pd.read_csv('test/dataset_train.csv') 
    except FileNotFoundError:
        # Fallback if it's in the root instead
        df = pd.read_csv('dataset_train.csv')

    # Shuffle the data
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Split: 80% for training, 20% for testing
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    # Save training set (overwriting with the 80% split)
    train_df.to_csv('test/dataset_train.csv', index=False)
    print("Created: test/dataset_train.csv (Training Split)")

    # Save truth file (Index and House only)
    truth_df = test_df[['Index', 'Hogwarts House']]
    truth_df.to_csv('test/dataset_truth.csv', index=False)
    print("Created: test/dataset_truth.csv (Answers)")

    # Save test set (Removing answers so the AI can't cheat)
    test_features_df = test_df.drop(columns=['Hogwarts House'])
    test_features_df.to_csv('test/dataset_test.csv', index=False)
    print("Created: test/dataset_test.csv (Test Features)")

if __name__ == "__main__":
    setup()