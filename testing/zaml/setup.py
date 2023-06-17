from setuptools import setup, Extension
from setuptools_ziglang.build_zig_ext import BuildZigExt


zaml = Extension(name="zaml", sources=["zamlmodule.zig"], py_limited_api=True)

setup(
    ext_modules=[zaml],
    cmdclass={"build_ext": BuildZigExt},
    zip_safe=False,
)
