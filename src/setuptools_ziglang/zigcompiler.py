from setuptools._distutils.unixccompiler import UnixCCompiler

import sys


class ZigCompiler(UnixCCompiler):
    compiler_type = 'zig'
    
    #### FIXME!
    # Prefer using the PyPI zig binary, else fall back to the system zig
    ##if find_spec("ziglang"):
    ##    zig_bin = [sys.executable, '-m', 'ziglang',]
    ##else:
    ##    zig_bin = ['zig']

    zig_bin = [sys.executable, '-m', 'ziglang',]

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
    if sys.platform.startswith("cygwin") or sys.platform.startswith("win32"):
        exe_extension = ".exe"

    
    # TODO
    #def preprocess(...):
    #    ...

    # TODO
    #def create_static_lib(...):
    #    ...

    # TODO
    #def link(...):
    #    ...

    # TODO
    #def library_dir_option(...):
    #    ...

    # TODO
    #def runtime_library_dir_option(...):
    #    ...

    # TODO
    #def library_option(...):
    #    ...
   
    # TODO
    #def find_library_file(...):
    #    ...


