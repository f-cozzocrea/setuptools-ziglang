from setuptools import Extension, setup

setup(
    name='c_zig_ext_test',
    version='0.0.0',
    build_zig=True,
    ext_modules=[Extension('c_zig_ext_test.sum', ['c_int.c', 'sum.zig', ])],
    setup_requires=['setuptools-zig'],
)

