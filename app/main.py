import gzip
import json
import logging
import pandas as pd
import os
from transformations.user_agent_parser import parse_user_agent

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# File paths constants
INPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data/input/sample_orders.json.gz"
)
OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data/output/sample_orders_transformed.json.gz"
)


def read_data(file_name):
    """
    Read a gzipped JSON lines file into a pandas DataFrame.

    Args:
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
    Write the provided DataFrame to a gzipped JSON file.

    Args:
    - data (DataFrame): The pandas DataFrame to write to file.
    - file_name (str): The name of the output file including the path.

    Returns:
    - None

    Raises:
    - IOError: If the file cannot be opened or written to.
    - Exception: For other exceptions that are not IOError.
    """

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    # Write the DataFrame to a gzipped JSON file
    try:
        with gzip.open(file_name, "wt") as f:
            f.write(data.to_json(orient="records", lines=True))
    except IOError as e:
        raise IOError(f"An IOError occurred: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


def main():
    logging.info("Starting the data transformation process.")
    try:
        # Read data from a gzipped JSON lines file into a pandas DataFrame
        sample_orders = read_data(INPUT_FILE_PATH)

        # Apply the parse_user_agent transformation function to the USER_AGENT column
        logging.info("Applying user agent parser transformation.")
        sample_orders[
            ["DEVICE_TYPE", "BROWSER_TYPE", "BROWSER_VERSION"]
        ] = sample_orders.apply(
            lambda row: parse_user_agent(row["USER_AGENT"]),
            axis=1,
            result_type="expand",
        )

        # Write the transformed data back to a gzipped JSON lines file
        logging.info("Saving the transformed data.")
        save_data_as_compressed_json(sample_orders, OUTPUT_FILE_PATH)

        logging.info("Data transformation process completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during the data transformation process: {e}")
        raise


if __name__ == "__main__":
    main()
