"""Module interface.py"""
import logging
import typing

import pymc
import arviz

import src.elements.codes as ce
import src.elements.master as mr
import src.modelling.tc.algorithm
import src.modelling.tc.page


class Interface:

    def __init__(self, arguments: dict):
        """

        :param arguments:
        """

        self.__arguments = arguments

    def __determine(self, master: mr.Master) -> typing.Tuple[pymc.model.Model, pymc.gp.Marginal, arviz.InferenceData]:
        """

        :param master:
        :return:
        """

        algorithm = src.modelling.tc.algorithm.Algorithm(training=master.training, arguments=self.__arguments)

        return algorithm.exc()

    def exc(self, master: mr.Master, code: ce.Codes, state: bool) -> str:
        """

        :param master: The training & testing data of an institution.
        :param code: The health board & institution/hospital codes of an institution/hospital.
        :param state: If the seasonal component modelling step was a success, this will be True; otherwise False.
        :return:
        """

        if not state:
            return f'Trend Component Modelling: Skip -> {code.hospital_code}'

        # Model
        model, gp, details = self.__determine(master=master)

        # Estimates & Futures
        abscissae = master.training.shape[0] + (2 * self.__arguments.get('ahead'))[:, None]

        # Persist: Algorithm
        src.modelling.tc.page.Page(model=model, code=code).exc(label='algorithm')

        return f'Trend Component Modelling: Success -> {code.hospital_code}'
