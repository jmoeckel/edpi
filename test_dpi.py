# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:45:33 2016

@author: jmoeckel

Tests for the dpi module regarding the extended simulateModel-functionality
"""

import pytest
import dpi

MODEL = 'test_dpi'
dymola = dpi.DymolaInterface()


def test_simulateModel_still_works():
    success = dymola.simulateModel(MODEL)
    assert(success)


class Test_SimulateModelWithResult():

    def test_is_working(self):
        data = dymola.simulateModelwithResults(MODEL)
        assert(isinstance(data, dict))

    def test_input_resultFile_as_arg(self):
        data =  dymola.simulateModelwithResults(MODEL, 0, 10, 0, 0, 'Euler', 1e-4, 0, 'dsres_arg')
        assert(isinstance(data, dict))

    def test_input_resultFile_as_kwarg(self):
        data = dymola.simulateModelwithResults(MODEL, resultFile='dsres_kwarg')
        assert(isinstance(data, dict))

    def test_input_trajectoryNames(self):
        data = dymola.simulateModelwithResults(MODEL, trajectoryNames=['t', 'y'])
        assert(['y', 't'] == data.keys())

    def test_input_trajectoryNames_does_not_change_other_kwargs(self):
        data = dymola.simulateModelwithResults(MODEL, trajectoryNames=['t','y'], resultFile='dsres_kwarg')
        assert(['y', 't'] == data.keys())
