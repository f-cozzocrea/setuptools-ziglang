from setuptools._distutils.unixccompiler import UnixCCompiler

import os
import sys
from sysconfig import get_config_vars

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
        'compiler': zig_bin + ["cc"],  
        'compiler_so': zig_bin + ["cc"],
        'compiler_cxx': zig_bin + ["c++"],
        'compiler_zig': zig_bin + [],
        'linker_so': zig_bin + ["cc", "-shared"],
        'linker_exe': zig_bin + ["cc"],
        'archiver': zig_bin + ["ar", "-cr"],
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

   
    def set_default_flags(self) -> None:
        # TODO: OSX-specific customization
        #if sys.platform == "darwin":
        #    # Perform first-time customization of compiler-related
        #    # config vars on OS X now that we know we need a compiler.
        #    # This is primarily to support Pythons from binary
        #    # installers.  The kind and paths to build tools on
        #    # the user system may vary significantly from the system
        #    # that Python itself was built on.  Also the user OS
        #    # version and build tools may not support the same set
        #    # of CPU architectures for universal builds.
        #    global _config_vars
        #    # Use get_config_var() to ensure _config_vars is initialized.
        #    if not get_config_var('CUSTOMIZED_OSX_COMPILER'):
        #        import _osx_support

        #        _osx_support.customize_compiler(_config_vars)
        #        _config_vars['CUSTOMIZED_OSX_COMPILER'] = 'True'

        (
            cc,
            cflags,
            ccshared,
            ldshared,
            shlib_suffix,
            ar,
            ar_flags,
        ) = get_config_vars(
            'CC',
            'CFLAGS',
            'CCSHARED',
            'LDSHARED',
            'SHLIB_SUFFIX',
            'AR',
            'ARFLAGS',
        )

        if 'CC' in os.environ:
            newcc = os.environ['CC']
            if 'LDSHARED' not in os.environ and ldshared.startswith(cc):
                # If CC is overridden, use that as the default
                #       command for LDSHARED as well
                ldshared = newcc + ldshared[len(cc) :]
            cc = newcc
        else:
            cc = ' '.join(self.executables['compiler'])
        if 'CXX' in os.environ:
            cxx = os.environ['CXX']
        else:
            cxx = ' '.join(self.executables['compiler_cxx'])
        if 'LDSHARED' in os.environ:
            ldshared = os.environ['LDSHARED']
        if 'CPP' in os.environ:
            cpp = os.environ['CPP']
        else:
            cpp = cc + " -E"  # not always
        if 'LDFLAGS' in os.environ:
            ldshared = ldshared + ' ' + os.environ['LDFLAGS']
        if 'CFLAGS' in os.environ:
            cflags = cflags + ' ' + os.environ['CFLAGS']
            ldshared = ldshared + ' ' + os.environ['CFLAGS']
        if 'CPPFLAGS' in os.environ:
            cpp = cpp + ' ' + os.environ['CPPFLAGS']
            cflags = cflags + ' ' + os.environ['CPPFLAGS']
            ldshared = ldshared + ' ' + os.environ['CPPFLAGS']
        if 'AR' in os.environ:
            ar = os.environ['AR']
        if 'ARFLAGS' in os.environ:
            archiver = ar + ' ' + os.environ['ARFLAGS']
        else:
            archiver = ar + ' ' + ar_flags

        cc_cmd = cc + ' ' + cflags

        zig_bin = ' '.join(self.executables['compiler_zig'])
        zig_cmd = zig_bin + ' ' + '-cflags' + ' ' + cflags + ' ' + '--'

        if sys.platform.startswith("win32"):
            zig_cmd += ["-target", "x86_64-windows-msvc"]

        self.set_executables(
            compiler=cc_cmd,
            compiler_so=cc_cmd + ' ' + ccshared,
            compiler_cxx=cxx,
            compiler_zig=zig_cmd,
            linker_so=ldshared,
            linker_exe=cc,
            archiver=archiver,
        )

        if 'RANLIB' in os.environ and self.executables.get('ranlib', None):
            self.set_executables(ranlib=os.environ['RANLIB'])

        self.shared_lib_extension = shlib_suffix


