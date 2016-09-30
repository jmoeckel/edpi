# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 08:19:24 2016

@author: jmoeckel

Extended Dymola-Python interface

Usage:
======
import dpi
dymola = dpi.DymolaInterface()

# from here on, use the Interface described as in the documentation provided by
# Dymola.
"""

import os
import sys

PATH_DPI = 'C:\Program Files (x86)\Dymola 2017\Modelica\Library\python_interface\dymola.egg'
sys.path.append(os.path.normpath(PATH_DPI))


def DymolaInterface():
    """Instantiates an extended version of the Dymola-Python interface

    The Dymola-Python interface provided by Dymola is instantiated with an
    extended simulateModel functionality.

    :ivar simulateModelwithResults: Same as simulateModel, but automatically
        loads data from the resultfile and provides them in form of an
        dictionary. See documentation of the modul for more information.
    """
    from dymola.dymola_interface import DymolaInterface
    from dymola.dymola_exception import DymolaException

    dymola = DymolaInterface()

    def simulateModelwithResults(*args, **kwargs):
        """simulate a modelica model within Dymola and returns simulated values

        This module provides the possibity to simulate a model with given
        simulation settings AND automatically use the simulated values, which
        are provided as an output in form of a dictionary.

        :param trajectoryNames: The possibility, to choose, which simulated
            parameters should be included in the output 'data'. If not set, all
            results are returned.

        :returns: A dictionary, that contains simulated values. This dictionary
            structure is: {'param name':[param values]}
        :rtype: dict

        :raises: DymolaException, if the simulation fails

        .. note::
            Besides the additional input argument 'trajectoryNames' and the
            output parameter, this module provides the exact the same API as
            'simulateModel'. So for more informations regarding different
            input-arguments, see the documentation for 'simulateModel'
        """

        # reduce kwargs by the new input arguments - otherwise simulateModel
        # will throw an exception
        reduced_kwargs = kwargs.copy()
        try:
            del reduced_kwargs['trajectoryNames']
        except KeyError:
            pass

        success = dymola.simulateModel(*args, **reduced_kwargs)
        if not success:
            raise DymolaException('Simulation of was not successfull.'
                                  ' Below is the translation log:\n\n'
                                  .format(dymola.getLastError()))

        # Check for user-given result-file and add file extension
        try:
            resFile = args[8]
        except IndexError:
            try:
                resFile = kwargs['resultFile']
            except KeyError:
                resFile = 'dsres'
        finally:
            resFile = '{}.mat'.format(resFile)

        # Check for user-input regarding the result-output - if non given,
        # all results will be returned
        try:
            trajNames = kwargs['trajectoryNames']
        except KeyError:
            trajNames = dymola.readTrajectoryNames(resFile)

        # At the moment, dymola.readMatrix() is invoked, as there is a bug
        # in dymola.readTrajectory. Unfortunately. As this is very inefficient
        allTrajNames = dymola.readTrajectoryNames(resFile)
        values = dymola.readMatrix(resFile, 'data_2', len(allTrajNames), dymola.readTrajectorySize(resFile))

        if allTrajNames == trajNames:
            data = dict(zip(trajNames, values))
        else:
            data = {}
            for trajName in trajNames:
                ind = allTrajNames.index(trajName)
                value = values[ind]
                data.update({trajName: value})

        return data

    # Adding the extended simulateModel() to dymola
    setattr(dymola, 'simulateModelwithResults', simulateModelwithResults)
    return dymola
