from setuptools import Extension, setup

setup(
    name="c_ext",
    version='0.0.0',
    ext_modules=[Extension("c_sum", ["sum.c"])],
    setup_requires=['setuptools-ziglang'],
)

