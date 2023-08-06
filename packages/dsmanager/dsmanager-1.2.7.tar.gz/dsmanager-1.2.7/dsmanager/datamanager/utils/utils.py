"""@Author: Rayane AMROUCHE

Utils for DataManager.
"""

from typing import Any

import pandas as pd  # type: ignore
from pandas.core.base import PandasObject  # type: ignore

from dotenv import load_dotenv  # type: ignore

from dsmanager.datamanager.utils._dataframe import DataFrameUtils
from dsmanager.datamanager.utils._column import ColumnUtils
from dsmanager.datamanager.utils._plotting import PlottingUtils

from dsmanager.datamanager.utils import _pandas_object
from dsmanager.datamanager.utils.df_pipeline import DfPipeline


class Utils:
    """Utils class brings utils tools for the data manager."""

    DfPipeline = DfPipeline

    def __init__(self, __dm: Any) -> None:
        """Init class Utils with an empty local storage.

        Args:
            __dm (Any): DataManager from which these utils are called.
        """
        self.__dm = __dm
        self.column = ColumnUtils()
        self.dataframe = DataFrameUtils()
        self.plot = PlottingUtils()

    def copy_as(self, df_: pd.DataFrame, name: str) -> pd.DataFrame:
        """Copy a pandas DataFrame in the datamanager with a given name.

        Args:
            df_ (pd.DataFrame): DataFrame to save.
            name (str): Alias of the DataFrame in the DataStorage of the DataManager.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        self.__dm.datas[name] = df_
        return df_

    def load_env(
        self,
        env_path: str = "",
    ) -> None:
        """Load env file from a given path or from the datamanager.

        Args:
            env_path (str, optional): Path of the env file. Defaults to "".
        """
        if env_path:
            load_dotenv(env_path)


setattr(PandasObject, "to_datamanager", _pandas_object.to_datamanager)
setattr(PandasObject, "pipe_sklearn", _pandas_object.pipe_sklearn)
setattr(PandasObject, "pipe_leaf", _pandas_object.pipe_leaf)
setattr(PandasObject, "pipe_steps", DfPipeline.pipe_steps)
