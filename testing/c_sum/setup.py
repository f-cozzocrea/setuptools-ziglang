from setuptools import Extension, setup

setup(
    name="c_ext_test",
    version='0.0.0',
    build_zig=True,
    ext_modules=[Extension("c_ext_test.sum", ["sum.c"])],
    setup_requires=['pyzig'],
)

