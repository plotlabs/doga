import os
import sys
from setuptools import setup

if sys.version_info < (3, 4):
    sys.exit("Sorry, Python < 3.4 is not supported")

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(install_requires=required)
