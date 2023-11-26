import gzip
import json
import logging
import pandas as pd
import os
from great_expectations import get_context
from transformations.transformation_factory import TransformationFactory
from validations.data_validations import perform_and_save_raw_data_validation

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
INPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data/input/sample_orders.json.gz"
)
OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data/output/sample_orders_transformed.json.gz"
)
RAW_DATA_EXPECTATION_SUITE = "raw_user_agent_data_suite"


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
        # Initialize Great Expectations DataContext
        context = get_context()

        # Read data from a gzipped JSON lines file into a pandas DataFrame
        sample_orders = read_data(INPUT_FILE_PATH)

        # Validate the data
        # TODO: Validate transformed data as well
        validation_results = perform_and_save_raw_data_validation(
            sample_orders, RAW_DATA_EXPECTATION_SUITE
        )

        # Check validation results
        if validation_results["success"]:
            logging.info("Raw data validation passed.")
        else:
            logging.error(
                f"Raw data validation failed: {validation_results['failed_expectations']}"
            )

        # Get a user agent transformation instance from the factory and apply it
        logging.info("Applying user agent parser transformation.")
        transformation = TransformationFactory.get_transformation("user_agent")
        transformed_data = transformation.transform(sample_orders)

        # Write the transformed data back to a gzipped JSON lines file
        logging.info("Saving the transformed data.")
        save_data_as_compressed_json(transformed_data, OUTPUT_FILE_PATH)

        logging.info("Data processing and validation completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during the data transformation process: {e}")
        raise


if __name__ == "__main__":
    main()
