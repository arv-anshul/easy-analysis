import pandas as pd


def extract_outliers(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Extract outliers from a DataFrame based on a specified column.

    This function calculates the lower and upper bounds for outliers using the Inter-quartile Range (IQR)
    method and extracts rows from the input DataFrame where the specified column's values fall outside
    this range. The resulting DataFrame contains the outlier values and is sorted in descending order
    based on the specified column.

    Parameters:
        df (pd.DataFrame): The DataFrame from which to extract outliers.
        col (str): The name of the column in the DataFrame for outlier detection.

    Returns:
        pd.DataFrame: A DataFrame containing the outlier values from the specified column,
                      sorted in descending order based on the column values.

    Examples:
        >>> import pandas as pd
        >>> data = pd.DataFrame({'A': [1, 2, 3, 4, 5, 100],
        ...                      'B': [10, 20, 30, 40, 50, 200]})
        >>> extract_outliers(data, 'A')
           A    B
        0  100  200
    """
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = (
        df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        .sort_values(by=col, ascending=False)
        .reset_index(drop=True)
    )

    return outliers
