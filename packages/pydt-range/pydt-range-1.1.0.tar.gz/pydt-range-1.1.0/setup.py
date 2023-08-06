# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydt_range']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'pydt-range',
    'version': '1.1.0',
    'description': 'pydt-range is purely python mini library that allows to iterate over datetime objects with a specified step (similar to built-in range())',
    'long_description': '# Python Datetime Range\n[![tests](https://github.com/skroll182/pydt-range/actions/workflows/test.yml/badge.svg)](https://github.com/skroll182/datetime-range/actions/workflows/test.yml)\n\n`pydt-range` is purely python mini library that allows to iterate over `datetime` objects with a specified step (similar to built-in `range()`)\n\n## Installation\n### Pip\n```bash\npip install pydt-range\n```\n### Poetry\n```bash\npoetry add pydt-range\n```\n\n## Usage\n### With default step\n\n```python\nfrom datetime import datetime\n\nfrom pydt_range import datetime_range\n\nstart_dt = datetime(2022, 1, 1)\nend_dt = datetime(2022, 1, 10)\n\nfor dt in datetime_range(start_dt, end_dt):  # Default step is timedelta(days=1)\n    print(dt)\n"""\n2022-01-01 00:00:00\n2022-01-02 00:00:00\n2022-01-03 00:00:00\n2022-01-04 00:00:00\n2022-01-05 00:00:00\n2022-01-06 00:00:00\n2022-01-07 00:00:00\n2022-01-08 00:00:00\n2022-01-09 00:00:00\n"""\n```\n### With custom step\n\n```python\nfrom datetime import datetime\nfrom dateutil.relativedelta import relativedelta\n\nfrom pydt_range import datetime_range\n\nstart_dt = datetime(2022, 1, 1)\nend_dt = datetime(2022, 1, 10)\nstep = relativedelta(hours=6)\n\nfor dt in datetime_range(start_dt, end_dt, step):\n    print(dt)\n"""\n2022-01-01 00:00:00\n2022-01-01 06:00:00\n2022-01-01 12:00:00\n2022-01-01 18:00:00\n2022-01-02 00:00:00\n2022-01-02 06:00:00\n2022-01-02 12:00:00\n2022-01-02 18:00:00\n2022-01-03 00:00:00\n2022-01-03 06:00:00\n2022-01-03 12:00:00\n2022-01-03 18:00:00\n2022-01-04 00:00:00\n2022-01-04 06:00:00\n2022-01-04 12:00:00\n2022-01-04 18:00:00\n2022-01-05 00:00:00\n2022-01-05 06:00:00\n2022-01-05 12:00:00\n2022-01-05 18:00:00\n2022-01-06 00:00:00\n2022-01-06 06:00:00\n2022-01-06 12:00:00\n2022-01-06 18:00:00\n2022-01-07 00:00:00\n2022-01-07 06:00:00\n2022-01-07 12:00:00\n2022-01-07 18:00:00\n2022-01-08 00:00:00\n2022-01-08 06:00:00\n2022-01-08 12:00:00\n2022-01-08 18:00:00\n2022-01-09 00:00:00\n2022-01-09 06:00:00\n2022-01-09 12:00:00\n2022-01-09 18:00:00\n"""\n```\n',
    'author': 'Kirill Olar',
    'author_email': 'kirill.olar26@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skroll182/pydt-range',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
