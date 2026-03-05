import subprocess
import sys
import os


def run_script(command):
    """Executes a script in a subprocess."""
    print(f"\n>> Executing: {' '.join(command)}")
    try:
        # Use the current python executable to run the command
        subprocess.run([sys.executable] + command, check=True)
    except subprocess.CalledProcessError:
        print(f"\n[!] Error: The script '{command[0]}' crashed or returned an error.")
    except FileNotFoundError:
        print(f"\n[!] Error: Could not find script: {command[0]}")
    print("-" * 50)


def print_menu():
    print("\n" + "=" * 45)
    print(" 🧙‍♂️ Hogwarts Sorting Hat Orchestrator 🧙‍♂️")
    print("=" * 45)
    print("  1. describe   - Run data analysis")
    print("  2. histogram  - Generate histogram plot")
    print("  3. scatter    - Generate scatter plot")
    print("  4. pair       - Generate pair plot matrix")
    print("  5. train      - Train logistic regression")
    print("  6. predict    - Predict houses for test data")
    print("  7. evaluate   - Check accuracy against truth")
    print("  8. exit       - Exit the program")
    print("=" * 45)


def main():
    # Make sure the user is running this from the project root
    if not os.path.exists("data"):
        print("Warning: 'data' directory not found.")
        print(
            "Please ensure you are running main.py from the root of the dslr project."
        )

    while True:
        try:
            print_menu()
            choice = input("Enter a command or number: ").strip().lower()

            if choice in ["1", "describe"]:
                run_script(["data_analysis/describe.py", "data/dataset_train.csv"])

            elif choice in ["2", "histogram"]:
                run_script(["data_visualization/histogram.py"])

            elif choice in ["3", "scatter"]:
                run_script(["data_visualization/scatter_plot.py"])

            elif choice in ["4", "pair"]:
                run_script(["data_visualization/pair_plot.py"])

            elif choice in ["5", "train"]:
                run_script(["logistic_regression/logreg_train.py"])

            elif choice in ["6", "predict"]:
                run_script(
                    [
                        "logistic_regression/logreg_predict.py",
                        "data/dataset_test.csv",
                        "data/weights.json",
                    ]
                )

            elif choice in ["7", "evaluate"]:
                run_script(
                    ["utils/evaluate.py", "data/dataset_truth.csv", "data/houses.csv"]
                )

            elif choice in ["8", "exit", "q", "quit"]:
                print("\nMischief managed. Goodbye!\n")
                break

            else:
                print(
                    "\n[!] Invalid command. Please type a valid number or command name."
                )

        except (KeyboardInterrupt, EOFError):
            print("\n\nMischief managed. Goodbye!\n")
            break


if __name__ == "__main__":
    main()
