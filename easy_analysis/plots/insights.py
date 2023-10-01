import pandas as pd
from matplotlib import pyplot as plt


def null_plot(df: pd.DataFrame):
    """
    Plot a bar chart showing the percentage of null values in each column of a DataFrame.

    This function calculates the percentage of null values for each column in the input DataFrame
    and creates a bar chart to visualize the results. It provides insights into the missing data
    distribution across columns.

    Parameters:
        df (pd.DataFrame): The DataFrame for which to create the null values bar chart.

    Returns:
        None

    Example:
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> data = pd.DataFrame({'A': [1, None, 3, 4, None],
        ...                      'B': [None, 2, 3, None, 5]})
        >>> null_plot(data)
    """
    ax = (
        df.isnull()
        .sum()
        .div(len(df))
        .mul(100)
        .add(0.5)
        .round()
        .plot.bar(ylabel="Null Values (in %)", ylim=(0, 100), figsize=(12, 4))
    )

    for bar in ax.patches:
        plt.text(
            x=(bar.get_x() + (bar.get_width() // 2)),
            y=bar.get_height() + 2.5,
            s=str(round(bar.get_height())),
            rotation=90,
            fontsize=12,
        )
    plt.show()
