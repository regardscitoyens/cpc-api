# -*- coding: utf-8 -*-

from operator import itemgetter
import requests
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)
    from fuzzywuzzy.process import extractBests


__all__ = ['CPCApi']


def memoize(f):
    cache = {}

    def aux(*args, **kargs):
        k = (args, tuple(sorted(kargs.items())))
        if k not in cache:
            cache[k] = f(*args, **kargs)
        return cache[k]
    return aux


class CPCApi(object):
    format = 'json'

    def __init__(self, ptype='depute', legislature=None):
        """
        type: depute or senateur
        legislature: 2007-2012 or None
        """

        assert(ptype in ['depute', 'senateur'])
        assert(legislature in ['2007-2012', '2012-2017', None])
        self.legislature = legislature
        self.ptype = ptype
        self.ptype_plural = ptype + 's'
        self.base_url = 'https://%s.nos%s.fr' % (legislature or 'www', self.ptype_plural)

    def synthese(self, month=None):
        """
        month format: YYYYMM
        """
        if month is None and self.legislature == '2012-2017':
            raise AssertionError('Global Synthesis on legislature does not work, see https://github.com/regardscitoyens/nosdeputes.fr/issues/69')

        if month is None:
            month = 'data'

        url = '%s/synthese/%s/%s' % (self.base_url, month, self.format)

        data = requests.get(url).json()
        return [depute[self.ptype] for depute in data[self.ptype_plural]]

    def parlementaire(self, slug_name):
        url = '%s/%s/%s' % (self.base_url, slug_name, self.format)
        return requests.get(url).json()[self.ptype]

    def picture(self, slug_name, pixels='60'):
        return requests.get(self.picture_url(slug_name, pixels=pixels))

    def picture_url(self, slug_name, pixels='60'):
        return '%s/%s/photo/%s/%s' % (self.base_url, self.ptype, slug_name, pixels)

    def search(self, q, page=1):
        # XXX : the response with json format is not a valid json :'(
        # Temporary return csv raw data
        url = '%s/recherche/%s?page=%s&format=%s' % (self.base_url, q, page, 'csv')
        return requests.get(url).content

    @memoize
    def parlementaires(self, active=None):
        if active is None:
            url = '%s/%s/%s' % (self.base_url, self.ptype_plural, self.format)
        else:
            url = '%s/%s/enmandat/%s' % (self.base_url, self.ptype_plural, self.format)

        data = requests.get(url).json()
        return [depute[self.ptype] for depute in data[self.ptype_plural]]

    def search_parlementaires(self, q, field='nom', limit=5):
        return extractBests(q, self.parlementaires(), processor=lambda x: x[field] if type(x) == dict else x, limit=limit)
