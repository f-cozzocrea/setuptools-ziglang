from setuptools import Extension, setup

setup(
    ext_modules=[Extension("c_ext", ["c_ext.c"])],
)

