from setuptools._distutils.unixccompiler import UnixCCompiler

import sys
from importlib.util import find_spec



class ZigCompiler(UnixCCompiler):
    compiler_type = 'zig'

    # Prefer using the PyPI zig binary if it exists
    if find_spec("ziglang"):
        zig_bin = [sys.executable, '-m', 'ziglang',]
    else:
        zig_bin = ['zig']


    executables = {
        'preprocessor': None,
        'compiler': [*zig_bin, "cc"],  
        'compiler_so': [*zig_bin, "cc"],
        'compiler_cxx': [*zig_bin, "c++"],
        'compiler_zig': [*zig_bin, "build-obj"],
        'linker_so': [*zig_bin, "cc", "-shared"],
        'linker_exe': [*zig_bin, "cc"],
        'archiver': [*zig_bin, "ar", "-cr"],
        'ranlib': None,
    }

    if sys.platform[:6] == "darwin":
        executables['ranlib'] = [*zig_bin, "ranlib"]



