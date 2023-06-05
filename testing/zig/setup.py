from setuptools import Extension, setup

setup(
    name='zig_sum',
    version='0.0.0',
    ext_modules=[Extension('zig_sum', ['sum.c', 'add.zig', ])],
    setup_requires=['setuptools-ziglang'],
)

