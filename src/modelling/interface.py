"""Module interface.py"""
import logging
import os

import dask
import pandas as pd

import config
import src.elements.master as mr
import src.functions.directories
import src.modelling.decompose
import src.modelling.splits
import src.modelling.sc.interface


class Interface:
    """
    Interface
    """

    def __init__(self, data: pd.DataFrame, codes: dict, arguments: dict):
        """

        :param data:
        :param codes:
        :param arguments:
        """

        self.__data = data
        self.__codes = codes
        self.__arguments = arguments

        self.__configurations = config.Config()
        self.__directories = src.functions.directories.Directories()

    @dask.delayed
    def __get_data(self, code: str) -> pd.DataFrame:
        """

        :param code:
        :return:
        """

        return self.__data.copy().loc[self.__data['hospital_code'] == code, :]

    @dask.delayed
    def __set_directories(self, code: str) -> bool:
        """

        :param code:
        :return:
        """

        success = []
        for pathway in ['data', 'models']:
            success.append(
                self.__directories.create(path=os.path.join(self.__configurations.artefacts_, pathway, code)))
        return all(success)

    def exc(self):
        """
        The testing data has <ahead> instances.  Altogether predict <2 * ahead> points
        into the future.  The first set of ahead points are for weekly evaluations of
        a week's model; the true value of the latter set of ahead points will be known
        in future.

        :return:
        """

        # Additional delayed tasks
        decompose = dask.delayed(src.modelling.decompose.Decompose(arguments=self.__arguments).exc)
        splits = dask.delayed(src.modelling.splits.Splits(arguments=self.__arguments).exc)
        sc = dask.delayed(src.modelling.sc.interface.Interface(arguments=self.__arguments).exc)

        computations = []
        for code, board in self.__codes.items():
            """
            1. get institution data
            2. set up directories per institution
            3. decompose institution data
            4. split institution data
            5. seasonal component modelling: naive model
            6. trend component modelling: gaussian process
            """

            data = self.__get_data(code=code)
            success = self.__set_directories(code=code)
            decompositions = decompose(data=data)
            master: mr.Master = splits(data=decompositions, code=code, success=success)
            message = sc(master=master)
            computations.append(message)

        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info(calculations)
