# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdf_add_outline']

package_data = \
{'': ['*']}

install_requires = \
['pikepdf==6.2.9']

entry_points = \
{'console_scripts': ['pdf-add-outline = pdf_add_outline:main']}

setup_kwargs = {
    'name': 'pdf-add-outline',
    'version': '0.1.1',
    'description': 'Programmatically add an outline to a PDF.',
    'long_description': '# `pdf-add-outline`\n\nAdd an outline to a PDF file. What it says on the tin.\n\n# Installation\n\nInstall through `pip`:\n\n```\npip install pdf-add-outline\n```\n\n# Usage\n\n```\n$ pdf-add-outline --help\nusage: pdf-add-outline [-h] -o OUTPUT [-d] [--increment INCREMENT] <pdf_file> <toc_file>\n\nAdd an outline to a PDF.\n\npositional arguments:\n  <pdf_file>            Input PDF\n  <toc_file>            JSON- or TXT-encoded ToC file (file type suffix required)\n\noptions:\n  -h, --help            show this help message and exit\n  -o OUTPUT, --output OUTPUT\n                        Resultant filename (required)\n  -d, --dry             Output the parsed OutlineItem structure; don\'t touch the PDF\n  --increment INCREMENT\n                        Increase all entries by <increment> amount\n```\n\n## Example\n\n```\n$ pdf-add-outline tests/fixtures/Situated_Learning.pdf tests/fixtures/situated_learning.txt -o situated_with_outline.pdf\n```\n\n## ToC File Formats\n\n```\n$ head tests/fixtures/situated_learning.json\n[\n    ["Series Foreword", 11, []],\n    ["Foreword by William F. Hanks", 13, []],\n    ["Acknowledgments", 25, []],\n    ["1. Legitimate Peripheral Participation", 27, [\n        ["From apprenticeship to situated learning", 32, []],\n        ["From situated learning to legitimate peripheral participation", 34, []],\n        ["An analytic perspective on learning", 37, []],\n        ["With legitimate peripheral participation", 39, []],\n        ["The organization of this monograph", 42, []]\n```\n\n```\n$ head tests/fixtures/situated_learning.txt\nSeries Foreword, 11\nForeword by William F. Hanks, 13\nAcknowledgments, 25\n1. Legitimate Peripheral Participation, 27\n    From apprenticeship to situated learning, 32\n    From situated learning to legitimate peripheral participation, 34\n    An analytic perspective on learning, 37\n    With legitimate peripheral participation, 39\n    The organization of this monograph, 42\n2. Practice, Person, Social World, 45\n```\n\n# Development\n\n1. Prerequisites: Clone the repository. Install [Poetry](https://python-poetry.org/).\n2. Run `poetry install` in the root of the directory.\n3. Run the tests.\n\n   ```\n   $ poetry run pytest tests\n   collected 4 items\n\n   tests/test_parsing.py ....        [100%]\n\n   ========== 4 passed in 0.03s ===========\n   ```\n\n4. Run `mypy`.\n\n   ```\n   $ poetry run mypy pdf_add_outline tests\n   Success: no issues found in 4 source files\n   ```\n\n5. Run `black`.\n\n   ```\n   $ poetry run black pdf_add_outline tests\n   All done! ✨ 🍰 ✨\n   4 files left unchanged.\n   ```\n\n# Acknowledgements\n\nThe excellent [PikePDF](https://github.com/pikepdf/pikepdf) package, which wraps the [QPDF](https://github.com/qpdf/qpdf) library. Jean Lave and Etienne Wenger\'s _Situated Learning_ for the example (and test) table of contents.\n',
    'author': 'Sameer Ismail',
    'author_email': '38896593+sameersismail@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sameersismail/pdf-add-outline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
