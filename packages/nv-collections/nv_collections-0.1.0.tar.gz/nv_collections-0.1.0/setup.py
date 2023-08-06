# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nv',
 'nv.collections',
 'nv.collections.chainsequence',
 'nv.collections.mappings',
 'nv.collections.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nv-collections',
    'version': '0.1.0',
    'description': 'Data collections to be used with Python 3.10+',
    'long_description': '# nv-collections\nEnhanced data structures.\n\n- ChainSequence: chained lists (i.e. group of individual lists that behave as a single flattened list)\n- ObjectDict: dictionary that implements attribute search\n- StandardKeyMapping: dictionary that standardize keys (e.g. lower case)\n- OrderedSet: a set that preserves order (similar to OrderedDict)\n- Singletons: Singleton metaclass and semantic singletons\n',
    'author': 'Gustavo Santos',
    'author_email': 'gustavo@next.ventures',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gstos/nv-utils-collections',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
