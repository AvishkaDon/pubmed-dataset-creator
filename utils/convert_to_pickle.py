import pandas as pd
import argparse
import os


def load_data(filename):
    """Load data from a CSV file into a DataFrame."""
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None


def save_to_pickle(data, filename):
    """Save a DataFrame to a pickle file."""
    try:
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        data.to_pickle(filename)
        print(f"Data saved to {filename}.")
    except Exception as e:
        print(f"Error saving data to {filename}. Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a CSV file to a pickle file using this script. Provide the path to the CSV file and optionally the output directory for the pickle file.")
    parser.add_argument("filepath", help="Specify the full path to the CSV file you want to convert.")
    parser.add_argument(
        "output_dir",
        nargs="?",
        default="../data_pkl",
        help="Specify the directory where the output pickle file will be saved. Defaults to '../data_pkl' if not provided.",
    )

    args = parser.parse_args()
    data = load_data(args.filepath)
    if data is not None:
        base_name = os.path.basename(args.filepath)
        filename_without_ext = os.path.splitext(base_name)[0]
        output_path = os.path.join(args.output_dir, filename_without_ext + ".pkl")
        save_to_pickle(data, output_path)
