import json
import os
import pytest
from app.transformations.user_agent_parser import parse_user_agent


# Test data file path constant
TEST_DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "test_data.json")


def load_test_data():
    """
    Load test data from a JSON file and convert expected results to tuples.

    Returns:
    - list: A list of dictionaries, where each dictionary has two keys:
        'ua_string' containing the user agent string, and 'expected' containing
        the expected tuple result from the parse_user_agent function.

    Raises:
    - RuntimeError: If the test data file does not exist at the specified path.
    - RuntimeError: If the test data file cannot be decoded as valid JSON.
    """
    try:
        with open(TEST_DATA_FILE_PATH, "r") as f:
            data = json.load(f)
            for item in data:
                item["expected"] = tuple(item["expected"])
            return data
    except FileNotFoundError:
        raise RuntimeError(f"The test data file was not found at {TEST_DATA_FILE_PATH}")
    except json.JSONDecodeError:
        raise RuntimeError("The test data file contains invalid JSON")


# Load test data from the JSON file
test_data = load_test_data()


# Decorator to parameterize the test function
@pytest.mark.parametrize(
    "ua_string, expected", [(item["ua_string"], item["expected"]) for item in test_data]
)
def test_parse_user_agent(ua_string, expected):
    """
    Test the parse_user_agent function with a series of user agent strings.

    Args:
    - ua_string (str): A user agent string to be parsed by the function.
    - expected (tuple): The expected tuple result consisting of device type, browser, and version.

    Asserts:
    - The function's output matches the expected result.
    """
    result = parse_user_agent(ua_string)
    assert result == expected
