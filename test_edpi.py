# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:45:33 2016
@author: jmoeckel
Tests for the dpi module regarding the extended simulateModel-functionality
"""

import pytest
import os
import edpi


class Test_Get_Dymola_Python_Interface_Path():

    def test_is_working(self):
        s = edpi._get_dymola_python_interface_path()
        assert(s)

    def test_detects_missing_dymola(self):
        with pytest.raises(edpi.NoDymolaFoundException) as excpt:
            edpi._get_dymola_python_interface_path(key='bla')
        assert('No Dymola installation' in str(excpt.value))


@pytest.mark.parametrize('model', ['test_edpi_1', 'test_edpi_2'])
class Test_SimulateModelWithResult():

    @pytest.yield_fixture(scope='class')
    def dymola(self):
        dymola = edpi.DymolaInterface()
        yield dymola
        print('...teardown...')
        dymola.close()
        [os.remove(x) for x in os.listdir('.') if os.path.splitext(x)[1] not in ['.md', '.py', '.pyc', '.mo', ''] and x not in ['test_read.mat']]

    def test_simulateModel_still_works(self, model, dymola):
        success = dymola.simulateModel(model)
        assert(success)

    def test_is_working(self, model, dymola):
        data = dymola.simulateModelwithResults(model)
        assert(isinstance(data, dict))

    def test_input_resultFile_as_arg(self, model, dymola):
        data =  dymola.simulateModelwithResults(model, 0, 10, 0, 0, 'Euler', 1e-4, 0, 'dsres_arg_{}'.format(model))
        assert(isinstance(data, dict))

    def test_input_resultFile_as_kwarg(self, model, dymola):
        data = dymola.simulateModelwithResults(model, resultFile='dsres_kwarg_{}'.format(model))
        assert(isinstance(data, dict))

    def test_input_trajectoryNames(self, model, dymola):
        data = dymola.simulateModelwithResults(model, trajectoryNames=['t'])
        assert(['t'] == data.keys())

    def test_input_trajectoryNames_does_not_change_other_kwargs(self, model, dymola):
        data = dymola.simulateModelwithResults(model, trajectoryNames=['t'], resultFile='dsres_kwarg_{}'.format(model))
        assert(['t'] == data.keys())

    def test_detects_bad_trajectoryName(self, model, dymola):
        with pytest.raises(edpi.BadTrajectoryNameException) as excpt:
            dymola.simulateModelwithResults(model, trajectoryNames=['not_existent'], resultFile='dsres_kwarg_{}'.format(model))
        assert('Some of the input trajectory' in str(excpt.value))
