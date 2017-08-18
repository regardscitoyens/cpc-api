# -*- coding: utf-8 -*-

import unittest

from cpc_api import CPCApi


class SearchQuestionServiceTest(unittest.TestCase):
    def test_deputes(self):
        api = CPCApi(legislature='2012-2017')
        self.assertGreater(len(api.parlementaires()), 1)
        self.assertEqual(api.search_parlementaires('Cope')[0][0]['nom_de_famille'], u'Copé')

    def test_senateurs(self):
        api = CPCApi(ptype='senateur')
        self.assertGreater(len(api.parlementaires()), 1)
        self.assertEqual(api.search_parlementaires('Larcher')[0][0]['nom_de_famille'], u'Larcher')

    def test_2007_2012(self):
        api = CPCApi(legislature='2007-2012')
        self.assertGreater(len(api.parlementaires()), 1)
        self.assertEqual(api.search_parlementaires('Morano')[0][0]['nom_de_famille'], u'Morano')