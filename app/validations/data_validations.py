from great_expectations.dataset import PandasDataset
from great_expectations.data_context import DataContext


def validate_raw_data(data_frame):
    """
    Apply raw data expectations to the given DataFrame, validate it, and return the results.

    Args:
    - data_frame (DataFrame): The pandas DataFrame to validate.

    Returns:
    - dict: A dictionary containing the validation results.
    """
    # Convert DataFrame to Great Expectations Dataset
    ge_df = PandasDataset(data_frame)

    # Define raw data expectations for USER_AGENT column
    ge_df.expect_column_to_exist("USER_AGENT")
    ge_df.expect_column_values_to_not_be_null("USER_AGENT")
    ge_df.expect_column_values_to_not_match_regex("USER_AGENT", "^$")
    ge_df.expect_column_values_to_not_match_regex("USER_AGENT", "^''$")

    # Perform validation
    validation_results = ge_df.validate()

    # Prepare and return summary of results
    results_summary = {
        "success": validation_results.success,
        "statistics": validation_results.statistics,
        "failed_expectations": [
            exp.expectation_config.expectation_type
            for exp in validation_results.results
            if not exp.success
        ],
    }
    return results_summary
