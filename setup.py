#!/usr/bin/env python3
import platform
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
boost_python_library_name_dict = {'Darwin': 'boost_python37'}
boost_python_library_name_default = 'boost_python-p35' # Ubuntu 16.04
if platform.system() in boost_python_library_name_dict:
    boost_python_library_name = boost_python_library_name_dict[platform.system()]
else:
    boost_python_library_name = boost_python_library_name_default
allsources = mpwalgorithm_sources + mpwalgorithmwrapper_sources
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
      ext_modules=[
          Extension('pympw',
                    allsources,
                    include_dirs=['core', 'core/mpw-algorithm'],
                    libraries=[boost_python_library_name, 'boost_system',
                               'boost_filesystem', 'sodium'],
                    extra_compile_args=allflags
          ),
      ],
      setup_requires=["pytest-runner"],
      install_requires=['pyperclip'],
      tests_require=['pytest', 'pexpect']
)
