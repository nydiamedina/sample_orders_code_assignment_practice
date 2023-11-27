from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from transformations.base_transformation import BaseTransformation
from user_agents import parse


class SparkUserAgentTransformation(BaseTransformation):
    def __init__(self):
        """
        Initialize the SparkUserAgentTransformation with a Spark session.

        Args:
            spark_session (SparkSession): An existing Spark session.
        """
        self.spark = SparkSession.builder.appName("SparkUserAgentTransformation").getOrCreate()

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

    def transform(self, spark_df):
        """
        Applies the parse_user_agent method to the 'USER_AGENT' column of a Spark DataFrame and adds the results as new columns.

        Args:
            spark_df (pyspark.sql.DataFrame): Spark DataFrame with a 'USER_AGENT' column to apply the transformation.

        Returns:
            pyspark.sql.DataFrame: The original Spark DataFrame enriched with three new columns: 'DEVICE_TYPE', 'BROWSER_TYPE', 'BROWSER_VERSION'.
        """
        parse_udf = udf(self.parse_user_agent, StringType())

        # Add the new columns to the Spark DataFrame using the UDF
        return (
            spark_df.withColumn("DEVICE_TYPE", parse_udf(spark_df["USER_AGENT"]))
            .withColumn("BROWSER_TYPE", parse_udf(spark_df["USER_AGENT"]))
            .withColumn("BROWSER_VERSION", parse_udf(spark_df["USER_AGENT"]))
        )
