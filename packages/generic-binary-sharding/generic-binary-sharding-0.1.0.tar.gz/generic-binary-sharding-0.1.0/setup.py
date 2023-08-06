# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['generic_binary_sharding']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['serialize-js = generic_binary_sharding.serialize:cli']}

setup_kwargs = {
    'name': 'generic-binary-sharding',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Generic Binary Sharding Tool\n\nThis tool is a Generic Binary Sharding tool which serializes binaries into a javascript package where each file is at max a specified shard size.\n\n\n## How it Works\n\nThis tool works by determining all the files that match the given criterion (extensions and paths). We read all of these files and store the base64 encoding of their bytes in a dictionary. Later we write a bunch of js files having a maximum of `shard_size` megabytes size. By default this is set to 64MB.\n\nFinally an entrypoint file is provided which requires all the appropriate files.\n\n### DCP Modules\n\nThis tool was built to aid in development of dcp packages and for publishing extremely large models and binary files. As such, we've also included some dcp based package generation features.\n\nThese features take advantage of a feature bravojs module packages have called `module.provide`. This feature allows users to request packages to load in dynamically that weren't explicitly required by `job.requires`. \n\n\n",
    'author': 'Hamada Gasmallah',
    'author_email': 'hamada@distributive.network',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
