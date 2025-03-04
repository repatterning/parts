"""Module splits.py"""
import logging
import os
import typing

import pandas as pd

import config
import src.functions.streams


class Splits:
    """
    The training & testing splits.
    """

    def __init__(self, arguments: dict):
        """

        :param arguments: Modelling arguments.
        """

        self.__arguments = arguments
        self.__configurations = config.Config()
        self.__streams = src.functions.streams.Streams()

    def __include(self, blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        return blob.copy()[:-self.__arguments.get('ahead')]

    def __exclude(self, blob: pd.DataFrame) -> pd.DataFrame:
        """
        Excludes instances that will be predicted

        :param blob:
        :return:
        """

        return blob.copy()[-self.__arguments.get('ahead'):]

    def __persist(self, blob: pd.DataFrame, pathstr: str) -> None:
        """

        :param blob:
        :param pathstr:
        :return:
        """

        message = self.__streams.write(blob=blob, path=os.path.join(self.__configurations.data_, pathstr))
        logging.info(message)

    def exc(self, data: pd.DataFrame, code: str) -> typing.Tuple[pd.DataFrame, pd.DataFrame]:
        """

        :param data: The data set consisting of the attendance numbers of <b>an</b> institution/hospital.
        :param code: An institution's identification code
        :return:
        """

        frame = data.copy()

        # Split
        training = self.__include(blob=frame)
        testing = self.__exclude(blob=frame)

        # Persist
        for instances, name in zip([frame, training, testing], ['data.csv', 'training.csv', 'testing.csv']):
            self.__persist(blob=instances, pathstr=os.path.join(code, name))

        return training, testing
