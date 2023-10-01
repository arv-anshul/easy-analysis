import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def count_plot(df: pd.DataFrame, columns: list[str], title: str = ...):
    """
    Create count plots for one or more categorical columns in a DataFrame.

    This function generates count plots to visualize the distribution of categorical data in the
    specified columns of the input DataFrame. It arranges multiple plots in a grid format.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data to be visualized.
        columns (list of str): A list of column names for which count plots will be created.
        title (str, optional): A title for the overall figure. Default is None.

    Returns:
        None

    Example:
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> import seaborn as sns
        >>> data = pd.DataFrame({'Category': ['A', 'B', 'A', 'C', 'B', 'C'],
        ...                      'Status': ['Yes', 'No', 'No', 'Yes', 'Yes', 'No']})
        >>> count_plot(
        ...    df=data,
        ...    columns=['Category', 'Status'],
        ...    title='Distribution of Categories and Status',
        ...)
    """
    num_plots = len(columns)

    cols = int(np.ceil(np.sqrt(num_plots)))
    rows = int(np.ceil(num_plots / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
    fig.tight_layout(pad=2)

    if isinstance(title, str):
        fig.suptitle(title)

    for i, col in enumerate(columns):
        ax: plt.Axes = axes[i // cols, i % cols] if num_plots > 1 else axes  # type: ignore

        sns.countplot(data=df, x=col, ax=ax)
        ax.set_ylabel("")

    plt.show()


def agg_plot(
    df: pd.DataFrame,
    x: list[str],
    y: list[str],
    agg: list[str] = ["mean"],
) -> None:
    """
    Create aggregated bar plots to visualize relationships between variables.

    This function generates bar plots to visualize relationships between variables in the input
    DataFrame. It supports multiple x and y variables, allowing you to explore how different
    combinations of variables relate to each other. You can also specify aggregation methods for
    the y-axis values.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data to be visualized.
        x (list of str): A list of column names to be used on the x-axis.
        y (list of str): A list of column names to be used on the y-axis.
        agg (list of str, optional): A list of aggregation methods for the y-axis values.
            Default is ["mean"].

    Returns:
        None

    Example:
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> import seaborn as sns
        >>> data = pd.DataFrame({'Category': ['A', 'B', 'A', 'C', 'B', 'C'],
        ...                      'Value': [10, 20, 15, 30, 25, 35]})
        >>> agg_plot(data, x=['Category'], y=['Value'], agg=['mean', 'median'])
    """
    num_plots = len(x) * len(y)
    cols = int(np.ceil(np.sqrt(num_plots)))
    rows = int(np.ceil(num_plots / cols))

    for method in agg:
        plot_count = 0

        fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
        fig.suptitle(f"Method: {method.title()}", fontsize=15)

        for x_col in x:
            for y_col in y:
                ax: plt.Axes = (
                    axes[plot_count // cols, plot_count % cols]
                    if num_plots > 1
                    else axes
                )  # type: ignore

                sns.barplot(
                    data=df,
                    x=x_col,
                    y=y_col,
                    estimator=method,
                    ax=ax,
                    errorbar=("ci", 0),
                )
                ax.set_xlabel(x_col)

                plot_count += 1

    plt.tight_layout()
    plt.show()
