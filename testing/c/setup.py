from setuptools import setup
from setuptools_ziglang import Extension

setup(
    ext_modules=[Extension("c_ext", ["c_ext.c"])],
)

