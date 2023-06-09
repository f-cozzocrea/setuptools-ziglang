from setuptools import setup, Extension
from os import path
from setuptools_ziglang.build_zig_ext import BuildZigExt

DIR = path.dirname(__file__)
setup(
    name="hpy-test",
    hpy_ext_modules=[
        Extension('hpy_test', sources=[path.join(DIR, 'hpy-test.c')]),
    ],
    cmdclass={'build_ext': BuildZigExt},
    setup_requires=['hpy'],
    zip_safe=False,
)

