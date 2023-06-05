# setup.py

from setuptools import setup, Extension
from os import path

DIR = path.dirname(__file__)
setup(
    name="hpy-test",
    hpy_ext_modules=[
        Extension('hpy_test', sources=[path.join(DIR, 'hpy-test.c')]),
    ],
    setup_requires=['hpy'],
)

