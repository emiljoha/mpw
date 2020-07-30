#!/usr/bin/env python3
from setuptools import setup

setup(name='mpw',
      version='0.1',
      description='Calculate a site\'s password',
      author='Emil Johansson',
      author_email='emil.sweden@gmail.com',
      url='https://github.com/emiljoha/mpw',
      entry_points={
        'console_scripts': [
            'mpw = mpwcli:main',
            'mpw_snap = mpwcli:main_snap',
        ],},
      py_modules=['mpwcli'],
      setup_requires=["pytest-runner"],
      install_requires=['pyperclip', 'git+https://github.com/emiljoha/pympw.git@acc48fe'],
      tests_require=['pytest', 'pexpect']
)
