# coding: utf-8
#!/usr/bin/env python

from setuptools import setup, find_packages

readme = open('README.md').read()

setup(
    name='wecha',
    version='${version}',
    description='',
    long_description=readme,
    author='the5fire',
    author_email='thefivefire@gmail.com',
    url='http://chat.the5fire.com',
    packages=['src',],
    package_data={
        'src':['*.py', 'static/*', 'templates/*'],
    },
    include_package_data = True,
    install_requires=[
        'web.py',
        'jinja2',
        'gunicorn',
    ],
)
