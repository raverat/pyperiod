import os
import re

from setuptools import setup, find_packages


def get_version(package):
    with open(os.path.join(package, '__init__.py'), 'rb') as mod:
        src = mod.read().decode('utf-8')
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", src).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages

    :return: List of packages
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in package themselves.

    :param package:
    :return:
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


name = 'pyperiod'
package = 'pyperiod'
description = 'PyPeriod generates daily, weekly or monthly period between two dates'
author = 'Thibault Ravera'

setup(
    name=name,
    version=get_version(package),
    licence='MIT',
    description=description,
    author=author,
    packages=get_package_data(package),
    package_data=get_package_data(package),
    install_requires=[
    ]
)