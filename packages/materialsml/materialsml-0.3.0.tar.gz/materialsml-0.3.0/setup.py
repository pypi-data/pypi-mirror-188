# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['materialsml', 'materialsml.neuralnetwork']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.50,<2.0.0',
 'chardet>=5.1.0,<6.0.0',
 'mp-api>=0.30.5,<0.31.0',
 'mpcontribs-client>=5.0.7,<6.0.0',
 'pytest>=7.2.0,<8.0.0',
 'pyvista>=0.37.0,<0.38.0',
 'stellargraph==1.2.1']

setup_kwargs = {
    'name': 'materialsml',
    'version': '0.3.0',
    'description': 'A Machine Learning package for materials informatics',
    'long_description': '# materialsML\n\nA Machine Learning package for materials informatics. A crafty data analysis complement to the materials database from [The Materials Project](https://materialsproject.org)\n\n\n<img src="https://raw.githubusercontent.com/andrewrgarcia/materialsML/main/materialsML.svg" width="400">\n\n## Getting Started \n\n<a href="https://colab.research.google.com/drive/19PD1d6FlRWKdhBYoTWkKfI9O3XiLDZeM?usp=sharing"><img src="https://raw.githubusercontent.com/andrewrgarcia/materialsML/main/notebook.png" width=600></a>\n\n\n## Local Installation and Usage \n\n```ruby\npip install materialsml\n```\nIt is recommended to run this package using a `virtualenv` virtual environment. To do so, follow the below simple protocol to create the virtual environment, run it, and install the package there:\n\n```ruby \nvirtualenv venv\nsource venv/bin/activate\npip install materialsml\npython [your-script.py]\n```\nTo exit the virtual environment, simply type `deactivate`. To access it at any other time, type `source venv/bin/activate` on the directory containing the `venv` folder. \n\n\n## viewer (in development)\n\n<img src="https://raw.githubusercontent.com/andrewrgarcia/materialsML/main/examples/images/materialsML_view0126.png">\n\n\n## Disclaimer: Use At Your Own Risk\n\nThis program is free software. It comes without any warranty, to the extent permitted by applicable law. You can redistribute it and/or modify it under the terms of the MIT LICENSE, as published by Andrew Garcia. See LICENSE below for more details.\n\n[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)\n\n**[MIT license](./LICENSE)** Copyright 2023 © <a href="https://github.com/andrewrgarcia" target="_blank">Andrew Garcia</a>.\n\n',
    'author': 'andrewrgarcia',
    'author_email': 'garcia.gtr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9.0',
}


setup(**setup_kwargs)
