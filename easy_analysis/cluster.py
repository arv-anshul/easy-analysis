import importlib
from typing import Literal, TypeAlias

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from easy_analysis.core import _errors

ScalerType: TypeAlias = Literal["StandardScaler", "RobustScaler", "MinMaxScaler"]


class ClusterAnalyzer:
    """Analyze your feature using `KMeans` clustering method."""

    def __init__(
        self,
        data: pd.DataFrame,
        *,
        scaler_type: ScalerType = "StandardScaler",
    ) -> None:
        """
        Parameters:
            data (pd.DataFrame): A fully imputed and encoded dataframe.
            scaler_type (ScalerType, optional): You can choose the scaler algorithm.
                `["StandardScaler", "RobustScaler", "MinMaxScaler"]`.
                Default to `"StandardScaler"`.

        Example:
            >>> analyzer = ClusterAnalyzer(df)
            >>> wcss = analyzer.find_optimal_clusters(range(1, 11))
            >>> # Visualize cluster to determine best clusters.
            >>> analyzer.plot_clusters(wcss)
            >>> # Now fit the KMeans model and fit it.
            >>> analyzer.fit_kmeans_model(5)
        """
        self.__validate_df(data)
        self.data = self.__scale_df(data, scaler_type=scaler_type)

    def __validate_df(self, data: pd.DataFrame) -> None:
        if data.isnull().sum().sum() > 0:
            raise _errors.NullInDataFrame("Passed dataframe must be imputed.")

        not_encoded_cols = data.select_dtypes(["object", "category"]).columns
        if not_encoded_cols.values.size > 0:
            raise _errors.DFNotEncoded(
                "Passed dataframe is not encoded. Encode these columns: "
                f"{not_encoded_cols.tolist()}."
            )

    def __scale_df(
        self,
        df: pd.DataFrame,
        *,
        scaler_type: ScalerType,
    ) -> np.ndarray:
        preprocessing_pkg = importlib.import_module("sklearn.preprocessing")
        scaler: StandardScaler = getattr(preprocessing_pkg, scaler_type)()
        return scaler.fit_transform(df)

    def find_optimal_clusters(self, cluster_range: range = ...) -> list[float]:
        """
        Find the optimal number of clusters using the Elbow Method.

        Parameters:
            cluster_range (range, optional): A range of cluster numbers to evaluate.
                Default is None, which uses the range from 1 to the number of features.

        Returns:
            np.ndarray: List of within-cluster sum of squares (WCSS) for different cluster numbers.
        """
        if not isinstance(cluster_range, range):
            cluster_range = range(1, self.data.shape[1] + 1)

        wcss = []  # Within-Cluster-Sum-of-Squares
        for i in cluster_range:
            kmeans = KMeans(n_clusters=i, init="k-means++", n_init=10, random_state=42)
            kmeans.fit(self.data)
            wcss.append(kmeans.inertia_)

        return wcss

    @staticmethod
    def plot_clusters(
        wcss: list[float],
        *,
        cluster_range: range = ...,
        title: str = ...,
    ) -> None:
        """
        Plot the Elbow Method results. Use (WCSS) from `find_optimal_clusters` method.

        Parameters:
            wcss (list[float]): List of within-cluster sum of squares (WCSS) for different cluster numbers.
            cluster_range (range, optional): A range of cluster numbers to evaluate.
                Default is None, which uses the range from 1 to the length of wcss.
            title (str, optional): The title of the plot.

        Returns:
            None
        """
        if not isinstance(cluster_range, range):
            cluster_range = range(1, len(wcss) + 1)

        plt.plot(cluster_range, wcss, marker="o", linestyle="--")

        plt.title(
            title
            if isinstance(title, str)
            else "Elbow Method for Optimal Number of Clusters"
        )
        plt.xticks(cluster_range)
        plt.xlabel("Number of Clusters")
        plt.ylabel("WCSS")
        plt.show()

    def get_clusters(self, best_n_clusters: int) -> np.ndarray:
        """
        Fit the KMeans model with the best number of clusters.

        Parameters:
            best_n_clusters (int): The number of clusters to fit the KMeans model.

        Returns:
            np.ndarray: An array containing clusters assigned to corresponding data points.
        """
        kmeans = KMeans(
            n_clusters=best_n_clusters, init="k-means++", n_init=10, random_state=42
        )
        kmeans.fit(self.data)
        return kmeans.predict(self.data)
