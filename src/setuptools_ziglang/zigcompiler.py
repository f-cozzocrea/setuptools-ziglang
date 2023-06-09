from setuptools._distutils.unixccompiler import UnixCCompiler

import sys
from importlib.util import find_spec


class ZigCompiler(UnixCCompiler):
    compiler_type = 'zig'

    # Prefer using the PyPI zig binary, else fall back to the system zig
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

    # Needed for the filename generation methods provided by the base
    # class, CCompiler.  NB. whoever instantiates/uses a particular
    # UnixCCompiler instance should set 'shared_lib_ext' -- we set a
    # reasonable common default here, but it's not necessarily used on all
    # Unices!
    src_extensions = [".zig", ".c", ".C", ".cc", ".cxx", ".cpp", ".m"]
    obj_extension = ".o"
    static_lib_extension = ".a"
    shared_lib_extension = ".so"
    dylib_lib_extension = ".dylib"
    xcode_stub_lib_extension = ".tbd"
    static_lib_format = shared_lib_format = dylib_lib_format = "lib%s%s"
    xcode_stub_lib_format = dylib_lib_format
    if sys.platform == "cygwin":
        exe_extension = ".exe"



