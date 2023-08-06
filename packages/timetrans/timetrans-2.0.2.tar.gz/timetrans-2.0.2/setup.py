# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['timetrans']
install_requires = \
['googletrans==3.1.0a0']

setup_kwargs = {
    'name': 'timetrans',
    'version': '2.0.2',
    'description': 'Time trans to transfer to a normal date and clearance ',
    'long_description': 'Приветствую всёх наших любителей Python, думаю многим из вас надоедало то что когда вы получаете время используя Datetime мы получаем не особо красивые текста, что-же я решыл исправить это',
    'author': 'Sad_Cat0326',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
