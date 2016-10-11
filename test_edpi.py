# -*- coding: utf-8 -*-
"""
  Copyright (C) 2016  Jens Möckel <j.moeckel@udk-berlin.de>, All Rights Reserved

  Implemented by Jens Möckel

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  For a copy of the GNU General Public License see:
  <http://www.gnu.org/licenses/>.
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
        [os.remove(x) for x in os.listdir('.') if os.path.splitext(x)[1] not in ['.md', '.py', '.pyc', '.mo', '']]

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
