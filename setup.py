#!/usr/bin/env python3

from setuptools import setup, Extension

cppflags = ['-lm', '-fPIC']
cflags = ['-fPIC', '-O3', '-DMPW_SODIUM=1']
allflags = list(set(cppflags).union(set(cflags)))
mpwalgorithmwrapper_sources = ['core/wrapper/mpwalgorithmwrapper.cpp',]
mpwalgorithm_sources = ['core/mpw-algorithm/aes.c',
                        'core/mpw-algorithm/mpw-algorithm.c',
                        'core/mpw-algorithm/mpw-util.c',
                        'core/mpw-algorithm/mpw-marshal-util.c',
                        'core/mpw-algorithm/mpw-types.c',
                        'core/mpw-algorithm/mpw-marshal.c',
                        'core/mpw-algorithm/mpw-algorithm_v0.c',
                        'core/mpw-algorithm/mpw-algorithm_v1.c',
                        'core/mpw-algorithm/mpw-algorithm_v2.c',
                        'core/mpw-algorithm/mpw-algorithm_v3.c',
                        'core/mpw-algorithm/base64.c',]
allsources = mpwalgorithm_sources + mpwalgorithmwrapper_sources
setup(name='mpw',
      version='0.1',
      description='Calculate a site\'s password',
      author='Emil Johansson',
      author_email='emil.sweden@gmail.com',
      url='https://gitlab.com/emijoha/MasterPassword',
      install_requires=['pyperclip'],
      entry_points={
        'console_scripts': [
            'mpw = mpw:main',
            'mpw_snap = mpw:main_snap',
        ],},
      scripts=['mpw.py'],
      ext_modules=[
          Extension('pympw',
                    allsources,
                    include_dirs=['core', 'core/mpw-algorithm'],
                    libraries=['boost_python-py35', 'boost_system',
                               'boost_filesystem', 'sodium'],
                    extra_compile_args=allflags
          ),
      ],
      setup_requires=["pytest-runner"],
      tests_require=["pytest"]
)
      
# aes.h
# mpw-algorithm.h
# mpw-marshal-util.h
# mpw-util.h
# base64.h
# mpw-marshal.h
# mpw-types.h
# 'core/conversions.h',
