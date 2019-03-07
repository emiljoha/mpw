#!/usr/bin/env python3
from setuptools import setup

setup(name='mpw',
      version='0.1',
      description='Calculate a site\'s password',
      author='Emil Johansson',
      author_email='emil.sweden@gmail.com',
      url='https://gitlab.com/emijoha/MasterPassword',
      entry_points={
        'console_scripts': [
            'mpw = mpw:main',
            'mpw_snap = mpw:main_snap',
        ],},
      scripts=['mpw.py'],
      py_modules=['pympw'],
      setup_requires=["pytest-runner"],
      install_requires=['pyperclip', 'scrypt'],
      tests_require=['pytest', 'pexpect']
)
