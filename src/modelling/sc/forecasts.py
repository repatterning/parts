import logging
import pandas as pd

import statsmodels.tsa.forecasting.stl as tfc


class Forecasts:

    def __init__(self, data: pd.DataFrame, testing: pd.DataFrame, system: tfc.STLForecastResults, code: str):
        """

        :param data:
        :param testing:
        :param system: The results of the seasonal component model
        :param code: The identification code of an institution
        """

        self.__data = data
        self.__testing = testing
        self.__system = system
        self.__code = code

    def __estimates(self):

        values: pd.DataFrame = self.__system.result.seasonal.to_frame()
        values.rename(columns={'season': 'seasonal_est'}, inplace=True)
        values = self.__data.copy()[['seasonal']].join(values.copy())
        logging.info(values)

    def __tests(self, projections: pd.DataFrame):

        values = self.__testing.copy()[['seasonal']].join(projections)
        logging.info(values)

    def __futures(self):
        pass

    def exc(self, arguments: dict):
        """

        :param arguments:
        :return:
        """

        forecasts = self.__system.forecast(steps=(2 * arguments.get('ahead'))).to_frame()
        forecasts.rename(columns={0: 'seasonal_est'}, inplace=True)



