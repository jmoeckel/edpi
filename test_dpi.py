# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:45:33 2016

@author: jmoeckel

Tests for the dpi module regarding the extended simulateModel-functionality
"""

import pytest
import dpi



class Test_Get_Dymola_Python_Interface_Path():

    def test_is_working(self):
        s = dpi.get_dymola_python_interface_path()
        assert(s)

    def test_detects_missing_dymola(self):
        with pytest.raises(dpi.NoDymolaFoundException) as excpt:
            dpi.get_dymola_python_interface_path(key='bla')
        assert('No Dymola installation' in str(excpt.value))


class Test_SimulateModelWithResult():

    @pytest.fixture(scope='class')
    def model(self):
        return 'test_dpi'

    @pytest.fixture(scope='class')
    def dymola(self):
        return dpi.DymolaInterface()

    def test_simulateModel_still_works(self, model, dymola):
        success = dymola.simulateModel(model)
        assert(success)

    def test_is_working(self, model, dymola):
        data = dymola.simulateModelwithResults(model)
        assert(isinstance(data, dict))

    def test_input_resultFile_as_arg(self, model, dymola):
        data =  dymola.simulateModelwithResults(model, 0, 10, 0, 0, 'Euler', 1e-4, 0, 'dsres_arg')
        assert(isinstance(data, dict))

    def test_input_resultFile_as_kwarg(self, model, dymola):
        data = dymola.simulateModelwithResults(model, resultFile='dsres_kwarg')
        assert(isinstance(data, dict))

    def test_input_trajectoryNames(self, model, dymola):
        data = dymola.simulateModelwithResults(model, trajectoryNames=['t', 'y'])
        assert(['y', 't'] == data.keys())

    def test_input_trajectoryNames_does_not_change_other_kwargs(self, model, dymola):
        data = dymola.simulateModelwithResults(model, trajectoryNames=['t','y'], resultFile='dsres_kwarg')
        assert(['y', 't'] == data.keys())
