import gzip
import json
import logging
import pandas as pd
import os
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
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


def read_data_to_pandas_df(file_name):
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


def read_data_to_spark_df(file_path):
    """
    Reads a gzipped JSON lines file into a Spark DataFrame.

    Args:
        file_path (str): The path to the gzipped JSON lines file.

    Returns:
        pyspark.sql.DataFrame: A Spark DataFrame containing the data from the JSON lines file.

    Raises:
        FileNotFoundError: If the file cannot be found.
        AnalysisException: If there is an error in reading the JSON file.
        Exception: For other exceptions that might occur.
    """
    try:
        spark = SparkSession.builder.appName(
            "SparkUserAgentTransformation"
        ).getOrCreate()
        spark_df = spark.read.json(file_path)
        return spark_df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error finding the file {file_path}: {e}")
    except AnalysisException as e:
        raise AnalysisException(f"Error analyzing JSON from {file_path}: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")


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
        # Pandas Implementation
        # Read data from a gzipped JSON lines file into a pandas DataFrame
        sample_orders = read_data_to_pandas_df(INPUT_FILE_PATH)

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
        transformation = TransformationFactory.get_transformation("pandas_user_agent")
        transformed_data = transformation.transform(sample_orders)

        # Write the transformed data back to a gzipped JSON lines file
        logging.info("Saving the transformed data.")
        save_data_as_compressed_json(transformed_data, OUTPUT_FILE_PATH)

        # Spark Implementation
        # Read the data using the Spark-specific function and get the Spark session
        spark_df = read_data_to_spark_df(INPUT_FILE_PATH)

        # Use the factory to get a Spark user agent transformation
        transformation = TransformationFactory.get_transformation("spark_user_agent")

        # Apply the transformation
        transformed_spark_df = transformation.transform(spark_df)

        # For testing purposes, print the first 5 rows of the transformed Spark DataFrame
        transformed_spark_df.show(5)

        logging.info("Data processing and validation completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during the data transformation process: {e}")
        raise


if __name__ == "__main__":
    main()
