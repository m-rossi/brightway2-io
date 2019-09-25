# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from eight import *

from bw2data import Database, config
# from bw2data.parameters import *
from bw2data.tests import bw2test
from bw2io.importers.base_lcia import LCIAImporter
# from bw2io.errors import NonuniqueCode, WrongDatabase
# from bw2io.importers.base_lci import LCIImporter
# from copy import deepcopy
# import numpy as np
import pytest
from .fixtures import biosphere as biosphere_data


def initial_biosphere():
    config.p["biosphere_database"] = "biosphere"
    Database("biosphere").write(biosphere_data)


@bw2test
def test_add_missing_cfs():
    initial_biosphere()
    assert len(Database("biosphere"))
    assert not len(Database("biosphere3"))

    class FakeLCIAImporter(LCIAImporter):
        def __init__(self):
            self.data = []
            self.biosphere_name = "biosphere"

    imp = FakeLCIAImporter()
    imp.data = [{
        'exchanges': [{
            'categories': ('foo',),
            'name': 'cookies',
            'unit': 'calories',
        }, {
            'name': 'toys',
            'unit': 'kilogram',
            'categories': ('resource', 'fun'),
        }]
    }]
    imp.add_missing_cfs()

    assert len(Database("biosphere")) == 4

    cookies = [x for x in Database("biosphere") if x['name'] == 'cookies'][0]._data
    assert len(cookies['code']) == 36
    assert cookies['categories'] == ('foo',)
    assert cookies['type'] == 'emission'
    assert cookies['unit'] == 'calories'

    toys = [x for x in Database("biosphere") if x['name'] == 'toys'][0]._data
    assert len(toys['code']) == 36
    assert toys['categories'] == ('resource', 'fun')
    assert toys['type'] == 'resource'
    assert toys['unit'] == 'kilogram'
    assert toys['database'] == 'biosphere'
    assert len(toys.keys()) == 6