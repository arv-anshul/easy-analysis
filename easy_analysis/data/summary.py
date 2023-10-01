import pandas as pd


def custom_describe(data: pd.Series | pd.DataFrame) -> pd.DataFrame:
    """
    Customized describe function for pandas Series or DataFrames.

    Calculates various statistics for each column in the input pandas Series or DataFrame,
    including skewness, kurtosis, counts of non-null and null values. It extends the standard
    `describe` method by adding skewness, kurtosis, and counts.

    Parameters:
        data (pd.Series or pd.DataFrame): The pandas Series or DataFrame to be described.

    Returns:
        pd.DataFrame: A DataFrame containing descriptive statistics for the input data.

    Examples:
        >>> import pandas as pd
        >>> data = pd.DataFrame({'A': [1, 2, 3, 4, 5],
        ...                      'B': [5, 4, 3, 2, 1]})
        >>> custom_describe(data)
                   A         B
        count  5.000     5.000
        mean   3.000     3.000
        std    1.581     1.581
        min    1.000     1.000
        1%     1.000     1.000
        5%     1.200     1.200
        25%    2.000     2.000
        50%    3.000     3.000
        75%    4.000     4.000
        95%    4.800     4.800
        99%    4.960     4.960
        max    5.000     5.000
        skew   0.000     0.000
        kurt   -1.3     -1.3
        notnull 5         5
        isnull  0         0
    """
    if isinstance(data, pd.Series):
        data = data.to_frame()

    describe_stats = []
    for col in data.columns:
        d: pd.Series = data[col]

        skew = d.skew()
        kurt = d.kurt()
        notnull = d.notnull().sum()
        isnull = d.isnull().sum()

        describe_stats.append([skew, kurt, notnull, isnull])

    columns = ["skew", "kurtosis", "notnull", "isnull"]
    more_describe = pd.DataFrame(describe_stats, index=data.columns, columns=columns).T

    return pd.concat(
        [
            data.describe(percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]),
            more_describe,
        ],
    ).round(3)


def compare_describe(
    data1: pd.Series,
    data2: pd.Series,
    *,
    reciprocal_ratio: bool = False,
) -> pd.DataFrame:
    """
    Compare and describe two pandas Series objects.

    This function takes two pandas Series objects, calculates descriptive statistics for each Series,
    and performs various comparisons between them, such as subtraction and division. The results are
    returned as a DataFrame.

    Parameters:
        data1 (pd.Series): The first pandas Series to be compared and described.
        data2 (pd.Series): The second pandas Series to be compared and described.
        reciprocal_ratio (bool, optional): If True, include the reciprocal ratio of data2 to data1
            in the output DataFrame. Default is False.

    Returns:
        pd.DataFrame: A DataFrame containing descriptive statistics and comparisons between data1 and data2.

    Example:
        >>> import pandas as pd
        >>> data1 = pd.Series([1, 2, 3, 4, 5])
        >>> data2 = pd.Series([2, 4, 6, 8, 10])
        >>> compare_describe(data1, data2)
             data1 as data1  data2 as data2  data1 - data2  data1 ÷ data2
        count             5.0             5.0           -5.0           0.5
        mean              3.0             6.0           -3.0           0.5
        std               1.581139         3.162278       -1.581139       0.5
        min               1.0             2.0           -3.0           0.5
        25%               2.0             4.0           -3.0           0.5
        50%               3.0             6.0           -3.0           0.5
        75%               4.0             8.0           -3.0           0.5
        max               5.0            10.0           -3.0           0.5
    """
    desc1 = custom_describe(data1).iloc[:, 0].rename(f"{data1.name} as data1")
    desc2 = custom_describe(data2).iloc[:, 0].rename(f"{data2.name} as data2")

    sub_desc = desc1.sub(desc2).rename("data1 - data2")
    ratio_desc = desc1.div(desc2).rename("data1 ÷ data2")

    to_concat = [desc1, desc2, sub_desc, ratio_desc]

    if reciprocal_ratio:
        to_concat.append(desc2.div(desc1).rename("data2 ÷ data1"))

    desc_df = pd.concat(to_concat, axis=1)
    return desc_df
