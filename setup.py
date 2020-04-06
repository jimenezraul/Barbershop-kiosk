# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
import re

from os.path import join, dirname
from setuptools import setup


VERSION_RE = re.compile('__version__ = \'([\d\.]+)\'')


def read_version():
    with open('src/user_profile/__init__.py') as file:
        version_line = [line for line in file.readlines()
                        if line.startswith('__version__')][0]
        return VERSION_RE.match(version_line).groups()[0]


def long_description():
    return open(join(dirname(__file__), 'README.md')).read()


def load_requirements():
    return open(join(dirname(__file__), 'requirements.txt')).readlines()

setup(
    name='barbershop-kiosk-app-django',
    version=read_version(),
    author='Raul  Jimenez',
    author_email='jimenezraul1981@gmail.com',
    description='Python Barbershop, Django integration.',
    license='BSD',
    keywords='django, barbershop',
    url='https://github.com/jimenezraul/Barbershop-kiosk',
    packages=[
        'barbershop',
        'barbershop.migrations',
        'barbershop.management',
        'barbershop.management.commands',
    ],
    long_description=long_description(),
    long_description_content_type='text/markdown',
    install_requires=load_requirements(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
)
