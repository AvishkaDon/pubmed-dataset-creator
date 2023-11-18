import pandas as pd
import argparse


def load_data(filename):
    """Load data from a CSV file into a DataFrame."""
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None


if __name__ == "__main__":
    # Initialize the argparse
    parser = argparse.ArgumentParser(
        description="This script loads data from a specified CSV file and displays it. Simply provide the path to the CSV file you wish to view."
    )
    parser.add_argument("filepath", help="Provide the full path to the CSV file you want to load and display.")

    args = parser.parse_args()

    # Load the data using the provided filename path
    data = load_data(args.filepath)

    # If data is loaded successfully, display it
    if data is not None:
        print(data)
