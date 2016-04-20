"""
Bookkeeping to setup Application.
"""

import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]

INSTALL_REQUIREMENTS = [
    'Django>=1.8,<1.10',
    'oauth2client>=2.0',
    ]

setup(
    name='SymmetricalEureka',
    version='0.1',
    packages=['SymmetricalEureka', 'tests'],
    include_package_data=True,
    license='MIT',
    description='I don\'t know what to say',
    long_description=README,
    url='https://github.com/degustaf/symmetrical-eureka',
    author='Derek Gustafson',
    author_email='degustaf@gmail.com',
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIREMENTS,
)
