[![Build Status](https://travis-ci.org/regardscitoyens/cpc-api.svg)](https://travis-ci.org/regardscitoyens/cpc-api)

# CPC-API
A python api for http://nosdeputes.fr and http://nossenateurs.fr

CPC is for *Controle Parlementaire Citoyens*.

See full API documentation here: https://github.com/regardscitoyens/nosdeputes.fr/blob/master/doc/api.md

## Examples

 * Députes
 
```python
from cpc_api import CPCApi
api = CPCApi(legislature='2012-2017')
# synthese of legislature
synthese = api.synthese()
# search for a depute
cope = api.search_parlementaires('Cope')[0][0]
# get all info of cope
all_info = api.parlementaire(cope['slug'])
```

 * Sénateurs & députés legislature 2007-2012...

```python
from cpc_api import CPCApi
# do the same with senateurs
api = CPCApi(ptype='senateur')
larcher = api.search_parlementaires('larcher')[0][0]
# 'or with legislature 2007-2012'
api = CPCApi(ptype='depute', legislature='2007-2012')
morano = api.search_parlementaires('morano')[0][0]
# ...
```
