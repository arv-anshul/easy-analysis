class ClusterAnalyzerException(Exception):
    """Exception for ClusterAnalyzer class."""


class NullInDataFrame(ClusterAnalyzerException):
    """Raises when passed DataFrame has null values."""


class DFNotEncoded(ClusterAnalyzerException):
    """
    Raises when passed DataFrame is not encoded and contains
    `["object", "category"]` datatype.
    """
