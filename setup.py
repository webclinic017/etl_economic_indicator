from setuptools import setup, find_packages

classifiers = [
    'Developement Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9.5'
]

setup(
name = 'etl_economic_indicator',
version ='2.0.1',
description = 'etl_economic_indicator is a a python program that download the economic data indicators in investing.com and upload it to a sql server database',
url= 'https://github.com/Iankfc/etl_economic_indicator',
author='ece',
author_email='odesk5@outlook.com',
license = 'None',
classifiers=classifiers,
keywords='None',
packages=find_packages(),
use_scm_version=True,
include_package_data=True,
setup_requires=['setuptools_scm'],
install_requires = open('requirements.txt','r').read().split('\n')[:-1]
)