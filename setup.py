#!/usr/bin/env python3
from setuptools import setup

setup(name='mpw',
      version='2021.09.5',
      description='Calculate a site\'s password',
      author='Emil Johansson',
      author_email='emil.sweden@gmail.com',
      url='https://github.com/emiljoha/mpw',
      entry_points={
        'console_scripts': [
            'mpw = mpwcli:main',
            'mpw_snap = mpwcli:main_snap',
        ],
      },
      py_modules=['mpwcli'],
      install_requires=[
          'pyperclip',
          'mpwalg==0.2.3'
      ],
      tests_require=['pytest', 'pexpect']
      )
