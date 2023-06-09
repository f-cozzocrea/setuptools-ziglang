from setuptools_ziglang.zigcompiler import ZigCompiler
from setuptools_ziglang.zigextension import ZigExtension

from setuptools._distutils.errors import DistutilsSetupError
from setuptools._distutils.dep_util import newer_group 
from setuptools.command.build_ext import build_ext

import logging as log

log.basicConfig(level=log.INFO)

class build_zig_ext(build_ext):
    def build_extension(self, ext):
        if isinstance(ext, ZigExtension):
            print("ZIGEXTENSION DETECTED")
            self.compiler = ZigCompiler() 
        build_ext.build_extension(self, ext)
