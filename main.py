import gzip
import json
import pandas as pd
from transformations.user_agent_parser import parse_user_agent


def read_data(file_name):
    """
    Reads a gzipped JSON lines file into a pandas DataFrame.

    Parameters:
    - file_name (str): The path to the gzipped JSON lines file.

    Returns:
    - DataFrame: A pandas DataFrame containing the data from the JSON lines file.

    Raises:
    - IOError: If the file cannot be opened or read.
    - ValueError: If a line in the file cannot be decoded as JSON.
    """
    try:
        with gzip.open(file_name, "rt", encoding="utf-8") as f:
            # List comprehension reads and converts each JSON line to a dictionary
            data_list = [json.loads(line) for line in f]

        # Convert the list of dictionaries to a DataFrame
        data = pd.DataFrame(data_list)
        return data
    except IOError as e:
        raise IOError(f"Error opening or reading the file {file_name}: {e}")
    except ValueError as e:
        raise ValueError(f"Error decoding JSON from {file_name}: {e}")


def save_data_as_compressed_json(data, file_name):
    """
    Writes the provided DataFrame to a gzipped JSON file.

    Parameters:
    - data (DataFrame): The pandas DataFrame to write to file.
    - file_name (str): The name of the output file including the path.

    Returns:
    - None

    Raises:
    - IOError: If the file cannot be opened or written to.
    - Exception: For other exceptions that are not IOError.
    """

    # Write the DataFrame to a gzipped JSON file
    try:
        with gzip.open(file_name, "wt") as f:
            f.write(data.to_json(orient="records", lines=True))
    except IOError as e:
        print(f"An IOError occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    # Read data from a gzipped JSON lines file into a pandas DataFrame
    sample_orders = read_data("sample_orders.json.gz")

    # Apply the parse_user_agent transformation function to the USER_AGENT column
    sample_orders[
        ["DEVICE_TYPE", "BROWSER_TYPE", "BROWSER_VERSION"]
    ] = sample_orders.apply(
        lambda row: parse_user_agent(row["USER_AGENT"]), axis=1, result_type="expand"
    )

    # Write the transformed data back to a gzipped JSON lines file
    save_data_as_compressed_json(sample_orders, "sample_orders_transformed.json.gz")


if __name__ == "__main__":
    main()
