# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from eight import *

import unittest
from ...strategies import es1_allocate_multioutput


class Ecospold1AllocationTestCase(unittest.TestCase):
    def test_allocation(self):
        data = [{
            'products': [{
                'type': 'production',
                'code': 'p1',
                'amount': 1,
            }, {
                'type': 'production',
                'code': 'p2',
                'amount': 2,
            }],
            'exchanges': [{
                'type': 'production',
                'code': 'p1',
                'amount': 1,
            }, {
                'type': 'production',
                'code': 'p2',
                'amount': 2,
            }, {
                'type': 'emission',
                'code': 'e1',
                'amount': 10,
            }, {
                'type': 'technosphere',
                'code': 't1',
                'amount': 20,
            }],
            'allocations': [{
                'exchanges': ['e1', 't1'],
                'fraction': 50.,
                'reference': 'p1',
            }, {
                'exchanges': ['e1'],
                'fraction': 10.,
                'reference': 'p2',
            }, {
                'exchanges': ['t1'],
                'fraction': 100.,
                'reference': 'p2',
            }]
        }]
        answer = [
            {
                'exchanges': [
                    {'amount': 10 * 0.5, 'code': 'e1', 'type': 'emission'},
                    {'amount': 20 * 0.5, 'code': 't1', 'type': 'technosphere'}
                ],
                'products': [
                    {'amount': 1, 'code': 'p1', 'type': 'production'}
                ]
            }, {
                'exchanges': [
                    {'amount': 10 * 0.1, 'code': 'e1', 'type': 'emission'},
                    {'amount': 20 * 1., 'code': 't1', 'type': 'technosphere'}
                ],
                'products': [
                    {'amount': 2, 'code': 'p2', 'type': 'production'}
                ]
            }
        ]
        self.maxDiff = None
        # import pprint
        # pprint.pprint(es1_allocate_multioutput(data))
        self.assertEqual(es1_allocate_multioutput(data), answer)
