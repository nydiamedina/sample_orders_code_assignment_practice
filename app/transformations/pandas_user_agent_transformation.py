import pandas as pd
from transformations.base_transformation import BaseTransformation
from user_agents import parse


class PandasUserAgentTransformation(BaseTransformation):
    """
    Transformation class to parse user agent strings.
    """

    @staticmethod
    def parse_user_agent(user_agent_str):
        """
        Parses a user agent string and return device type, browser type, and browser version.

        Parameters:
        - user_agent_str (str): The user agent string to be parsed.

        Returns:
        - tuple: A tuple containing the device type, browser type, and browser version as strings.
            If the user agent string is missing or empty, returns ("Unknown", "Unknown", "Unknown").

        """
        if not user_agent_str or user_agent_str == "" or user_agent_str == "''":
            return "Unknown", "Unknown", "Unknown"

        user_agent = parse(user_agent_str)

        # Determining the device type
        device_type = (
            "Mobile"
            if user_agent.is_mobile
            else "Tablet"
            if user_agent.is_tablet
            else "Computer"
            if user_agent.is_pc
            else "Bot"
            if user_agent.is_bot
            else "Other"
        )

        # Extracting browser type and version
        browser_type = user_agent.browser.family
        browser_version = ".".join(map(str, user_agent.browser.version))

        return device_type, browser_type, browser_version

    def transform(self, data):
        """
        Applies the parse_user_agent method to the 'USER_AGENT' column of a DataFrame and adds the results as new columns.

        Parameters:
        - data (pandas.DataFrame): DataFrame with a 'USER_AGENT' column to apply the transformation.

        Returns:
        - pandas.DataFrame: The original DataFrame enriched with three new columns: 'DEVICE_TYPE', 'BROWSER_TYPE', and 'BROWSER_VERSION'.
        """

        def apply_parse(row):
            device_type, browser_type, browser_version = self.parse_user_agent(
                row["USER_AGENT"]
            )
            return pd.Series([device_type, browser_type, browser_version])

        # Apply the parse_user_agent function to each row and assign the result to new columns
        data[["DEVICE_TYPE", "BROWSER_TYPE", "BROWSER_VERSION"]] = data.apply(
            apply_parse, axis=1
        )
        return data
