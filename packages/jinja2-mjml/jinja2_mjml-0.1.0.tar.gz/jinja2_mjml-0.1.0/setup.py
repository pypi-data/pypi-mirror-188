# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jinja2_mjml']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'mjml-python>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'jinja2-mjml',
    'version': '0.1.0',
    'description': 'Jinja2 integration with MJML',
    'long_description': "# Jinja2 MJML\n\nMicro-package that integrates [MJML](https://mjml.io/) \nwith [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/).\n\nUnder the hood it uses [mjml_python](https://pypi.org/project/mjml-python/) \npackage, that is a wrapper around [rust port](https://github.com/jolimail/mrml-core)\nof MJML.\n\n## Example\n\n```python\nfrom jinja2_mjml import Environment\n\n# MJMLEnvironment it's thin wrapper around jinja2.Environment,\n# so you can use all the features of Jinja2 package.\nenvironment = Environment()\ntemplate = environment.from_string('''\n    <mjml>\n      <mj-body>\n        <mj-section>\n          <mj-column>\n            <mj-text>Hello {{ name }}!</mj-text>\n          </mj-column>\n        </mj-section>\n      </mj-body>\n    </mjml>\n''')\n\n# Render MJML template to HTML\nprint(template.render(name='MJML'))\n```",
    'author': 'Yevhenii Hyzyla',
    'author_email': 'hyzyla@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hyzyla/jinja2_mjml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
