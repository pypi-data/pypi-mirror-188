# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['markdown_pytest']
entry_points = \
{'pytest11': ['markdown-pytest = markdown_pytest']}

setup_kwargs = {
    'name': 'markdown-pytest',
    'version': '0.2.1',
    'description': 'Pytest plugin for runs tests directly from Markdown files',
    'long_description': 'markdown-pytest\n===============\n\nPytest plugin for running tests directly from Markdown files.\n\nMarkdown:\n\n````markdown\n<!-- name: test_assert_true -->\n```python\nassert True\n```\n````\n\n<details>\n<summary>Will be shown as</summary>\n\n<!-- name: test_assert_true -->\n```python\nassert True\n```\n\n</details>\n\nThis module parsed code by these rules:\n\n* Code without `<!-- name: test_name -->` comment will not be executed.\n* Allowed two or three dashes in the comment symbols\n* Code blocks with same names will be merged in one code and executed once\n\nCode split\n----------\n\nYou can split test to the multiple blocks with the same test name:\n\nMarkdown:\n\n````markdown\nThis block performs import:\n\n<!-- name: test_example -->\n```python\nfrom itertools import chain\n```\n\n`chain` usage example:\n\n<!-- name: test_example -->\n```python\nassert list(chain(range(2), range(2))) == [0, 1, 0, 1]\n```\n````\n\n<details>\n<summary>Will be shown as</summary>\n\nThis block performs import:\n\n<!-- name: test_example -->\n```python\nfrom itertools import chain\n```\n\n`chain` usage example:\n\n<!-- name: test_example -->\n```python\nassert list(chain(range(2), range(2))) == [0, 1, 0, 1]\n```\n\n</details>\n\nFictional Code Examples\n-----------------------\n\nCode without `<!-- name: test_name -->` comment will not be executed.\n\n````markdown\n```python\nfrom universe import antigravity, WrongPlanet\n\ntry:\n    antigravity()\nexcept WrongPlanet:\n    print("You are on the wrong planet.")\n    exit(1)\n```\n````\n\n<details>\n<summary>Will be shown as</summary>\n\n```python\nfrom universe import antigravity, WrongPlanet\n\ntry:\n    antigravity()\nexcept WrongPlanet:\n    print("You are on the wrong planet.")\n    exit(1)\n```\n</details>\n\nUsage example\n-------------\n\nThis README.md file might be tested like this:\n\n```bash\n$ pytest -v README.md\n======================= test session starts =======================\nplatform darwin -- Python 3.10.2, pytest-7.2.0, pluggy-1.0.0\nplugins: markdown-pytest-0.1.0\ncollected 2 items\n\nREADME.md::test_assert_true PASSED                                                                                                                                                                                                     [ 50%]\nREADME.md::test_example PASSED\n```\n',
    'author': 'Dmitry Orlov',
    'author_email': 'me@mosquito.su',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mosquito/markdown-pytest',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
