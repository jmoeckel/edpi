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
import dpi
dymola = dpi.DymolaInterface()

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

    # initialize dymola-interface
    dymola = DymolaInterface()

    # Adding the extended simulateModel() to dymola
    setattr(dymola, 'simulateModelwithResults', simulateModelwithResults)
    return dymola


class NoDymolaFoundException(Exception):
    def __str__(self):
        return('No Dymola installation found in environmental variables.'
               ' In case that there is a Dymola-installation available, but it'
               ' is not included in the windows environmental variables, you '
               ' have to manually include the path to the Dymola-Python'
               ' interface BEFORE invoking \'DymolaInterface()\'!')


def get_dymola_python_interface_path(key='Dymola'):
    """get the path of the dymola python interface from windows env. variables

    :param key: optional input, keyword, that identifies the path of the
                Dymola installatio
    :type key: str

    :returns: path as a string
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
    path_dpi = get_dymola_python_interface_path()
except:
    raise
sys.path.append(os.path.normpath(path_dpi))
