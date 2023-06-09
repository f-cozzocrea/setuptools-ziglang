from setuptools_ziglang import zigcompiler
from setuptools_ziglang.zigextension import ZigExtension as Extension

import os
import distutils
from setuptools._distutils import ccompiler

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




