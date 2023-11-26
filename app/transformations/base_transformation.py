class BaseTransformation:
    """
    Base class for all transformations. Defines the interface for transformations.
    """

    def transform(self, data):
        """
        Transforms the input data. Should be implemented by all subclasses.

        Args:
            data: The data to transform.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Transform method not implemented.")
