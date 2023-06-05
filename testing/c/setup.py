from setuptools import Extension, setup

setup(
    name="c-ext",
    version='0.0.0',
    ext_modules=[Extension("c_ext", ["c_ext.c"])],
    setup_requires=['setuptools-ziglang'],
)

