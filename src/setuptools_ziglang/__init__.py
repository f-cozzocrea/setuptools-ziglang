from setuptools_ziglang import zigcompiler
from setuptools_ziglang.zigextension import ZigExtension as Extension

import os
import distutils
from setuptools import Distribution
from setuptools._distutils import ccompiler
from setuptools.command.build_ext import build_ext
from wheel.bdist_wheel import bdist_wheel

__all__ = ['Extension']


# Add the Zig language and compiler to the setuptools list of compilers
ccompiler.compiler_class['zig'] = ("zigcompiler", "ZigCompiler", "The Zig language compiler")
ccompiler.CCompiler.language_map[".zig"] = "zig"
ccompiler.CCompiler.language_order.insert(0, "zig")
distutils.zigcompiler = zigcompiler

# Users can set this if they want Zig as the default compiler. May be useful if the compiler mutates
# because of other extensions
if os.getenv("SETUPTOOLS_FORCE_ZIG", None):
    ccompiler._default_compilers = (
        ('cygwin.*', 'zig'),
        ('posix', 'zig'),
        ('nt', 'zig'),
    )


# dist finalize options entry point
def set_zig_compiler(dist: Distribution) -> None:
    print("Setting zig as the compiler for build_ext...")
    base_build_ext = dist.cmdclass.get('build_ext', build_ext)
    base_build_ext.compiler = 'zig'
    dist.cmdclass['build_ext'] = base_build_ext

    #print("Setting zig as the compiler for bdist_wheel")
    #base_bdist_wheel = dist.cmdclass.get('bdist_wheel', bdist_wheel)
    #base_bdist_wheel.

    breakpoint()

# Defines the order that setuptools runs entry points for 'finalize_distribution_options'.
# 0 is the default. 100 is arbitrarily chosen so that users can set their own entry points
# either before or after this one.
set_zig_compiler.order = 100


