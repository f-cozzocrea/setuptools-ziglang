from setuptools import setup, Extension
from os import path
from setuptools_ziglang.build_zig_ext import BuildZigExt

DIR = path.dirname(__file__)
setup(
    name="hpy-test",
    hpy_ext_modules=[
        Extension(
            name='hpy_test', 
            sources=[path.join(DIR, 'hpy-test.c')], 
            extra_compile_args=['-lc'],
            py_limited_api=True,
        ),
    ],
    cmdclass={'build_ext': BuildZigExt},
    setup_requires=['hpy'],
    zip_safe=False, 
)

