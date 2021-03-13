# -*- coding: utf-8 -*-
"""
documentation
"""

from setuptools import setup, find_packages


setup(
    name='yaval',
    version='0.0.1.post3',
    description='yet another visualization abstraction layer',
    long_description='',
    author='Christian C. Sachs',
    author_email='sachs.christian@gmail.com',
    url='https://github.com/csachs/yaval',
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib', 'vispy', 'pyside2'],
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Image Recognition',
    ]
)
