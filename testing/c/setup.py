from setuptools import setup
from setuptools import Extension
from setuptools_ziglang.build_zig_ext import BuildZigExt

setup(
    ext_modules=[Extension(
        name="c_ext", 
        sources=["src/c_ext.c"],
        extra_compile_args=['-lc'],
        #include_dirs=["/usr/include"], ## FIXME: Why is this needed?
        #libraries=["c"],
        py_limited_api=True,
    )],
    cmdclass={'build_ext': BuildZigExt},
    zip_safe=False,
)

