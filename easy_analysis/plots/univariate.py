from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from scipy import stats

from easy_analysis import _constants as C

_QQDist = Literal["norm", "uniform", "log"]
_WIDTH = 100


def univariate_eda(
    data: pd.Series,
    describe_plot: str = ...,
    *,
    visualize: bool = True,
    compare: bool = False,
    ecdf: bool = False,
    qqplot_kw: dict[Literal["dist"], _QQDist] | Literal[False] = False,
):
    """
    Perform Univariate Exploratory Data Analysis (EDA) for a pandas Series.

    This function conducts univariate EDA for the input pandas Series, including descriptive statistics,
    visualization of the data distribution, comparison of distributions (optional), Empirical Cumulative
    Distribution Function (ECDF) plot (optional), and Quantile-Quantile (QQ) plot (optional).

    Parameters:
        data (pd.Series): The pandas Series for which to perform EDA.
        describe_plot (str, optional): A custom description or title for the EDA. Default is None.
        visualize (bool, optional): Whether to visualize the data distribution using boxplots,
            histograms, and stripplots. Default is True.
        compare (bool, optional): Whether to create a compare plot for distribution comparison
            between the original and log-transformed data. Default is False.
        ecdf (bool, optional): Whether to create an ECDF plot for visualizing the cumulative
            distribution of the data. Default is False.
        qqplot_kw (dict[str, _QQDist] | False, optional): A dictionary with a 'dist' key specifying
            the distribution for the QQ plot. Options are 'norm' (normal), 'uniform', or 'log'.
            Pass False to skip the QQ plot. Default is False.

    Returns:
        None

    Example:
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> data = pd.Series([1, 2, 3, 4, 5])
        >>> univariate_eda(data, visualize=True, compare=True, ecdf=True, qqplot_kw={'dist': 'norm'})
    """
    if isinstance(describe_plot, str):
        print("+" * _WIDTH)
        print(describe_plot.center(_WIDTH))
        print("+" * _WIDTH)

    if visualize:
        visualize_feature(data)
    if compare:
        compare_plot(data)
    if ecdf:
        ecdf_plot(data)
    if qqplot_kw:
        qqplot(data, **qqplot_kw)


def visualize_feature(data: pd.Series) -> None:
    """
    Visualize a pandas Series with boxplots, histograms, and stripplots.

    This function creates subplots to visualize the distribution of the input pandas Series using
    boxplots, histograms, and stripplots.

    Parameters:
        data (pd.Series): The pandas Series to be visualized.

    Returns:
        None
    """
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

    fig.suptitle(f"Visualize {data.name}", fontsize=18)

    sns.boxplot(x=data, ax=ax1).set_title("Boxplot")
    sns.histplot(data, kde=True, ax=ax2).set_title("Histplot")
    sns.stripplot(data, ax=ax3).set_title("Stripplot")

    plt.tight_layout()
    plt.show()


def qqplot(data: pd.Series, dist: _QQDist) -> None:
    """
    Create a Quantile-Quantile (QQ) plot for comparing the distribution of a pandas Series
    to a theoretical distribution.

    This function generates a QQ plot to visually compare the distribution of the input pandas
    Series to a specified theoretical distribution (e.g., normal, uniform, or log-normal).
    It helps assess the similarity between the empirical and theoretical distributions.

    Parameters:
        data (pd.Series): The pandas Series for which to create the QQ plot.
        dist (_QQDist): Theoretical distribution to compare against. Options are 'norm' (normal),
            'uniform', or 'log' (log-normal).

    Returns:
        None

    Raises:
        ValueError: If the 'dist' parameter is not one of ['norm', 'uniform', 'log'].

    Example:
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> import statsmodels.api as sm
        >>> data = pd.Series([1, 2, 3, 4, 5])
        >>> qqplot(data, dist='norm')
    """
    if dist == "norm":
        theoretical_dist = stats.norm
    elif dist == "uniform":
        theoretical_dist = stats.uniform
    elif dist == "log":
        data = pd.Series(np.log1p(data), name=data.name)
        theoretical_dist = stats.norm
    else:
        raise ValueError("dist parameter must be ['norm', 'uniform', 'log']")

    fig = sm.qqplot(data, theoretical_dist, line="45")  # type: ignore
    fig.suptitle(f"{dist.title()} QQ-Plot of {data.name}")
    plt.show()


def compare_plot(data: pd.Series) -> None:
    """
    Create a compare plot for visualizing the distribution of a pandas Series.

    This function generates a compare plot to visualize the distribution of the input pandas Series.
    It includes two subplots: a histogram and a box plot, both for the original and log-transformed
    versions of the data. This plot is useful for comparing the characteristics of data distributions.

    Parameters:
        data (pd.Series): The pandas Series for which to create the compare plot.

    Returns:
        None

    Example:
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> data = pd.Series([1, 2, 3, 4, 5])
        >>> compare_plot(data)
    """
    data_log = np.log1p(data)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 8))

    fig.suptitle(f"Compare plot of {data.name}", fontsize=18)

    org_dist_str = "Original Distribution"
    trf_dist_str = "Log Transformed Distribution"

    # HistPlot
    sns.histplot(data, kde=True, color=C.SKY_BLUE, ax=ax1)
    ax1.set_title(org_dist_str)

    sns.histplot(data_log, kde=True, color=C.LIGHT_GREEN, ax=ax2)
    ax2.set_title(trf_dist_str)

    # BoxPlot
    sns.boxplot(x=data, color=C.SKY_BLUE, ax=ax3)
    sns.boxplot(x=data_log, color=C.LIGHT_GREEN, ax=ax4)

    plt.tight_layout()
    plt.show()


def ecdf_plot(data: pd.Series) -> None:
    """
    Create an Empirical Cumulative Distribution Function (ECDF) plot for a pandas Series.

    This function generates an ECDF plot to visualize the cumulative distribution of values in
    the input pandas Series. It shows how the data is spread across different values.

    Parameters:
        data (pd.Series): The pandas Series for which to create the ECDF plot.

    Returns:
        None

    Example:
        >>> import pandas as pd
        >>> import matplotlib.pyplot as plt
        >>> import seaborn as sns
        >>> data = pd.Series([1, 2, 2, 3, 3, 3, 4, 4, 5])
        >>> ecdf_plot(data)
    """
    ecdf = data.value_counts().sort_index().cumsum().div(data.shape[0])
    sns.lineplot(x=ecdf.index, y=ecdf, marker="o", linestyle="none")

    plt.xticks(rotation="vertical")
    plt.title(f"ECDF plot of {data.name}")
    plt.show()
