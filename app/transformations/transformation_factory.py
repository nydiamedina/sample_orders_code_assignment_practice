from transformations.pandas_user_agent_transformation import PandasUserAgentTransformation
from transformations.spark_user_agent_transformation import SparkUserAgentTransformation

class TransformationFactory:
    """
    Factory class to get the appropriate transformation instance based on a type identifier.
    """

    @staticmethod
    def get_transformation(transformation_type):
        """
        Get a transformation instance based on the transformation type.

        Args:
            transformation_type (str): The type of transformation.

        Returns:
            BaseTransformation: An instance of a transformation class.

        Raises:
            ValueError: If the transformation type is not recognized.
        """
        if transformation_type == "pandas_user_agent":
            return PandasUserAgentTransformation()
        elif transformation_type == "spark_user_agent":
            return SparkUserAgentTransformation()
        else:
            raise ValueError("Transformation type not recognized.")
