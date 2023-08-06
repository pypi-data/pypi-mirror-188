# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apispec_pydantic_plugin']

package_data = \
{'': ['*']}

install_requires = \
['apispec>=6.0.2,<7', 'pydantic>=1.10.4,<2']

setup_kwargs = {
    'name': 'apispec-pydantic-plugin',
    'version': '0.2.2',
    'description': '',
    'long_description': "\n# APISpec Pydantic Plugin\n\nThis is a plugin that replaces `apispec.ext.marshmallow:MarshmallowPlugin` with an equivalent plugin for use with Pydantic.\n\n\n\n## Acknowledgements\n\n - [APISpec's Marshmallow Plugin ](https://github.com/marshmallow-code/apispec/tree/dev/src/apispec/ext/marshmallow)\n- [challice-spec](https://github.com/TestBoxLab/chalice-spec)",
    'author': 'Kevin Kirsche',
    'author_email': 'kevin.kirsche@one.verizon.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
