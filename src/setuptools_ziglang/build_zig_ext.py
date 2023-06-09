from setuptools_ziglang.zigcompiler import ZigCompiler
#from setuptools_ziglang.zigextension import ZigExtension

from setuptools.command.build_ext import build_ext

class BuildZigExt(build_ext):
    def build_extension(self, ext):
        self.compiler = ZigCompiler() 
        build_ext.build_extension(self, ext)
