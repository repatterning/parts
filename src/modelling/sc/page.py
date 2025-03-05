"""Module page.py"""
import os
import statsmodels.tsa.forecasting.stl as tfc

import config


class Page:

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def exc(self, system: tfc.STLForecastResults, code: str):
        """

        :param system:
        :param code:
        :return:
        """

        pathstr = os.path.join(self.__configurations.artefacts_, 'models', code, 'sc.txt')

        with open(file=pathstr, mode='w', encoding='utf-8', newline='\r\n') as disk:
            disk.write(system.summary().as_text())
