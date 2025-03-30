"""Module forecasts.py"""
import datetime
import os

import pandas as pd
import statsmodels.tsa.forecasting.stl as tfs

import src.elements.gauge as ge
import src.elements.master as mr
import src.functions.objects


class Forecasts:
    """
    Determines forecasts/predictions vis-à-vis a developed model; predictions.
    """

    def __init__(self, master: mr.Master, arguments: dict, system: tfs.STLForecastResults, path: str):
        """

        :param master: A named tuple consisting of training & testing data.<br>
        :param arguments: A set of model development, and supplementary, arguments.<br>
        :param system: The forecasting object.<br>
        :param path: The storage path.<br>
        """

        self.__training = master.training
        self.__testing = master.testing
        self.__arguments = arguments
        self.__system = system
        self.__path = path

        self.__objects = src.functions.objects.Objects()

    def __get_predictions(self, limit: datetime.datetime) -> pd.DataFrame:
        """

        :param limit: Predictions will be until limit.
        :return:
        """

        details = self.__system.get_prediction(end=limit)

        # Final State -> ['date', 'mean', 'mean_se', 'mean_ci_lower', 'mean_ci_upper']
        predictions = details.summary_frame()
        predictions.reset_index(drop=False, inplace=True)
        predictions.rename(columns={'index': 'date'}, inplace=True)

        return predictions

    def __get_training(self, predictions: pd.DataFrame):
        """

        :param predictions:
        :return:
        """

        _training = self.__training[['ts_id', 'timestamp', 'date', 'measure']].merge(predictions, how='left', on='date')
        return _training.to_dict(orient='tight')

    def __get_testing(self, predictions: pd.DataFrame):
        """

        :param predictions:
        :return:
        """

        _testing = self.__testing[['ts_id', 'timestamp', 'date', 'measure']].merge(predictions, how='left', on='date')
        _testing.to_dict(orient='tight')

    def __get_futures(self, predictions: pd.DataFrame):
        """

        :param predictions:
        :return:
        """

        _futures: pd.DataFrame = predictions[-self.__arguments.get('ahead'):]
        _futures.to_dict(orient='tight')

    def exc(self,  gauge: ge.Gauge) -> str:
        """

        :param gauge: Encodes the time series & catchment identification codes of a gauge, and its gauge datum.<br>
        :return:
        """

        limit: datetime.datetime = (self.__training['date'].max().to_pydatetime() +
                 datetime.timedelta(hours=2*self.__arguments.get('ahead')))
        predictions = self.__get_predictions(limit=limit)

        # Hence
        nodes = {'ts_id': gauge.ts_id,
                 'catchment_id': gauge.catchment_id,
                 'training': self.__get_training(predictions=predictions),
                 'testing': self.__get_testing(predictions=predictions),
                 'futures': self.__get_futures(predictions=predictions)}
        message = self.__objects.write(nodes=nodes, path=os.path.join(self.__path, 'estimates.json'))

        return f'{message} ({gauge.ts_id} of {gauge.catchment_id})'
