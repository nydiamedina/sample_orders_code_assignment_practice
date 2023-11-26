import logging
from datetime import datetime
from great_expectations import get_context
from great_expectations.dataset import PandasDataset


def perform_and_save_raw_data_validation(data_frame, suite_name):
    """
    Apply expectations, validate the DataFrame, and save the validation results.

    Args:
    - data_frame (DataFrame): The DataFrame to validate.
    - suite_name (str): The name of the expectation suite.

    Returns:
    - dict: Validation results.
    """
    # Get the Great Expectations context
    context = get_context()

    # Convert DataFrame to Great Expectations Dataset
    ge_df = PandasDataset(data_frame)

    # Define raw data expectations for USER_AGENT column
    ge_df.expect_column_to_exist("USER_AGENT")
    ge_df.expect_column_values_to_not_be_null("USER_AGENT")
    ge_df.expect_column_values_to_not_match_regex("USER_AGENT", "^$")
    ge_df.expect_column_values_to_not_match_regex("USER_AGENT", "^''$")

    # Perform validation
    validation_results = ge_df.validate()

    # Save the ExpectationSuite
    # TODO: Use update_expectation_suite or add_or_update_expectation_suite instead
    context.save_expectation_suite(ge_df.get_expectation_suite(), suite_name)

    # Build Data Docs
    context.build_data_docs()

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
