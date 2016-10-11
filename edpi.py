# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 08:19:24 2016

@author: jmoeckel

Extended Dymola-Python interface

REQUIREMENTS:
=============
- Dymola 2015 or newer
- Python 2.x (Interface does not support Python 3.x)

Usage:
======
import edpi
dymola = edpi.DymolaInterface()

# from here on, use the Interface described as in the documentation provided by
# Dymola.
"""

import os
import sys


def DymolaInterface():
    """Instantiates an extended version of the Dymola-Python interface

    The Dymola-Python interface provided by Dymola is instantiated with an
    extended simulateModel functionality.

    :ivar simulateModelwithResults: Same as simulateModel, but automatically
        loads data from the resultfile and provides them in form of an
        dictionary. See documentation of the modul for more information.
    """
    try:
        from dymola.dymola_interface import DymolaInterface
        from dymola.dymola_exception import DymolaException
    except ImportError as err:
        raise ImportError('Import of DymolaInterface failed.\n {}'.format(err.args))

    def simulateModelwithResults(*args, **kwargs):
        """simulate a modelica model within Dymola and returns simulated values

        This module provides the possibity to simulate a model with given
        simulation settings AND automatically use the simulated values, which
        are provided as an output in form of a dictionary.

        :param trajectoryNames: The possibility, to choose, which simulated
            parameters should be included in the output 'data'. If not set, all
            results are returned.
        :type trajectoryNames: list (of strings)

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
                                  ' Below is the translation log:\n{}'
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

        data = _read_dymola_mat(dymola, trajNames, resFile)

        return data

    # initialize dymola-interface
    dymola = DymolaInterface()

    # Adding the extended simulateModel() to dymola
    setattr(dymola, 'simulateModelwithResults', simulateModelwithResults)
    return dymola


def _read_dymola_mat(dymola, trajNames, resFile):
    # At the moment, dymola.readMatrix() is invoked, as there is a bug
    # in dymola.readTrajectory. Unfortunately - as this is very
    # inefficient

    szI = dymola.readMatrixSize(resFile, 'dataInfo')
    dataI = dymola.readMatrix(resFile, 'dataInfo', szI[0], szI[1])
    sz1 = dymola.readMatrixSize(resFile, 'data_1')
    data1 = dymola.readMatrix(resFile, 'data_1', sz1[0], sz1[1])
    sz2 = dymola.readMatrixSize(resFile, 'data_2')
    data2 = dymola.readMatrix(resFile, 'data_2', sz2[0], sz2[1])

    # all trajectories - needed because of positions within data matrices
    allTrajNms = dymola.readTrajectoryNames(resFile)

    # initialize result dictionary
    res = {}
    for trajName in trajNames:
        # this gets the position of the trajectory
        ind = allTrajNms.index(trajName)

        # this determines, if the trajectory is in data_1 or data_2
        data = dataI[0][ind]

        # this determines the position in data_1 or data_2,
        # -1 because its matlab syntax (starting with 1 instead of 0)
        dataInd = int(dataI[1][ind])-1

        if data in (0, 2):
            # 0: Case for Time -> its in data_2
            values = data2[dataInd]
        elif data == 1:
            values = data1[dataInd]

        res.update({trajName: values})
    return res


class NoDymolaFoundException(Exception):
    def __str__(self):
        return('No Dymola installation found in environmental variables.'
               ' In case that there is a Dymola-installation available, but it'
               ' is not included in the windows environmental variables, you '
               ' have to manually include the path to the Dymola-Python'
               ' interface BEFORE invoking \'DymolaInterface()\'!')


def _get_dymola_python_interface_path(key='Dymola'):
    """get the path of the dymola python interface from windows env. variables

    :param key: optional input, keyword, that identifies the path of the
                Dymola installatio
    :type key: str

    :returns: path of the Dymola-Python interface
    :rtype: str

    :raises: NoDymolaFoundException, if there is no path to a Dymola
             installation in the environmental variables.
    """
    envpaths = os.getenv('PATH').split(';')
    path_dymola = next((s for s in envpaths if key in s), None)

    try:
        path_dpi = os.path.normpath(os.path.join(path_dymola, '..\Modelica\Library\python_interface\dymola.egg'))
    except TypeError:
        raise NoDymolaFoundException()

    return path_dpi


# Add path to Dymola-Python interface to the python-path.
try:
    path_dpi = _get_dymola_python_interface_path()
except:
    raise
sys.path.append(os.path.normpath(path_dpi))
